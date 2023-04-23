from typing import Optional

from sqlalchemy import and_, case, func, or_, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas
from app.models import Account, Transaction


async def create_account(
    session: AsyncSession, data: schemas.AccountCreate
) -> models.Account:
    account = Account(**data.dict(by_alias=False))
    session.add(account)
    await session.commit()
    return account


async def get_account_by_id(
    session: AsyncSession, account_id: int
) -> Optional[models.Account]:
    result = await session.get(models.Account, account_id)
    return result


async def get_account_balance(session: AsyncSession, account: models.Account):
    value = await session.scalar(
        select(
            func.sum(
                case(
                    (Transaction.reciever_id == account.id, Transaction.amount),
                    (
                        Transaction.sender_id == account.id,
                        -Transaction.amount * Transaction.rate,
                    ),
                    else_=-Transaction.amount,
                )
            ).filter(
                or_(
                    Transaction.reciever_id == account.id,
                    Transaction.sender_id == account.id,
                )
            )
        )
    )
    return round(value or 0, 2)
