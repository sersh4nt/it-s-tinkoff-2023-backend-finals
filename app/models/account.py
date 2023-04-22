from datetime import date, datetime
from decimal import Decimal
from sqlalchemy.orm import relationship
from sqlalchemy import BigInteger, Column, Date, DateTime, Numeric, String

from app.db.base_class import Base


class Account(Base):
    __tablename__ = "accounts"

    id: int = Column(BigInteger, primary_key=True, index=True)
    currency: str = Column(String(length=3))
    first_name: str = Column(String)
    last_name: str = Column(String)
    country: str = Column(String)
    birthday: date = Column(Date)

    cached_balance: Decimal = Column(Numeric(22, 2))
    cached_time: datetime = Column(DateTime(timezone=True))
