from fastapi import APIRouter, Depends, HTTPException
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
    session=Depends(get_async_session),
):
    transaction = await transactions_service.topup_account(data, account, session)
    amount = await accounts_service.get_account_balance(session, account)
    return {"amount": amount, "topUpDate": transaction.date}
