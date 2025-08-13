# !/usr/bin/python
# vi: fileencoding=utf-8
from pydantic import BaseModel
from pydantic import Field
from pydantic import field_validator

EVENT_TYPE_DEPOSIT: str = "deposit"
EVENT_TYPE_WITHDRAW: str = "withdraw"
EVENT_TYPE_TRANSFER: str = "transfer"

EVENT_TYPE_ALLOWED_LIST: list[str] = [
    EVENT_TYPE_DEPOSIT,
    EVENT_TYPE_WITHDRAW,
    EVENT_TYPE_TRANSFER
]

class EventModel(BaseModel):
    type: str
    destination: str = Field(default="")
    origin: str = Field(default="")
    amount: int

    @field_validator("type")
    @classmethod
    def check_type(cls, value: str) -> str:
        if not isinstance(value, str):
            return ""

        if value not in EVENT_TYPE_ALLOWED_LIST:
            return ""

        return value
