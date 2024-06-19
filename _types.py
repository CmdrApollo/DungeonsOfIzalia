class ItemType:
    WEAPON = 0
    ARMOR = 1
    CONSUMABLE = 2

class StatChange:
    HEALTH = 0
    MAGIC = 1
    SPEED = 2

class Menu:
    INVENTORY = 0
    SYSTEM = 1

class MenuAction:
    USE = 0
    DROP = 1

class DamageType:
    SLASH = 0
    CRUSH = 1
    PIERCE = 2

class RoomType:
    ENTER = 0
    EXIT = 1

    SHOP = 2
    MINIBOSS = 3
    BOSS = 4
    REGULAR = 5
    TREASURE = 6

class Race:
    HUMAN  = 0
    DWARF  = 1
    GNOME  = 2
    ELF    = 3
    ORC    = 4
    DRAGON = 5

    GOBLIN = 6
    AQUAFID = 7
    WEREWOLF = 8

    def to_string(value):
        if value == None: return "---"
        return [
            "Human",
            "Dwarf",
            "Gnome",
            "Elf",
            "Orc",
            "Dragon",
            "Goblin",
            "Aquafid",
            "Werewolf"
        ][value]

class Class:
    FIGHTER = 0
    MAGE = 1
    THIEF = 2
    BATTLEMAGE = 3
    RANGER = 4
    WITCH = 5

    def to_string(value):
        if value == None: return "---"
        return [
            "Fighter",
            "Mage",
            "Thief",
            "Battlemage",
            "Ranger",
            "Witch"
        ][value]