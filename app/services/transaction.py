from datetime import datetime
from decimal import Decimal
from typing import Optional

from fastapi import HTTPException
from sqlalchemy import case, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas
from app.models.transaction import Transaction

from .account import get_account_balance
from .kafka import rate as rate_service


async def topup_account(
    data: schemas.TopUp, account: models.Account, session: AsyncSession
) -> models.Transaction:
    amount = Decimal(data.amount)
    transaction = models.Transaction(
        reciever_id=account.id,
        reciever_currency=account.currency,
        amount=amount,
        date=data.topup_date,
        rate=Decimal(1),
    )
    session.add(transaction)
    await session.commit()
    return transaction


async def create_transaction(
    sender: models.Account,
    reciever: models.Account,
    date: datetime,
    amount: float,
    session: AsyncSession,
) -> models.Transaction:
    rate = Decimal(1)
    amount = Decimal(amount)

    if sender.currency != reciever.currency:
        rate = rate_service.get_rate(sender.currency, reciever.currency)
        amount /= rate

    sender_money = await get_account_balance(session, sender)
    if sender_money < amount:
        raise HTTPException(400)

    transaction = models.Transaction(
        reciever_id=reciever.id,
        reciever_currency=reciever.currency,
        sender_id=sender.id,
        sender_currency=sender.currency,
        amount=amount,
        rate=rate,
        date=date,
    )
    session.add(transaction)
    await session.commit()
    return transaction


async def get_trans_sum(
    account: models.Account,
    start_date: Optional[datetime],
    end_date: Optional[datetime],
    session: AsyncSession,
):
    query = func.sum(
        case(
            (Transaction.reciever_id == account.id, Transaction.amount),
            else_=-Transaction.amount,
        )
    ).filter(
        or_(
            Transaction.reciever_id == account.id,
            Transaction.sender_id == account.id,
        )
    )

    if start_date is not None:
        query.filter(Transaction.date >= start_date)

    if end_date is not None:
        query.filter(Transaction.date <= end_date)

    value = await session.scalar(select(query))
    return value or 0
