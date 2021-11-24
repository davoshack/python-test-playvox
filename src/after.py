import boto3
import json
import logging
import mysql.connector

from typing import List
from . import config
from .db_utils.raw_querys import SELECT_USER_BY_EMAIL

logger = logging.getLogger(__name__)


MESSAGE_TEXT = 'Hey {} {}  we have some information about your {} account, ' \
               'please go to {} to get more details.'


class UserProfile:
    """
    Represents a user profile object
    """
    def __init__(self, account_type: str, user_email: str):
        self.account_type = account_type
        self.user_email = user_email
        self.first_name = ""
        self.last_name = ""
        self.phone_number = ""
        self.service_link = ""
        self.select_user_by_email = SELECT_USER_BY_EMAIL.format(self.user_email)

    def set_profile_user_info(self, data: list):
        self.first_name = data[0].first_name
        self.last_name = data[0].last_name
        self.phone_number = data[0].phone_number
        self.service_link = data[0].service_link

    def set_user_message(self) -> str:
        # This text will be use to send notification to user
        message = MESSAGE_TEXT.format(self.first_name, self.last_name,
                                      self.account_type, self.service_link)
        return message


class DataBaseManager:
    """
    Class that handle the communication to the Database
    """
    def __init__(self):
        self.user = config.DB_USER
        self.password = config.DB_PASSWORD
        self.host = config.DB_HOST
        self.database = config.DB_NAME
        self.connection = None

    def set_connection_db(self):
        try:
            self.connection = mysql.connector.connect(
                user=self.user,
                password=self.password,
                host=self.password,
                database=self.database
            )
        except mysql.connector.Error as e:
            logger.exception(f'MySQL: Something went wrong: {e.text}')
            raise Exception(f'A MySQL exception occurred: {e.text}')

    def close_connection_db(self):
        self.connection.close()

    def get_data(self, query: str) -> list:
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            data = cursor.fetchall()
        except mysql.connector.Error as e:
            logger.exception(f'MySQL: Something went wrong: {e.text}')
            raise Exception(f'A MySQL exception occurred: {e.text}')

        return data


class NotificationServiceManager:
    """
    Class that handle the notification service
    """

    def __init__(self):
        self.service_name = config.AWS_SERVICE_NAME
        self.aws_access_key_id = config.AWS_ACCESS_KEY_ID
        self.aws_secret_access_key = config.AWS_SECRET_ACCESS_KEY
        self.region_name = config.AWS_REGION
        self.client_obj = None

    def set_notification_client(self):
        self.client_obj = boto3.client(
            service_name=self.service_name,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.region_name
        )

    def send_message(self, phone_number: str, message: str):
        self.client_obj.publish(phone_number=phone_number, message=message)


def create_connection_db():
    connection_db = DataBaseManager()
    connection_db.set_connection_db()
    return connection_db


def create_notification_client():
    notification = NotificationServiceManager()
    notification.set_notification_client()
    return notification


def close_connection_db(connection_db):
    connection_db.close_connection_db()
    logger.info("The database connection has been closed")


def main() -> None:
    with open("profileDB.json", "r") as file:
        data = json.load(file)
        users: List[UserProfile] = [UserProfile(**item) for item in data]

        connection_db = create_connection_db()
        notification = create_notification_client()

        for user in users:
            # Get user info from data base
            info_user = connection_db.get_data(user.select_user_by_email)

            user.set_profile_user_info(info_user)
            message = user.set_user_message()

            # Send notification to user
            notification.send_message(user.phone_number, message)
            logger.info(f'Sent notification to user with email: {user.user_email}')

        close_connection_db(connection_db)


if __name__ == "__main__":
    main()
