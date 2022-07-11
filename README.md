# Password Manager

## <ins> Disclaimer

I will not support this repository. Use it at your own risk.

I created this to learn about sockets, encoding, hashing.

## <ins>Introduction

This project is a password manager using Python, PyQt, MySQL

I do not recommend using this project for your own use because it isn't up to security standards.

Keep in mind that this is code I wrote in my learning period.

## <ins>Usage

Supposing you have all the necessary python packages installed and have a mysql database respecting the .sql file:

Command to execute to build the .exe version:

    - pyinstaller.exe --icon=images/password.ico  --noconsole .\password_manager.py



## Notes

For the project to run, the server side needs to use a .env file containing the following parameters

MYSQL_HOST
MYSQL_USER
MYSQL_PASS
MYSQL_DATABASE
SERVER_PORT