from pyne.pyne import *
from utils import *
from loot import ENEMY_LOOT_TABLE

class Character:
    def __init__(self, name, race, char_class, game, level=1):
        self.name = name
        self.race = race
        self.char_class = char_class

        self.level = level

        self.money = 0

        self.inventory = {

        }

        self.dead = False

        self.game = game

        try:
            self.calculate_stats()
            self.generate_final_stats()
        except:
            pass

        self.chance_to_drop_loot = 0.8

    def attack(self, other):
        # Simulate a dice roll for damage
        dmg = self.roll_damage()

        # Silly math to determine crits
        critical = random.random() * 10 >= 10 - 3 * pow(self.luck / 10, 2)

        # Double damage on crit
        if critical:
            dmg *= 2

        other.hp -= dmg

        # Add to the dialogue
        self.game.dialogue.append(f"{self.name}{' critically ' if critical else ' '}{random.choice(['attacked', 'struck', 'hit'])} {other.name} for {dmg} damage!")

        # The other character died
        if other.hp <= 0:
            other.hp = 0
            other.dead = True

            self.game.dialogue.append(f"{other.name} died!")

    def GiveItem(self, item):
        item_count = 0
        if item.name in self.inventory:
            item_count = self.inventory[item.name]

        self.inventory.update({ item.name: item_count + 1 })

    def DropLoot(self):
        if random.random() <= self.chance_to_drop_loot:
            return ExpWeightedChoice(ENEMY_LOOT_TABLE[self.name])
        return None

    def GainXP(self, enemies):
        enemy_lvls = [e.level for e in enemies.characters]

        xp = random.randint(0, 2) + round(sum(enemy_lvls) * 1.5)

        self.game.dialogue.append(f"{self.name} gained {xp} XP!")

    def roll_damage(self):
        # Add strength to a d6 for damage
        return self.strength + roll(6)

    def calculate_stats(self):

        stat_block = self.game.race_stats[self.race]

        self.sprite = stat_block['sprite']

        self.strength = stat_block['strength']
        self.intelligence = stat_block['intelligence']
        self.mysticism = stat_block['mysticism']
        self.perception = stat_block['perception']
        self.luck = stat_block['luck']
        self.endurance = stat_block['endurance']
    
    def generate_final_stats(self):

        self.hp = self.max_hp = 5 * self.endurance + self.strength
        self.mp = self.max_mp = 5 * self.mysticism + self.intelligence

        self.base_speed = 2 * self.perception + self.strength
        self.speed = self.base_speed

class Party:
    def __init__(self, characters, show_pos, move_left = False):
        self.characters = characters
        self.show_pos = show_pos
        self.selected_character = 0
        self.move_left = move_left # Fuck this variable

    def draw(self, engine, selected_character, selected_color):
        # Show all the sprites for characters and show
        # '*' on selected character if necessary
        for i in range(len(self.characters)):
            if self.characters[i]:
                engine.DrawSprite(self.characters[i].sprite, engine.background_color, self.show_pos[0] - i * 5 * (2 * self.move_left - 1) - 1, self.show_pos[1] - 2)

                if selected_character == self.characters[i]:
                    engine.DrawChar('*', (selected_color if selected_color else engine.Color.YELLOW, engine.background_color), self.show_pos[0] - i * 5 * (2 * self.move_left - 1), self.show_pos[1] - 3)