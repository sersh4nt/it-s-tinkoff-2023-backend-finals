from collections import defaultdict
from decimal import Decimal

from aiokafka import AIOKafkaConsumer


class CurrencyRate:
    def __init__(self):
        self._rate = dict()

    def get_rate(self, currency1: str, currency2: str) -> Decimal:
        if currency1 == currency2:
            return Decimal(1)
        return self._rate.get(currency1, {}).get(currency2, None)

    def update_rate(self, rate: dict) -> None:
        self._rate = rate


rate = CurrencyRate()


async def consume(consumer: AIOKafkaConsumer):
    await consumer.start()
    try:
        async for message in consumer:
            rate_ = defaultdict(lambda: dict())
            for k, v in message.value.items():
                rate[k[:3]][k[3:]] = Decimal(v)
                rate[k[3:]][k[:3]] = Decimal(1) / Decimal(v)
            rate.update_rate(rate_)
    finally:
        consumer.stop()
