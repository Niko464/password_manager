from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from qtwidgets import PasswordEdit
import bcrypt
import src.utils as utils
import src.config as config
import src.utils_server as utils_server

class sign_in_up(QDialog):
    def __init__(self):
        super().__init__()
        self.main_layout = QGridLayout()
        self.width = 400
        self.height = 500
        self.user_info = {"hashed_master_password": "", "master_password": ""}
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
                result = utils_server.try_logging_in(username_str, password_str)
                if ("Logged In" in result[0]):
                    self.parent.user_info["hashed_master_password"] = result[1]
                    self.parent.user_info["master_password"] = password_str
                    self.parent.accept()
                return
            except Exception as e:
                utils.show_error(msg=config.MESSAGE_DATABASE_DOWN + str(e), should_quit=True)
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
        self.confirmation_password_field.returnPressed.connect(self.sign_up_clicked)

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
            if ("@" in username_str):
                utils.show_error(config.MESSAGE_USERNAME_NO_AT_SYMBOL)
                return
            if ("@" in mail_str):
                if (len(username_str) >= config.MIN_USERNAME_SIZE):
                    if (len(password_str) >= config.MIN_MASTER_PASSWORD_SIZE):
                        if (password_str == password_confirmation_str):
                            try:
                                hashed_pass = bcrypt.hashpw(password_str.encode("utf-8"), bcrypt.gensalt())
                                result = utils_server.try_signing_up(username_str, mail_str, hashed_pass)
                                if (result['code'] == 0):
                                    utils.info_dialog(result['message'])
                                    self.parent.user_info["hashed_master_password"] = result['hashed_master_password']
                                    self.parent.user_info["master_password"] = password_str
                                    self.parent.accept()
                                else:
                                    utils.show_error(result['message'])
                                return
                            except:
                                utils.show_error(msg=config.MESSAGE_DATABASE_DOWN, should_quit=True)
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


