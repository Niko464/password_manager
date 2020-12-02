import socket
import mysql.connector as mysql
import src.config as config
import src.utils_encryption as utils_encryption
import bcrypt
#import pickle
import select
import json
from datetime import datetime

old_print = print
def timestamped_print(*args, **kwargs):
    old_print(datetime.now(), *args, **kwargs)
print = timestamped_print


MYSQL_HOST = "127.0.0.1"
MYSQL_USER = "nikolaj"
MYSQL_PASS = "fopHJ97kL0m6d@aKDL4r"
MYSQL_DATABASE = "password_manager"

SERVER_IP = "45.140.164.47" #"45.140.164.47"
SERVER_PORT = 1234

PREFIX = ">> "

sockets_list = []
clients = {}

def main():
    print(PREFIX + "Starting Server...")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print(PREFIX + "Server started!")
    print(PREFIX + "Waiting for clients...")
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen(5)

    sockets_list.append(server_socket)

    while True:
        read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

        for notified_socket in read_sockets:
            if (notified_socket == server_socket):
                # Someone connected to server
                client_socket, client_address = server_socket.accept()
                print(f"{PREFIX}Accepted new connection from: {client_address[0]}:{client_address[1]}")
                sockets_list.append(client_socket)
                send_message(client_socket, {'code': 0})
            else:
                message = receive_message(notified_socket)

                if message == False:
                    print(PREFIX + "Client disconnected.")
                    sockets_list.remove(notified_socket)
                    continue
                try:
                    print(PREFIX + "Received code:" + str(message['code']))
                    if (message['code'] == 1):
                        print(PREFIX + "Calling try_logging_in with params: " + message['username_str'] + " ***********")
                        response = try_logging_in(message['username_str'], message['password_str'])
                        send_message(notified_socket, response)
                    elif (message['code'] == 2):
                        print(PREFIX + "Calling try_signing_up with params: " + message['username_str'], message['mail_str'], message['hashed_pass'])
                        response = try_signing_up(message['username_str'], message['mail_str'], message['hashed_pass'])
                        send_message(notified_socket, response)
                    elif (message['code'] == 3):
                        print(PREFIX + "Calling get_user_passwords_info with params: " + message['hashed_master_password'])
                        response = get_user_passwords_info(message['hashed_master_password'])
                        send_message(notified_socket, response)
                    elif (message['code'] == 4):
                        print(PREFIX + "Calling check_if_name_exists with params: " + message['hashed_master_password'], message['name'])
                        response = check_if_name_exists(message['hashed_master_password'], message['name'])
                        send_message(notified_socket, response)
                    elif (message['code'] == 5):
                        print(PREFIX + "Calling save_new_password with params: " + message['hashed_master_password'], message['name'], message['encrypted_password'], " username, mail, pin_code, comment")
                        response = save_new_password(message['hashed_master_password'], message['name'], message['encrypted_password'], message['encrypted_username'], message['encrypted_mail'], message['encrypted_pin_code'], message['comment'])
                        send_message(notified_socket, response)
                    elif (message['code'] == 6):
                        print(PREFIX + "Calling update_existing_password with params: " + message['hashed_master_password'], message['old_name'], message['new_name'], message['new_encrypted_password'], " username, mail, pin_code, comment")
                        response = update_existing_password(message['hashed_master_password'], message['old_name'], message['new_name'], message['new_encrypted_password'], message['new_encrypted_username'], message['new_encrypted_mail'], message['new_encrypted_pin_code'], message['new_comment'])
                        send_message(notified_socket, response)
                    elif (message['code'] == 7):
                        print(PREFIX + "Calling remove_password with params: " + message['hashed_master_password'], message['name'])
                        response = remove_password(message['hashed_master_password'], message['name'])
                        send_message(notified_socket, response)
                except KeyError as e:
                    print("Key error: " + str(e))
                    continue

        for notified_socket in exception_sockets:
            sockets_list.remove(notified_socket)


def send_message(socket_to_send_to, msg):
    try:
        to_send = json.dumps(msg)
        print(PREFIX + "Sending: " + str(to_send))
        to_send = bytes(f'{len(to_send):<{config.HEADER_SIZE}}' + str(to_send), 'utf-8')
        socket_to_send_to.sendall(to_send)
    except Exception as e:
        print("Exception: " + str(e))
        return False

def receive_message(socket_to_send_to):
    try:
        msg_header = socket_to_send_to.recv(config.HEADER_SIZE)

        if not len(msg_header):
            return False
        msg_len = int(msg_header)
        if msg_len > 256:
            data = []
            while (msg_len > 0):
                packet = socket_to_send_to.recv(256)
                if not packet:
                    break
                data.append(packet)
                msg_len -= len(packet)
            to_return = json.loads(b"".join(data))
        else:
            to_return = json.loads(socket_to_send_to.recv(msg_len).decode('utf-8'))
        return to_return
    except Exception as e:
        print("Exception: " + str(e))
        return False


def save_new_password(hashed_master_password, name, password, username, mail, pin_code, comment):
    try:
        connection = mysql.connect(
                host = MYSQL_HOST,
                user = MYSQL_USER,
                passwd = MYSQL_PASS,
                database = MYSQL_DATABASE,
                auth_plugin = 'mysql_native_password'
            )
        crsr = connection.cursor()

        sql_query = """SELECT * FROM users WHERE master_password = %s;"""
        sql_args = (hashed_master_password, )
        crsr.execute(sql_query, sql_args)

        user_id = crsr.fetchone()[0]
        sql_query = """INSERT INTO passwords (owner_id, name, password, username, mail, pin_code, comment) VALUES (%s,%s,%s,%s, %s, %s, %s);"""
        sql_args = (user_id, name, bytes(password, 'utf-8'), bytes(username, 'utf-8'), bytes(mail, 'utf-8'), bytes(pin_code, 'utf-8'), comment)
        crsr.execute(sql_query, sql_args)
        connection.commit()

        crsr.close()
        connection.close()
        return {'code': 0}
    except Exception as e:
        print("Exception: " + str(e))
    return {'code': -1, 'message': config.MESSAGE_ERROR_SERVER_SIDE}

def get_user_passwords_info(hashed_master_password):
    to_return = {'code': 0, 'results': []}
    try:
        connection = mysql.connect(
                host = MYSQL_HOST,
                user = MYSQL_USER,
                passwd = MYSQL_PASS,
                database = MYSQL_DATABASE,
                auth_plugin = 'mysql_native_password'
            )
        crsr = connection.cursor()
        sql_query = """SELECT * FROM users WHERE master_password = %s;"""
        sql_args = (hashed_master_password, )
        crsr.execute(sql_query, sql_args)

        user_id = crsr.fetchone()[0]

        sql_query = """SELECT Id, owner_id, name, TRIM(TRAILING CHAR(0) FROM password) as password, TRIM(TRAILING CHAR(0) FROM username) as username, TRIM(TRAILING CHAR(0) FROM mail) as mail, TRIM(TRAILING CHAR(0) FROM pin_code) as pin_code, comment FROM passwords WHERE owner_id = %s;"""
        sql_args = (user_id, )
        crsr.execute(sql_query, sql_args)
        
        data = crsr.fetchall()

        for row in data:
            to_append = {"name": row[2], "encrypted_password": row[3], "encrypted_username": "", "encrypted_mail": "", "encrypted_pin_code": "", "comment": row[7]}
            if (row[4] != None):
                to_append['encrypted_username'] = row[4]
            if (row[5] != None):
                to_append['encrypted_mail'] = row[5]
            if (row[6] != None):
                to_append['encrypted_pin_code'] = row[6]
            to_return['results'].append(to_append)

        crsr.close()
        connection.close()
        
    except Exception as e:
        print("Exception: " + str(e))
        to_return['code'] = -1
        to_return['message'] = config.MESSAGE_ERROR_SERVER_SIDE
    return to_return


def check_if_name_exists(hashed_master_password, name):
    try:
        connection = mysql.connect(
                host = MYSQL_HOST,
                user = MYSQL_USER,
                passwd = MYSQL_PASS,
                database = MYSQL_DATABASE,
                auth_plugin = 'mysql_native_password'
            )
        crsr = connection.cursor()

        sql_query = """SELECT * FROM users WHERE master_password = %s;"""
        sql_args = (hashed_master_password, )
        crsr.execute(sql_query, sql_args)

        user_id = crsr.fetchone()[0]

        sql_query = """SELECT * FROM passwords WHERE owner_id = %s AND name = %s;"""
        sql_args = (user_id, name)
        crsr.execute(sql_query, sql_args)

        data = crsr.fetchall()
        
        crsr.close()
        connection.close()

        if len(data) > 0:
            return {'code': 0, 'result': True}
        else:
            return {'code': 0, 'result': False}
    except Exception as e:
        print("Exception: " + str(e))
    return {'code': -1, 'message': config.MESSAGE_ERROR_SERVER_SIDE}

def update_existing_password(hashed_master_password, old_name, new_name, new_encrypted_password, new_encrypted_username, new_encrypted_mail, new_encrypted_pin_code, new_comment):
    try:
        connection = mysql.connect(
                host = MYSQL_HOST,
                user = MYSQL_USER,
                passwd = MYSQL_PASS,
                database = MYSQL_DATABASE,
                auth_plugin = 'mysql_native_password'
            )
        crsr = connection.cursor()
        sql_query = """SELECT * FROM users WHERE master_password = %s;"""
        sql_args = (hashed_master_password, )
        crsr.execute(sql_query, sql_args)

        user_id = crsr.fetchone()[0]

        sql_query = """UPDATE passwords SET name = %s, password = %s, username = %s, mail = %s, pin_code = %s, comment = %s WHERE name = %s AND owner_id = %s;"""
        sql_args = (new_name, bytes(new_encrypted_password, 'utf-8'), bytes(new_encrypted_username, 'utf-8'), bytes(new_encrypted_mail, 'utf-8'), bytes(new_encrypted_pin_code, 'utf-8'), new_comment, old_name, user_id)
        crsr.execute(sql_query, sql_args)
        connection.commit()
        
        crsr.close()
        connection.close()
        return {'code': 0}
    except Exception as e:
        print("Exception: " + str(e))
    return {'code': -1, 'message': config.MESSAGE_ERROR_SERVER_SIDE}

def remove_password(hashed_master_password, name):
    try:
        connection = mysql.connect(
                host = MYSQL_HOST,
                user = MYSQL_USER,
                passwd = MYSQL_PASS,
                database = MYSQL_DATABASE,
                auth_plugin = 'mysql_native_password'
            )
        crsr = connection.cursor()
        sql_query = """SELECT * FROM users WHERE master_password = %s;"""
        sql_args = (hashed_master_password, )
        crsr.execute(sql_query, sql_args)

        user_id = crsr.fetchone()[0]

        sql_query = """DELETE FROM passwords WHERE name = %s AND owner_id = %s;"""
        sql_args = (name, user_id)
        crsr.execute(sql_query, sql_args)
        connection.commit()
        
        crsr.close()
        return {'code': 0}
    except Exception as e:
        print("Exception: " + str(e))
    return {'code': -1, 'message': config.MESSAGE_ERROR_SERVER_SIDE}

def try_logging_in(username_str, password_str):
    try:
        username_or_mail = ("username" if not "@" in username_str else "mail")
        connection = mysql.connect(
                    host = MYSQL_HOST,
                    user = MYSQL_USER,
                    passwd = MYSQL_PASS,
                    database = MYSQL_DATABASE,
                    auth_plugin = 'mysql_native_password'
                )
        crsr = connection.cursor()
        sql_query = """SELECT * FROM users WHERE """ + username_or_mail + """ = %s;"""
        sql_args = (username_str, )
        crsr.execute(sql_query, sql_args)
        for row in crsr.fetchall():
            if bcrypt.checkpw(bytes(password_str, 'utf-8'), bytes(row[3], encoding='utf-8')):
                crsr.close()
                connection.close()
                return {'code': 0, 'message': 'Logged In', 'hashed_master_password': row[3]}
    except Exception as e:
        print("Exception: " + str(e))
        return {'code': -1, 'message': config.MESSAGE_ERROR_SERVER_SIDE}
    return {'code': 0, 'message': 'Nope'}


def try_signing_up(username_str, mail_str, hashed_pass):
    try:
        nbr_usernames = 0
        nbr_mails = 0
        connection = mysql.connect(
            host = MYSQL_HOST,
            user = MYSQL_USER,
            passwd = MYSQL_PASS,
            database = MYSQL_DATABASE,
            auth_plugin = 'mysql_native_password'
        )
        crsr = connection.cursor()
        sql_query = """SELECT * FROM users WHERE username = %s;"""
        sql_args = (username_str, )
        crsr.execute(sql_query, sql_args)

        for _ in crsr.fetchall():
            nbr_usernames += 1
            break
        
        sql_query = """SELECT * FROM users WHERE mail = %s;"""
        sql_args = (mail_str, )
        crsr.execute(sql_query, sql_args)

        for _ in crsr.fetchall():
            nbr_mails += 1
            break

        
        if (nbr_usernames != 0):
            crsr.close()
            connection.close()
            return {'code': -1, 'message': config.MESSAGE_USERNAME_TAKEN}
        if (nbr_mails != 0):
            crsr.close()
            connection.close()
            return {'code': -1, 'message': config.MESSAGE_MAIL_TAKEN}

        sql_query = """INSERT INTO users (username, mail, master_password) VALUES (%s,%s,%s);"""
        sql_args = (username_str, mail_str, bytes(hashed_pass, 'utf-8'))
        crsr.execute(sql_query, sql_args)
        connection.commit()

        sql_query = """SELECT * FROM users WHERE username = %s;"""
        sql_args = (username_str, )
        crsr.execute(sql_query, sql_args)

        hashed_master_password = crsr.fetchone()[3]

        crsr.close()
        connection.close()
        return {'code': 0, 'message': 'Success !', 'hashed_master_password': hashed_master_password}
    except Exception as e:
        print("Exception: " + str(e))
        print("Exception happened in try_signing_up")
        return {'code': -1, 'message': config.MESSAGE_ERROR_SERVER_SIDE}

if __name__ == "__main__":
    main()