import random
from pyne.pyne import PyneEngine

# To save my hands :) (just a little bit)
C = PyneEngine.Color

def roll(n):
    return random.randint(1, n)

def ExpWeightedChoice(iterable):
    return iterable[int(pow(random.random(), 2) * len(iterable))]

# Enum: what action are we waiting for the player to perform?
class Await:
    ATTACK = 0
    ITEM = 1
    MAGIC = 2

# Enum: where are we lol
class SceneType:
    OVERWORLD = 0
    BATTLE = 1
    MENU = 2

def repl_ind_str(s, char, index):
    return s[:index] + char + s[index + 1:]