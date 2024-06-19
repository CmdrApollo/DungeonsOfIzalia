from stats import *

# TODO: FUCKING MAKE THIS
class Item:
    def __init__(self, stat_block):
        self.sprite = stat_block['sprite']
        self.name = stat_block['name']

        self.price = stat_block['price']
        self.type = stat_block['type']

        match self.type:
            case ItemType.WEAPON:
                self.damage = stat_block['damage']
                self.damage_type = stat_block['damage_type']
            case ItemType.ARMOR:
                pass
            case ItemType.CONSUMABLE:
                self.stat = stat_block['stat']
                self.amount = stat_block['amount']
    
    def use(self, game):
        match self.type:
            case ItemType.WEAPON:
                return False
            case ItemType.ARMOR:
                return False
            case ItemType.CONSUMABLE:
                match self.stat:
                    case StatChange.HEALTH:
                        game.player_character.hp = min(game.player_character.max_hp, game.player_character.hp + self.amount)
                    case StatChange.MAGIC:
                        game.player_character.mp = min(game.player_character.max_mp, game.player_character.mp + self.amount)
                    case StatChange.SPEED:
                        return False
                return True