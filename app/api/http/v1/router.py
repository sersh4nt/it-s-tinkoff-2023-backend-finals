from fastapi import APIRouter

from .endpoints import account

http_router = APIRouter(prefix="/api/v1")

http_router.include_router(account.router)
