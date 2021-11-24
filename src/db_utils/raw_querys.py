# query users
SELECT_USER_BY_EMAIL = '''
                       SELECT first_name, 
                              last_name, 
                              service_link, 
                              phone_number 
                       FROM users 
                       WHERE user_email={}'''
