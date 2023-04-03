
from dataclasses import dataclass
from enum import Enum
from typing import NamedTuple, Union


class CurrencyType(str, Enum):
    COPPER = "Copper"
    SILVER = "Silver"
    GOLD   = "Gold"


class CurrencyAmount(NamedTuple):
    gold: int
    silver: int
    copper: int


@dataclass
class Wallet:
    _currency_base: int

    def __iadd__(self, other: Union[int, 'Wallet']) -> 'Wallet':
        if isinstance(other, int):
            self._currency_base += other
        elif isinstance(other, Wallet):
            self._currency_base += other._currency_base
        else:
            raise ValueError("Expected a Wallet instance or an integer.")
        return self

    def _color_up(self) -> CurrencyAmount:
        gold, remainder = divmod(self._currency_base, 1000)
        silver, copper = divmod(remainder, 100)
        return CurrencyAmount(gold=gold, silver=silver, copper=copper)

    @property
    def copper(self) -> int:
        return self._currency_base

    @property
    def silver(self) -> int:
        return self._color_up().silver

    @property
    def gold(self) -> int:
        return self._color_up().gold


j = Wallet(1296)

print(j.copper)
print(j.silver)

j += j
print(f"{j=}")


# if not(isinstance(j, Wallet) | isinstance(j, int)):
#     raise ValueError("Expected a Wallet instance or an integer.")

#     self._currency_base += other or other._currency_base

#     return self

# 500
# 50
# 5


_currency_base = 1296
gold, remainder = divmod(_currency_base, 1000)
silver, copper = divmod(remainder, 100)

print(f"{_currency_base=} | {gold=}, {silver=}, {copper=}")
