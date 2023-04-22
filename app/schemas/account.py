from datetime import date, datetime
from typing import Any, Literal

from pydantic import BaseModel, Field, validator


class AccountCreate(BaseModel):
    first_name: str = Field(..., alias="firstName")
    last_name: str = Field(..., alias="lastName")
    country: str
    birthday: date = Field(..., alias="birthDay")
    currency: Literal["RUB", "USD", "GBP", "EUR"]

    # @validator("birthday", pre=True)
    # def parse_birthday(cls, value: Any) -> date:
    #     return datetime.strptime(value, "%Y-%m-%d").date()


class AccountCreateResponse(BaseModel):
    account_number: int = Field(..., alias="accountNumber")


class AccountBalance(BaseModel):
    amount: float
    currency: str
