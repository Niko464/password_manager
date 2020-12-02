from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import src.utils as utils
import src.utils_server as utils_server
import src.utils_encryption as utils_encryption
import src.config as config
import src.enums as enums
import src.add_edit_dialog_class as add_edit_dialog_class
from qtwidgets import PasswordEdit
import clipboard

class list_object(QHBoxLayout):
    def __init__(self, name, password, username, mail, pin_code, comment, main_wrapper):
        super().__init__()
        self.name = name
        self.password = password
        self.username = username
        self.mail = mail
        self.pin_code = pin_code
        self.comment = comment
        self.main_wrapper = main_wrapper
        self.create_ui()

    def create_ui(self):
        self.main_widget = QWidget()
        self.main_widget.setFixedWidth(self.main_wrapper.width - 100)
        self.main_widget.setStyleSheet('QWidget { background-color: ' + config.LIGHT_GRAY_COLOR + '; border-radius: 10px}')

        self.vbox_layout = QVBoxLayout()

        self.password_layout = QHBoxLayout()
        self.btns_layout = QHBoxLayout()

        self.name_label = QLabel("Name: " + self.get_formated_name(self.name))
        self.name_label.setFont(config.BASIC_STR_FONT)
        self.name_label.setStyleSheet('QLabel {color: ' + config.BASIC_STR_COLOR + '}')
        """
        if (self.username != ""):
            self.username_label = QLabel("Username: " + self.get_formated_name(self.username))
            self.username_label.setFont(config.BASIC_STR_FONT)
            self.username_label.setStyleSheet('QLabel {color: ' + config.BASIC_STR_COLOR + '}')
        if (self.mail != ""):
            self.mail_label = QLabel("Mail: " + self.get_formated_name(self.mail))
            self.mail_label.setFont(config.BASIC_STR_FONT)
            self.mail_label.setStyleSheet('QLabel {color: ' + config.BASIC_STR_COLOR + '}')
        if (self.pin_code != ""):
            self.pin_code_layout = QHBoxLayout()

            self.pin_code_label = QLabel("Pin code: ")
            self.pin_code_label.setFont(config.BASIC_STR_FONT)
            self.pin_code_label.setStyleSheet('QLabel {color: ' + config.BASIC_STR_COLOR + '}')

            self.pin_code_line_edit = PasswordEdit()
            self.pin_code_line_edit.setReadOnly(True)
            self.pin_code_line_edit.setText(str(self.pin_code))
            self.pin_code_line_edit.setStyleSheet('QLineEdit {background-color: ' + config.DARK_GRAY_COLOR + '; color: ' + config.BASIC_STR_COLOR + ';'
                                            'border-radius: 5px; font-size: 14pt}')

            self.pin_code_layout.addWidget(self.pin_code_label)
            self.pin_code_layout.addWidget(self.pin_code_line_edit)

        if (self.comment != ""):
            self.comment_label = QLabel("Comment: " + self.get_formated_name(self.username))
            self.comment_label.setFont(config.BASIC_STR_FONT)
            self.comment_label.setStyleSheet('QLabel {color: ' + config.BASIC_STR_COLOR + '}')
        """
        self.password_label = QLabel("Password: ")
        self.password_label.setFont(config.BASIC_STR_FONT)
        self.password_label.setStyleSheet('QLabel {color: ' + config.BASIC_STR_COLOR + '}')

        self.password_line_edit = PasswordEdit()
        self.password_line_edit.setReadOnly(True)
        self.password_line_edit.setText(str(self.password))
        self.password_line_edit.setStyleSheet('QLineEdit {background-color: ' + config.DARK_GRAY_COLOR + '; color: ' + config.BASIC_STR_COLOR + ';'
                                            'border-radius: 5px; font-size: 14pt}')

        self.copy_btn = QPushButton("Copy")
        self.copy_btn.setFixedSize(70, 30)
        self.copy_btn.setStyleSheet(config.BASIC_BLUE_BTN_STYLE_SHEET)
        self.copy_btn.clicked.connect(self.copy_btn_clicked)

        self.edit_btn = QPushButton("Edit")
        self.edit_btn.setFixedSize(70, 30)
        self.edit_btn.setStyleSheet(config.BASIC_BLUE_BTN_STYLE_SHEET)
        self.edit_btn.clicked.connect(self.edit_btn_clicked)

        self.delete_btn = QPushButton("Delete")
        self.delete_btn.setFixedSize(85, 30)
        self.delete_btn.setStyleSheet(config.BASIC_BLUE_BTN_STYLE_SHEET)
        self.delete_btn.clicked.connect(self.delete_btn_clicked)

        self.btns_layout.addStretch(1)
        self.btns_layout.addWidget(self.copy_btn)
        self.btns_layout.addWidget(self.edit_btn)
        self.btns_layout.addWidget(self.delete_btn)
        self.btns_layout.addStretch(1)

        self.password_layout.addWidget(self.password_label)
        self.password_layout.addWidget(self.password_line_edit)

        self.vbox_layout.addWidget(self.name_label)
        """
        if (self.username != ""):
            print("username: START" + str(self.username) + "END")
            self.vbox_layout.addWidget(self.username_label)
        if (self.mail != ""):
            self.vbox_layout.addWidget(self.mail_label)
        if (self.pin_code != ""):
            self.vbox_layout.addLayout(self.pin_code_layout)
        """
        self.vbox_layout.addLayout(self.password_layout)
        #if (self.comment != ""):
        #    self.vbox_layout.addWidget(self.comment_label)
        self.vbox_layout.addLayout(self.btns_layout)
        
        self.main_widget.setLayout(self.vbox_layout)

        self.addStretch(1)
        self.addWidget(self.main_widget)
        self.addStretch(1)

    def copy_btn_clicked(self):
        clipboard.copy(self.password_line_edit.text())

    def edit_btn_clicked(self):
        dialog = add_edit_dialog_class.add_edit_dialog(self.main_wrapper, enums.EDIT_DIALOG_ENUM, {"name": self.name, "password": self.password, "username": self.username, "mail": self.mail, "pin_code": self.pin_code, "comment": self.comment})
        if (dialog.exec()):
            new_info = dialog.get_new_password_info()
            # DO THE SQL QUERY
            encryption_key = utils_encryption.get_key_from_master_password(self.main_wrapper.user_info["master_password"])
            encrypted_password = utils_encryption.encode_password(encryption_key, new_info["password"])
            encrypted_username = utils_encryption.encode_password(encryption_key, new_info["username"]) if new_info['username'] != "" else bytes("", 'utf-8')
            encrypted_mail = utils_encryption.encode_password(encryption_key, new_info["mail"]) if new_info['mail'] != "" else bytes("", 'utf-8')
            encrypted_pin_code = utils_encryption.encode_password(encryption_key, new_info["pin_code"]) if new_info['pin_code'] != "" else bytes("", 'utf-8')

            server_result = utils_server.update_existing_password(self.main_wrapper.user_info["hashed_master_password"], self.name, new_info["name"], encrypted_password, encrypted_username, encrypted_mail, encrypted_pin_code, new_info["comment"])
            if (server_result == True):
                self.password_line_edit.setText(new_info["password"])
                self.name_label.setText("Name: " + self.get_formated_name(new_info["name"]))
                self.name = new_info["name"]
                self.password = new_info["password"]
                self.username = new_info["username"]
                self.mail = new_info["mail"]
                self.pin_code = new_info["pin_code"]
                self.comment = new_info["comment"]

    def delete_btn_clicked(self):
        confirm_dialog = utils.confirmation_dialog("Are you sure you want to delete '" + self.name + "' ?")
        if (confirm_dialog.exec() == QMessageBox.Yes):
            server_result = utils_server.remove_password(self.main_wrapper.user_info["hashed_master_password"], self.name)
            if (server_result == True):
                for obj in self.main_wrapper.password_list:
                    if (obj["name"] == self.name):
                        self.main_wrapper.password_list.remove(obj)
                        break
            # the next line removes this widget from the GUI
            self.main_widget.setParent(None)
            self.setParent(None)

    def get_formated_name(self, name):
        to_return = "\t"
        next_part = ""
        fm = QFontMetrics(config.BASIC_STR_FONT)
        for i in range(0, len(name)):
            next_part_width = fm.width(next_part + name[i])
            if (next_part_width > 400): #185
                to_return += next_part + "\n\t"
                next_part = ""
            next_part += name[i]
        if (next_part != ""):
            to_return += next_part
        return to_return