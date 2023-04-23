from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from .models import Account, Transaction
from .schemas import AccountCreate, TopupPayload


async def get_account_by_id(session: AsyncSession, account_id: int) -> Account | None:
    account = await session.get(Account, account_id)
    return account


async def create_account(session: AsyncSession, data: AccountCreate) -> Account:
    account = Account(**data.dict(by_alias=False))
    session.add(account)
    await session.commit()
    return account


async def topup_account(session: AsyncSession, account: Account, data: TopupPayload):
    amount = Decimal(data.amount)
    account.balance += amount
    transaction = Transaction(
        reciever_id=account.id, amount=amount, rate=Decimal(1), date=data.date
    )
    session.add(transaction)
    await session.commit()
