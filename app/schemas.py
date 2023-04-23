from datetime import date, datetime
from typing import Literal

from dateutil.relativedelta import relativedelta
from pydantic import BaseModel, Field, ValidationError, validator


class AccountCreate(BaseModel):
    first_name: str = Field(..., alias="firstName")
    last_name: str = Field(..., alias="lastName")
    country: str
    birthday: date = Field(..., alias="birthDay")
    currency: Literal["USD", "EUR", "GBP", "RUB"]

    @validator("birthday")
    def validate_age(cls, value: date):
        age = relativedelta(date.today(), value).years
        if age < 14 or age > 120:
            raise ValidationError()


class AccountCreateResponse(BaseModel):
    id: int = Field(..., alias="accountNumber")


class AccountBalance(BaseModel):
    amount: float
    currency: str


class TopupPayload(BaseModel):
    amount: float
    date: datetime = Field(..., alias="topUpDate")


class TransferCreate(BaseModel):
    sender_id: int = Field(..., alias="senderAccount")
    reciever_id: int = Field(..., alias="recieverAccount")
    date: datetime = Field(..., alias="transferDate")
    sender_amount: float = Field(..., alias="amountInSenderCurrency")
