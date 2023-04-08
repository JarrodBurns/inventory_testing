
from enum import Enum


class Border(str, Enum):
    LBC = '╚'
    LTC = '╔'
    LRM = '║'
    RBC = '╝'
    RTC = '╗'
    TBM = '═'


class CurrencyDenomination(str, Enum):
    """
    order: descending
    scale: 100x
    """
    GOLD   = "Gold"
    SILVER = "Silver"
    COPPER = "Copper"


class ItemName(str, Enum):
    BRASS_BUTTON        = "Button"
    FLINT               = "Flint"
    HAMMER              = "Hammer"
    MEASURING_STICK     = "Measuring Stick"
    NAIL                = "Nail"
    PLIERS              = "Pliers"
    SAW                 = "Saw"
    SMOKED_FISH         = "Smoked Fish"
    SPIDER_SILK_ROPE    = "Spider Silk Rope"
    TOOLBOX             = "Toolbox"

    # Junk--Scrap
    BOTTLE_CAP          = "Bottle Cap"
    DULL_TOOTH          = "Dull Tooth"
    INKWELL             = "Inkwell"
    PENCIL              = "Pencil"
    RUSTY_NAIL          = "Rusty Nail"
    TOXIC_MUSHROOM      = "Toxic Mushroom"
    TRASH               = "Trash"
    WOVEN_BASKET        = "Woven Basket"

    # Treasure--VendorTrash
    BRONZE_MIRROR       = "Bronze Mirror"
    COPPER_KETTLE       = "Copper Kettle"
    GOBLET_OF_BRASS     = "Goblet of Brass"
    JADE_EARRING        = "Jade Earring"
    RUNED_STONE         = "Runed Stone"
    SILVER_TOOTH_PICK   = "Silver Tooth Pick"


class MaterialType(str, Enum):
    ALUMINUM    = "Aluminum"
    BONE        = "Bone"
    BRASS       = "Brass"
    BRONZE      = "Bronze"
    COPPER      = "Copper"
    CORK        = "Cork"
    ESSENCE     = "Essence"
    GLASS       = "Glass"
    GRAPHITE    = "Graphite"
    FIBER       = "Fiber"
    FLINT       = "Flint"
    INK         = "Ink"
    IRON        = "Iron"
    JADE        = "Jade"
    ORGANIC     = "Organic"
    PAPER       = "Paper"
    PLASTIC     = "Plastic"
    POISON      = "Poison"
    RUBBER      = "Rubber"
    SILVER      = "Silver"
    SPIDER_SILK = "Spider Silk"
    STEEL       = "Steel"
    STONE       = "Stone"
    WOOD        = "Wood"


class Monster(str, Enum):
    GIANT_SPIDER    = "Giant Spider"
    GOBLIN          = "Goblin"
    GOBLIN_SHAMAN   = "Goblin Shaman"
    OGRE            = "Ogre"
    TROLL           = "Troll"


class Quality(str, Enum):
    POOR        = "Poor"
    COMMON      = "Common"
    UNCOMMON    = "Uncommon"
    RARE        = "Rare"
    EPIC        = "Epic"
    LEGENDARY   = "Legendary"


class Tag(str, Enum):
    ACCESSORY       = "Accessory"
    CONSTRUCTION    = "Construction"
    CLOTHING        = "Clothing"
    DINING          = "Dining"
    OFFICE          = "Office"
    DECORATION      = "Decoration"
    JEWELRY         = "Jewelry"
    JUNK            = "Junk"
    MECHANICAL      = "Mechanical"
    POCKET_LITTER   = "Pocket Litter"
    STORAGE         = "Storage"
    TOOL            = "Tool"
    TREASURE        = "Treasure"
    SURVIVAL        = "Survival"

    POISON          = "Poison"
    MAGIC           = "Magic"
    WEAVING         = "Weaving"
    FOOD            = "Food"
    EQUIPMENT       = "Equipment"
