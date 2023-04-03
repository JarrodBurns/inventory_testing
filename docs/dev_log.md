# Developer Log
describe intent

## Tasks
- [ ] Wallet Object, takes in funds distributes them through the scales
- [ ] Inventory Object, should contain Item, Material, and Currency

## Notes

## Dependencies

class CurrencyType(str, Enum):
    COPPER = "Copper"
    SILVER = "Silver"
    GOLD   = "Gold"

Lets make a wallet class, called Wallet. 

It should manage the currenies provided by the CurrencyType enum, and the code should leave the class open to adding more currencies in the future.

Each CurrencyType is worth 100 of the previous currency, i.e. 1 gold = 100 silver.

The class needs a way for it to 

You should be able to add or subtract a Wallet from another Wallet, and handle all appropriate errors.

I also think the wallet should be smart enough to color up it's own currencies, meaning if it has 101 silver, it should actually be 1 silver and 1 gold.

