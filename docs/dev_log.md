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

## Text Blurbs for the Farm
### Tome of Unspekable Horrors
"The Tome of Unspeakable Horrors is a cursed book of black magic and eldritch knowledge. Its ancient pages are bound in human skin and inked in blood, containing rituals and spells that defy human comprehension. The whispers of long-forgotten gods and nameless abominations can be heard emanating from its pages, driving all but the strongest-willed mad with terror. The book's power is palpable, yet so is the evil that courses through its every word. Only the bravest and most foolish would dare to unlock the secrets within, for once the tome is opened, there is no going back."

### Tome of Forbidden Knowledge
You struggle to comprehend the arcane symbols and eldritch languages scrawled across the pages of this ancient tome. As you delve deeper, your mind races and your hands shake, as if unable to contain the unspeakable secrets contained within. Your eyes dart back and forth, searching for some shred of comprehension amidst the maddening chaos.

Thoughts of madness and hysteria consume you, as you feel your grip on reality slipping away. The words on the pages seem to writhe and twist, forming hideous images in your mind's eye. And yet, you cannot look away. The knowledge contained within this cursed tome is too powerful, too tantalizing to ignore.

In the end, you know that you will pay a terrible price for this knowledge. But for now, you cannot resist the lure of the forbidden, the dark secrets hidden within the pages of the Tome of Forbidden Knowledge.

### The Blasphemous Journal of the Occult Investigator--Occult Investigator's Blasphemous Journal--Blasphemous Jornal of an Occult investigator
WIP: Logic needs a bit of a resturcture, the capture part doesn't quite make sense

Entry 1:  
I am Jeremiah Blackwood, and I am beginning this journal to document my investigation into the strange occurrences happening in this town. I've always been a skeptic of the supernatural, but I cannot deny the evidence before me. The townspeople whisper of dark forces at work, and I have seen things that cannot be explained by mere coincidence or chance.

Entry 2:  
The more I investigate, the more I find evidence of an ancient cult that has resurfaced in this town. Their rituals and sacrifices are unspeakable, and I fear for what may happen if they are allowed to continue unchecked. My mind races with the implications of what I have uncovered, and I cannot help but feel a sense of dread that I cannot shake.

Entry 3:  
I've come too close to the truth. They know I'm watching them. I can hear their whispers and feel their eyes on me wherever I go. I fear for my safety, but I cannot stop now. Too much is at stake. The town is a breeding ground for eldritch horrors, and I must stop them before they unleash their malevolence on the world.

Entry 4:  
I have made a grave mistake. I thought I could outsmart them, but I was wrong. The cultists have captured me, and they're taking me to their sacrificial altar. I know now that they were never human, but something much darker and much older. The darkness is consuming me, and I can feel it seeping into my very soul. I fear that I will never be the same, that I will become one of them. I can only hope that someone finds this journal and continues my work, so that the truth may be revealed and the darkness banished from this world.

Entry 5:  
I have managed to escape from the cultists' clutches, but I am not sure how long I can stay hidden. They are still searching for me, and I fear they will not rest until I am dead or worse. I cannot go to the authorities, for they would not believe me. They are too blinded by their own sense of logic and reason. I am on my own, but I will not stop until I have uncovered the truth and put an end to this madness.

Entry 6:  
I have come across some documents detailing the blasphemous practices and rituals of the cult. The descriptions of the eldritch horrors they seek to summon have left me shaken to my core. How can anyone willingly subject themselves to such terror? And yet, their fervor and devotion is undeniable. I fear for my own sanity as I delve deeper into this dark world. The pages of these documents seem to pulse with an unnatural energy, as if the horrors described within are trying to break free from their ink and parchment prison. I must steel myself for what lies ahead, for I fear that I may have already gone too far down this path to turn back.

Entry 7:  
I am losing my grip on reality. The more I delve into these dark rituals and incantations, the more the lines between the physical and the metaphysical seem to blur. It's as if the very air around me is alive with a malevolent energy that seeks to consume me whole.

Last night, I snuck into the abandoned church on the outskirts of town. I found a stash of old manuscripts hidden beneath the altar. These texts contained detailed descriptions of summoning rituals and blood sacrifices, and they filled me with a sense of terror that I cannot fully articulate. I cannot imagine what kind of person would engage in such vile practices.

And yet, I cannot stop reading. I feel as though I am being drawn ever deeper into this twisted world, unable to turn back or escape its grasp. I have left my old life behind, and now my only purpose is to stop these cultists and the eldritch horrors they seek to summon. But at what cost? Will I lose my sanity or my soul in the process? I fear that I may have already crossed a point of no return, and that there is no going back now. But I must press on, for the sake of all that is good and pure in this world.

Entry 9:  

I am no longer certain of who I am or what I am doing. The darkness that I once sought to banish has now consumed me, and I can feel its presence all around me. The documents that I uncovered in the abandoned church continue to call out to me, urging me to perform the rituals that will summon the ancient horrors.

I try to resist, but it's as if the very fibers of my being have been altered. I no longer fear the eldritch abominations that once filled me with terror. Now, they seem almost...familiar. As if they have been a part of me all along.

I am no longer fighting against the cult; I am serving them. I can feel their presence all around me, guiding me towards their twisted goals. I am lost to them, a pawn in their dark game. And yet, even as I write these words, I feel a sense of perverse satisfaction.

The darkness has claimed me, body and soul. And I fear that I will never be able to escape its grasp.

### Other names
The Malefic Grimoire of Dr. Navendalle--Dr. Navendalle's Malefic Grimoire
The Eldritch Compendium of Abhorrent Knowledge--Abhorrent Knowledge: An Eldritch Compendium
The Profane Codex of the Nameless Sect--The Nameless Sect's Profane Codex
The Blasphemous Journal of the Occult Investigator--Occult Investigator's Blasphemous Journal--Blasphemous Jornal of an Occult investigator

