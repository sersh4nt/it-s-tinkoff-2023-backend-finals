from datetime import date, datetime
from decimal import Decimal

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
    amount: int = Column(Numeric(18, 9))
    rate: Decimal = Column(Numeric(18, 9))
