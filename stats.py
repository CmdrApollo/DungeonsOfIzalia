from sprites import *
from _types import *

###Race stats###

basic_human_stats = {
    "sprite": human,

    "strength": 5,
    "intelligence": 5,
    "mysticism": 4,
    "perception": 5,
    "luck": 5,
    "endurance": 6
}

basic_dwarf_stats = {
    "sprite": dwarf,

    "strength": 6,
    "intelligence": 5,
    "mysticism": 5,
    "perception": 4,
    "luck": 5,
    "endurance": 5
}

basic_gnome_stats = {
    "sprite": gnome,

    "strength": 4,
    "intelligence": 6,
    "mysticism": 6,
    "perception": 5,
    "luck": 5,
    "endurance": 4
}

basic_elf_stats = {
    "sprite": elf,

    "strength": 5,
    "intelligence": 6,
    "mysticism": 5,
    "perception": 5,
    "luck": 5,
    "endurance": 4
}

basic_orc_stats = {
    "sprite": orc,

    "strength": 6,
    "intelligence": 4,
    "mysticism": 4,
    "perception": 5,
    "luck": 5,
    "endurance": 6
}

basic_goblin_stats = {
    "sprite": goblin,

    "strength": 4,
    "intelligence": 6,
    "mysticism": 5,
    "perception": 5,
    "luck": 5,
    "endurance": 5
}

###Class stats###

base_fighter_stats = {}
base_mage_stats = {}
base_thief_stats = {}
base_battlemage_stats = {}
base_ranger_stats = {}
base_witch_stats = {}

###Item stats###

# Weapons

bronze_sword_stats = {
    'sprite': sword,

    'name': "Bronze Sword",
    'price': 10,

    'type': ItemType.WEAPON,
    'damage': 5,

    'damage_type': DamageType.SLASH
}

steel_sword_stats = {
    'sprite': sword,

    'name': "Steel Sword",
    'price': 25,

    'type': ItemType.WEAPON,
    'damage': 12,

    'damage_type': DamageType.SLASH
}

bronze_mace_stats = {
    'sprite': mace,

    'name': "Bronze Mace",
    'price': 12,

    'type': ItemType.WEAPON,
    'damage': 5,

    'damage_type': DamageType.CRUSH
}

steel_mace_stats = {
    'sprite': mace,

    'name': "Steel Mace",
    'price': 28,

    'type': ItemType.WEAPON,
    'damage': 12,

    'damage_type': DamageType.CRUSH
}

journeyman_bow_stats = {
    'sprite': bow,

    'name': "Journeyman Bow",
    'price': 15,

    'type': ItemType.WEAPON,
    'damage': 7,

    'damage_type': DamageType.PIERCE
}

small_healing_pot_stats = {
    'sprite': None,

    'name': "S. Healing Potion",
    'price': 25,

    'type': ItemType.CONSUMABLE,
    'stat': StatChange.HEALTH,
    'amount': 10,
}