
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

    def __str__(self):

        a = f"{self.gold} Gold" if self.gold else ''
        b = f"{self.silver} Silver" if self.silver else ''
        c = f"{self.copper} Copper" if self.copper else ''

        return ", ".join(s for s in [a, b, c] if s) or "Worthless..."


@dataclass
class Wallet:
    balance: int

    def __iadd__(self, other: Union[int, 'Wallet']) -> 'Wallet':

        if isinstance(other, int):
            if other < 0:
                raise ValueError("Supply a positive integer.")

            newtotal_currency = self.balance + other

        elif isinstance(other, Wallet):
            newtotal_currency = self.balance + other.balance

        else:
            raise ValueError("Expected a Wallet instance or an integer.")

        if newtotal_currency < 0:
            raise ValueError("Insufficient funds.")

        self.balance = newtotal_currency
        return self

    def __isub__(self, other: Union[int, 'Wallet']) -> 'Wallet':

        if isinstance(other, int):
            if other < 0:
                raise ValueError("Supply a positive integer.")

            newtotal_currency = self.balance - other

        elif isinstance(other, Wallet):
            newtotal_currency = self.balance - other.balance

        else:
            raise ValueError("Expected a Wallet instance or an integer.")

        if newtotal_currency < 0:
            raise ValueError("Insufficient funds.")

        self.balance = newtotal_currency
        return self

    def _color_up(self) -> CurrencyAmount:
        gold, remainder = divmod(self.balance, 1000)
        silver, copper = divmod(remainder, 100)
        return CurrencyAmount(gold=gold, silver=silver, copper=copper)

    @property
    def copper(self) -> int:
        return self._color_up().copper

    @property
    def silver(self) -> int:
        return self._color_up().silver

    @property
    def gold(self) -> int:
        return self._color_up().gold

    def add(self, amt: int) -> None:
        self += amt

    def sub(self, amt: int) -> None:
        self -= amt


if __name__ == '__main__':

    # Testing
    w = Wallet(1296)

    print(w.gold)
    print(w.silver)

    w += w      # 2592
    w -= 37     # 2555
    print(f"{w=}")

    # w -= 2556

    # w.sub(2556)
