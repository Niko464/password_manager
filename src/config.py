from PyQt5.QtGui import *

# COLORS
BLACK_COLOR = "#0a0a0a"

DARK_GRAY_COLOR = "#202225"
GRAY_COLOR = "#2f3136"
LIGHT_GRAY_COLOR = "#36393f"

DARK_BLUE_COLOR = "#677bc4"
BLUE_COLOR = "#7086d5"

DARK_RED_COLOR = "#d84040"
RED_COLOR = "#f04747"

BASIC_STR_COLOR = "#fafafa"
BASIC_STR_FONT = QFont('Cursive', 14)

# GENERAL

MAX_EMAIL_SIZE = 45
MAX_USERNAME_SIZE = 20
MIN_USERNAME_SIZE = 4
MAX_MASTER_PASSWORD_SIZE = 40
MIN_MASTER_PASSWORD_SIZE = 8
MAX_NAME_SIZE = 255
ERROR_WINDOW_TITLE = "Error"

# PASSWORD GENERATION

MIN_PASSWORD_LENGTH = 12
MAX_PASSWORD_LENGTH = 20
ALPHABET = "AzByCxDwEvFuGtHsIrJqKpLoMnNmOlPkQjRiShTgUfVeWdXcYbZa"
NUMBERS = "0123456789"
SPECIAL_CHARS = ".=?/:\\_!"

# ERROR MESSAGES

MESSAGE_FILL_IN_INFO = "Please fill in all the information"
MESSAGE_INVALID_MAIL = "You need to enter a valid email."
MESSAGE_USERNAME_INVALID_LENGTH = "Your username's length has to be longer or equal to " + str(MIN_USERNAME_SIZE) + " characters."
MESSAGE_PASSWORD_INVALID_LENGTH = "Your password's length has to be longer or equal to " + str(MIN_PASSWORD_LENGTH) + " characters."
MESSAGE_MASTER_PASSWORD_INVALID_LENGTH = "Your master password's length has to be longer or equal to " + str(MIN_MASTER_PASSWORD_SIZE) + " characters."
MESSAGE_CONFIRMATION_PASS_DIFFERENT_PASS = "Your confirmation password is different from your password."
MESSAGE_MAIL_TAKEN = "That email is already registered."
MESSAGE_USERNAME_TAKEN = "That username is already taken."
MESSAGE_INVALID_CREDENTIALS = "The entered credentials are incorrect."
