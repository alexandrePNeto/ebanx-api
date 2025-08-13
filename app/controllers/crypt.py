#!/usr/bin/python
# vi: fileencoding=utf-8
from os import environ

from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken

TYPE_FILE = "FILE"
TYPE_STRING = "STRING"

CRYPTO_KEY = environ.get("CRYPTO_KEY")

class Crypt:
    @classmethod
    def read_encrypt_content(cls, value: str = "") -> str:
        if not isinstance(value, str):
            return ""

        content_value = ""

        try:
            content = value.encode()

            try:
                decrypt_content = Fernet(CRYPTO_KEY).decrypt(content)

                if decrypt_content is None or decrypt_content == "":
                    raise Exception("Invalid content")

                content_value = decrypt_content.decode()

            except InvalidToken as e:
                content_value = content.decode()

            except Exception as e:
                raise Exception(e)

        except Exception as e:
            content_value = ""

        return content_value

    @classmethod
    def encrypt_content(cls, content_param: str) -> str:
        content: str = ""
        try:
            if not isinstance(content_param, str):
                content_param = str(content_param)

            content = Fernet(CRYPTO_KEY.encode()).encrypt(content_param.encode()).decode()

        except Exception as e:
            content = ""

        return content


if __name__ == '__main__':
    print(Fernet.generate_key())