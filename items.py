from stats import *
from item import Item

bronze_sword = Item(bronze_sword_stats)
steel_sword = Item(steel_sword_stats)
bronze_mace = Item(bronze_mace_stats)
steel_mace = Item(steel_mace_stats)
journeyman_bow = Item(journeyman_bow_stats)
small_healing_pot = Item(small_healing_pot_stats)

ITEM_DICTIONARY = {
    bronze_sword.name: bronze_sword,
    steel_sword.name: steel_sword,
    bronze_mace.name: bronze_mace,
    steel_mace.name: steel_mace,
    journeyman_bow.name: journeyman_bow,
    small_healing_pot.name: small_healing_pot
}