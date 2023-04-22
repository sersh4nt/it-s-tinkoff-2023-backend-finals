from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Numeric, String

from app.db.base_class import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id: int = Column(BigInteger, primary_key=True, index=True)
    reciever_id: int = Column(ForeignKey("accounts.id"))
    sender_id: Optional[int] = Column(ForeignKey("accounts.id"))
    amount: Decimal = Column(Numeric(22, 2))
    date: datetime = Column(DateTime(timezone=True))
    reciever_currency: str = Column(String(length=3))
    sender_currency: Optional[str] = Column(String(length=3))
    rate: Decimal = Column(Numeric(22, 2))
