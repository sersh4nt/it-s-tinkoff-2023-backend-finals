from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Account, Transaction, rate_aggregator
from .schemas import AccountCreate, TopupPayload, TransferCreate


async def get_account_by_id(session: AsyncSession, account_id: int) -> Account | None:
    account = await session.get(Account, account_id)
    return account


async def create_account(session: AsyncSession, data: AccountCreate) -> Account:
    account = Account(**data.dict(by_alias=False))
    session.add(account)
    await session.commit()
    return account


async def topup_account(
    session: AsyncSession, account: Account, data: TopupPayload
) -> Transaction:
    amount = Decimal(data.amount)
    account.balance += amount
    transaction = Transaction(reciever_id=account.id, reciever_amount=amount, date=data.date)
    session.add(transaction)
    await session.commit()
    return transaction


async def create_transfer(
    session: AsyncSession, sender: Account, reciever: Account, data: TransferCreate
) -> Transaction:
    sender_amount = Decimal(data.sender_amount)
    if sender.balance < data.sender_amount:
        raise HTTPException(400)

    reciever_amount = rate_aggregator.calculate_reciever_amount(
        sender.currency, reciever.currency, sender_amount
    )

    sender.balance -= sender_amount
    reciever.balance += reciever_amount

    transaction = Transaction(
        sender_id=sender.id,
        reciever_id=reciever.id,
        date=data.date,
        reciever_amount=reciever_amount,
        sender_amount=sender_amount,
    )
    session.add(transaction)
    await session.commit()
    return transaction
