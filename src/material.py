
from dataclasses import dataclass
from typing import List, Union

from enums import MaterialType, Quality


@dataclass
class Material:
    """
    Raw Material which composes an Item. Can be used for crafting.
    """
    name: MaterialType
    quality: Quality
    quantity: int = 0

    # def __str__(self) -> str:
    #     return f"|  ({self.quantity}) {self.name} [{self.quality}]"

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

            if self.quantity - other < 0:
                raise ValueError("Insufficient material.")

            return Material(self.name, self.quality, self.quantity - other)

        elif isinstance(other, Material):

            if self.name != other.name or self.quality != other.quality:
                raise ValueError("Cannot subtract Materials of different types or qualities")

            if self.quantity - other.quantity < 0:
                raise ValueError("Insufficient material.")

            return Material(self.name, self.quality, self.quantity - other.quantity)

        raise TypeError(f"Unsupported operand type(s) for -: 'Material' and '{type(other)}'")

    def __isub__(self, other: Union[int, 'Material']) -> 'Material':
        if isinstance(other, int):

            if self.quantity - other < 0:
                raise ValueError("Insufficient material.")

            self.quantity -= other

        elif isinstance(other, Material) and self.name == other.name and self.quality == other.quality:

            if self.quantity - other.quantity < 0:
                raise ValueError("Insufficient material.")

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
    MaterialType.BRONZE     : Material(MaterialType.BRONZE, Quality.COMMON),
    MaterialType.COPPER     : Material(MaterialType.COPPER, Quality.COMMON),
    MaterialType.CORK       : Material(MaterialType.CORK, Quality.COMMON),
    MaterialType.ESSENCE    : Material(MaterialType.ESSENCE, Quality.UNCOMMON),
    MaterialType.GLASS      : Material(MaterialType.GLASS, Quality.COMMON),
    MaterialType.GRAPHITE   : Material(MaterialType.GRAPHITE, Quality.COMMON),
    MaterialType.FIBER      : Material(MaterialType.FIBER, Quality.COMMON),
    MaterialType.FLINT      : Material(MaterialType.FLINT, Quality.COMMON),
    MaterialType.INK        : Material(MaterialType.INK, Quality.COMMON),
    MaterialType.IRON       : Material(MaterialType.IRON, Quality.COMMON),
    MaterialType.JADE       : Material(MaterialType.JADE, Quality.COMMON),
    MaterialType.ORGANIC    : Material(MaterialType.ORGANIC, Quality.COMMON),
    MaterialType.PAPER      : Material(MaterialType.PAPER, Quality.COMMON),
    MaterialType.PLASTIC    : Material(MaterialType.PLASTIC, Quality.COMMON),
    MaterialType.POISON     : Material(MaterialType.POISON, Quality.UNCOMMON),
    MaterialType.RUBBER     : Material(MaterialType.RUBBER, Quality.COMMON),
    MaterialType.SILVER     : Material(MaterialType.SILVER, Quality.COMMON),
    MaterialType.SPIDER_SILK: Material(MaterialType.SPIDER_SILK, Quality.UNCOMMON),
    MaterialType.STONE      : Material(MaterialType.STONE, Quality.COMMON),
    MaterialType.STEEL      : Material(MaterialType.STEEL, Quality.UNCOMMON),
    MaterialType.WOOD       : Material(MaterialType.WOOD, Quality.COMMON),

}


def select_materials_by_quality(quality: Quality) -> List[Material]:
    return [material for material in MATERIALS.values() if material.quality == quality]


if __name__ == '__main__':

    import _CopyToClipBoard

    name = "test"
    quality = "common"
    # name = []
    # quality = []

    # _CopyToClipBoard.materials(name, quality)
    # _CopyToClipBoard.material_type(name)

    # print(MATERIALS[MaterialType.BONE].name)
    # mats = [MATERIALS[m] for m in [MaterialType.STEEL, MaterialType.WOOD]]
    # print(type(mats))
