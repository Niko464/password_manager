from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import mysql.connector as mysql
import src.utils as utils
import src.config as config
import src.add_dialog_class as add_dialog_class

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



class main_wrapper(QMainWindow):
    def __init__(self, user_info):
        super().__init__()
        self.central_widget = QWidget()
        self.main_layout = QVBoxLayout()
        self.width = 400
        self.height = 500
        print(user_info["user_id"], user_info["master_password"])
        self.create_ui()

    def create_ui(self):
        self.setWindowTitle("Password Manager")
        utils.move_window_to_middle_of_screen(self.width, self.height, self)
        self.lower_widget = self.get_lower_widget()
        self.middle_widget = self.get_middle_widget()


        self.main_layout.addStretch(1)
        self.main_layout.addWidget(self.middle_widget)
        self.main_layout.addWidget(self.lower_widget)
        self.central_widget.setStyleSheet('QWidget {background-color: ' + config.GRAY_COLOR + ';}')

        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

    def get_middle_widget(self):
        to_return = QWidget()
        to_return.setStyleSheet('QWidget {background-color: ' + 'red' + ';}')
        to_return.setFixedSize(400, 350)

        layout = QHBoxLayout()

        to_return.setLayout(layout)
        return to_return

    def get_lower_widget(self):
        to_return = QWidget()
        to_return.setStyleSheet('QWidget {background-color: ' + 'red' + ';}')
        to_return.setFixedSize(400, 75)

        add_btn = QPushButton("+")
        add_btn.setFixedSize(50, 50)
        add_btn.clicked.connect(self.add_btn_clicked)

        edit_btn = QPushButton(',')
        edit_btn.setFixedSize(50, 50)
        edit_btn.clicked.connect(self.edit_btn_clicked)

        remove_btn = QPushButton('x')
        remove_btn.setFixedSize(50, 50)
        remove_btn.clicked.connect(self.remove_btn_clicked)

        layout = QHBoxLayout()
        
        layout.addWidget(add_btn)
        layout.addWidget(edit_btn)
        layout.addWidget(remove_btn)
        to_return.setLayout(layout)
        return to_return

    def add_btn_clicked(self):
        print("ADDING PASSWORD")
        dialog = add_dialog_class.add_dialog(self)
        if (dialog.exec()):
            new_password_info = dialog.get_new_password_info()
            print(new_password_info["name"], new_password_info["password"])

    def edit_btn_clicked(self):
        print("EDITING")

    def remove_btn_clicked(self):
        print("REMOVING")