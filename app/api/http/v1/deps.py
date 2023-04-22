from typing import AsyncGenerator
from fastapi import Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from app.services.account import get_account_by_id
from app.db.session import async_session


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


async def get_account(
    account_id: int, session: AsyncSession = Depends(get_async_session)
):
    account = await get_account_by_id(session, account_id)
    if account is None:
        raise HTTPException(400)
    return account
