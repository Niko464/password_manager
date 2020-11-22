from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from qtwidgets import PasswordEdit
import bcrypt
import mysql.connector as mysql
import src.utils as utils
import src.config as config
import src.private_config as private_config

class sign_in_up(QDialog):
    def __init__(self):
        super().__init__()
        self.main_layout = QGridLayout()
        self.width = 400
        self.height = 500
        self.user_info = {"user_id": "", "master_password": ""}
        self.create_ui()

    def create_ui(self):
        self.setWindowTitle("Sign In / Sign Up")
        utils.move_window_to_middle_of_screen(self.width, self.height, self)
        self.tabs_list = QTabWidget()

        self.tabs_list.addTab(sign_in_tab(self.width, self.height, self), "Sign In")
        self.tabs_list.addTab(sign_up_tab(self.width, self.height, self), "Sign Up")

        self.tabs_list.setStyleSheet('QTabBar { font-size: 18pt; font-family: Cursive; color: ' + config.BASIC_STR_COLOR + '} '
                                    'QTabBar::tab:selected {height: 50px; width: ' + str((self.width - 25) / 2) + 'px; background-color: ' + config.DARK_GRAY_COLOR + ';}'
                                    'QTabBar::tab:!selected {height: 50px; width: ' + str((self.width - 25) / 2) + 'px; background-color: ' + config.DARK_GRAY_COLOR + ';}'
                                    'QTabWidget>QWidget {background-color: ' + config.GRAY_COLOR + ';}'
                                    'QTabWidget::pane { border: 0; }')

        self.setStyleSheet('QWidget {background-color: ' + config.GRAY_COLOR + ';}')

        self.main_layout.addWidget(self.tabs_list)
        self.setLayout(self.main_layout)

    def get_user_info(self):
        return self.user_info


class sign_in_tab(QWidget):
    def __init__(self, width, height, parent):
        super().__init__()
        self.parent = parent
        self.width = width
        self.height = height
        self.create_ui()

    def create_ui(self):
        self.main_layout = QVBoxLayout()
        self.hbox_layout = QHBoxLayout()

        self.hbox_layout.addStretch(1)
        self.hbox_layout.addLayout(self.main_layout)
        self.hbox_layout.addStretch(1)



        self.username_mail_label = QLabel("Username or Mail:")
        self.username_mail_label.setFont(config.BASIC_STR_FONT)
        self.username_mail_label.setStyleSheet('QLabel {color: ' + config.BASIC_STR_COLOR + '}')

        self.username_mail_field = utils.create_custom_line_edit(default_text="", placeholder_text="ex: example@gmail.com", regex=None, max_len=max(config.MAX_USERNAME_SIZE, config.MAX_EMAIL_SIZE))
        self.username_mail_field.setFixedSize((self.width - 100), 35)
        self.username_mail_field.setStyleSheet('QLineEdit {background-color: ' + config.DARK_GRAY_COLOR + '; color: ' + config.BASIC_STR_COLOR + ';'
                                            'border: 2px solid ' + config.GRAY_COLOR + '; border-radius: 5px; font-size: 14pt}'
                                            'QLineEdit:hover {border: 1px solid ' + config.BLACK_COLOR + ';}'
                                            'QLineEdit:focus {border: 2px solid ' + config.BLUE_COLOR + ';}')

        self.password_label = QLabel("Master Password:")
        self.password_label.setFont(config.BASIC_STR_FONT)
        self.password_label.setStyleSheet('QLabel {color: ' + config.BASIC_STR_COLOR + '}')

        self.password_field = PasswordEdit()
        self.password_field.setPlaceholderText("ex: password")
        self.password_field.setFixedSize((self.width - 100), 35)
        self.password_field.setStyleSheet('QLineEdit {background-color: ' + config.DARK_GRAY_COLOR + '; color: ' + config.BASIC_STR_COLOR + ';'
                                            'border: 2px solid ' + config.GRAY_COLOR + '; border-radius: 5px; font-size: 14pt}'
                                            'QLineEdit:hover {border: 1px solid ' + config.BLACK_COLOR + ';}'
                                            'QLineEdit:focus {border: 2px solid ' + config.BLUE_COLOR + ';}')

        self.login_btn = QPushButton("Login")
        self.login_btn.setFixedSize(self.width - 100, (self.height * 0.10))
        self.login_btn.setStyleSheet('QPushButton { font-size: 18pt; font-family: Cursive; border-radius: 15px; background-color: ' + config.BLUE_COLOR + '; color: ' + config.BASIC_STR_COLOR +  '}'
                                    'QPushButton:hover {background-color: ' + config.DARK_BLUE_COLOR + '}')
        self.login_btn.clicked.connect(self.login_btn_clicked)



        self.main_layout.addStretch(1)
        self.main_layout.addWidget(self.username_mail_label)
        self.main_layout.addWidget(self.username_mail_field)
        self.main_layout.addWidget(self.password_label)
        self.main_layout.addWidget(self.password_field)
        self.main_layout.addWidget(self.login_btn)
        self.main_layout.addStretch(1)

        self.setLayout(self.hbox_layout)

    def login_btn_clicked(self):
        username_str = self.username_mail_field.text()
        password_str = self.password_field.text()

        if (username_str != "" and password_str != ""):
            try:
                username_or_mail = ("username" if not "@" in username_str else "mail")
                connection = mysql.connect(
                            host = private_config.MYSQL_HOST,
                            user = private_config.MYSQL_USER,
                            passwd = private_config.MYSQL_PASS,
                            database = private_config.MYSQL_DATABASE
                        )
                crsr = connection.cursor()
                sql_query = """SELECT * FROM users WHERE """ + username_or_mail + """ = %s"""
                sql_args = (username_str, )
                crsr.execute(sql_query, sql_args)
                for row in crsr.fetchall():
                    try:
                        if bcrypt.checkpw(password_str.encode("utf-8"), bytes(row[3])):
                            self.parent.user_info["user_id"] = row[0]
                            self.parent.user_info["master_password"] = password_str
                            crsr.close()
                            connection.close()
                            self.parent.accept()
                            return
                    except KeyError as e:
                        utils.show_error("KeyError - Should never happen...")
                utils.show_error(config.MESSAGE_INVALID_CREDENTIALS)
                return

            except Exception as e:
                utils.show_error("An Unusual error occurred...\n" + str(e))
        else:
            utils.show_error(config.MESSAGE_FILL_IN_INFO)
    

class sign_up_tab(QWidget):
    def __init__(self, width, height, parent):
        super().__init__()
        self.parent = parent
        self.width = width
        self.height = height
        self.create_ui()

    def create_ui(self):
        self.main_layout = QVBoxLayout()
        self.hbox_layout = QHBoxLayout()

        self.hbox_layout.addStretch(1)
        self.hbox_layout.addLayout(self.main_layout)
        self.hbox_layout.addStretch(1)


        self.username_label = QLabel("Username:")
        self.username_label.setFont(config.BASIC_STR_FONT)
        self.username_label.setStyleSheet('QLabel {color: ' + config.BASIC_STR_COLOR + '}')

        self.username_field = utils.create_custom_line_edit(default_text="", placeholder_text="ex: Username", regex=None, max_len=config.MAX_USERNAME_SIZE)
        self.username_field.setFixedSize((self.width - 100), 35)
        self.username_field.setStyleSheet('QLineEdit {background-color: ' + config.DARK_GRAY_COLOR + '; color: ' + config.BASIC_STR_COLOR + ';'
                                            'border: 2px solid ' + config.GRAY_COLOR + '; border-radius: 5px; font-size: 14pt}'
                                            'QLineEdit:hover {border: 1px solid ' + config.BLACK_COLOR + ';}'
                                            'QLineEdit:focus {border: 2px solid ' + config.BLUE_COLOR + ';}')

        self.mail_label = QLabel("Mail:")
        self.mail_label.setFont(config.BASIC_STR_FONT)
        self.mail_label.setStyleSheet('QLabel {color: ' + config.BASIC_STR_COLOR + '}')

        self.mail_field = utils.create_custom_line_edit(default_text="", placeholder_text="ex: example@gmail.com", regex=None, max_len=config.MAX_EMAIL_SIZE)
        self.mail_field.setFixedSize((self.width - 100), 35)
        self.mail_field.setStyleSheet('QLineEdit {background-color: ' + config.DARK_GRAY_COLOR + '; color: ' + config.BASIC_STR_COLOR + ';'
                                            'border: 2px solid ' + config.GRAY_COLOR + '; border-radius: 5px; font-size: 14pt}'
                                            'QLineEdit:hover {border: 1px solid ' + config.BLACK_COLOR + ';}'
                                            'QLineEdit:focus {border: 2px solid ' + config.BLUE_COLOR + ';}')

        self.password_label = QLabel("Master Password:")
        self.password_label.setFont(config.BASIC_STR_FONT)
        self.password_label.setStyleSheet('QLabel {color: ' + config.BASIC_STR_COLOR + '}')

        self.password_field = PasswordEdit()
        self.password_field.setPlaceholderText("ex: password")
        self.password_field.setFixedSize((self.width - 100), 35)
        self.password_field.setStyleSheet('QLineEdit {background-color: ' + config.DARK_GRAY_COLOR + '; color: ' + config.BASIC_STR_COLOR + ';'
                                            'border: 2px solid ' + config.GRAY_COLOR + '; border-radius: 5px; font-size: 14pt}'
                                            'QLineEdit:hover {border: 1px solid ' + config.BLACK_COLOR + ';}'
                                            'QLineEdit:focus {border: 2px solid ' + config.BLUE_COLOR + ';}')
        self.password_field.textEdited.connect(self.pass_line_edit_changed)
    

        self.confirmation_password_label = QLabel("Confirm Password:")
        self.confirmation_password_label.setFont(config.BASIC_STR_FONT)
        self.confirmation_password_label.setStyleSheet('QLabel {color: ' + config.BASIC_STR_COLOR + '}')

        self.confirmation_password_field = PasswordEdit()
        self.confirmation_password_field.setPlaceholderText("ex: password")
        self.confirmation_password_field.setFixedSize((self.width - 100), 35)
        self.confirmation_password_field.setStyleSheet('QLineEdit {background-color: ' + config.DARK_GRAY_COLOR + '; color: ' + config.BASIC_STR_COLOR + ';'
                                            'border: 2px solid ' + config.GRAY_COLOR + '; border-radius: 5px; font-size: 14pt}'
                                            'QLineEdit:hover {border: 1px solid ' + config.BLACK_COLOR + ';}'
                                            'QLineEdit:focus {border: 2px solid ' + config.BLUE_COLOR + ';}')
        self.confirmation_password_field.textEdited.connect(self.confirmation_pass_line_edit_changed)

        self.sign_up_btn = QPushButton("Sign Up")
        self.sign_up_btn.setFixedSize(self.width - 100, (self.height * 0.10))
        self.sign_up_btn.setStyleSheet('QPushButton { font-size: 18pt; font-family: Cursive; border-radius: 15px; background-color: ' + config.BLUE_COLOR + '; color: ' + config.BASIC_STR_COLOR +  '}'
                                    'QPushButton:hover {background-color: ' + config.DARK_BLUE_COLOR + '}')
        self.sign_up_btn.clicked.connect(self.sign_up_clicked)



        self.main_layout.addStretch(1)
        self.main_layout.addWidget(self.username_label)
        self.main_layout.addWidget(self.username_field)
        self.main_layout.addWidget(self.mail_label)
        self.main_layout.addWidget(self.mail_field)
        self.main_layout.addWidget(self.password_label)
        self.main_layout.addWidget(self.password_field)
        self.main_layout.addWidget(self.confirmation_password_label)
        self.main_layout.addWidget(self.confirmation_password_field)
        self.main_layout.addWidget(self.sign_up_btn)
        self.main_layout.addStretch(1)

        self.setLayout(self.hbox_layout)

    def pass_line_edit_changed(self, msg):
        if (len(msg) > config.MAX_MASTER_PASSWORD_SIZE):
            self.password_field.setStyleSheet('QLineEdit {background-color: ' + config.DARK_GRAY_COLOR + '; color: ' + config.BASIC_STR_COLOR + ';'
                                            'border: 2px solid red; border-radius: 5px; font-size: 14pt}'
                                            'QLineEdit:hover { border: 1px solid red;}'
                                            'QLineEdit:focus { border: 2px solid red;}')
        else:
            self.password_field.setStyleSheet('QLineEdit {background-color: ' + config.DARK_GRAY_COLOR + '; color: ' + config.BASIC_STR_COLOR + ';'
                                            'border: 2px solid ' + config.GRAY_COLOR + '; border-radius: 5px; font-size: 14pt}'
                                            'QLineEdit:hover {border: 1px solid ' + config.BLACK_COLOR + ';}'
                                            'QLineEdit:focus {border: 2px solid ' + config.BLUE_COLOR + ';}')

    def confirmation_pass_line_edit_changed(self, msg):
        pass_txt = self.password_field.text()
        if (pass_txt != ""):
            if (msg != pass_txt):
                self.confirmation_password_field.setStyleSheet('QLineEdit {background-color: ' + config.DARK_GRAY_COLOR + '; color: ' + config.BASIC_STR_COLOR + ';'
                                                'border: 2px solid red; border-radius: 5px; font-size: 14pt}'
                                                'QLineEdit:hover { border: 1px solid red;}'
                                                'QLineEdit:focus { border: 2px solid red;}')
            else:
                self.confirmation_password_field.setStyleSheet('QLineEdit {background-color: ' + config.DARK_GRAY_COLOR + '; color: ' + config.BASIC_STR_COLOR + ';'
                                                'border: 2px solid green; border-radius: 5px; font-size: 14pt}'
                                                'QLineEdit:hover { border: 1px solid green;}'
                                                'QLineEdit:focus { border: 2px solid green;}')
        else:
            self.confirmation_password_field.setStyleSheet('QLineEdit {background-color: ' + config.DARK_GRAY_COLOR + '; color: ' + config.BASIC_STR_COLOR + ';'
                                            'border: 2px solid ' + config.GRAY_COLOR + '; border-radius: 5px; font-size: 14pt}'
                                            'QLineEdit:hover {border: 1px solid ' + config.BLACK_COLOR + ';}'
                                            'QLineEdit:focus {border: 2px solid ' + config.BLUE_COLOR + ';}')

    def sign_up_clicked(self):
        username_str = self.username_field.text()
        mail_str = self.mail_field.text()
        password_str = self.password_field.text()
        password_confirmation_str = self.confirmation_password_field.text()
        if (username_str != "" and mail_str != "" and password_str != "" and password_confirmation_str != ""):
            print(mail_str)
            if ("@" in mail_str):
                if (len(username_str) >= config.MIN_USERNAME_SIZE):
                    if (len(password_str) >= config.MIN_MASTER_PASSWORD_SIZE):
                        if (password_str == password_confirmation_str):
                            try:
                                nbr_usernames = 0
                                nbr_mails = 0
                                connection = mysql.connect(
                                    host = private_config.MYSQL_HOST,
                                    user = private_config.MYSQL_USER,
                                    passwd = private_config.MYSQL_PASS,
                                    database = private_config.MYSQL_DATABASE
                                )
                                crsr = connection.cursor()
                                sql_query = """SELECT * FROM users WHERE username = %s"""
                                sql_args = (username_str, )
                                crsr.execute(sql_query, sql_args)

                                for _ in crsr.fetchall():
                                    nbr_usernames += 1
                                    break
                                
                                sql_query = """SELECT * FROM users WHERE mail = %s"""
                                sql_args = (mail_str, )
                                crsr.execute(sql_query, sql_args)

                                for _ in crsr.fetchall():
                                    nbr_mails += 1
                                    break
                            
                                
                                if (nbr_usernames != 0):
                                    utils.show_error(config.MESSAGE_USERNAME_TAKEN)
                                    crsr.close()
                                    connection.close()
                                    return
                                if (nbr_mails != 0):
                                    utils.show_error(config.MESSAGE_MAIL_TAKEN)
                                    crsr.close()
                                    connection.close()
                                    return
                                hashed_pass = bcrypt.hashpw(password_str.encode("utf-8"), bcrypt.gensalt())
                                
                                sql_query = """INSERT INTO users (username, mail, master_password) VALUES (%s,%s, _binary %s)"""
                                sql_args = (username_str, mail_str, hashed_pass)
                                crsr.execute(sql_query, sql_args)
                                connection.commit()

                                crsr.close()
                                connection.close()
                                utils.info_dialog("Success !")

                            except Exception as e:
                                utils.show_error("An Unusual error occurred...\n" + str(e))
                        else:
                            utils.show_error(config.MESSAGE_CONFIRMATION_PASS_DIFFERENT_PASS)
                    else:
                        utils.show_error(config.MESSAGE_MASTER_PASSWORD_INVALID_LENGTH)
                else:
                    utils.show_error(config.MESSAGE_USERNAME_INVALID_LENGTH)
            else:
                utils.show_error(config.MESSAGE_INVALID_MAIL)
        else:
            utils.show_error(config.MESSAGE_FILL_IN_INFO)


