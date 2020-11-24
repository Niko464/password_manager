from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import mysql.connector as mysql
import src.utils as utils
import src.utils_server as utils_server
import src.utils_encryption as utils_encryption
import src.config as config
import src.add_edit_dialog_class as add_edit_dialog_class
import src.list_object_class as list_object_class
import src.enums as enums
import time
from operator import itemgetter


class main_wrapper(QMainWindow):
    def __init__(self, user_info):
        super().__init__()
        self.central_widget = QWidget()
        self.main_layout = QVBoxLayout()
        self.width = 400
        self.height = 500
        self.user_info = user_info
        self.password_list = utils_server.get_user_passwords_info(user_info["hashed_master_password"], user_info["master_password"])
        self.create_ui()

    def create_ui(self):
        self.setWindowTitle("Password Manager")
        utils.move_window_to_middle_of_screen(self.width, self.height, self)
        self.lower_widget = self.get_lower_widget()
        self.middle_layout = self.get_middle_layout()
        self.upper_widget = self.get_upper_widget()


        self.main_layout.addStretch(1)
        self.main_layout.addLayout(self.upper_widget)
        self.main_layout.addLayout(self.middle_layout)
        self.main_layout.addWidget(self.lower_widget)
        self.central_widget.setObjectName("main_background")
        self.central_widget.setStyleSheet('QWidget#main_background {background-color: ' + config.GRAY_COLOR + ';}')

        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

    def get_upper_widget(self):
        to_return = QHBoxLayout()
        self.search_bar = utils.create_custom_line_edit(default_text="", placeholder_text="Search here...", regex=None, max_len=config.MAX_NAME_SIZE)
        self.search_bar.setStyleSheet('QLineEdit {background-color: ' + config.DARK_GRAY_COLOR + '; color: ' + config.BASIC_STR_COLOR + ';'
                                'border-radius: 10px; font-size: 14pt}')
        self.search_bar.setFixedSize(250, 27)
        self.search_bar.returnPressed.connect(self.search_btn_clicked)

        self.search_btn = QPushButton("Search")
        self.search_btn.setStyleSheet(config.BASIC_BLUE_BTN_STYLE_SHEET + 'QPushButton { border-radius: 10px;}')
        self.search_btn.setFixedSize(85, 27)
        self.search_btn.clicked.connect(self.search_btn_clicked)

        to_return.addStretch(1)
        to_return.addWidget(self.search_bar)
        to_return.addWidget(self.search_btn)
        to_return.addStretch(1)
        return to_return
        

    def get_middle_layout(self):
        to_return = QHBoxLayout()
        scroll_area = QScrollArea()
        self.container = QWidget()
        self.gui_layout = QVBoxLayout()

        self.container.setStyleSheet('QWidget { background-color: transparent;}')
        
        scroll_area.setStyleSheet('QScrollArea {background-color: ' + 'transparent' + ';}'
                                    'QScrollBar { height:0px; }')
        scroll_area.setFrameShape(QFrame.NoFrame)
        
        scroll_area.setFixedSize(320, 350)
        
        
        for obj in self.password_list:
        #obj = self.password_list[0]
            self.add_to_gui_list(obj["name"], obj["password"])
        self.gui_layout.addStretch(1)

        self.container.setLayout(self.gui_layout)

        scroll_area.setWidget(self.container)
        scroll_area.setWidgetResizable(True)
        
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
        add_btn.setStyleSheet(config.BASIC_BLUE_BTN_STYLE_SHEET)
        add_btn.clicked.connect(self.add_btn_clicked)

        layout = QHBoxLayout()
        
        layout.addWidget(add_btn)
        to_return.setLayout(layout)
        return to_return

    def add_to_gui_list(self, name, password):
        # maybe remember something here in order to be able to delete it later on
        to_add = list_object_class.list_object(name, password, self)
        """
        to_add = QHBoxLayout()
        to_add.addWidget(QLabel("TEST"))
        to_add.addStretch(1)
        """
        self.gui_layout.insertLayout(0, to_add)
        #to_add.main_widget.updateGeometry()

    def add_btn_clicked(self):
        dialog = add_edit_dialog_class.add_edit_dialog(self, enums.ADD_DIALOG_ENUM)
        if (dialog.exec()):
            new_password_info = dialog.get_new_password_info()
            encrypted_password = utils_encryption.encode_password(utils_encryption.get_key_from_master_password(self.user_info["master_password"]), new_password_info["password"])
            server_result = utils_server.save_new_password(self.user_info["hashed_master_password"], new_password_info["name"], encrypted_password)
            if server_result['code'] == 0:
                self.add_to_gui_list(new_password_info["name"], new_password_info["password"])
                self.password_list.append(new_password_info)
            else:
                utils.show_error(server_result['message'])


    def search_btn_clicked(self):
        print("Search btn clicked")
        search_bar_txt = self.search_bar.text()
        if (search_bar_txt == ""):
            return
        levenshtein_distances = []
        for obj in self.password_list:
            splitted_name = obj["name"].upper().split(" ")
            to_add_to_levenshtein = []
            for word in splitted_name:
                to_add_to_levenshtein.append(utils.min_edit_distance(search_bar_txt.upper(), word))
            levenshtein_distances.append(to_add_to_levenshtein)
        
        if (len(levenshtein_distances) == 0):
            return
        # Sort each name's word's distances in ascending order
        #print("normal levenshtein: " + str(levenshtein_distances))
        for i in range(len(levenshtein_distances)):
            levenshtein_distances[i] = sorted(levenshtein_distances[i])
        #print("sorted levenshtein: " + str(levenshtein_distances))
        # Need to modify this to sort like this, but if the value is the same, then sort by amount of words in name if that's the same, sort by amount of characters in name
        sorted_indexes = sorted(range(len(levenshtein_distances)), key=lambda k: (levenshtein_distances[k][0], len(levenshtein_distances[k]), len(self.password_list[k]["name"])))
        #print("sorted indexes: " + str(sorted_indexes))
        #print("\n\nSorted list: ")
        counter = 0
        for index in sorted_indexes:
            #print(self.password_list[index]["name"])
            widget_index = self.get_gui_widget_index_according_to_name(self.password_list[index]["name"])
            if (widget_index != -1):
                self.gui_layout.insertLayout(counter, self.gui_layout.takeAt(widget_index))
            counter += 1

        # 12 11 1 0 is the expected result for this test

    def get_gui_widget_index_according_to_name(self, name):
        for i in range(self.gui_layout.count()):
            try:
                widget = self.gui_layout.itemAt(i)
                if widget.name == name:
                    return i
            except Exception as e:
                print("Error: " + str(e))
        return -1
