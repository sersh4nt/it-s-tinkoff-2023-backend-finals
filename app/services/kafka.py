from decimal import Decimal

from aiokafka import AIOKafkaConsumer

from app.core.config import settings


class CurrencyRate:
    def __init__(self):
        self._rate = dict()

    def get_rate(self, currency1: str, currency2: str) -> Decimal:
        if currency1 == currency2:
            return Decimal(1)

    def update_rate(self, rate: dict) -> None:
        pass


async def consume(consumer: AIOKafkaConsumer):
    await consumer.start()
    try:
        async for message in consumer:
            print(message)
    finally:
        consumer.stop()


rate = CurrencyRate()
