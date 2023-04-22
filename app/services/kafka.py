from decimal import Decimal


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
