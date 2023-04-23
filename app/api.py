from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from .deps import get_account, get_async_session
from .models import Account
from .schemas import (
    AccountBalance,
    AccountCreate,
    AccountCreateResponse,
    TopupPayload,
    TransferCreate,
)
from .services import (
    create_account,
    create_transfer,
    get_account_by_id,
    get_transactions_saldo,
    topup_account,
)

router = APIRouter(prefix="/api/v1")


@router.post("/accounts", response_model=AccountCreateResponse)
async def create_new_account(
    data: AccountCreate, session: AsyncSession = Depends(get_async_session)
):
    account = await create_account(session, data)
    return {"accountNumber": account.id}


@router.get("/accounts/{account_id}", response_model=AccountBalance)
async def get_balance(account: Account = Depends(get_account)):
    return {"amount": account.balance, "currency": account.currency}


@router.post("/accounts/{account_id}/top-up")
async def topup(
    data: TopupPayload,
    account: Account = Depends(get_account),
    session: AsyncSession = Depends(get_async_session),
):
    await topup_account(session, account, data)
    return {}


@router.post("/transfers")
async def transfer(
    data: TransferCreate, session: AsyncSession = Depends(get_async_session)
):
    sender = await get_account_by_id(session, data.sender_id)
    reciever = await get_account_by_id(session, data.reciever_id)

    if sender is None or reciever is None:
        raise HTTPException(400)

    await create_transfer(session, sender, reciever, data)
    return {}


@router.get("/account-turnover/{account_id}", response_model=AccountBalance)
async def get_turnover_balance(
    account: Account = Depends(get_account),
    session: AsyncSession = Depends(get_async_session),
    dt_from: Annotated[datetime | None, Query(alias="startDate")] = None,
    dt_to: Annotated[datetime | None, Query(alias="endDate")] = None,
):
    if dt_from and dt_to and dt_from >= dt_to:
        raise HTTPException(400)

    amount = await get_transactions_saldo(session, account, dt_from, dt_to)
    return {"amount": amount, "currency": account.currency}
