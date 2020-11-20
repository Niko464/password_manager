from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import src.sign_in_up_class as sign_in_up_class
import sys

def main():
    app = QApplication(sys.argv)
    main = sign_in_up_class.sign_in_up()
    main.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()