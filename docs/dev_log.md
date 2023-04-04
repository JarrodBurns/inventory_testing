# Developer Log
describe intent

## Tasks
- [ ] Wallet Object, takes in funds distributes them through the scales
- [ ] Function to sort by Rarity and Tag
- [ ] Custom errors for Inventory.remove_material and Material dunder methods
- [ ] Look into adding negative numbers to material and see if it breaks
- [ ] Some functions could return bool and error code for custom errors

## Notes


## Dependencies

## Module TODO

### Inventory
- [X] Inventory Object, should contain: `Item`, `Material`, and `Currency`
- [X] add logic to delete materials from dict
- [ ] \_\_iadd\_\_ logic needs testing and probably a refactor 
- [ ] `Inventory` \_\_str\_\_ should be \_\_repr\_\_
- [ ] Unit tests, hand tests are too cumbersome here, I think.
- [ ] Consider add and remove methods for the `.wallet`
- [ ] `CurrencyAmount` getter for `.wallet`