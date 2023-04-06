
from dataclasses import dataclass
from enum import Enum
from typing import NamedTuple, Union


class CurrencyDenomination(str, Enum):
    """
    order: decending
    scale: 100x
    """
    GOLD   = "Gold"
    SILVER = "Silver"
    COPPER = "Copper"


class Wallet(NamedTuple):

    gold: int
    silver: int
    copper: int

    def __str__(self):
        values = [
            f"{getattr(self, denomination.lower())} {denomination}"
            for denomination
            in (member.value for member in CurrencyDenomination)
            if getattr(self, denomination.lower())
        ]

        return ", ".join(values) or "Worthless..."


@dataclass
class Currency:
    value: int = 0

    def __iadd__(self, other: Union[int, 'Currency']) -> 'Currency':

        if isinstance(other, int):
            if other < 0:
                raise ValueError("Supply a positive integer.")

            newtotal_currency = self.value + other

        elif isinstance(other, Currency):
            newtotal_currency = self.value + other.value

        else:
            raise ValueError("Expected a Currency instance or an integer.")

        if newtotal_currency < 0:
            raise ValueError("Insufficient funds.")

        self.value = newtotal_currency
        return self

    def __isub__(self, other: Union[int, 'Currency']) -> 'Currency':

        if isinstance(other, int):
            if other < 0:
                raise ValueError("Supply a positive integer.")

            newtotal_currency = self.value - other

        elif isinstance(other, Currency):
            newtotal_currency = self.value - other.value

        else:
            raise ValueError("Expected a Currency instance or an integer.")

        if newtotal_currency < 0:
            raise ValueError("Insufficient funds.")

        self.value = newtotal_currency
        return self

    @property
    def wallet(self) -> Wallet:
        gold, remainder = divmod(self.value, 1000)
        silver, copper = divmod(remainder, 100)
        return Wallet(gold=gold, silver=silver, copper=copper)

    def credit_funds(self, amt: int) -> None:
        self += amt

    def debit_funds(self, amt: int) -> None:
        self -= amt


if __name__ == '__main__':

    # Testing
    w = Currency(1296)

    print(w.wallet.gold)
    print(w.wallet.silver)

    w += w      # 2592
    w -= 37     # 2555
    print(f"{w=}")

    # w -= 2556

    # w.debit_funds(2556)
