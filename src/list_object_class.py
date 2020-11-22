from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import src.utils as utils
import src.config as config
from qtwidgets import PasswordEdit

class list_object(QWidget):
    def __init__(self, name, password, parent):
        super().__init__(parent=parent)
        print("Creating object: name: " + str(name) + " password: " + str(password))
        self.create_ui(name, password)

    def create_ui(self, name, password):
        self.main_layout = QHBoxLayout()
        self.left_layout = QVBoxLayout()
        self.right_layout = QHBoxLayout()
        self.under_left_layout = QHBoxLayout()

        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addLayout(self.right_layout)

        self.name_label = QLabel("Name: " + self.get_formated_name(name))
        self.name_label.setFont(config.BASIC_STR_FONT)
        self.name_label.setStyleSheet('QLabel {color: ' + config.BASIC_STR_COLOR + '}')

        self.password_label = QLabel("Pass: ")
        self.password_label.setFont(config.BASIC_STR_FONT)
        self.password_label.setStyleSheet('QLabel {color: ' + config.BASIC_STR_COLOR + '}')

        self.password_line_edit = PasswordEdit()
        self.password_line_edit.setReadOnly(True)
        self.password_line_edit.setText(str(password))
        self.password_line_edit.setStyleSheet('QLineEdit {background-color: ' + config.DARK_GRAY_COLOR + '; color: ' + config.BASIC_STR_COLOR + ';'
                                            'border: 2px solid ' + config.GRAY_COLOR + '; border-radius: 5px; font-size: 14pt}')

        self.left_layout.addWidget(self.name_label)
        self.left_layout.addLayout(self.under_left_layout)

        self.under_left_layout.addWidget(self.password_label)
        self.under_left_layout.addWidget(self.password_line_edit)

        #ADD COPY MODIFY AND DELETE TO RIGHT LAYOUT

        #self.right_layout.addWidget()
        self.setObjectName("list_object_widget")
        #print(self.parentWidget().accessibleName())
        self.setStyleSheet('QWidget { background-color: ' + 'green' + ';}')
        self.setLayout(self.main_layout)

    def get_formated_name(self, name):
        to_return = "\t"
        next_part = ""
        fm = QFontMetrics(config.BASIC_STR_FONT)
        for i in range(0, len(name)):
            next_part_width = fm.width(next_part + name[i])
            if (next_part_width > 185):
                to_return += next_part + "\n\t"
                next_part = ""
            next_part += name[i]
        if (next_part != ""):
            to_return += next_part
        self.get_formated_name = to_return
        return to_return