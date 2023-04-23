from datetime import date, datetime
from decimal import Decimal
from typing import Dict, Tuple

from sqlalchemy import BigInteger, Column, Date, DateTime, ForeignKey, Numeric, String

from .db import Base


class Account(Base):
    __tablename__ = "accounts"

    id: int = Column(BigInteger, primary_key=True, index=True)
    currency: str = Column(String(length=3))
    first_name: str = Column(String)
    last_name: str = Column(String)
    country: str = Column(String)
    birthday: date = Column(Date)

    balance: Decimal = Column(Numeric(22, 2), default=Decimal(0))


class Transaction(Base):
    __tablename__ = "transactions"

    id: int = Column(BigInteger, primary_key=True, index=True)
    sender_id: int = Column(ForeignKey("accounts.id"))
    reciever_id: int = Column(ForeignKey("accounts.id"), nullable=False)
    date: datetime = Column(DateTime(timezone=True))
    reciever_amount: int = Column(Numeric(18, 2))
    sender_amount: int = Column(Numeric(18, 2))


class RateAggregator:
    def __init__(self):
        self.rates = dict()

    def calculate_reciever_amount(
        self, sender_currency: str, reciever_currency: str, amount: Decimal
    ) -> Decimal:
        rate = self.get_rate(sender_currency, reciever_currency)
        return round(amount * rate, 2)

    def get_rate(self, sender_currency: str, reciever_currency: str) -> Decimal:
        if sender_currency == reciever_currency:
            return Decimal(1)
        return self.rates[(sender_currency, reciever_currency)]

    def update_rates(self, new_rates: Dict[Tuple[str, str], Decimal]) -> None:
        self.rates = new_rates


rate_aggregator = RateAggregator()
