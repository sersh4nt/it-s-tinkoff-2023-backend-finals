import asyncio

import uvicorn
from aiokafka import AIOKafkaConsumer
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.http.v1.router import http_router
from app.core.config import settings
from app.db.base_class import Base
from app.db.session import engine
from app.services.kafka import consume

loop = asyncio.get_event_loop()

consumer = AIOKafkaConsumer(
    settings.CURRENCY_KAFKA_TOPIC_NAME,
    bootstrap_servers=f"{settings.KAFKA_HOST}:{settings.KAFKA_PORT}",
    loop=loop,
)

app = FastAPI()


@app.on_event("startup")
async def create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    loop.create_task(consume(consumer))


@app.on_event("shutdown")
async def shutdown():
    await consumer.stop()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(exc.json(), status_code=400)


app.include_router(http_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
