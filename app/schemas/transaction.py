from datetime import datetime
from dateutil.parser import isoparse

from pydantic import BaseModel, Field, validator


def convert_datetime_to_iso_8601_with_z_suffix(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


class TopUp(BaseModel):
    amount: float = Field(..., ge=0)
    topup_date: datetime = Field(..., alias="topUpDate")


class TopUpResponse(BaseModel):
    amount: float
    topup_date: datetime = Field(..., alias="topUpDate")

    class Config:
        json_encoders = {datetime: convert_datetime_to_iso_8601_with_z_suffix}


class TransactionCreate(BaseModel):
    reciever_id: int = Field(..., alias="receiverAccount")
    sender_id: int = Field(..., alias="senderAccount")
    amount: float = Field(..., alias="amountInSenderCurrency")
    date: datetime = Field(..., alias="transferDate")

    class Config:
        json_encoders = {datetime: convert_datetime_to_iso_8601_with_z_suffix}
