
from dataclasses import dataclass, field
from typing import List, Optional
import random
import textwrap

from currency import Currency
from enums import Border, ItemName, Quality, Tag
from material import Material


@dataclass(frozen=True)
class Item:
    name        : ItemName
    weight      : int   # grams
    value       : int   # Indicative of average cost to purchase in the US. Represented in pennies.
    description : str
    quality     : Quality
    craftable   : bool
    composition : List[Material]
    tags        : List[Tag] = field(default_factory=list)
    flavor_text : Optional[str] = None

    @property
    def scrap(self) -> List[Material]:

        max_reward = self.weight // 2 if self.weight > 1 else 2
        return [
            material + quantity
            for material
            in self.composition
            if (quantity := random.randint(0, max_reward))
        ]

    def ascii_art(self, min_line_length=80, max_line_length=80) -> str:
        name    = f"{self.name.value} ({self.quality.name})"
        desc    = self.description
        tags    = ", ".join(self.tags)
        value   = str(Currency(self.value).wallet)
        weight  = f"{self.weight} grams"
        scrap   = ", ".join(mat.name for mat in self.composition)
        lines   = [
            name,
            "=" * len(name),
            desc,
            "",
            "Tags:",
            tags,
            "",
            "Value:",
            value,
            "Weight:",
            weight,
            "Scrap:",
            scrap
        ]

        # Wrap lines that exceed max_line_length
        wrapped_lines = []
        for line in lines:
            if len(line) > max_line_length:
                wrapped_lines.extend(textwrap.wrap(line, width=max_line_length))
            else:
                wrapped_lines.append(line)

        # Add padding to lines shorter than min_line_length
        padded_lines = []
        for line in wrapped_lines:
            if len(line) < min_line_length:
                line += " " * (min_line_length - len(line))
            padded_lines.append(line)

        # Pad lines to be equal length
        max_length = max(len(line) for line in padded_lines)
        padded_lines = [f"{Border.LRM} {line.ljust(max_length)} {Border.LRM}" for line in padded_lines]

        # Format lines as ASCII card
        card = [
            f"{Border.LTC}{Border.TBM * (max_length + 2)}{Border.RTC}"
        ] + padded_lines + [
            f"{Border.LBC}{Border.TBM * (max_length + 2)}{Border.RBC}"
        ]

        return "\n".join(card)


if __name__ == '__main__':
    ...
