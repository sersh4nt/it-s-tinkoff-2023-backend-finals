import asyncio
import json
from decimal import Decimal

import uvicorn
from aiokafka import AIOKafkaConsumer
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from .api import router
from .config import settings
from .db import Base, engine
from .models import rate_aggregator


async def consume():
    async with AIOKafkaConsumer(
        settings.CURRENCY_KAFKA_TOPIC_NAME,
        bootstrap_servers=f"{settings.KAFKA_HOST}:{settings.KAFKA_PORT}",
        value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    ) as consumer:
        async for message in consumer:
            new_rate = {}
            for k, v in message.value.items():
                l, r = k[:3], k[3:]
                new_rate[(l, r)] = Decimal(v)
                new_rate[(r, l)] = Decimal(1) / Decimal(v)
            rate_aggregator.update_rates(new_rate)


app = FastAPI()


@app.on_event("startup")
async def create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    asyncio.create_task(consume())


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(exc.json(), status_code=400)


app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
