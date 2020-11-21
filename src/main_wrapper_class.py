from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import mysql.connector as mysql
import src.utils as utils
import src.sql_utils as sql_utils
import src.config as config
import src.add_dialog_class as add_dialog_class
import src.list_object_class as list_object_class
"""
class HoverButton(QToolButton):
    def __init__(self, parent=None):
        super(HoverButton, self).__init__(parent)
        self.setStyleSheet('''border-image: url(images/add.png) 128 128 128 128;
            border-top: 0px transparent;
            border-bottom: 64px transparent;
            border-right: 64px transparent;
            border-left: 0px transparent;
            background-color: green;''')
        #self.setGeometry(0, 0, 0, 0)

    def resizeEvent(self, event):
        pass
        #self.setMask(QRegion(self.rect(), QRegion.Ellipse))
        #QToolButton.resizeEvent(self, event)
"""


class main_wrapper(QMainWindow):
    def __init__(self, user_info):
        super().__init__()
        self.central_widget = QWidget()
        self.main_layout = QVBoxLayout()
        self.width = 400
        self.height = 500
        self.user_info = user_info
        self.password_list = sql_utils.get_user_passwords_info(user_info["user_id"], user_info["master_password"])
        self.create_ui()

    def create_ui(self):
        self.setWindowTitle("Password Manager")
        utils.move_window_to_middle_of_screen(self.width, self.height, self)
        self.lower_widget = self.get_lower_widget()
        self.middle_layout = self.get_middle_layout()


        self.main_layout.addStretch(1)
        self.main_layout.addLayout(self.middle_layout)
        self.main_layout.addWidget(self.lower_widget)
        self.central_widget.setStyleSheet('QWidget {background-color: ' + config.GRAY_COLOR + ';}')

        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

    def get_middle_layout(self):
        to_return = QHBoxLayout()
        scroll_area = QScrollArea()
        container = QWidget()
        self.gui_layout = QVBoxLayout()

        scroll_area.setStyleSheet('QScrollArea {background-color: ' + config.LIGHT_GRAY_COLOR + ';}')
        scroll_area.setFixedSize(350, 350)
        
        
        for obj in self.password_list:
            self.add_to_gui_list(obj["name"], obj["password"])
        self.gui_layout.addStretch(1)

        container.setLayout(self.gui_layout)

        scroll_area.setWidget(container)
        to_return.addStretch(1)
        to_return.addWidget(scroll_area)
        to_return.addStretch(1)
        return to_return

    def get_lower_widget(self):
        to_return = QWidget()
        to_return.setStyleSheet('QWidget {background-color: ' + config.GRAY_COLOR + ';}')
        to_return.setFixedSize(400, 75)

        add_btn = QPushButton("Add")
        add_btn.setFixedSize(self.width - 50, 50)
        add_btn.setStyleSheet('QPushButton { font-size: 18pt; font-family: Cursive; border-radius: 15px; background-color: ' + config.BLUE_COLOR + ';'
                            'color: ' + config.BASIC_STR_COLOR +  '}'
                            'QPushButton:hover {background-color: ' + config.DARK_BLUE_COLOR + '}')
        add_btn.clicked.connect(self.add_btn_clicked)

        layout = QHBoxLayout()
        
        layout.addWidget(add_btn)
        to_return.setLayout(layout)
        return to_return

    def add_to_gui_list(self, name, password):
        self.gui_layout.addWidget(list_object_class.list_object(name, password))
        # maybe remember something here in order to be able to delete it later on

    def add_btn_clicked(self):
        dialog = add_dialog_class.add_dialog(self)
        if (dialog.exec()):
            new_password_info = dialog.get_new_password_info()
            encoded_password = utils.encode_password(utils.get_key_from_master_password(self.user_info["master_password"]), new_password_info["password"])
            sql_utils.save_new_password(self.user_info["user_id"], new_password_info["name"], encoded_password)
            self.add_to_gui_list(new_password_info["name"], new_password_info["password"])