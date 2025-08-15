# !/usr/bin/python
# vi: fileencoding=utf-8
from fastapi import status
from fastapi import Response

from controllers.account_file import AccountFile

from models.event import EventModel
from models.account import AccountModel

from models.event import EVENT_TYPE_DEPOSIT
from models.event import EVENT_TYPE_TRANSFER
from models.event import EVENT_TYPE_WITHDRAW

class AccountExceptionNotFound(Exception):
    pass

class Account:
    def reset(self, response: Response) -> Response:
        if not AccountFile.reset_file():
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return "ERROR"

        response.status_code = status.HTTP_200_OK
        return "OK"

    def event(self, response: Response, event: EventModel) -> Response:
        try:
            if not event.type:
                raise Exception("Evento inválido")

            accounts: dict = AccountFile.read_file()

            if event.type == EVENT_TYPE_DEPOSIT:
                return self.__deposit(response, event, accounts)

            elif event.type == EVENT_TYPE_WITHDRAW:
                return self.__withdraw(response, event, accounts)

            elif event.type == EVENT_TYPE_TRANSFER:
                return self.__transfer(response, event, accounts)

        except Exception as e:
            response.status_code = status.HTTP_404_NOT_FOUND
            return 0

    def balance(self, response: Response, account_id: str | None = None) -> Response:
        try:
            if not account_id:
                raise AccountExceptionNotFound("ID não informado")

            accounts: dict = AccountFile.read_file()

            if not accounts:
                raise AccountExceptionNotFound("Contas não registradas")

            if not accounts.get(account_id):
                raise AccountExceptionNotFound("Conta não registrada")

        except AccountExceptionNotFound as e:
            response.status_code = status.HTTP_404_NOT_FOUND
            return 0

        except Exception as e:
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return 0

        response.status_code = status.HTTP_200_OK

        return accounts[account_id]

    def __deposit(self, response: Response, event: EventModel, accounts: dict) -> dict:
        if not accounts.get(event.destination):
            accounts.update({event.destination: event.amount})

        else:
            accounts[event.destination] = accounts[event.destination] + event.amount

        AccountFile.write_file(accounts)

        account: AccountModel = AccountModel(id=event.destination, amout=accounts[event.destination])

        response.status_code = status.HTTP_201_CREATED

        return {
            "destination": account.model_dump()
        }

    def __withdraw(self, response: Response, event: EventModel, accounts: dict) -> dict:
        if not accounts.get(event.origin):
            raise Exception("Conta não encontrada")

        accounts[event.origin] = accounts[event.origin] - event.amount

        AccountFile.write_file(accounts)

        account: AccountModel = AccountModel(id=event.origin, amout=accounts[event.origin])

        response.status_code = status.HTTP_201_CREATED

        return {
            "origin": account.model_dump()
        }

    def __transfer(self, response: Response, event: EventModel, accounts: dict) -> dict:
        if accounts.get(event.origin) is None or accounts.get(event.destination) is None:
            raise Exception("Conta não encontrada")

        accounts[event.origin] = accounts[event.origin] - event.amount
        accounts[event.destination] = accounts[event.destination] + event.amount

        AccountFile.write_file(accounts)

        origin_account: AccountModel = AccountModel(id=event.origin, amout=accounts[event.origin])
        destination_account: AccountModel = AccountModel(id=event.destination, amout=accounts[event.destination])

        response.status_code = status.HTTP_201_CREATED

        return {
            "origin": origin_account.model_dump(),
            "destination": destination_account.model_dump()
        }
