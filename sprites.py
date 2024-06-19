from pyne.pyne import PyneEngine
from utils import *
import json, os

world = json.load(open(os.path.join('maps', 'world.json')))
semar = json.load(open(os.path.join('maps', 'semar.json')))
isat  = json.load(open(os.path.join('maps', 'isat.json')))

goblin = { # Elf / Mischieve Aspect
    "lines": [
        "<0>",
        "/|\\",
        " M ",
    ],
    "colors": [
        (C.GREEN, C.GREEN, C.GREEN),
        (C.GREEN, C.GREEN, C.GREEN),
        (None, C.BROWN, None),
    ]
}

human = {
    "lines": [
        " 0 ",
        "/|\\",
        " M "
    ],
    "colors": [
        (None, C.GRAY, None),
        (C.GRAY, C.GRAY, C.GRAY),
        (None, C.BROWN, None),
    ]
}

dwarf = {
    "lines": [
        " 0 ",
        "/#\\",
        " M "
    ],
    "colors": [
        (None, C.YELLOW, None),
        (C.YELLOW, C.BROWN, C.YELLOW),
        (None, C.BROWN, None),
    ]
}

gnome = {
    "lines": [
        "~0~",
        "/|\\",
        " M "
    ],
    "colors": [
        (C.GRAY, C.GRAY, C.GRAY),
        (C.GRAY, C.GRAY, C.GRAY),
        (None, C.BROWN, None),
    ]
}

elf = {
    "lines": [
        " 0 ",
        "/%\\",
        " M "
    ],
    "colors": [
        (None, C.YELLOW, None),
        (C.YELLOW, C.DARK_GREEN, C.YELLOW),
        (None, C.BROWN, None),
    ]
}

orc = {
    "lines": [
        "-^-",
        "/|\\",
        " M "
    ],
    "colors": [
        (C.DARK_GREEN, C.GRAY, C.DARK_GREEN),
        (C.DARK_GREEN, C.DARK_GREEN, C.DARK_GREEN),
        (None, C.BROWN, None),
    ]
}

aquafid = { # Orc / Aquatic Aspect
    "lines": [
        ">0<",
        "/|\\",
        " M "
    ],
    "colors": [
        (C.CYAN, C.CYAN, C.CYAN),
        (C.CYAN, C.CYAN, C.CYAN),
        (None, C.BROWN, None),
    ]
}

werewolf = { # Human / Primal Aspect
    "lines": [
        "<o>",
        "/|\\",
        " M "
    ],
    "colors": [
        (C.DARK_BROWN, C.DARK_BROWN, C.DARK_BROWN),
        (C.DARK_BROWN, C.DARK_BROWN, C.DARK_BROWN),
        (None, C.BROWN, None),
    ]
}

bat = {
    "lines": [
        "   ",
        "   ",
        "^o^"
    ],
    "colors": [
        (None, None, None),
        (None, None, None),
        (C.DARK_MAGENTA, C.GRAY, C.DARK_MAGENTA),
    ]
}

pig = {
    "lines": [
        "   ",
        "o^-",
        ' ""'
    ],
    "colors": [
        (None, None, None),
        (C.MAGENTA, C.MAGENTA, C.MAGENTA),
        (None, C.MAGENTA, C.MAGENTA),
    ]
}

pet_automaton = {
    "lines": [
        "   ",
        "/o\\",
        ' ""'
    ],
    "colors": [
        (None, None, None),
        (C.GRAY, C.RED, C.GRAY),
        (None, C.GRAY, C.GRAY),
    ]
}

rat = {
    "lines": [
        "   ",
        "*=~",
        " ''"
    ],
    "colors": [
        (None, None, None),
        (C.DARK_MAGENTA, C.GRAY, C.DARK_MAGENTA),
        (None, C.GRAY, C.GRAY),
    ]
}

mech = {
    "lines": [
        "\\0/",
        "/V\\",
        " M "
    ],
    "colors": [
        (C.RED, C.DARK_RED, C.RED),
        (C.RED, C.DARK_RED, C.RED),
        (None, C.DARK_RED, None),
    ]
}

automaton = { # Elf / Innovation Aspect
    "lines": [
        " 0 ",
        "/*\\",
        " M "
    ],
    "colors": [
        (None, C.CYAN, None),
        (C.CYAN,  C.RED, C.CYAN),
        (None, C.CYAN, None),
    ]
}

grave = {
    "lines": [
        " _ ",
        "|-|",
        "*-* "
    ],
    "colors": [
        (None, C.GRAY, None),
        (C.GRAY, C.GRAY, C.GRAY),
        (C.RED, C.GRAY, C.YELLOW),
    ]
}

sword = {
    "lines": [
        "  /",
        "_//",
        "// "
    ],
    "colors": [
        (None, None, C.GRAY),
        (C.WHITE, C.GRAY, C.GRAY),
        (C.BROWN, C.BROWN, None),
    ]
}

club = {
    "lines": [
        "   ",
        " / ",
        "/  "
    ],
    "colors": [
        (None, None, None),
        (None, C.DARK_BROWN, None),
        (C.BROWN, None, None),
    ]
}

mace = {
    "lines": [
        "  _",
        " /|",
        "/ *"
    ],
    "colors": [
        (None, None, C.DARK_GRAY),
        (None, C.BROWN, C.WHITE),
        (C.BROWN, None, C.DARK_GRAY),
    ]
}

fishing_rod = {
    "lines": [
        "  /",
        " /|",
        "/ *"
    ],
    "colors": [
        (None, None, C.BROWN),
        (None, C.BROWN, C.WHITE),
        (C.BROWN, None, C.RED),
    ]
}

bow = {
    "lines": [
        "+\\ ",
        "|| ",
        "+/ "
    ],
    "colors": [
         (C.GRAY, C.BROWN, None),
        (C.WHITE, C.BROWN, None),
         (C.GRAY, C.BROWN, None),
    ]
}