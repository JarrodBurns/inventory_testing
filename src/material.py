

from dataclasses import dataclass
from enum import Enum
from typing import Union

from quality import Quality


class MaterialType(str, Enum):
    ALUMINUM    = "Aluminum"
    BONE        = "Bone"
    BRASS       = "Brass"
    CORK        = "Cork"
    GLASS       = "Glass"
    GRAPHITE    = "Graphite"
    FLINT       = "Flint"
    INK         = "Ink"
    IRON        = "Iron"
    PAPER       = "Paper"
    PLASTIC     = "Plastic"
    RUBBER      = "Rubber"
    STEEL       = "Steel"
    WOOD        = "Wood"


@dataclass
class Material:
    """
    Raw Material which composes an Item. Can be used for crafting.
    """
    name: MaterialType
    quality: Quality
    quantity: int = 0

    def __bool__(self) -> bool:
        return self.quantity > 0

    def __eq__(self, other):
        return isinstance(other, Material) and self.name == other.name and self.quality == other.quality and self.quantity == other.quantity

    def __add__(self, other: Union[int, 'Material']) -> 'Material':
        if isinstance(other, int):
            return Material(self.name, self.quality, self.quantity + other)

        elif isinstance(other, Material):
            if self.name != other.name or self.quality != other.quality:
                raise ValueError("Cannot add Materials of different types or qualities")

            return Material(self.name, self.quality, self.quantity + other.quantity)

        raise TypeError(f"Unsupported operand type(s) for +: 'Material' and '{type(other)}'")

    def __iadd__(self, other: Union[int, 'Material']) -> 'Material':
        if isinstance(other, int):
            self.quantity += other

        elif isinstance(other, Material) and self.name == other.name and self.quality == other.quality:
            self.quantity += other.quantity

        else:
            raise ValueError("Can only add Material objects with the same name and quality")

        return self

    def __sub__(self, other: Union[int, 'Material']) -> 'Material':
        if isinstance(other, int):
            return Material(self.name, self.quality, self.quantity - other)

        elif isinstance(other, Material):
            if self.name != other.name or self.quality != other.quality:
                raise ValueError("Cannot subtract Materials of different types or qualities")

            return Material(self.name, self.quality, self.quantity - other.quantity)

        raise TypeError(f"Unsupported operand type(s) for -: 'Material' and '{type(other)}'")

    def __isub__(self, other: Union[int, 'Material']) -> 'Material':
        if isinstance(other, int):
            self.quantity -= other

        elif isinstance(other, Material) and self.name == other.name and self.quality == other.quality:
            self.quantity -= other.quantity

        else:
            raise ValueError("Can only subtract Material objects with the same name and quality")

        return self

    def __mul__(self, other: Union[int, 'Material']) -> 'Material':
        if isinstance(other, int):
            return Material(self.name, self.quality, self.quantity * other)

        raise TypeError(f"Unsupported operand type(s) for *: 'Material' and '{type(other)}'")

    def __truediv__(self, other: Union[int, 'Material']) -> 'Material':
        if isinstance(other, int):
            return Material(self.name, self.quality, self.quantity // other)

        elif isinstance(other, Material):
            if self.name != other.name or self.quality != other.quality:
                raise ValueError("Cannot divide Materials of different types or qualities")

            return self.quantity // other.quantity

        raise TypeError(f"Unsupported operand type(s) for /: 'Material' and '{type(other)}'")


MATERIALS = {
    MaterialType.ALUMINUM   : Material(MaterialType.ALUMINUM, Quality.COMMON),
    MaterialType.BONE       : Material(MaterialType.BONE, Quality.COMMON),
    MaterialType.BRASS      : Material(MaterialType.BRASS, Quality.COMMON),
    MaterialType.CORK       : Material(MaterialType.CORK, Quality.COMMON),
    MaterialType.GLASS      : Material(MaterialType.GLASS, Quality.COMMON),
    MaterialType.GRAPHITE   : Material(MaterialType.GRAPHITE, Quality.COMMON),
    MaterialType.FLINT      : Material(MaterialType.FLINT, Quality.COMMON),
    MaterialType.INK        : Material(MaterialType.INK, Quality.COMMON),
    MaterialType.IRON       : Material(MaterialType.IRON, Quality.COMMON),
    MaterialType.PAPER      : Material(MaterialType.PAPER, Quality.COMMON),
    MaterialType.PLASTIC    : Material(MaterialType.PLASTIC, Quality.COMMON),
    MaterialType.RUBBER     : Material(MaterialType.RUBBER, Quality.COMMON),
    MaterialType.STEEL      : Material(MaterialType.STEEL, Quality.UNCOMMON),
    MaterialType.WOOD       : Material(MaterialType.WOOD, Quality.COMMON),
}
