from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from qtwidgets import PasswordEdit
import src.utils as utils
import src.config as config
import src.utils_server as utils_server
import src.enums as enums
import random
import clipboard

class add_edit_dialog(QDialog):
    def __init__(self, main_wrapper, dialog_type, additional_info=None):
        super().__init__()
        self.type = dialog_type
        self.width = main_wrapper.width
        self.height = main_wrapper.height
        self.main_wrapper = main_wrapper
        self.additional_info = additional_info
        self.create_ui()

    def create_ui(self):
        if (self.type == enums.ADD_DIALOG_ENUM):
            self.setWindowTitle("Add a new password")
        elif (self.type == enums.EDIT_DIALOG_ENUM):
            self.setWindowTitle("Edit password")
        self.main_layout = QVBoxLayout()
        self.hbox_layout = QHBoxLayout()
        self.form_layout = QFormLayout()

        self.hbox_layout.addStretch(1)
        self.hbox_layout.addLayout(self.main_layout)
        self.hbox_layout.addStretch(1)
        self.setStyleSheet('QWidget {background-color: ' + config.GRAY_COLOR + ';}')


        self.name_label = QLabel("Name:")
        self.name_label.setFont(config.BASIC_STR_FONT)
        self.name_label.setStyleSheet('QLabel {color: ' + config.BASIC_STR_COLOR + '}')

        self.name_field = utils.create_custom_line_edit(default_text="", placeholder_text="Required", regex=None, max_len=config.MAX_NAME_SIZE)
        self.name_field.setFixedHeight(35)
        self.name_field.setStyleSheet(config.BASIC_BLUE_LINE_EDIT_STYLE_SHEET)

        self.username_label = QLabel("Username:")
        self.username_label.setFont(config.BASIC_STR_FONT)
        self.username_label.setStyleSheet('QLabel {color: ' + config.BASIC_STR_COLOR + '}')

        self.username_field = utils.create_custom_line_edit(default_text="", placeholder_text="Optional", regex=None, max_len=config.MAX_USERNAME_SIZE)
        self.username_field.setFixedHeight(35)
        self.username_field.setStyleSheet(config.BASIC_BLUE_LINE_EDIT_STYLE_SHEET)

        self.mail_label = QLabel("Mail:")
        self.mail_label.setFont(config.BASIC_STR_FONT)
        self.mail_label.setStyleSheet('QLabel {color: ' + config.BASIC_STR_COLOR + '}')

        self.mail_field = utils.create_custom_line_edit(default_text="", placeholder_text="Optional", regex=None, max_len=config.MAX_EMAIL_SIZE)
        self.mail_field.setFixedHeight(35)
        self.mail_field.setStyleSheet(config.BASIC_BLUE_LINE_EDIT_STYLE_SHEET)

        self.pin_code_label = QLabel("Pin code:")
        self.pin_code_label.setFont(config.BASIC_STR_FONT)
        self.pin_code_label.setStyleSheet('QLabel {color: ' + config.BASIC_STR_COLOR + '}')
        """
        self.pin_code_field = utils.create_custom_line_edit(default_text="", placeholder_text="Optional", regex=None, max_len=config.MAX_PIN_CODE_SIZE)
        self.pin_code_field.setFixedHeight(35)
        self.pin_code_field.setStyleSheet(config.BASIC_BLUE_LINE_EDIT_STYLE_SHEET)
        """
        self.pin_code_field = PasswordEdit()
        self.pin_code_field.setMaxLength(config.MAX_PIN_CODE_SIZE)
        self.pin_code_field.setPlaceholderText("Optional")
        self.pin_code_field.setFixedHeight(35)
        self.pin_code_field.setStyleSheet(config.BASIC_BLUE_LINE_EDIT_STYLE_SHEET)

        self.comment_label = QLabel("Comment:")
        self.comment_label.setFont(config.BASIC_STR_FONT)
        self.comment_label.setStyleSheet('QLabel {color: ' + config.BASIC_STR_COLOR + '}')

        self.comment_field = QTextEdit()
        self.comment_field.setFixedHeight(200)
        self.comment_field.setPlaceholderText("Optional - Any security questions or personal notes to add ?")
        self.comment_field.setStyleSheet("""
                                    QTextEdit {background-color: """ + config.DARK_GRAY_COLOR + """; color: """ + config.BASIC_STR_COLOR + """
                                    ;border: 2px solid """ + config.GRAY_COLOR + """; border-radius: 5px; font-size: 14pt}
                                    QTextEdit:hover {border: 1px solid """ + config.BLACK_COLOR + """
                                    ;}QTextEdit:focus {border: 2px solid """ + config.BLUE_COLOR + """;}
                                    """)


        self.password_label = QLabel("Password:")
        self.password_label.setFont(config.BASIC_STR_FONT)
        self.password_label.setStyleSheet('QLabel {color: ' + config.BASIC_STR_COLOR + '}')

        self.password_field = PasswordEdit()
        self.password_field.setMaxLength(config.MAX_PASSWORD_LENGTH)
        self.password_field.setPlaceholderText("Required")
        self.password_field.setFixedHeight(35)
        self.password_field.setStyleSheet(config.BASIC_BLUE_LINE_EDIT_STYLE_SHEET)
        self.password_field.textEdited.connect(self.pass_line_edit_changed)
    

        self.confirmation_password_label = QLabel("Confirm Password:")
        self.confirmation_password_label.setFont(config.BASIC_STR_FONT)
        self.confirmation_password_label.setStyleSheet('QLabel {color: ' + config.BASIC_STR_COLOR + '}')

        self.confirmation_password_field = PasswordEdit()
        self.confirmation_password_field.setMaxLength(config.MAX_PASSWORD_LENGTH)
        self.confirmation_password_field.setPlaceholderText("Required")
        self.confirmation_password_field.setFixedHeight(35)
        self.confirmation_password_field.setStyleSheet(config.BASIC_BLUE_LINE_EDIT_STYLE_SHEET)
        self.confirmation_password_field.textEdited.connect(self.confirmation_pass_line_edit_changed)


        self.generate_password_btn = QPushButton("Generate")
        self.generate_password_btn.setFixedSize((self.width - 100) / 2, 40)
        self.generate_password_btn.setStyleSheet(config.BASIC_BLUE_BTN_STYLE_SHEET)
        self.generate_password_btn.clicked.connect(self.generate_password_clicked)


        self.copy_password_btn = QPushButton("Copy")
        self.copy_password_btn.setFixedSize((self.width - 100) / 2, 40)
        self.copy_password_btn.setStyleSheet(config.BASIC_BLUE_BTN_STYLE_SHEET)
        self.copy_password_btn.clicked.connect(self.copy_password_btn_clicked)
        
        self.generate_copy_layout = QHBoxLayout()
        self.generate_copy_layout.addWidget(self.generate_password_btn)
        self.generate_copy_layout.addWidget(self.copy_password_btn)
        
        self.add_btn = QPushButton()
        if (self.type == enums.ADD_DIALOG_ENUM):
            self.add_btn.setText("Add")
        elif (self.type == enums.EDIT_DIALOG_ENUM):
            self.add_btn.setText("Confirm")
            self.name_field.setText(self.additional_info["name"])
            self.username_field.setText(self.additional_info["username"])
            self.mail_field.setText(self.additional_info["mail"])
            self.pin_code_field.setText(self.additional_info["pin_code"])
            self.comment_field.setPlainText(self.additional_info["comment"])
            self.password_field.setText(self.additional_info["password"])
            self.confirmation_password_field.setText(self.additional_info["password"])
        self.add_btn.setFixedSize((self.width - 100) / 2, 50)
        self.add_btn.setStyleSheet(config.BASIC_BLUE_BTN_STYLE_SHEET)
        self.add_btn.clicked.connect(self.add_btn_clicked)


        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setFixedSize((self.width - 100) / 2, 50)
        self.cancel_btn.setStyleSheet(config.BASIC_RED_BTN_STYLE_SHEET)
        self.cancel_btn.clicked.connect(self.cancel_btn_clicked)

        self.add_cancel_layout = QHBoxLayout()
        self.add_cancel_layout.addWidget(self.cancel_btn)
        self.add_cancel_layout.addWidget(self.add_btn)


        self.form_layout.setVerticalSpacing(5)
        self.form_layout.setLabelAlignment(Qt.AlignRight)
        self.form_layout.addRow(self.name_label, self.name_field)
        self.form_layout.addRow(self.username_label, self.username_field)
        self.form_layout.addRow(self.mail_label, self.mail_field)
        self.form_layout.addRow(self.pin_code_label, self.pin_code_field)
        self.form_layout.addRow(self.password_label, self.password_field)
        self.form_layout.addRow(self.confirmation_password_label, self.confirmation_password_field)


        self.main_layout.addStretch(1)
        self.main_layout.addLayout(self.form_layout)
        self.main_layout.addLayout(self.generate_copy_layout)
        self.main_layout.addWidget(self.comment_label)
        self.main_layout.addWidget(self.comment_field)
        self.main_layout.addItem(QSpacerItem(10, 50, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.main_layout.addLayout(self.add_cancel_layout)
        self.main_layout.addStretch(1)

        self.setLayout(self.hbox_layout)

    def generate_password_clicked(self):
        password = utils.create_random_password(random.randint(config.MIN_PASSWORD_GENERATION_LENGTH, config.MAX_PASSWORD_GENERATION_LENGTH))
        self.password_field.setText(password)
        self.confirmation_password_field.setText(password)

    def copy_password_btn_clicked(self):
        clipboard.copy(self.password_field.text())

    def pass_line_edit_changed(self, msg):
        if (len(msg) > config.MAX_PASSWORD_LENGTH):
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

    def add_btn_clicked(self):
        name_str = self.name_field.text()
        password_str = self.password_field.text()
        confirmation_password_str = self.confirmation_password_field.text()
        comment_str = self.comment_field.toPlainText()
        username_str = self.username_field.text()
        mail_str = self.mail_field.text()
        pin_code_str = self.pin_code_field.text()

        if (name_str != "" and password_str != "" and confirmation_password_str != ""):
            if (password_str == confirmation_password_str):
                if (len(password_str) <= config.MAX_PASSWORD_LENGTH):
                    if (len(comment_str) <= config.MAX_COMMENT_SIZE):
                        if (self.type == enums.ADD_DIALOG_ENUM):
                            if (not utils_server.check_if_name_exists(self.main_wrapper.user_info["hashed_master_password"], name_str)):
                                self.accept()
                            else:
                                utils.show_error(config.MESSAGE_NAME_ALREADY_EXISTS)
                        elif (self.type == enums.EDIT_DIALOG_ENUM):
                            if ((self.additional_info["name"] != name_str) or (self.additional_info["password"] != password_str) or (self.additional_info["username"] != username_str) or
                                (self.additional_info["mail"] != mail_str) or (self.additional_info["pin_code"] != pin_code_str) or (self.additional_info['comment'] != comment_str)):
                                self.accept()
                            else:
                                utils.show_error(config.MESSAGE_INVALID_EDIT)
                    else:
                        utils.show_error(config.MESSAGE_COMMENT_INVALID_LENGTH)
                else:
                    utils.show_error(config.MESSAGE_PASSWORD_INVALID_LENGTH)
            else:
                utils.show_error(config.MESSAGE_CONFIRMATION_PASS_DIFFERENT_PASS)
        else:
            utils.show_error(config.MESSAGE_FILL_IN_INFO)

    def cancel_btn_clicked(self):
        self.reject()

    def get_new_password_info(self):
        return {"name": self.name_field.text(), "password": self.password_field.text(), "username": self.username_field.text(), "mail": self.mail_field.text(), "pin_code": self.pin_code_field.text(), "comment": self.comment_field.toPlainText()}