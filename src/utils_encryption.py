from cryptography.fernet import Fernet
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import sys

def encode_password(key, password):
    try:
        cipher_suite = Fernet(key)
        return cipher_suite.encrypt(bytes(password, encoding="utf8"))
    except Exception as e:
        print("Unresolvable error in encode_password, exiting")
        print(str(e))
        sys.exit(-1)

def decode_password(key, encrypted_password):
    try:
        cipher_suite = Fernet(key)
        return cipher_suite.decrypt(encrypted_password)
    except Exception as e:
        print("Unresolvable error in decode_password, exiting")
        print(str(e))
        sys.exit(-1)

def get_key_from_master_password(master_password):
    try:
        password_bytes = master_password.encode()
        salt = b'SALT'
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password_bytes))
        return key
    except Exception as e:
        print("Unresolvable error in get_key_from_master_password, exiting")
        print(str(e))
        sys.exit(-1)