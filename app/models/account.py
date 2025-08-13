# !/usr/bin/python
# vi: fileencoding=utf-8
from decimal import Decimal

from pydantic import BaseModel
from pydantic import Field
from pydantic import field_validator
from pydantic import model_serializer

DECIMAL_CASE = 1000

class AccountModel(BaseModel):
    id: str = Field(pattern=r"^[0-9]*$", examples=["100", "200"])
    amout: int

    @field_validator("amout")
    @classmethod
    def change_balance(cls, value: int) -> int:
        if not isinstance(value, int):
            return 0

        return value * DECIMAL_CASE

    @property
    def balance(self) -> Decimal:
        if not self.amout:
            return Decimal(0.0)

        return Decimal(self.amout / DECIMAL_CASE)

    @model_serializer
    def account_dump(self) -> dict:
        return {
            "id": self.id,
            "balance": self.balance
        }
