from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import src.utils as utils
import src.config as config
from qtwidgets import PasswordEdit
import clipboard

class list_object(QHBoxLayout):
    def __init__(self, name, password):
        super().__init__()
        print("Creating object: name: " + str(name) + " password: " + str(password))
        self.create_ui(name, password)

    def create_ui(self, name, password):
        """
        self.left_layout = QVBoxLayout()
        self.right_layout = QHBoxLayout()
        self.under_left_layout = QHBoxLayout()

        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addLayout(self.right_layout)

        

        

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
    """
        self.main_widget = QWidget()
        self.main_widget.setFixedWidth(300)
        self.main_widget.setStyleSheet('QWidget { background-color: ' + config.LIGHT_GRAY_COLOR + '; border-radius: 10px}')

        self.vbox_layout = QVBoxLayout()
        self.password_layout = QHBoxLayout()
        self.btns_layout = QHBoxLayout()

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
        self.vbox_layout.addLayout(self.password_layout)
        self.vbox_layout.addLayout(self.btns_layout)

        self.main_widget.setLayout(self.vbox_layout)

        self.addStretch(1)
        self.addWidget(self.main_widget)
        self.addStretch(1)

    def copy_btn_clicked(self):
        clipboard.copy(self.password_line_edit.text())

    def edit_btn_clicked(self):
        print("Edit clicked")

    def delete_btn_clicked(self):
        print("Delete clicked")

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