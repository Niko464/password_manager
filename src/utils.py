from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from cryptography.fernet import Fernet
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import src.config as config
import random
import sys

def create_custom_line_edit(default_text = None, placeholder_text = None, regex = None, max_len = 30):
    to_return = QLineEdit()
    if (default_text):
        to_return.setText(default_text)
    if (placeholder_text):
        to_return.setPlaceholderText(placeholder_text)
    if (regex):
        to_return.setValidator(regex)
    to_return.setMaxLength(max_len)
    return to_return


def move_window_to_middle_of_screen(win_width, win_height, win):
    win.setFixedSize(win_width, win_height)
    screenGeometry = QApplication.desktop().geometry()
    x = (screenGeometry.width() - win_width) / 2
    y = (screenGeometry.height() - win_height) / 2
    win.move(x, y)

def create_random_password(length):
    password = ""
    len_special_chars = len(config.SPECIAL_CHARS)
    len_numbers_chars = len(config.NUMBERS)
    len_alphabet_chars = len(config.ALPHABET)
    for _ in range(length):
        next_char_type = random.randint(1, 8)
        if (next_char_type == 1):
            password += config.SPECIAL_CHARS[random.randint(0, len_special_chars - 1)]
        elif (next_char_type == 2):
            password += config.NUMBERS[random.randint(0, len_numbers_chars - 1)]
        else:
            password += config.ALPHABET[random.randint(0, len_alphabet_chars - 1)]
    return password

def encode_password(key, password):
    try:
        cipher_suite = Fernet(key)
        return cipher_suite.encrypt(bytes(password, encoding="utf8"))
    except Exception as e:
        print("Unresolvable error in decode_password, exiting")
        print(str(e))
        sys.exit(-1)

def decode_password(key, encrypted_password):
    try:
        cipher_suite = Fernet(key)
        return cipher_suite.decrypt(encrypted_password)
    except Exception as e:
        print("Unresolvable error in decode_password, exiting")
        print(str(e))
        sys.exit(-1)

def get_key_from_master_password(master_password):
    try:
        password_bytes = master_password.encode()
        salt = b'SALT'
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password_bytes))
        return key
    except Exception as e:
        print("Unresolvable error in get_key_from_master_password, exiting")
        print(str(e))
        sys.exit(-1)

def show_error(msg):
    error_dialog(msg)


class error_dialog(QDialog):
    def __init__(self, msg):
        super().__init__()
        message_box = QMessageBox()
        message_box.setStyleSheet('QMessageBox { background-color: ' + config.GRAY_COLOR + ';}'
                                    'QMessageBox>QWidget>QWidget { background-color: ' + config.DARK_GRAY_COLOR + '; color: ' + config.BASIC_STR_COLOR + '}'
                                    'QMessageBox>QWidget>QWidget::pane { border: 0; }'
                                    'QMessageBox>QLabel { color: ' + config.BASIC_STR_COLOR + '}')
        #message_box.setIcon(QMessageBox.Warning)
        message_box.setFont(config.BASIC_STR_FONT)
        message_box.setText(msg)
        message_box.setWindowTitle(config.ERROR_WINDOW_TITLE)
        message_box.setStandardButtons(QMessageBox.Ok)
        message_box.exec()