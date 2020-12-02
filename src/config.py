from PyQt5.QtGui import *

BUFFER = ""

# COLORS
BLACK_COLOR = "#0a0a0a"

DARK_GRAY_COLOR = "#202225"
GRAY_COLOR = "#2f3136"
LIGHT_GRAY_COLOR = "#36393f"

DARK_BLUE_PLUS_COLOR = "#5b6eae"
DARK_BLUE_COLOR = "#677bc4"
BLUE_COLOR = "#7086d5"

DARK_RED_PLUS_COLOR = "#c03939"
DARK_RED_COLOR = "#d84040"
RED_COLOR = "#f04747"

BASIC_STR_COLOR = "#fafafa"
BASIC_STR_FONT = QFont('Cursive', 14)

# GENERAL

MAX_COMMENT_SIZE = 1024
MAX_PIN_CODE_SIZE = 10
MAX_EMAIL_SIZE = 45
MAX_USERNAME_SIZE = 20
MIN_USERNAME_SIZE = 4
MAX_MASTER_PASSWORD_SIZE = 40
MIN_MASTER_PASSWORD_SIZE = 8
MAX_NAME_SIZE = 255
ERROR_WINDOW_TITLE = "Error"
HEADER_SIZE = 10
DEVELOPPER = "Nikolaj"

# PASSWORD GENERATION

MIN_PASSWORD_GENERATION_LENGTH = 12
MAX_PASSWORD_GENERATION_LENGTH = 20
MAX_PASSWORD_LENGTH = 200
ALPHABET = "AzByCxDwEvFuGtHsIrJqKpLoMnNmOlPkQjRiShTgUfVeWdXcYbZa"
NUMBERS = "0123456789"
SPECIAL_CHARS = ".=?/:\\_!"

# ERROR MESSAGES

MESSAGE_FILL_IN_INFO = "Please fill in all the 'Required' information"
MESSAGE_INVALID_MAIL = "You need to enter a valid email."
MESSAGE_USERNAME_INVALID_LENGTH = "Your username's length has to be longer or equal to " + str(MIN_USERNAME_SIZE) + " characters."
MESSAGE_PASSWORD_INVALID_LENGTH = "Your password's length has to be shorter than " + str(MAX_PASSWORD_LENGTH) + " characters."
MESSAGE_COMMENT_INVALID_LENGTH = "Your comment's length has to be shorter than " + str(MAX_COMMENT_SIZE) + " characters."
MESSAGE_MASTER_PASSWORD_INVALID_LENGTH = "Your master password's length has to be longer or equal to " + str(MIN_MASTER_PASSWORD_SIZE) + " characters."
MESSAGE_CONFIRMATION_PASS_DIFFERENT_PASS = "Your confirmation password is different from your password."
MESSAGE_MAIL_TAKEN = "That email is already registered."
MESSAGE_USERNAME_TAKEN = "That username is already taken."
MESSAGE_INVALID_CREDENTIALS = "The entered credentials are incorrect."
MESSAGE_NAME_ALREADY_EXISTS = "You already have a password with that name registered"
MESSAGE_INVALID_EDIT = "Can't confirm the edit if you didn't change anything, please cancel."
MESSAGE_DATABASE_DOWN = "We encountered an error, the database is probably down, sorry..."
MESSAGE_SOCKET_CONNECTED = "Connected"
MESSAGE_FAILED_TO_CONNECT_SERVER = "Failed to connect to the server.\nPlease ask " + DEVELOPPER + " what's going on."
MESSAGE_ERROR_SERVER_SIDE = "An error occurred server side."
MESSAGE_UNUSUAL_ERROR = "An Unusual error occurred, please report this message to " + DEVELOPPER + "."
MESSAGE_USERNAME_NO_AT_SYMBOL = "Your username can't contain an '@' symbol."



# STYLE SHEETS

BASIC_BLUE_BTN_STYLE_SHEET = """
                            QPushButton { font-size: 18pt; font-family: Cursive; border-radius: 15px; background-color: """ + BLUE_COLOR + """
                            ;color: """ + BASIC_STR_COLOR + """
                            } QPushButton:hover {background-color: """ + DARK_BLUE_COLOR + """
                            } QPushButton:pressed {background-color: """ + DARK_BLUE_PLUS_COLOR + """}
                            """

BASIC_RED_BTN_STYLE_SHEET = """
                            QPushButton { font-size: 18pt; font-family: Cursive; border-radius: 15px; background-color: """ + RED_COLOR + """
                            ;color: """ + BASIC_STR_COLOR + """
                            } QPushButton:hover {background-color: """ + DARK_RED_COLOR + """
                            } QPushButton:pressed {background-color: """ + DARK_RED_PLUS_COLOR + """}
                            """

BASIC_BLUE_LINE_EDIT_STYLE_SHEET = """
                                    QLineEdit {background-color: """ + DARK_GRAY_COLOR + """; color: """ + BASIC_STR_COLOR + """
                                    ;border: 2px solid """ + GRAY_COLOR + """; border-radius: 5px; font-size: 14pt}
                                    QLineEdit:hover {border: 1px solid """ + BLACK_COLOR + """
                                    ;}QLineEdit:focus {border: 2px solid """ + BLUE_COLOR + """;}
                                    """