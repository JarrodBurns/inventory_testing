
from enum import Enum


class Quality(str, Enum):
    JUNK        = "Junk"
    TREASURE    = "Treasure"
    POOR        = "Poor"
    COMMON      = "Common"
    UNCOMMON    = "Uncommon"
    RARE        = "Rare"
    EPIC        = "Epic"
    LEGENDARY   = "Legendary"
