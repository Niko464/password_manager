from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

def create_custom_line_edit(default_text = None, placeholder_text = None, regex = None, max_len = 30):
    to_return = QLineEdit()
    if (default_text):
        to_return.setText(default_text)
    if (placeholder_text):
        to_return.setPlaceholderText(placeholder_text)
    if (regex):
        to_return.setValidator(regex)
    to_return.setMaxLength(30)
    return to_return


def move_window_to_middle_of_screen(win_width, win_height, win):
    win.setGeometry(1, 1, win_width, win_height)
    screenGeometry = QApplication.desktop().geometry()
    x = (screenGeometry.width() - win_width) / 2
    y = (screenGeometry.height() - win_height) / 2
    win.move(x, y)

def show_error(msg):
    print("ERROR | " + msg)