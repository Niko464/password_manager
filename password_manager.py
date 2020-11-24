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
    
    main = main_wrapper_class.main_wrapper({"user_id": 3, "master_password": "cacacaca"})
    main.show()
    """
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()