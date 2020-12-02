from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import src.sign_in_up_class as sign_in_up_class
import src.main_wrapper_class as main_wrapper_class
import src.utils as utils
import sys

def main():
    app = QApplication(sys.argv)
    
    login_screen = sign_in_up_class.sign_in_up()
    if (login_screen.exec()):
        main = main_wrapper_class.main_wrapper(login_screen.get_user_info())
        main.show()
    else:
        sys.exit(0)
    
    """
    
    main = main_wrapper_class.main_wrapper({"hashed_master_password": "$2b$12$4BjM1gQ3BeXIK/RfRceTy.opbE42Zq/I/FDconsWUX.hfDofkI8Z2", "master_password": "=iaLEu9\\"})
    main.show()
    """
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()