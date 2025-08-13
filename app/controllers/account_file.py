# !/usr/bin/python
# vi: fileencoding=utf-8
from os import path
from os import getcwd

from json import loads
from json import dumps

from controllers.crypt import Crypt

FILE_NAME: str = "accounts.txt"
FILE_PATH: str = path.join(getcwd(), FILE_NAME)

class AccountFile:
    @classmethod
    def reset_file(cls) -> bool:
        try:
            with open(FILE_PATH, "wb") as file:
                file.write(b"")
                file.close()

        except Exception as e:
            return False

        return True

    @classmethod
    def read_file(cls) -> dict:
        if not path.isfile(FILE_PATH):
            cls.reset_file()
        result: dict = {}
        try:
            with open(FILE_PATH, "rb") as file:
                result = loads(Crypt.read_encrypt_content(file.read().decode()))
                file.close()

        except Exception as e:
            return {}

        return result

    @classmethod
    def write_file(cls, json: dict) -> dict:
        if not path.isfile(FILE_PATH):
            cls.reset_file()

        result: dict = {}

        if not isinstance(json, dict):
            return {}

        try:
            with open(FILE_PATH, "wb") as file:
                result = file.write(Crypt.encrypt_content(dumps(json)).encode())
                file.close()

        except Exception as e:
            return {}

        return result
