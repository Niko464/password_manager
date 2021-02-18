from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
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
    #win.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignCenter, win.size(), QApplication.desktop().availableGeometry()))
    frame_geom = win.frameGeometry()
    screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
    centerPoint = QApplication.desktop().screenGeometry(screen).center()
    frame_geom.moveCenter(centerPoint)
    win.move(frame_geom.topLeft())

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

def min_edit_distance(word1, word2):
    matrix = [[0 for i in range(len(word1) + 1)] for j in range(len(word2) + 1)]

    for i in range(1, len(word1) + 1):
        matrix[0][i] = i
    for j in range(1, len(word2) + 1):
        matrix[j][0] = j

    for j in range(1, len(word2) + 1):
        for i in range(1, len(word1) + 1):
            if (word2[j - 1] == word1[i - 1]):
                matrix[j][i] = matrix[j - 1][i - 1]
            else:
                matrix[j][i] = min(matrix[j - 1][i], matrix[j][i - 1], matrix[j - 1][i - 1]) + 1

    return matrix[len(word2)][len(word1)]

    

def show_error(msg, should_quit = False):
    error_dialog(msg, should_quit)


class error_dialog(QMessageBox):
    def __init__(self, msg, should_quit):
        super().__init__()
        self.setStyleSheet('QMessageBox { background-color: ' + config.GRAY_COLOR + ';}'
                                    'QMessageBox>QWidget>QWidget { background-color: ' + config.DARK_GRAY_COLOR + '; color: ' + config.BASIC_STR_COLOR + '}'
                                    'QMessageBox>QWidget>QWidget::pane { border: 0; }'
                                    'QMessageBox>QLabel { color: ' + config.BASIC_STR_COLOR + '}')
        self.setFont(config.BASIC_STR_FONT)
        self.setText(msg)
        self.setWindowTitle(config.ERROR_WINDOW_TITLE)
        self.setStandardButtons(QMessageBox.Ok)
        self.exec()
        if (should_quit == True):
            sys.exit(-1)


class confirmation_dialog(QMessageBox):
    def __init__(self, msg):
        super().__init__()
        self.setStyleSheet('QMessageBox { background-color: ' + config.GRAY_COLOR + ';}'
                                    'QMessageBox>QWidget>QWidget { background-color: ' + config.DARK_GRAY_COLOR + '; color: ' + config.BASIC_STR_COLOR + '}'
                                    'QMessageBox>QWidget>QWidget::pane { border: 0; }'
                                    'QMessageBox>QLabel { color: ' + config.BASIC_STR_COLOR + '}')
        self.setFont(config.BASIC_STR_FONT)
        self.setText(msg)
        self.setWindowTitle("Confirmation")
        self.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)

        
class info_dialog(QMessageBox):
    def __init__(self, msg):
        super().__init__()
        self.setStyleSheet('QMessageBox { background-color: ' + config.GRAY_COLOR + ';}'
                                    'QMessageBox>QWidget>QWidget { background-color: ' + config.DARK_GRAY_COLOR + '; color: ' + config.BASIC_STR_COLOR + '}'
                                    'QMessageBox>QWidget>QWidget::pane { border: 0; }'
                                    'QMessageBox>QLabel { color: ' + config.BASIC_STR_COLOR + '}')
        self.setFont(config.BASIC_STR_FONT)
        self.setText(msg)
        self.setWindowTitle("Information")
        self.setStandardButtons(QMessageBox.Ok)
        self.exec()
