import base64
from Crypto.Cipher import AES
from .metadata import Singleton


class MyCrypto(Singleton):
    def __init__(
        self, key: str
    ):  # TODO: Change from key passing to parse from settings
        self.key = key.encode("utf8")

    def encrypt(self, raw: str):  # для шифрования паролей перед внесением в бд
        cipher = AES.new(self.key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(raw.encode("utf8"))
        return base64.b64encode(cipher.nonce + tag + ciphertext).decode("utf8")

    def decrypt(
        self, password: str
    ):  # для рассшифровки паролей для использования в парсинге
        password = base64.b64decode(password)
        nonce = password[:16]
        tag = password[16:32]
        ciphertext = password[32:]
        cipher = AES.new(self.key, AES.MODE_EAX, nonce=nonce)
        return cipher.decrypt_and_verify(ciphertext, tag).decode("utf8")
