# !/usr/bin/python
# vi: fileencoding=utf-8
from fastapi import status
from fastapi import Response

from controllers.account_file import AccountFile

from models.event import EventModel

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
                if not accounts.get(event.destination):
                    accounts.update({event.destination: event.amount})

                else:
                    accounts[event.destination] = accounts[event.destination] + event.amount

                AccountFile.write_file(accounts)

                response.status_code = status.HTTP_201_CREATED

                return {
                    "destination": {
                        "id": event.destination,
                        "balance": accounts[event.destination]
                    }
                }

            elif event.type == EVENT_TYPE_WITHDRAW:
                if not accounts.get(event.origin):
                    raise Exception("Conta não encontrada")

                else:
                    accounts[event.origin] = accounts[event.origin] - event.amount

                AccountFile.write_file(accounts)

                response.status_code = status.HTTP_201_CREATED

                return {
                    "origin": {
                        "id": event.origin,
                        "balance": accounts[event.origin]
                    }
                }

            elif event.type == EVENT_TYPE_TRANSFER:
                if accounts.get(event.origin) is None or accounts.get(event.destination) is None:
                    raise Exception("Conta não encontrada")

                else:
                    accounts[event.origin] = accounts[event.origin] - event.amount
                    accounts[event.destination] = accounts[event.destination] + event.amount

                AccountFile.write_file(accounts)

                response.status_code = status.HTTP_201_CREATED

                return {
                    "origin": {
                        "id": event.origin,
                        "balance": accounts[event.origin]
                    },
                    "destination": {
                        "id": event.destination,
                        "balance": accounts[event.destination]
                    }
                }

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
