from datetime import datetime
from dateutil.parser import isoparse

from pydantic import BaseModel, Field, validator


class TopUp(BaseModel):
    amount: float = Field(..., ge=0)
    topup_date: datetime = Field(..., alias="topUpDate")

    # @validator("topup_date")
    # def parse_date(cls, value):
    #     return isoparse(value)


class TopUpResponse(BaseModel):
    amount: float
    topup_date: datetime = Field(..., alias="topUpDate")
