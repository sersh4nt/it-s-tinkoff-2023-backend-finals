from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas


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
