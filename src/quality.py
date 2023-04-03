
from enum import Enum


class Quality(str, Enum):
    JUNK        = "Junk"            # Scrap
    TREASURE    = "Treasure"        # Sell
    POOR        = "Poor"
    COMMON      = "Common"
    UNCOMMON    = "Uncommon"
    RARE        = "Rare"
    EPIC        = "Epic"
    LEGENDARY   = "Legendary"
