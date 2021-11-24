import mysql.connector
import boto3

client = boto3.client(
    "sns",
    aws_acces_key_id="",
    aws_secret_access_key="",
    region_name=""
)

dic = {}

cnx = mysql.connector.connect(user='admin', password='', host='127.0.0.1',
                              database='users')


def send_message(message, number):
    client.publish(phone_number=number, message=message)


def func03(user_profile):
    query = "select * from users whwere profile="+user_profile
    cursor = cnx.cursor()
    cursor.execute(query)

    for (first_name, last_name, phone_numbers, service_link) in cursor:
        for number in phone_numbers:
            query2 = "select number from phone_numer where phone_id="+number
            cursor.execute(query2)
            dic['table'] = cursor.fetchall()
            send_message("Hey " + first_name + " " + last_name + " we have some"
                         " information about your platinum account, please"
                         " go to "+service_link+"to get more details",
                         dic['table'][0])


def func04(user_profile):
    query = "select * from users whwere profile=" + user_profile
    cursor = cnx.cursor()
    cursor.execute(query)

    for (first_name, last_name, phone_numbers, service_link) in cursor:
        for number in phone_numbers:
            query2 = "select number from phone_numer where phone_id=" + number
            cursor.execute(query)
            dic['table'] = cursor.fetchall()
            send_message("Hey " + first_name + " " + last_name + " we have some"
                         " information about your gold account, please"
                         " go to " + service_link + "to get more details",
                         dic['table'][0])


def func05(user_profile):
    query = "select * from users whwere profile=" + user_profile
    cursor = cnx.cursor()
    cursor.execute(query)

    for (first_name, last_name, phone_numbers, service_link) in cursor:
        for number in phone_numbers:
            query2 = "select number from phone_numer where phone_id=" + number
            cursor.execute(query)
            dic['table'] = cursor.fetchall()
            send_message("Hey " + first_name + " " + last_name + " we have some"
                         " information about your silver account, please"
                         " go to " + service_link + "to get more details",
                         dic['table'][0])


def func06(user_profile):
    query = "select * from users whwere profile=" + user_profile
    cursor = cnx.cursor()
    cursor.execute(query)

    for (first_name, last_name, phone_numbers, service_link) in cursor:
        for number in phone_numbers:
            query2 = "select number from phone_numer where phone_id=" + number
            cursor.execute(query)
            dic['table'] = cursor.fetchall()
            send_message("Hey " + first_name + " " + last_name + " we have some"
                         " information about your bronze account, please"
                         " go to " + service_link + "to get more details",
                         dic['table'][0])


def func02(x):
    y = x[0]
    if y == "user platinum":
        func03(x[1])
    elif y == "user gold":
        func04(x[1])
    elif y ==  "user silver":
        func05(x[1])
    elif y == "user bronze":
        func06(x[1])


def func01(line):
    x = line.split(";")
    func02(x)


f = open("profileDB_id.txt", "r")
lines = f.readline()

for line in lines:
    func01(line)

