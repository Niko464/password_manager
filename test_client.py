from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import src.utils_server as utils_server
import src.utils as utils
import sys

app = QApplication(sys.argv)
hashed_master_pass = "mon hashed mdp"

for i in range(1000):
    print("Test: " + str(i))
    utils_server.get_user_passwords_info(hashed_master_pass, "mon mdp")

sys.exit(app.exec_())

