
from dataclasses import dataclass
from enum import Enum
from typing import NamedTuple, Union


class CurrencyDenominaton(str, Enum):
    COPPER = "Copper"
    SILVER = "Silver"
    GOLD   = "Gold"


class CurrencyAmount(NamedTuple):
    gold: int
    silver: int
    copper: int


@dataclass
class Wallet:
    total_currency: int

    def __iadd__(self, other: Union[int, 'Wallet']) -> 'Wallet':
        if isinstance(other, int):
            newtotal_currency = self.total_currency + other

        elif isinstance(other, Wallet):
            newtotal_currency = self.total_currency + other.total_currency

        else:
            raise ValueError("Expected a Wallet instance or an integer.")

        if newtotal_currency < 0:
            raise ValueError("Insufficient funds.")

        self.total_currency = newtotal_currency
        return self

    def __isub__(self, other: Union[int, 'Wallet']) -> 'Wallet':
        if isinstance(other, int):
            newtotal_currency = self.total_currency - other

        elif isinstance(other, Wallet):
            newtotal_currency = self.total_currency - other.total_currency

        else:
            raise ValueError("Expected a Wallet instance or an integer.")

        if newtotal_currency < 0:
            raise ValueError("Insufficient funds.")

        self.total_currency = newtotal_currency
        return self

    def _color_up(self) -> CurrencyAmount:
        gold, remainder = divmod(self.total_currency, 1000)
        silver, copper = divmod(remainder, 100)
        return CurrencyAmount(gold=gold, silver=silver, copper=copper)

    @property
    def copper(self) -> int:
        return self.total_currency

    @property
    def silver(self) -> int:
        return self._color_up().silver

    @property
    def gold(self) -> int:
        return self._color_up().gold


if __name__ == '__main__':

    # Testing
    w = Wallet(1296)

    print(w.gold)
    print(w.silver)

    w += w      # 2592
    w -= 37     # 2555
    print(f"{w=}")
