from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .deps import get_account, get_async_session
from .models import Account
from .schemas import AccountBalance, AccountCreate, AccountCreateResponse, TopupPayload
from .services import create_account, topup_account

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
