from datetime import date, datetime
from typing import Annotated, Optional

from dateutil.relativedelta import relativedelta
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas
from app.api.http.v1.deps import get_account, get_async_session
from app.services import account as accounts_service
from app.services import transaction as transactions_service

router = APIRouter()


@router.post("/accounts", response_model=schemas.AccountCreateResponse)
async def create_account(
    data: schemas.AccountCreate, session: AsyncSession = Depends(get_async_session)
):
    age = relativedelta(date.today(), data.birthday).years
    if age < 14 or age > 120:
        raise HTTPException(400)
    account = await accounts_service.create_account(session, data)
    return {"accountNumber": account.id}


@router.get("/accounts/{account_id}", response_model=schemas.AccountBalance)
async def get_account_balance(
    account: models.Account = Depends(get_account),
    session=Depends(get_async_session),
):
    amount = await accounts_service.get_account_balance(session, account)
    return {"amount": amount, "currency": account.currency}


@router.post("/accounts/{account_id}/top-up", response_model=schemas.TopUpResponse)
async def topup(
    data: schemas.TopUp,
    account: models.Account = Depends(get_account),
    session: AsyncSession = Depends(get_async_session),
):
    transaction = await transactions_service.topup_account(data, account, session)
    amount = await accounts_service.get_account_balance(session, account)
    return {"amount": amount, "topUpDate": transaction.date}


@router.post("/transfers")
async def create_transfer(
    data: schemas.TransactionCreate, session: AsyncSession = Depends(get_async_session)
):
    sender = await accounts_service.get_account_by_id(session, data.sender_id)
    reciever = await accounts_service.get_account_by_id(session, data.reciever_id)

    if sender is None or reciever is None:
        raise HTTPException(400)

    await transactions_service.create_transaction(
        sender, reciever, data.date, data.amount, session
    )

    return JSONResponse({})


@router.get(
    "/account-turnover/{account_id}", response_model=schemas.AccountBalance
)
async def get_transactions(
    start_date: Annotated[datetime | None, Query(..., alias="startDate")] = None,
    end_date: Annotated[datetime | None, Query(..., alias="endDate")] = None,
    session: AsyncSession = Depends(get_async_session),
    account: models.Account = Depends(get_account),
):
    if start_date and end_date and start_date >= end_date:
        raise HTTPException(400)

    sum = await transactions_service.get_trans_sum(
        account, start_date, end_date, session
    )
    return {"amount": sum, "currency": account.currency}
