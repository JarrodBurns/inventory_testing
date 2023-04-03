
from enum import Enum


class Quality(str, Enum):
    POOR        = "Poor"
    COMMON      = "Common"
    UNCOMMON    = "Uncommon"
    RARE        = "Rare"
    EPIC        = "Epic"
    LEGENDARY   = "Legendary"
