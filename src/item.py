
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional
import random
import textwrap

from material import Material, MaterialType, MATERIALS
from quality import Quality
from tag import Tag


class ItemName(str, Enum):
    BRASS_BUTTON        = "Button"
    DULL_TOOTH          = "Dull Tooth"
    FLINT               = "Flint"
    PENCIL              = "Pencil"
    INKWELL             = "Inkwell"
    PLIERS              = "Pliers"
    HAMMER              = "Hammer"
    SAW                 = "Saw"
    MEASURING_STICK     = "Measuring Stick"
    TOOLBOX             = "Toolbox"
    TRASH               = "Trash"
    NAIL                = "Nail"
    RUSTY_NAIL          = "Rusty Nail"
    BOTTLE_CAP          = "Bottle Cap"

    GOBLET_OF_BRASS     = "Goblet of Brass"
    SILVER_TOOTH_PICK   = "Silver Tooth Pick"
    JADE_EARRING        = "Jade Earring"
    COPPER_KETTLE       = "Copper Kettle"
    BRONZE_MIRROR       = "Bronze Mirror"


@dataclass
class Item:
    name        : ItemName
    weight      : int   # grams
    value       : int   # Indicitive of average cost to purchase in the US. Represented in pennies.
    description : str
    quality     : Quality
    craftable   : bool
    composition : List[Material]
    tags        : List[str] = field(default_factory=list)
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
        name    = f"{self.name} ({self.quality.name})"
        desc    = self.description
        tags    = ", ".join(self.tags)
        value   = f"{self.value/100:.2f} Silver"
        weight  = f"{self.weight} grams"
        scrap   = ", ".join(mat.name.value for mat in self.scrap)
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
        padded_lines = [f"║ {line.ljust(max_length)} ║" for line in padded_lines]

        # Format lines as ASCII card
        card = [
            f"╔{'═' * (max_length + 2)}╗"
        ] + padded_lines + [
            f"╚{'═' * (max_length + 2)}╝"
        ]

        return "\n".join(card)


ITEMS = {
    ItemName.BOTTLE_CAP         : Item(
        name=ItemName.BOTTLE_CAP,
        weight=2,
        value=5,
        description="A small metal cap that fits over the top of a bottle. This one is heavily worn and has a faded logo on it.",
        tags=[Tag.POCKET_LITTER, Tag.JUNK],
        quality=Quality.POOR,
        composition=[MATERIALS[MaterialType.ALUMINUM]],
        craftable=False,
        flavor_text="This bottle cap has seen better days, with scratches and dents all over its surface. The logo on the top is so faded that it's hard to make out what it used to be."
    ),
    ItemName.BRASS_BUTTON       : Item(
        name=ItemName.BRASS_BUTTON,
        weight=2,
        value=25,
        description="A small brass button that can be used to fasten clothing or other materials together.",
        tags=[Tag.CLOTHING, Tag.ACCESSORY],
        quality=Quality.COMMON,
        composition=[MATERIALS[MaterialType.BRASS]],
        craftable=True,
        flavor_text="This button is a simple and practical accessory that can be used to add a finishing touch to any piece of clothing."
    ),
    ItemName.DULL_TOOTH         : Item(
        name=ItemName.DULL_TOOTH,
        weight=5,
        value=10,
        description="A dull and worn tooth that was likely pulled from an animal's mouth. It's not very useful for anything.",
        tags=[Tag.POCKET_LITTER, Tag.JUNK],
        quality=Quality.POOR,
        composition=[MATERIALS[MaterialType.BONE]],
        craftable=False,
        flavor_text="This tooth is so worn and useless that you might as well just throw it away."
    ),
    ItemName.FLINT              : Item(
        name=ItemName.FLINT,
        weight=10,
        value=50,
        description="A sharp piece of flint that can be used to start fires or cut through materials.",
        tags=[Tag.TOOL, Tag.SURVIVAL],
        quality=Quality.COMMON,
        composition=[MATERIALS[MaterialType.FLINT]],
        craftable=False,
        flavor_text="This piece of flint is well-suited for starting fires or making tools in a pinch."
    ),
    ItemName.HAMMER             : Item(
        name=ItemName.HAMMER,
        weight=600,
        value=8_000,
        description="A versatile tool used for pounding nails, shaping metal, and other construction tasks.",
        tags=[Tag.TOOL, Tag.CONSTRUCTION],
        quality=Quality.COMMON,
        composition=[MATERIALS[m] for m in [MaterialType.STEEL, MaterialType.WOOD]],
        craftable=True,
        flavor_text="This hammer has seen a lot of use, but it still has plenty of life left in it. The wooden handle is worn and smooth from years of hard work, but it still provides a comfortable grip. The steel head is dinged and scratched from pounding nails and shaping metal, but it still delivers a solid blow. Whether you're building a house or just hanging a picture frame, this hammer is up to the task."
    ),
    ItemName.INKWELL            : Item(
        name=ItemName.INKWELL,
        weight=50,
        value=500,
        description="A small jar filled with ink, intended for writing or drawing purposes.",
        tags=[Tag.OFFICE, Tag.DECORATION, Tag.JUNK],
        quality=Quality.COMMON,
        composition=[MATERIALS[m] for m in (MaterialType.GLASS, MaterialType.INK, MaterialType.CORK)],
        craftable=True,
        flavor_text="TODO"
    ),
    ItemName.MEASURING_STICK    : Item(
        name=ItemName.MEASURING_STICK,
        weight=250,
        value=500,
        description="An old-fashioned wooden tool used for measuring lengths and distances, typically used by carpenters and other craftsmen.",
        tags=[Tag.CONSTRUCTION, Tag.TOOL],
        quality=Quality.COMMON,
        composition=[MATERIALS[MaterialType.WOOD]],
        craftable=True,
        flavor_text="This measuring stick has been passed down through generations of carpenters, and has been used to build everything from houses to furniture. Made from solid wood, it is marked with precise measurements and has a smooth finish that makes it easy to handle. Whether you're building a bookshelf or measuring out a room, this measuring stick is a reliable tool that will never let you down."
    ),
    ItemName.NAIL               : Item(
        name=ItemName.NAIL,
        weight=3,
        value=15,
        description="A small metal nail that can be used to fasten materials together.",
        tags=[Tag.CONSTRUCTION, Tag.TOOL],
        quality=Quality.COMMON,
        composition=[MATERIALS[MaterialType.IRON]],
        craftable=True,
        flavor_text="This nail is a simple and reliable tool that can be used for a variety of construction projects."
    ),
    ItemName.PENCIL             : Item(
        name=ItemName.PENCIL,
        weight=8,  # grams
        value=25,  # pennies
        description="A small implement used for writing",
        tags=[Tag.OFFICE, Tag.DECORATION, Tag.JUNK],
        quality=Quality.COMMON,
        composition=[MATERIALS[m] for m in (MaterialType.WOOD, MaterialType.ALUMINUM, MaterialType.GRAPHITE, MaterialType.RUBBER)],
        craftable=True,
        flavor_text="Get to the point..."
    ),
    ItemName.PLIERS             : Item(
        name=ItemName.PLIERS,
        weight=150,
        value=10_000,
        description="A versatile tool with two serrated jaws for gripping and manipulating objects.",
        tags=[Tag.CONSTRUCTION, Tag.TOOL],
        quality=Quality.COMMON,
        composition=[MATERIALS[m] for m in (MaterialType.STEEL, MaterialType.RUBBER)],
        craftable=True,
        flavor_text="These pliers have been through a lot, but they still get the job done. The rubber grip is worn, but it still provides a comfortable hold. The serrated jaws show signs of wear and tear, but they can still grip tightly and manipulate objects with ease. Whether you're working on a mechanical project or just need to tighten a bolt, these trusty pliers are up to the task."
    ),
    ItemName.RUSTY_NAIL         : Item(
        name=ItemName.RUSTY_NAIL,
        weight=3,
        value=5,
        description="A small metal nail that appears to be old and rusted beyond use.",
        tags=[Tag.POCKET_LITTER, Tag.JUNK],
        quality=Quality.POOR,
        composition=[MATERIALS[MaterialType.IRON]],
        craftable=False,
        flavor_text="This nail is so rusty and corroded that it would likely break if you tried to use it for anything."
    ),
    ItemName.SAW                : Item(
        name=ItemName.SAW,
        weight=400,  # grams
        value=12_000,  # pennies
        description="A cutting tool used for making precise cuts in wood, metal, and other materials.",
        tags=[Tag.TOOL, Tag.CONSTRUCTION],
        quality=Quality.COMMON,
        composition=[MATERIALS[m] for m in [MaterialType.STEEL, MaterialType.WOOD]],
        craftable=True,
        flavor_text="This saw is a reliable tool for any cutting job. The steel blade is sharp and durable, and the wooden handle provides a comfortable grip. Whether you're cutting through a thick piece of wood or making precise cuts in metal, this saw will get the job done."
    ),
    ItemName.TOOLBOX            : Item(
        name=ItemName.TOOLBOX,
        weight=3_000,
        value=50_000,
        description="A sturdy box used for storing and transporting tools.",
        tags=[Tag.TOOL, Tag.CONSTRUCTION, Tag.STORAGE],
        quality=Quality.COMMON,
        composition=[MATERIALS[m] for m in [MaterialType.STEEL, MaterialType.ALUMINUM]],
        craftable=True,
        flavor_text="This toolbox is a great way to keep your tools organized and easily accessible. The steel body is sturdy and durable, and the ergonomic handle makes it easy to carry. With plenty of compartments and storage space, you can keep all your tools neatly arranged and ready for use."
    ),
    ItemName.TRASH              : Item(
        name=ItemName.TRASH,
        weight=10,
        value=0,
        description="A piece of garbage that someone threw away.",
        tags=[Tag.POCKET_LITTER, Tag.JUNK],
        quality=Quality.POOR,
        composition=[MATERIALS[m] for m in [MaterialType.PAPER, MaterialType.PLASTIC]],
        craftable=False,
        flavor_text="This piece of trash doesn't seem to have any use or value. It's dirty and smelly, and definitely not something you want to keep around."
    ),

    # Treasure
    ItemName.GOBLET_OF_BRASS    : Item(
        name=ItemName.GOBLET_OF_BRASS,
        weight=4,
        value=2_300,
        description="A simple goblet made of brass, probably used for drinking.",
        tags=[Tag.DINING, Tag.ACCESSORY, Tag.TREASURE],
        quality=Quality.POOR,
        composition=[MATERIALS[MaterialType.BRASS]],
        craftable=True,
        flavor_text="Despite its modest appearance, this goblet has likely seen many a raucous goblin feast."
    ),
    ItemName.SILVER_TOOTH_PICK  : Item(
        name=ItemName.SILVER_TOOTH_PICK,
        weight=1,
        value=6_200,
        description="A small silver toothpick, probably used to clean teeth after meals.",
        tags=[Tag.DINING, Tag.ACCESSORY, Tag.TREASURE],
        quality=Quality.COMMON,
        composition=[MATERIALS[MaterialType.SILVER]],
        craftable=True,
        flavor_text="This toothpick may seem like a small and unremarkable item, but its craftsmanship is surprisingly delicate."
    ),
    ItemName.JADE_EARRING       : Item(
        name=ItemName.JADE_EARRING,
        weight=2,
        value=8_000,
        description="A single jade earring, probably worn as an accessory.",
        tags=[Tag.JEWELRY, Tag.ACCESSORY, Tag.TREASURE],
        quality=Quality.UNCOMMON,
        composition=[MATERIALS[MaterialType.JADE]],
        craftable=True,
        flavor_text="This earring may have once belonged to a goblin of high status, or perhaps it was stolen from a human traveler."
    ),
    ItemName.COPPER_KETTLE      : Item(
        name=ItemName.COPPER_KETTLE,
        weight=7,
        value=3_100,
        description="A large copper kettle, probably used for boiling water or brewing tea.",
        tags=[Tag.DINING, Tag.ACCESSORY, Tag.TREASURE],
        quality=Quality.POOR,
        composition=[MATERIALS[MaterialType.COPPER]],
        craftable=True,
        flavor_text="Despite its dents and scratches, this kettle still seems to function well enough for its intended purpose."
    ),
    ItemName.BRONZE_MIRROR      : Item(
        name=ItemName.BRONZE_MIRROR,
        weight=5,
        value=9_200,
        description="A small bronze mirror, probably used for personal grooming or vanity.",
        tags=[Tag.ACCESSORY, Tag.TREASURE],
        quality=Quality.COMMON,
        composition=[MATERIALS[MaterialType.BRONZE]],
        craftable=True,
        flavor_text="This mirror may have been stolen from a human's vanity, or perhaps it was a treasured possession of a particularly vain goblin."
    ),
}


def _tag_index() -> Dict[Tag, List[ItemName]]:
    tag_index = defaultdict(list)

    for item in ITEMS.values():
        for tag in item.tags:
            tag_index[tag].append(item.name)

    return tag_index


def random_fm_tag(tag: Tag) -> ItemName:
    return random.choice(TAG_INDEX[tag])


TAG_INDEX = _tag_index()

if __name__ == '__main__':

    from pprint import pprint as pprint

    print(TAG_INDEX[Tag.POCKET_LITTER])
    print(TAG_INDEX[Tag.JUNK])
    print()
    print(random_fm_tag(Tag.POCKET_LITTER))
    print()
    pprint(TAG_INDEX)

    print(ITEMS[ItemName.TOOLBOX].ascii_art())
