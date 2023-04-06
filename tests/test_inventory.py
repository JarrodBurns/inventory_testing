

from inventory import Inventory
from item import ItemName
from material import MaterialType, Material
from quality import Quality


from collections import defaultdict
from typing import Dict, List

import pytest


@pytest.fixture
def inventory():
    inventory = Inventory()
    inventory.add_item(ItemName.TRASH)
    inventory.add_item(ItemName.SAW)
    inventory.add_item(ItemName.SAW)
    inventory.add_materials([
        Material(MaterialType.PAPER, Quality.COMMON, 10),
        Material(MaterialType.STEEL, Quality.COMMON, 5),
    ])
    inventory.wallet += 100
    return inventory


def test_add_item(inventory):
    inventory.add_item(ItemName.TRASH)
    assert inventory.items[ItemName.TRASH] == 2


def test_remove_item(inventory):
    inventory.remove_item(ItemName.TRASH)
    assert inventory.items[ItemName.TRASH] == 0
    with pytest.raises(KeyError):
        inventory.remove_item(ItemName.TRASH)


def test_add_materials(inventory):
    inventory.add_materials([
        Material(MaterialType.PAPER, Quality.COMMON, 5),
        Material(MaterialType.STEEL, Quality.COMMON, 3),
    ])
    assert inventory.materials[MaterialType.PAPER].quantity == 15
    assert inventory.materials[MaterialType.STEEL].quantity == 8


def test_remove_materials(inventory):
    inventory.remove_materials([
        Material(MaterialType.PAPER, Quality.COMMON, 5),
        Material(MaterialType.STEEL, Quality.COMMON, 3),
    ])
    assert inventory.materials[MaterialType.PAPER].quantity == 5
    assert inventory.materials[MaterialType.STEEL].quantity == 2
    with pytest.raises(ValueError):
        inventory.remove_materials([Material(MaterialType.PAPER, Quality.COMMON, 10)])


def test_add_wallet(inventory):
    inventory.wallet += 25
    inventory.wallet.add(25)
    assert inventory.wallet.balance == 150


def test_remove_wallet(inventory):
    inventory.wallet -= 25
    inventory.wallet.sub(25)
    assert inventory.wallet.balance == 50

    with pytest.raises(ValueError):
        inventory.wallet -= 10000


def test_inventory_merge():
    inv1 = Inventory()
    inv1.add_item(ItemName.TRASH)
    inv1.wallet.add(50)
    inv2 = Inventory()
    inv2.add_item(ItemName.SAW)
    inv2.wallet.add(100)
    inv1 += inv2
    assert inv1.items[ItemName.TRASH] == 1
    assert inv1.items[ItemName.SAW] == 1
    assert inv1.wallet.balance == 150
