import sys
import src.utils as utils
import src.config as config
import src.utils_encryption as utils_encryption
import socket
import pickle

SERVER_IP = "45.140.164.47" #"45.140.164.47"
SERVER_PORT = 1234

def save_new_password(hashed_master_password, name, encrypted_password):
    try:
        server_socket =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((SERVER_IP, SERVER_PORT))
        msg = receive_message(server_socket)
        try:
            if (msg['code'] == 0):
                send_message(server_socket, {'code': 5, 'hashed_master_password': hashed_master_password, 'name': name, 'encrypted_password': encrypted_password})
                response = receive_message(server_socket)
                return response
            else:
                utils.show_error(config.MESSAGE_DATABASE_DOWN)
        except Exception as e:
            utils.show_error(config.MESSAGE_UNUSUAL_ERROR + "\n" + str(e), should_quit=True)
    except Exception as e:
        utils.show_error(config.MESSAGE_FAILED_TO_CONNECT_SERVER + "\n" + str(e), should_quit=True)
    return False

def get_user_passwords_info(hashed_master_password, master_password):
    to_return = []
    try:
        server_socket =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((SERVER_IP, SERVER_PORT))
        msg = receive_message(server_socket)
        try:
            if (msg['code'] == 0):
                send_message(server_socket, {'code': 3, 'hashed_master_password': hashed_master_password})
                response = receive_message(server_socket)
                # Decrypting passwords here !
                fernet_key = utils_encryption.get_key_from_master_password(master_password)
                for row in response['results']:
                    to_return.append({"name": row['name'], "password": utils_encryption.decode_password(fernet_key, bytes(row['encrypted_password'], encoding="utf8")).decode()})
            else:
                utils.show_error(config.MESSAGE_DATABASE_DOWN)
        except Exception as e:
            utils.show_error(config.MESSAGE_UNUSUAL_ERROR + "\n" + str(e), should_quit=True)
    except Exception as e:
        utils.show_error(config.MESSAGE_FAILED_TO_CONNECT_SERVER + "\n" + str(e), should_quit=True)
        return False
    return to_return


def check_if_name_exists(hashed_master_password, name):
    try:
        server_socket =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((SERVER_IP, SERVER_PORT))
        msg = receive_message(server_socket)
        try:
            if (msg['code'] == 0):
                send_message(server_socket, {'code': 4, 'hashed_master_password': hashed_master_password, 'name': name})
                response = receive_message(server_socket)
                if (response['code'] == 0):
                    return response['result']
                else:
                    utils.show_error(response['message'])
                    return True
            else:
                utils.show_error(config.MESSAGE_DATABASE_DOWN)
        except Exception as e:
            utils.show_error(config.MESSAGE_UNUSUAL_ERROR + "\n" + str(e), should_quit=True)
    except Exception as e:
        utils.show_error(config.MESSAGE_FAILED_TO_CONNECT_SERVER + "\n" + str(e), should_quit=True)
    return True

def update_existing_password(hashed_master_password, old_name, new_name, new_encrypted_password):
    try:
        server_socket =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((SERVER_IP, SERVER_PORT))
        msg = receive_message(server_socket)
        try:
            if (msg['code'] == 0):
                send_message(server_socket, {'code': 6, 'hashed_master_password': hashed_master_password, 'old_name': old_name, 'new_name': new_name, 'new_encrypted_password': new_encrypted_password})
                response = receive_message(server_socket)
                if (response['code'] == 0):
                    return True
                else:
                    utils.show_error(response['message'])
                    return False
            else:
                utils.show_error(config.MESSAGE_DATABASE_DOWN)
        except Exception as e:
            utils.show_error(config.MESSAGE_UNUSUAL_ERROR + "\n" + str(e), should_quit=True)
    except Exception as e:
        utils.show_error(config.MESSAGE_FAILED_TO_CONNECT_SERVER + "\n" + str(e), should_quit=True)
    return False

def remove_password(hashed_master_password, name):
    try:
        server_socket =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((SERVER_IP, SERVER_PORT))
        msg = receive_message(server_socket)
        try:
            if (msg['code'] == 0):
                send_message(server_socket, {'code': 7, 'hashed_master_password': hashed_master_password, 'name': name})
                response = receive_message(server_socket)
                if (response['code'] == 0):
                    return True
                else:
                    utils.show_error(response['message'])
                    return False
            else:
                utils.show_error(config.MESSAGE_DATABASE_DOWN)
        except Exception as e:
            utils.show_error(config.MESSAGE_UNUSUAL_ERROR + "\n" + str(e), should_quit=True)
    except Exception as e:
        utils.show_error(config.MESSAGE_FAILED_TO_CONNECT_SERVER + "\n" + str(e), should_quit=True)
    return False

def try_logging_in(username_str, password_str):
    try:
        server_socket =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((SERVER_IP, SERVER_PORT))
        msg = receive_message(server_socket)
        try:
            if (msg['code'] == 0):
                send_message(server_socket, {'code': 1, 'username_str': username_str, 'password_str': password_str})
                response = receive_message(server_socket)
                try:
                    if (response['message'] == 'Logged In'):
                        return ("Logged In", response['hashed_master_password'])
                    elif (response['code'] == -1):
                        utils.show_error(response['message'])
                    else:
                        utils.show_error(config.MESSAGE_INVALID_CREDENTIALS)
                except KeyError:
                    print("Key error!")
                    sys.exit(-1)
            else:
                utils.show_error(config.MESSAGE_DATABASE_DOWN)
        except Exception as e:
            utils.show_error(config.MESSAGE_UNUSUAL_ERROR + "\n" + str(e), should_quit=True)
    except Exception as e:
        utils.show_error(config.MESSAGE_FAILED_TO_CONNECT_SERVER + "\n" + str(e), should_quit=True)
    return ("Nope", 0)

def try_signing_up(username_str, mail_str, hashed_pass):
    try:
        server_socket =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((SERVER_IP, SERVER_PORT))
        msg = receive_message(server_socket)
        try:
            if (msg['code'] == 0):
                send_message(server_socket, {'code': 2, 'username_str': username_str, 'mail_str': mail_str, 'hashed_pass': hashed_pass})
                response = receive_message(server_socket)
                return response
            else:
                utils.show_error(config.MESSAGE_DATABASE_DOWN)
        except Exception as e:
            utils.show_error(config.MESSAGE_UNUSUAL_ERROR + "\n" + str(e), should_quit=True)
    except Exception as e:
        utils.show_error(config.MESSAGE_FAILED_TO_CONNECT_SERVER + "\n" + str(e), should_quit=True)

def send_message(socket_to_send_to, msg):
    to_send = pickle.dumps(msg)
    to_send = bytes(f'{len(to_send):<{config.HEADER_SIZE}}', 'utf-8') + to_send
    socket_to_send_to.send(to_send)

def receive_message(socket_to_send_to):
    try:
        msg_header = socket_to_send_to.recv(config.HEADER_SIZE)

        if not len(msg_header):
            return False
        msg_len = int(msg_header)
        to_return = pickle.loads(socket_to_send_to.recv(msg_len))
        return to_return
    except:
        return False