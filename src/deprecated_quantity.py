
from dataclasses import dataclass
from typing import Union


@dataclass
class QuantityMixin:
    """
    As a side effect of how Dataclasses handle the MRO and resolve optional paramaters,
    this mixin will need to be inherited first.

    Relevant SO article:
    https://stackoverflow.com/questions/51575931/class-inheritance-in-python-3-7-dataclasses
    """
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

@dataclass
class MaterialBase:
    name: MaterialType
    quality: Quality


@dataclass
class Material(QuantityMixin, MaterialBase):
    pass


# This works, but the code needs to be rewitten so that the dunders are more abstract.