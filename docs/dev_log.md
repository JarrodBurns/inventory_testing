# Developer Log
LootSimlator is ...

## Tasks
- [ ] Wallet Object, takes in funds distributes them through the scales
- [ ] Function to sort by Rarity and Tag
- [ ] Custom errors for Inventory.remove_material and Material dunder methods
- [ ] Look into adding negative numbers to material and see if it breaks
- [ ] Some functions could return bool and error code for custom errors
- [ ] Save inventory data to toml

## Notes


## Dependencies
- Pytest
- Pyperclip

## Module TODO

### Inventory
- [X] Inventory Object, should contain: `Item`, `Material`, and `Currency`
- [X] add logic to delete materials from dict
- [ ] `__iadd__` logic needs testing and probably a refactor 
- [ ] `Inventory` `__str__` should be `__repr__`
- [ ] Unit tests, hand tests are too cumbersome here, I think.
- [ ] Consider: add and remove methods for the `.wallet`
- [ ] `CurrencyAmount` getter for `.wallet`
- [ ] subtracting from .balance passes silently. (Don't allow negative balances)

### Wallet
- [ ] Consider: Refactor current implementation with `CurrencyAmount` 
- [ ] Fix tests
- [ ] Refactor `__str__`


### Item
- [ ] Consider: raising error for `random_fm_tag` and `get_item` over returning None

### Monster
- [ ] Rename to MonsterName

### Loot
- [ ] Rename creature to monster_name?
- [ ] Add tags to `LootTable`

### Material
- [ ] Consider "always expecting list of material bs" overload for str
- [ ] 