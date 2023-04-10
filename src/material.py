
from dataclasses import dataclass
from typing import Union

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


if __name__ == '__main__':
    ...
