# Developer Log
LootSimlator is ...

## Tasks
- [X] Wallet Object, takes in funds distributes them through the scales
- [X] Function to sort by Rarity and Tag
- [X] Custom errors for Inventory.remove_material and Material dunder methods
- [ ] Look into adding negative numbers to material and see if it breaks
- [ ] Some functions could return bool and error code for custom errors
- [ ] Save inventory data to toml

## Notes

## Bugs
- `Item.ascii_art` Codec error occurs when using NativePython build at work machine. THe issue could be due to the way the build system is set up, but it probably makes sense to check for the error and replace the characters if necessary as they do come from the extended ASCII table.
- It may be prudent to optimize our enums later.

## ideas:
```
- Inventory
    - Materials
    - Wallet
    - Equipment
        - Weapons
        - Apparel
    - Consumables
        - Food
        - Potions

```

- omni wrapper for Query.Item.TOOLBOX, Query.ItemName.TOOLBOX, Query.Monster.loot, Query.Random, etc
```
desired wrapper access
        Query.Item.TOOLBOX
        Query.Item.random

        Query.ItemName.random

        Query.Monster.GOBLIN
        Query.Monster.random

        Query.Tag.TOOLBOX

```
- *Resolve* - Health
- *Sanity*  - Stamina
- *Essence* - Mana

- `Berserker` - you no longer lose sanity (maybe heal) but most merchants won't interact with you

## Dependencies
- Pytest
- Pyperclip

## Idea Farm
- Short rest
- Long rest
- Sanity


## Module TODO
- [ ] Consider renaming quantity to amount, otherwise it may lead to confusion

### Inventory
- [X] Inventory Object, should contain: `Item`, `Material`, and `Currency`
- [X] add logic to delete materials from dict
- [X] Consider: add and remove methods for the `.wallet`
- [ ] `__iadd__` logic needs testing and probably a refactor 
- [ ] `Inventory` `__str__` should be `__repr__`
- [ ] Unit tests, hand tests are too cumbersome here, I think.
- [ ] `CurrencyAmount` getter for `.wallet`
- [ ] subtracting from .balance passes silently. (Don't allow negative balances)

### Wallet
- [ ] Consider: Refactor current implementation with `CurrencyAmount` 
- [ ] Fix tests
- [ ] Refactor `__str__`


### Item
- [ ] Consider: raising error for `random_fm_tag` and `get_item` over returning None
- [ ] Scrub weights and values down to TRASH ("Switch to pounds?") consider economy
- [ ] Consider rename composition to materials

### Monster
- [ ] Rename to MonsterName

### Loot
- [ ] Rename creature to monster_name?
- [ ] Add tags to `LootTable`
- [ ] Loot table is a static class, freeze it?

### Material
- [ ] Consider "always expecting list of material bs" overload for str
- [ ] Consider: Create MaterialQuantity and remove quantity from material

### Loot
- [ ] `encounter_by_level code can be reduced by defining __add__`[^1]


### db_entries
- [ ] finish doing this.


##### Footnotes
[^1]: `return sum([self.inventory for _ in range(level)], Inventory())`


## Smells
- Str enums should probably just be regular enums for computational efficiency
- There isn't a model for `ItemName` (This may be fine, I can't decide)
- `creature` and `monster` violate naming consistency between models and objects
- `materials` and `composition` violate naming consistency between models and objects
- A call like `ItemManager.Item.model.get_fm_name(session, name) is possible` make private?

# 2

1. Enemy
    - LootTable
        - name
        - loot
        - weights

    - Inventory
        - Currency
        - Items
        - Materials

## Enums
- EnemyName
- ItemName
- TagName


## LootTable

### name
- Identifier for the loot table. Should be an `EnemyName`

### loot
- list of `ItemName` and or `Tag` used to derive an enemies loot by random choice

### weights
- choice weights for comparison against the `loot` 