from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from qtwidgets import PasswordEdit
import src.utils as utils
import src.config as config
import random
import clipboard

class add_dialog(QDialog):
    def __init__(self, main_wrapper):
        super().__init__()
        self.width = main_wrapper.width
        self.height = main_wrapper.height
        self.create_ui()

    def create_ui(self):
        self.setWindowTitle("Add a new password")
        self.main_layout = QVBoxLayout()
        self.hbox_layout = QHBoxLayout()

        self.hbox_layout.addStretch(1)
        self.hbox_layout.addLayout(self.main_layout)
        self.hbox_layout.addStretch(1)
        self.setStyleSheet('QWidget {background-color: ' + config.GRAY_COLOR + ';}')


        self.name_label = QLabel("Name:")
        self.name_label.setFont(config.BASIC_STR_FONT)
        self.name_label.setStyleSheet('QLabel {color: ' + config.BASIC_STR_COLOR + '}')

        self.name_field = utils.create_custom_line_edit(default_text="", placeholder_text="ex: <name>'s Minecraft Account", regex=None, max_len=config.MAX_NAME_SIZE)
        self.name_field.setFixedSize((self.width - 100), 35)
        self.name_field.setStyleSheet('QLineEdit {background-color: ' + config.DARK_GRAY_COLOR + '; color: ' + config.BASIC_STR_COLOR + ';'
                                            'border: 2px solid ' + config.GRAY_COLOR + '; border-radius: 5px; font-size: 14pt}'
                                            'QLineEdit:hover {border: 1px solid ' + config.BLACK_COLOR + ';}'
                                            'QLineEdit:focus {border: 2px solid ' + config.BLUE_COLOR + ';}')

        self.password_label = QLabel("Master Password:")
        self.password_label.setFont(config.BASIC_STR_FONT)
        self.password_label.setStyleSheet('QLabel {color: ' + config.BASIC_STR_COLOR + '}')

        self.password_field = PasswordEdit()
        self.password_field.setPlaceholderText("ex: zfdslmkxLPMofgk=dg457")
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
        self.confirmation_password_field.setPlaceholderText("ex: zfdslmkxLPMofgk=dg457")
        self.confirmation_password_field.setFixedSize((self.width - 100), 35)
        self.confirmation_password_field.setStyleSheet('QLineEdit {background-color: ' + config.DARK_GRAY_COLOR + '; color: ' + config.BASIC_STR_COLOR + ';'
                                            'border: 2px solid ' + config.GRAY_COLOR + '; border-radius: 5px; font-size: 14pt}'
                                            'QLineEdit:hover {border: 1px solid ' + config.BLACK_COLOR + ';}'
                                            'QLineEdit:focus {border: 2px solid ' + config.BLUE_COLOR + ';}')
        self.confirmation_password_field.textEdited.connect(self.confirmation_pass_line_edit_changed)


        self.generate_password_btn = QPushButton("Generate")
        self.generate_password_btn.setFixedSize((self.width - 100) / 2, self.height * 0.06)
        self.generate_password_btn.setStyleSheet('QPushButton { font-size: 18pt; font-family: Cursive; border-radius: 15px; background-color: ' + config.BLUE_COLOR + ';'
                                                'color: ' + config.BASIC_STR_COLOR +  '}'
                                                'QPushButton:hover {background-color: ' + config.DARK_BLUE_COLOR + '}')
        self.generate_password_btn.released.connect(self.generate_password_clicked)


        self.copy_password_btn = QPushButton("Copy")
        self.copy_password_btn.setFixedSize((self.width - 100) / 2, self.height * 0.06)
        self.copy_password_btn.setStyleSheet('QPushButton { font-size: 18pt; font-family: Cursive; border-radius: 15px; background-color: ' + config.BLUE_COLOR + ';'
                                                'color: ' + config.BASIC_STR_COLOR +  '}'
                                                'QPushButton:hover {background-color: ' + config.DARK_BLUE_COLOR + '}')
        self.copy_password_btn.released.connect(self.copy_password_btn_clicked)

        self.generate_copy_layout = QHBoxLayout()
        self.generate_copy_layout.addWidget(self.generate_password_btn)
        self.generate_copy_layout.addWidget(self.copy_password_btn)

        self.add_btn = QPushButton("Add")
        self.add_btn.setFixedSize((self.width - 100) / 2, self.height * 0.10)
        self.add_btn.setStyleSheet('QPushButton { font-size: 18pt; font-family: Cursive; border-radius: 15px; background-color: ' + config.BLUE_COLOR + ';'
                                                'color: ' + config.BASIC_STR_COLOR +  '}'
                                                'QPushButton:hover {background-color: ' + config.DARK_BLUE_COLOR + '}')
        self.add_btn.released.connect(self.add_btn_clicked)


        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setFixedSize((self.width - 100) / 2, self.height * 0.10)
        self.cancel_btn.setStyleSheet('QPushButton { font-size: 18pt; font-family: Cursive; border-radius: 15px; background-color: ' + config.RED_COLOR + ';'
                                                'color: ' + config.BASIC_STR_COLOR +  '}'
                                                'QPushButton:hover {background-color: ' + config.DARK_RED_COLOR + '}')
        self.cancel_btn.released.connect(self.cancel_btn_clicked)

        self.add_cancel_layout = QHBoxLayout()
        self.add_cancel_layout.addWidget(self.cancel_btn)
        self.add_cancel_layout.addWidget(self.add_btn)




        self.main_layout.addStretch(1)
        self.main_layout.addWidget(self.name_label)
        self.main_layout.addWidget(self.name_field)
        self.main_layout.addWidget(self.password_label)
        self.main_layout.addWidget(self.password_field)
        self.main_layout.addWidget(self.confirmation_password_label)
        self.main_layout.addWidget(self.confirmation_password_field)
        self.main_layout.addLayout(self.generate_copy_layout)
        self.main_layout.addItem(QSpacerItem(10, 25, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.main_layout.addLayout(self.add_cancel_layout)
        self.main_layout.addStretch(1)

        self.setLayout(self.hbox_layout)

    def generate_password_clicked(self):
        password = utils.create_random_password(random.randint(config.MIN_PASSWORD_LENGTH, config.MAX_PASSWORD_LENGTH))
        self.password_field.setText(password)
        self.confirmation_password_field.setText(password)

    def copy_password_btn_clicked(self):
        clipboard.copy(self.password_field.text())

    def pass_line_edit_changed(self):
        pass

    def confirmation_pass_line_edit_changed(self):
        pass

    def add_btn_clicked(self):
        name_str = self.name_field.text()
        password_str = self.password_field.text()
        confirmation_password_str = self.confirmation_password_field.text()

        if (name_str != "" and password_str != "" and confirmation_password_str != ""):
            if (password_str == confirmation_password_str):
                if (len(password_str) <= config.MAX_PASSWORD_LENGTH):
                    self.accept()
                else:
                    utils.show_error(config.MESSAGE_PASSWORD_INVALID_LENGTH)
            else:
                utils.show_error(config.MESSAGE_CONFIRMATION_PASS_DIFFERENT_PASS)
        else:
            utils.show_error(config.MESSAGE_FILL_IN_INFO)

    def cancel_btn_clicked(self):
        self.reject()

    def get_new_password_info(self):
        return {"name": self.name_field.text(), "password": self.password_field.text()}