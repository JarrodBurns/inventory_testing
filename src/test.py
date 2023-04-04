
from dataclasses import dataclass
from typing import List

from wallet import Wallet
from material import Material
from item import Item


@dataclass
class Inventory:
    wallet      : Wallet
    materials   : List[Material]
    items       : List[Item]
