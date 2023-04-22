from datetime import date
from typing import Literal

from pydantic import BaseModel, Field


class AccountCreate(BaseModel):
    first_name: str = Field(..., alias="firstName")
    last_name: str = Field(..., alias="lastName")
    country: str
    birthday: date = Field(..., alias="birthDay")
    currency: Literal["RUB", "USD", "GBP", "EUR"]


class AccountCreateResponse(BaseModel):
    account_number: int = Field(..., alias="accountNumber")


class AccountBalance(BaseModel):
    amount: float
    currency: str
