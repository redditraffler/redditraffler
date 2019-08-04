from flask import current_app
from cryptography.fernet import Fernet


def _to_bytes(data):
    if type(data) is bytes:
        return data
    if type(data) is str:
        return data.encode()

    raise ValueError("Data must be string or bytes")


class CryptoHelper:
    @staticmethod
    def encrypt(data):
        """ Given a byte string or string, returns the encrypted version of the
        data using the ENC_KEY environment variable. """
        f = Fernet(current_app.config["ENC_KEY"])
        data_bytes = _to_bytes(data)
        return f.encrypt(data_bytes)

    @staticmethod
    def decrypt(data):
        """ Given a byte string or string, returns the decrypted version of the
        data using the ENC_KEY environment variable. """
        f = Fernet(current_app.config["ENC_KEY"])
        data_bytes = _to_bytes(data)
        return f.decrypt(data_bytes)
