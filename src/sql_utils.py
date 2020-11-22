import src.private_config as private_config
import mysql.connector as mysql
import sys
import src.utils as utils

def save_new_password(owner_id, name, password):
    try:
        connection = mysql.connect(
                host = private_config.MYSQL_HOST,
                user = private_config.MYSQL_USER,
                passwd = private_config.MYSQL_PASS,
                database = private_config.MYSQL_DATABASE
            )
        crsr = connection.cursor()
        sql_query = """INSERT INTO passwords (owner_id, name, password) VALUES (%s,%s,%s)"""
        sql_args = (owner_id, name, password)
        crsr.execute(sql_query, sql_args)
        connection.commit()

        crsr.close()
        connection.close()
    except Exception as e:
        print("Exception in save_new_password, exiting")
        print(str(e))
        sys.exit(-1)

def get_user_passwords_info(owner_id, master_password):
    to_return = []
    try:
        connection = mysql.connect(
                host = private_config.MYSQL_HOST,
                user = private_config.MYSQL_USER,
                passwd = private_config.MYSQL_PASS,
                database = private_config.MYSQL_DATABASE
            )
        crsr = connection.cursor()
        sql_query = """SELECT * FROM passwords WHERE owner_id = %s"""
        sql_args = (owner_id, )
        crsr.execute(sql_query, sql_args)
        
        data = crsr.fetchall()

        fernet_key = utils.get_key_from_master_password(master_password)
        for row in data:
            to_return.append({"name": row[2], "password": utils.decode_password(fernet_key, bytes(row[3].decode(), encoding="utf8")).decode()})

        crsr.close()
        connection.close()
    except Exception as e:
        print("Exception in get_user_passwords_info, exiting")
        print(str(e))
        sys.exit(-1)
    return to_return


def check_if_name_exists(owner_id, name):
    try:
        connection = mysql.connect(
                host = private_config.MYSQL_HOST,
                user = private_config.MYSQL_USER,
                passwd = private_config.MYSQL_PASS,
                database = private_config.MYSQL_DATABASE
            )
        crsr = connection.cursor()
        sql_query = """SELECT * FROM passwords WHERE owner_id = %s AND name = %s"""
        sql_args = (owner_id, name)
        crsr.execute(sql_query, sql_args)

        data = crsr.fetchall()
        
        crsr.close()
        connection.close()

        if len(data) > 0:
            return True
        else:
            return False

    except Exception as e:
        print("Exception in check_if_name_exists, exiting")
        print(str(e))
        sys.exit(-1)

def update_existing_password(owner_id, old_name, new_name, new_hased_password):
    try:
        connection = mysql.connect(
                host = private_config.MYSQL_HOST,
                user = private_config.MYSQL_USER,
                passwd = private_config.MYSQL_PASS,
                database = private_config.MYSQL_DATABASE
            )
        crsr = connection.cursor()
        sql_query = """UPDATE passwords SET name = %s, password = %s WHERE name = %s AND owner_id = %s;"""
        sql_args = (new_name, new_hased_password, old_name, owner_id)
        crsr.execute(sql_query, sql_args)
        connection.commit()
        
        crsr.close()
        connection.close()
    except Exception as e:
        print("Exception in update_existing_password, exiting")
        print(str(e))
        sys.exit(-1)

def remove_password(owner_id, name):
    try:
        connection = mysql.connect(
                host = private_config.MYSQL_HOST,
                user = private_config.MYSQL_USER,
                passwd = private_config.MYSQL_PASS,
                database = private_config.MYSQL_DATABASE
            )
        crsr = connection.cursor()
        sql_query = """DELETE FROM passwords WHERE name = %s AND owner_id = %s;"""
        sql_args = (name, owner_id)
        crsr.execute(sql_query, sql_args)
        connection.commit()
        
        crsr.close()
        connection.close()
    except Exception as e:
        print("Exception in remove_password, exiting")
        print(str(e))
        sys.exit(-1)