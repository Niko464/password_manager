from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from qtwidgets import PasswordEdit
import src.utils as utils
import src.config as config

class sign_in_up(QMainWindow):
    def __init__(self):
        super().__init__()
        self.central_widget = QWidget()
        self.main_layout = QGridLayout()
        self.width = 400
        self.height = 500
        self.create_ui()

    def create_ui(self):
        self.setWindowTitle("Sign In / Sign Up")
        utils.move_window_to_middle_of_screen(self.width, self.height, self)
        self.tabs_list = QTabWidget()

        self.tabs_list.addTab(sign_in_tab(self.width, self.height), "Sign In")
        self.tabs_list.addTab(sign_up_tab(self.width, self.height), "Sign Up")

        self.tabs_list.setStyleSheet('QTabBar { font-size: 18pt; font-family: Cursive; color: ' + config.BASIC_STR_COLOR + '} '
                                    'QTabBar::tab:selected {height: 50px; width: ' + str((self.width - 18) / 2) + 'px; background-color: ' + config.DARK_GRAY_COLOR + ';}'
                                    'QTabBar::tab:!selected {height: 50px; width: ' + str((self.width - 18) / 2) + 'px; background-color: ' + config.DARK_GRAY_COLOR + ';}'
                                    'QTabWidget>QWidget {background-color: ' + config.GRAY_COLOR + ';}'
                                    'QTabWidget::pane { border: 0; }')

        self.central_widget.setStyleSheet('QWidget {background-color: ' + config.GRAY_COLOR + ';}')

        self.main_layout.addWidget(self.tabs_list)
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)


class sign_in_tab(QWidget):
    def __init__(self, width, height):
        super().__init__()
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

        self.username_mail_field = utils.create_custom_line_edit(default_text="", placeholder_text="ex: example@gmail.com", regex=None)
        self.username_mail_field.setFixedSize((self.width - 100), 35)
        self.username_mail_field.setStyleSheet('QLineEdit {background-color: ' + config.DARK_GRAY_COLOR + '; color: ' + config.BASIC_STR_COLOR + ';'
                                                'border: 2px solid #1f80ff; border-radius: 5px; font-size: 14pt}')

        self.password_label = QLabel("Master Password:")
        self.password_label.setFont(config.BASIC_STR_FONT)
        self.password_label.setStyleSheet('QLabel {color: ' + config.BASIC_STR_COLOR + '}')

        self.password_field = PasswordEdit()
        self.password_field.setPlaceholderText("ex: password")
        self.password_field.setFixedSize((self.width - 100), 35)
        #self.password_field.setEchoMode(QLineEdit.Password)
        self.password_field.setStyleSheet('QLineEdit {background-color: ' + config.DARK_GRAY_COLOR + '; color: ' + config.BASIC_STR_COLOR + ';'
                                                'border: 2px solid #1f80ff; border-radius: 5px; font-size: 14pt}')

        self.login_btn = QPushButton("Login")
        self.login_btn.setFixedSize(self.width - 100, (self.height * 0.10))
        self.login_btn.setStyleSheet('QPushButton { font-size: 18pt; font-family: Cursive; border-radius: 15px; background-color: #27c215; color: ' + config.BASIC_STR_COLOR +  '}'
                                    'QPushButton:hover {background-color: #19f200}')



        self.main_layout.addStretch(1)
        self.main_layout.addWidget(self.username_mail_label)
        self.main_layout.addWidget(self.username_mail_field)
        self.main_layout.addWidget(self.password_label)
        self.main_layout.addWidget(self.password_field)
        self.main_layout.addWidget(self.login_btn)
        self.main_layout.addStretch(1)

        self.setLayout(self.hbox_layout)
    

class sign_up_tab(QWidget):
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.create_ui()

    def create_ui(self):
        self.main_layout = QVBoxLayout()
        self.hbox_layout = QHBoxLayout()

        self.hbox_layout.addStretch(1)
        self.hbox_layout.addLayout(self.main_layout)
        self.hbox_layout.addStretch(1)

        self.username_mail_label = QLabel("HI:")

        self.main_layout.addStretch(1)
        self.main_layout.addWidget(self.username_mail_label)
        self.main_layout.addStretch(1)

        self.setLayout(self.hbox_layout)