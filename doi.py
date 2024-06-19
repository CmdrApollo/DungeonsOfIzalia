# All of the imports!!!!
from pyne.pyne import *
from utils import *
from sprites import *
from character import *
from stats import *
from _types import *
from maps import *
from trigger import *
from dungeon import *
from items import *

TITLE = json.load(open('title.json', encoding='utf-8'))

PLAYER_CLASS_COLORS = {
    Class.FIGHTER   : C.RED,
    Class.MAGE      : C.BLUE,
    Class.THIEF     : C.ORANGE,
    Class.BATTLEMAGE: C.CYAN,
    Class.RANGER    : C.GREEN,
    Class.WITCH     : C.MAGENTA
}

# The class that does everything
class Game(PyneEngine):
    # Some constants
    TITLE = "Dungeons of Izalia"
    background_color = C.BLACK

    # Custom sprite-drawing function
    # same as DrawTextLines but user can specify colors for each character
    def DrawSprite(self, sprite, bg, x, y):
        for j in range(len(sprite['lines'])):
            for i in range(len(sprite['lines'][j])):
                if sprite['lines'][j][i] != " ":
                    self.DrawChar(sprite['lines'][j][i], (sprite['colors'][j][i], bg), x + i, y + j)

    # Makes a tuple with the pre-specified background color and a chosen color
    # ( to save me from typing (C.WHITE, self.background_color) over and over )
    def from_fg(self, fg):
        return (fg, self.background_color)

    # you'll never guess what it does
    def GenerateDungeon(self):
        while True:
            # magic numbers yay my favorite
            x = random.randint(0, 71) // 2 + 35
            y = random.randint(0, 20) // 2 + 10
            
            if self.overworld_map.sprite['lines'][y][x] == '"':
                self.overworld_map.sprite['lines'][y] = repl_ind_str(self.overworld_map.sprite['lines'][y], '!', x)
                break
        
        return Dungeon(x, y, 0.2, None, self)

    # returns bool whether or not player is in a dungeon
    def InDungeon(self):
        return self.current_map == self.dungeons[self.current_dungeon].floors[self.dungeons[self.current_dungeon].current_floor]

    def GenerateMerchantInventory(self):
        return {
            "Bronze Sword": 3,
            "S. Healing Potion": 5,
            "Bronze Mace": 1,
            "Steel Sword": 1,
        }

    def OnConstruct(self):
        
        # Linking races to their stat-blocks
        self.race_stats = {
            Race.HUMAN: basic_human_stats,
            Race.DWARF: basic_dwarf_stats,
            Race.GNOME: basic_gnome_stats,
            Race.ELF: basic_elf_stats,
            Race.ORC: basic_orc_stats,
            Race.DRAGON: None,

            Race.GOBLIN: basic_goblin_stats,
            Race.AQUAFID: basic_orc_stats,
            Race.WEREWOLF: basic_human_stats
        }

        # Start the game in the overworld
        self.scene_type = SceneType.OVERWORLD
        
        # Initializing parties. These will get overwritten anyways
        self.player_party = Party([],
        (self.TerminalWidth() // 2 - 6, self.TerminalHeight() - 12), True)
        
        self.enemy_party = Party([],
        (self.TerminalWidth() // 2 + 6, self.TerminalHeight() - 12), False)

        # Opening dialogue
        self.dialogue = [
            "You find yourself on the shores of Ima, the south-easternmost region of Ahlun.",
            "You journeyed by ship from the far off continent of Merat, the land of the Humans.",
            "What reason you were on that ship matters not now. You were cast off of the vessel and left astray on the shores of Ima.",
            "You are aware that not far to the north-west lies the small village of Semar. Perhaps there you can gather supplies and find a way forwards."
        ]

        # Where is the player initially positioned in the overworld
        self.overworld_position = pygame.Vector2(46, 16)

        # All the characters taking place in a battle, regardless of party
        self.battle_characters = []
        self.current_character = 0

        # Helpful for menuing
        self.battle_phase = 0

        # Which menu element is the player targeting?
        self.menu_selection = pygame.Vector2(0, 0)

        # What colors of what characters does the player collide against in maps?
        self.collision_mask = [
            ( '#', [C.BROWN, C.DARK_BROWN, C.ORANGE, C.GRAY, C.DARK_GRAY, C.WHITE]),
            ( '~', [C.BLUE, C.DARK_BLUE, C.CYAN, C.DARK_CYAN, C.RED, C.DARK_RED, C.ORANGE]),
            ( '^', [C.BROWN, C.DARK_BROWN, C.ORANGE]),
            ( '/', [C.BLUE, C.DARK_BLUE, C.CYAN, C.DARK_CYAN, C.RED, C.DARK_RED, C.ORANGE, C.BROWN, C.DARK_BROWN]),
            ('\\', [C.BLUE, C.DARK_BLUE, C.CYAN, C.DARK_CYAN, C.RED, C.DARK_RED, C.ORANGE, C.BROWN, C.DARK_BROWN]),
            ( '_', [C.BLUE, C.DARK_BLUE, C.CYAN, C.DARK_CYAN, C.RED, C.DARK_RED, C.ORANGE, C.BROWN, C.DARK_BROWN]),
            ( '|', [C.BLUE, C.DARK_BLUE, C.CYAN, C.DARK_CYAN, C.RED, C.DARK_RED, C.ORANGE, C.BROWN, C.DARK_BROWN])
        ]

        # Initializing the over-arching overworld map, setting it to current
        self.overworld_map = Map("The Continent of Ahlun", world, [], [], self)

        self.current_map = self.overworld_map

        # City name -> Map dictionary
        self.cities = {
            'Semar': Map("The Village of Semar", semar, [Trigger(self.overworld_map, 0, 10, 43, 15)], [], self),
            'Isat' : Map("The Village of Isat" , isat , [Trigger(self.overworld_map, 0, 10, 33, 13)], [], self)
        }

        self.dungeons = [
            self.GenerateDungeon() for _ in range(3)
        ]

        self.current_dungeon = 0

        dungeon_triggers = [
            Trigger(
                dungeon.floors[0],
                dungeon.x,
                dungeon.y,
                dungeon.exit_point_x,
                dungeon.exit_point_y,
            ) for dungeon in self.dungeons ]

        # Generate city and dungeon entrance triggers
        self.overworld_map.triggers = [
            Trigger(self.cities[city],
                    self.cities[city].triggers[0].target_x,
                    self.cities[city].triggers[0].target_y,
                    self.cities[city].triggers[0].x + 1,
                    self.cities[city].triggers[0].y
                ) for city in self.cities
            ] + dungeon_triggers

        # Internal time, incremented when player moves in overworld
        # TODO: other actions advance time
        self.current_time = 0

        # Variables for showing the player the time
        self.day = 1

        self.months = ['Meyra', 'Hazar', 'Feran', 'Mora', 'Awan', 'Relan']
        self.month = 0

        self.battle_animation = False
        self.b_animation_time = 0
        self.b_animation_length = 3

        ### AUDIO ###

        self.LoadAudio('overworld_song', ['audio', 'music', 'song_1.wav'])
        self.LoadAudio('battle_start', ['audio', 'music', 'battle_start.wav'])
        self.LoadAudio('battle_theme', ['audio', 'music', 'battle_theme_1.wav'])

        self.LoadAudio('cursor', ['audio', 'select.wav'])

        self.PlaySong('overworld_song')

        self.GetAudioHandler().set_volume_music(0)
        self.GetAudioHandler().set_volume_sfx(0)

        self.character_create = True
        self.creation_step = 0

        self.player_character = Character("---", None, None, self)

        self.main_menu = True
        self.main_menu_timer = 0

        self.menu = None

        self.action = None
        self.menu_action = None
        
        self.merchant = None

    def OnCharacterCreate(self):
        race_key_map = {
            K_h: Race.HUMAN,
            K_d: Race.DWARF,
            K_g: Race.GNOME,
            K_e: Race.ELF,
            K_o: Race.ORC
        }

        class_key_map = {
            K_f: Class.FIGHTER,
            K_m: Class.MAGE,
            K_t: Class.THIEF,
            K_b: Class.BATTLEMAGE,
            K_r: Class.RANGER,
            K_w: Class.WITCH
        }

        self.Clear(' ', self.from_fg(C.WHITE))
        self.DrawRect(self.from_fg(C.WHITE), 0, 0, self.TerminalWidth() - 1, self.TerminalHeight() - 1)
        
        self.DrawTextLines([
            f"Name: {self.player_character.name}",
            f"Race: {Race.to_string(self.player_character.race)}",
            f"Class: {Class.to_string(self.player_character.char_class)}"
        ], self.from_fg(C.WHITE), self.TerminalWidth() - 2, 1, True)

        if self.player_character.char_class != None:
            stats = [self.player_character.strength, self.player_character.intelligence, self.player_character.mysticism, self.player_character.perception, self.player_character.luck, self.player_character.endurance]

            sr = 30 - sum(stats)

        match self.creation_step:
            case 0: # Race
                for k in race_key_map:
                    if self.KeyPressed(k):
                        self.player_character.race = race_key_map[k]
                        self.creation_step = 1
                if self.KeyPressed(K_z):
                    self.player_character.race = random.choice(list(race_key_map.values()))
                    self.creation_step = 1

                self.DrawTextLines([
                    "Pick a Race:",
                    "",
                    "[h]: Human",
                    "[d]: Dwarf",
                    "[g]: Gnome",
                    "[e]: Elf",
                    "[o]: Orc",
                    "[z]: Random"
                ], self.from_fg(C.WHITE), 1, 1)

            case 1: # Class
                for k in class_key_map:
                    if self.KeyPressed(k):
                        self.player_character.char_class = class_key_map[k]
                        self.creation_step = 2
                        self.player_character.calculate_stats()
                if self.KeyPressed(K_z):
                    self.player_character.char_class = random.choice(list(class_key_map.values()))
                    self.creation_step = 2
                    self.player_character.calculate_stats()

                self.DrawTextLines([
                    "Pick a Class:",
                    "",
                    "[f]: Fighter",
                    "[m]: Mage",
                    "[t]: Thief",
                    "[b]: Battlemage",
                    "[r]: Ranger",
                    "[w]: Witch",
                    "[z]: Random"
                ], self.from_fg(C.WHITE), 1, 1)

            case 2: # Stats
                if self.KeyPressed(K_UP):
                    self.menu_selection.y -= 1
                    if self.menu_selection.y < 0:
                        self.menu_selection.y += 7
                elif self.KeyPressed(K_DOWN):
                    self.menu_selection.y = (self.menu_selection.y + 1) % 7
                
                elif self.KeyPressed(K_LEFT) and self.menu_selection.y < 6:
                    v = max(stats[int(self.menu_selection.y)] - 1, 0)
                    match int(self.menu_selection.y):
                        case 0: self.player_character.strength = v
                        case 1: self.player_character.intelligence = v
                        case 2: self.player_character.mysticism = v
                        case 3: self.player_character.perception = v
                        case 4: self.player_character.luck = v
                        case 5: self.player_character.endurance = v
                elif self.KeyPressed(K_RIGHT) and self.menu_selection.y < 6 and sr > 0:
                    v = min(stats[int(self.menu_selection.y)] + 1, 10)
                    match int(self.menu_selection.y):
                        case 0: self.player_character.strength = v
                        case 1: self.player_character.intelligence = v
                        case 2: self.player_character.mysticism = v
                        case 3: self.player_character.perception = v
                        case 4: self.player_character.luck = v
                        case 5: self.player_character.endurance = v
                elif self.KeyPressed(K_z) and self.menu_selection.y == 6:
                    self.creation_step = 3
                    self.player_character.name = ''

                stats_lines = [
                    f"Pick your Stats ({sr} Points Remaining):",
                    "",
                    f"[ ] Strength    : {'+'*self.player_character.strength + '-' * (10 - self.player_character.strength)}",
                    f"[ ] Intelligence: {'+'*self.player_character.intelligence + '-' * (10 - self.player_character.intelligence)}",
                    f"[ ] Mysticism   : {'+'*self.player_character.mysticism + '-' * (10 - self.player_character.mysticism)}",
                    f"[ ] Perception  : {'+'*self.player_character.perception + '-' * (10 - self.player_character.perception)}",
                    f"[ ] Luck        : {'+'*self.player_character.luck + '-' * (10 - self.player_character.luck)}",
                    f"[ ] Endurance   : {'+'*self.player_character.endurance + '-' * (10 - self.player_character.endurance)}",
                    "",
                    "[ ] Done"
                ]

                self.DrawTextLines(stats_lines, self.from_fg(C.WHITE), 1, 1)

                y = 3
                for line in stats_lines[2:]:
                    for x in range(len(line)):
                        if line[x] == '+':
                            self.SetColor(self.from_fg(C.GREEN), x + 1, y)
                        elif line[x] == '-':
                            self.SetColor(self.from_fg(C.RED), x + 1, y)
                    y += 1

                if self.menu_selection.y < 6:
                    self.DrawChar('*', self.from_fg(C.WHITE), 2, 3 + int(self.menu_selection.y))
                else:
                    self.DrawChar('*', self.from_fg(C.WHITE), 2, 10)
            case 3: # Name
                if self.HasTextCache():
                    self.player_character.name += self.TextCache()
                elif self.KeyPressed(K_BACKSPACE) and len(self.player_character.name) > 0:
                    self.player_character.name = self.player_character.name[:-1]
                
                if self.KeyPressed(K_RETURN):
                    self.creation_step = 0
                    self.character_create = False

                    self.player_character.generate_final_stats()
                    self.player_party.characters.append(self.player_character)

                    self.menu_selection.xy = 0, 0

                self.DrawTextLines([
                    "Pick your Name:",
                    "",
                    self.player_character.name + '_'
                ], self.from_fg(C.WHITE), 1, 1)

    # Call when we start a new battle!
    def OnBattleStart(self):
        self.battle_animation = True
        self.b_animation_time = 0

        self.scene_type = SceneType.BATTLE

        for char in self.player_party.characters + self.enemy_party.characters:
            char.speed = char.base_speed + roll(6)
        
        self.battle_characters = self.player_party.characters + self.enemy_party.characters
        self.battle_characters.sort(key = lambda c: c.speed)

        self.current_character = 0
        self.battle_phase = 0

        self.battle_over = False

        self.player_party_won = False

    # Call at the end of any character's turn
    def OnNextTurn(self):
        for i in range(10):
            self.current_character = (self.current_character + 1) % len(self.battle_characters)
            
            if not self.battle_characters[self.current_character].dead:
                break
        
        if i >= len(self.battle_characters):
            # are all characters dead?
            self.battle_over = True

        self.battle_phase = 0

    # Check the (screen buffer oh no) for if we can move to a spot
    # TODO: make it check map sprite instead
    def AllowMove(self, x, y):            
        symbols = [c[0] for c in self.collision_mask]
        colors = [c[1] for c in self.collision_mask]

        if self.InDungeon():
            char = self.CharAt(int(x), int(y))
        else:
            char = self.CharAt(int(2 + x), int(2 + y))
        return char.symbol not in symbols or char.symbol in symbols and char.fg not in colors[symbols.index(char.symbol)]

    # Call when we wanna advance time
    def OnAdvanceTime(self):
        self.current_time += 1

        self.day = self.current_time // 3
        self.month = (self.day // 20) % len(self.months)
        self.day %= 20
        self.day += 1

    def IsBattleOver(self):
        is_player_char_in_alive_chars = False
        is_enemy_char_in_alive_chars = False

        for p_char in self.player_party.characters:
            if not p_char.dead and p_char in self.battle_characters:
                is_player_char_in_alive_chars = True
        
        for e_char in self.enemy_party.characters:
            if not e_char.dead and e_char in self.battle_characters:
                is_enemy_char_in_alive_chars = True

        if is_player_char_in_alive_chars and not is_enemy_char_in_alive_chars:
            # player party won
            self.battle_over = True
            self.player_party_won = True
        if is_enemy_char_in_alive_chars and not is_player_char_in_alive_chars:
            # enemy party won
            self.battle_over = True
            self.player_party_won = False

        return self.battle_over

    def OnMainMenu(self, delta):
        self.main_menu_timer += delta

        self.Clear(' ', self.from_fg(C.WHITE))

        if self.main_menu_timer >= 3.0:
            y = int(self.TerminalHeight() * 0.4) - len(TITLE['lines']) // 2
            self.DrawText(t := "Press [z] to Start", self.from_fg(C.WHITE), self.TerminalWidth() // 2 - len(t) // 2, int(self.TerminalHeight() * 0.8))
        else:
            y = int(self.TerminalHeight() * 0.4) + len(TITLE['lines']) // 2
            y = int(y * (self.main_menu_timer / 3.0))
            y -= len(TITLE['lines'])

        self.DrawSprite(TITLE, self.background_color, self.TerminalWidth() // 2 - len(TITLE['lines'][0]) // 2, y)

        if self.main_menu_timer > 3.0 and self.KeyPressed(K_z):
            self.main_menu = False
            
        self.DrawRect(self.from_fg(C.WHITE), 0, 0, self.TerminalWidth() - 1, self.TerminalHeight() - 1)

    # Called once per frame
    def OnUpdate(self, delta):
        if self.KeyPressed(K_p):
            self.player_character.GiveItem(random.choice([bronze_sword, small_healing_pot]))
        
        if self.main_menu:
            self.OnMainMenu(delta)
            return True

        if self.character_create:
            self.OnCharacterCreate()
            return True

        if self.battle_animation:
            spr = {
                'lines': [['=' for _ in range(self.TerminalWidth() // 2)] for _ in range(self.TerminalHeight())],
                'colors': [[C.GRAY if (x + y) & 1 else C.WHITE for x in range(self.TerminalWidth() // 2)] for y in range(self.TerminalHeight())]
            }

            if self.b_animation_time <= self.b_animation_length / 3 + 1e-02:
                self.DrawSprite(spr, C.BLACK, int(- self.TerminalWidth() // 2 + self.TerminalWidth() // 2 * self.b_animation_time / (self.b_animation_length / 3)), 0)
                self.DrawSprite(spr, C.BLACK, int(self.TerminalWidth() - self.TerminalWidth() // 2 * self.b_animation_time / (self.b_animation_length / 3)), 0)
            elif self.b_animation_time > self.b_animation_length * ( 2 / 3 ):
                self.Clear(' ', (C.BLACK, self.background_color))

                ## Copied from below, Battle drawing code
                self.FillRect('.', (C.DARK_GRAY, self.background_color), 1, 2, self.TerminalWidth() - 3, self.TerminalHeight() - 11)
                self.DrawRect(self.from_fg(C.WHITE), 1, 1, self.TerminalWidth() - 3, self.TerminalHeight() - 11)

                self.DrawTextLines([
                    "[ ] Attack       [ ] Item",
                    "",
                    "[ ] Magic        [ ] Escape"
                ], self.from_fg(C.WHITE), 3, self.TerminalHeight() - 7)

                # Show the sprites for each character
                self.player_party.draw(self, None, None)
                self.enemy_party.draw(self, None, None)

                self.DrawHLine(self.from_fg(C.WHITE), 0, self.TerminalHeight() - 3, self.TerminalWidth())

                y = self.TerminalHeight() * ((self.b_animation_time - self.b_animation_length * ( 2 / 3 )) / (self.b_animation_length / 3))
                y = int(y)

                self.DrawSprite(spr, C.BLACK, 0, y)
                self.DrawSprite(spr, C.BLACK, self.TerminalWidth() // 2, y)

            self.b_animation_time += delta

            if self.b_animation_time > self.b_animation_length:
                self.battle_animation = False
            return True

        # If we have no dialogue
        if len(self.dialogue) == 0:
            match self.scene_type:
                case SceneType.OVERWORLD:
                    # If the player presses 'z' and we are over a trigger, move to the appropriate map
                    if self.KeyPressed(K_z):
                        for t in self.current_map.triggers:
                            if int(self.overworld_position.x) == t.x and int(self.overworld_position.y) == t.y:
                                self.current_map = t.to_map
                                
                                self.overworld_position.x = t.target_x
                                self.overworld_position.y = t.target_y

                                test_against_dungeon_maps = [d.floors[0] for d in self.dungeons]

                                if self.current_map in test_against_dungeon_maps:
                                    self.current_dungeon = test_against_dungeon_maps.index(self.current_map)

                    if self.KeyPressed(K_i):
                        self.scene_type = SceneType.MENU
                        self.menu = Menu.INVENTORY

                    if self.KeyPressed(K_t):
                        self.action = Action.TALK

                    if self.KeyPressed(K_x) and self.InDungeon():
                        self.dungeons[self.current_dungeon].current_floor = (self.dungeons[self.current_dungeon].current_floor + 1) % self.dungeons[self.current_dungeon]._number_floors
                        self.current_map = self.dungeons[self.current_dungeon].floors[self.dungeons[self.current_dungeon].current_floor]

                    # Map movement code
                    moved = False
                    direction = None

                    if self.KeyPressed(K_LEFT):
                        direction = (-1, 0)
                    elif self.KeyPressed(K_RIGHT):
                        direction = (1, 0)
                    elif self.KeyPressed(K_UP):
                        direction = (0, -1)
                    elif self.KeyPressed(K_DOWN):
                        direction = (0, 1)

                    if direction:
                        match self.action:
                            case None:
                                if self.AllowMove(self.overworld_position.x + direction[0], self.overworld_position.y + direction[1]):
                                    self.overworld_position.x += direction[0]
                                    self.overworld_position.y += direction[1]
                                    moved = True
                            case Action.TALK:
                                print('talk')
                                for npc in self.current_map.npcs:
                                    print(npc.pos_x, npc.pos_y, *self.overworld_position.xy)
                                    if npc.pos_x == int(self.overworld_position.x + direction[0]) and npc.pos_y == int(self.overworld_position.y + direction[1]):
                                        print('npc found')
                                        match npc.type:
                                            case NPCType.MERCHANT:
                                                print('merchant found')
                                                self.scene_type = SceneType.MENU
                                                self.menu = Menu.SHOP
                                                self.merchant = npc
                                        
                        self.action = None

                    # If we move on the overworld, advance time
                    if moved and self.current_map == self.overworld_map:
                        self.OnAdvanceTime()
                    
                    # Tell the dungeon if we moved
                    if moved and self.InDungeon():
                        self.dungeons[self.current_dungeon].OnMove()

                case SceneType.BATTLE:
                    if self.battle_phase == 2:
                        # battle is over
                        if self.player_party_won:
                            # do loot and xp and things

                            # give characters xp
                            for p_char in self.player_party.characters:
                                p_char.GainXP(self.enemy_party)

                            gained_loot = {}

                            # give player party loot
                            for e_char in self.enemy_party.characters:
                                loot = e_char.DropLoot()
                                if loot:
                                    item_count = 0
                                    if loot.name in gained_loot:
                                        item_count = gained_loot[loot.name]

                                    gained_loot.update({ loot.name: item_count + 1 })
                                    self.player_character.GiveItem(loot)
                            
                            money_gained = len(self.enemy_party.characters) * random.randint(1, 3) + random.randint(1, 10)
                            self.dialogue.append(f"Party gained {money_gained}gp!")
                            self.player_character.money += money_gained
                            for k, v in list(gained_loot.items()):
                                self.dialogue.append(f"Party gained {k} x{v}!")

                        self.scene_type = SceneType.OVERWORLD
                        return True
                    
                    if self.battle_characters[self.current_character] in self.player_party.characters:
                        # It is the turn of one of the player's party members

                        # Do different things depending on the 'phase' of the turn
                        match self.battle_phase:
                            case 0: # Select Action
                                if self.KeyPressed(K_RIGHT):
                                    self.menu_selection.x = min(self.menu_selection.x + 1, 1)
                                    self.PlaySound('cursor')
                                if self.KeyPressed(K_LEFT):
                                    self.menu_selection.x = max(self.menu_selection.x - 1, 0)
                                    self.PlaySound('cursor')
                                    
                                if self.KeyPressed(K_DOWN):
                                    self.menu_selection.y = min(self.menu_selection.y + 1, 1)
                                    self.PlaySound('cursor')
                                if self.KeyPressed(K_UP):
                                    self.menu_selection.y = max(self.menu_selection.y - 1, 0)
                                    self.PlaySound('cursor')
                                
                                if self.KeyPressed(K_z):
                                    match (int(self.menu_selection.x), int(self.menu_selection.y)):
                                        case (0, 0): # Attack
                                            self.battle_phase = 1
                                            self.await_type = Await.ATTACK
                                        
                                        case (0, 1): # Item
                                            self.battle_phase = 1
                                            self.await_type = Await.ITEM

                                        case (1, 0): # Magic
                                            self.battle_phase = 1
                                            self.await_type = Await.MAGIC

                                        case (1, 1): # Escape
                                            if roll(6) < self.battle_characters[self.current_character].luck // 2:
                                                self.scene_type = SceneType.OVERWORLD
                                                self.dialogue.append("The party escaped successfully!")
                                            else:
                                                self.dialogue.append("The party failed to escape!")

                            case 1: # Select Targets/Perform Action
                                match self.await_type:
                                    case Await.ATTACK:
                                        if self.KeyPressed(K_RIGHT):
                                            self.menu_selection.x = (self.menu_selection.x + 1) % len(self.enemy_party.characters)
                                            self.PlaySound('cursor')
                                        elif self.KeyPressed(K_LEFT):
                                            self.menu_selection.x -= 1
                                            if self.menu_selection.x < 0: self.menu_selection.x += len(self.enemy_party.characters)
                                            self.PlaySound('cursor')
                                        
                                        # If player presses 'z', attack targeted character
                                        if self.KeyPressed(K_z):
                                            self.battle_characters[self.current_character].attack(self.enemy_party.characters[int(self.menu_selection.x)])

                                            if self.IsBattleOver():
                                                self.battle_phase = 2
                                                self.dialogue.append(f"Your party {['lost', 'won'][self.player_party_won]}!")
                                                
                                                return True

                                            self.OnNextTurn()

                                    # TODO: implement battle items and magic
                                    case Await.ITEM:
                                        pass
                                    case Await.MAGIC:
                                        pass
                                    
                    else:
                        # Otherwise, the enemy attacks a random player party member
                        # TODO: make an actual ai lol
                        self.battle_characters[self.current_character].attack(random.choice(self.player_party.characters))
                        
                        if self.IsBattleOver():
                            self.battle_phase = 2
                            self.dialogue.append(f"Your party {['lost', 'won'][self.player_party_won]}!")
                            
                            return True
                        
                        self.OnNextTurn()

                # TODO: implement menus
                case SceneType.MENU:
                    
                    match self.menu:
                        case Menu.INVENTORY:
                            if self.KeyPressed(K_i):
                                self.scene_type = SceneType.OVERWORLD
                                self.menu_action = None

                            if self.menu_action == None:
                                if self.KeyPressed(K_u):
                                    self.menu_action = MenuAction.USE
                                elif self.KeyPressed(K_d):
                                    self.menu_action = MenuAction.DROP
                            else:
                                keys = [chr(ord('a') + i) for i in range(26)] + [chr(ord('A') + i) for i in range(26)]
                                
                                keys = keys[:len(self.player_character.inventory)]

                                if self.HasTextCache():
                                    k = self.TextCache()

                                    print(k)

                                    if k in keys:
                                        item = list(self.player_character.inventory.keys())[keys.index(k)]
                                        print(item)
                                        if self.menu_action == MenuAction.USE:
                                            if ITEM_DICTIONARY[item].use(self):
                                                self.player_character.inventory[item] -= 1
                                                if self.player_character.inventory[item] <= 0:
                                                    self.player_character.inventory.pop(item)
                                                self.dialogue.append(f"Used the {item}")
                                        else:
                                            self.player_character.inventory[item] -= 1
                                            if self.player_character.inventory[item] <= 0:
                                                self.player_character.inventory.pop(item)
                                            self.dialogue.append(f"Dropped the {item}")
                                        
                                        self.menu_action = None
                        case Menu.SHOP:
                            if self.KeyPressed(K_z):
                                self.scene_type = SceneType.OVERWORLD
                                self.menu_action = None

                            if self.menu_action == MenuAction.BUY:
                                pass
                            else:
                                pass           
                        case _:
                            print("unimplemented menu update")
        else:
            # Otherwise, if player presses 'z', remove first element
            # Advances dialogue
            if self.KeyPressed(K_z):
                self.dialogue.pop(0)

        return True

    # Showing the stuff!
    def OnDraw(self):
        if self.battle_animation or self.character_create:
            return
        
        self.Clear(' ', (self.background_color, self.background_color))

        # If we have dialogue, show it
        if len(self.dialogue) > 0:
            # These following a million lines are for splitting the dialogue at word boundaries
            # To do automatic line-wrapping
            
            d = self.dialogue[0] + ("" if len(self.dialogue) == 1 else " [more]")

            words = d.split(' ')

            line_1 = ""
            line_2 = ""

            l = 0

            for w in words:
                if l + len(w) < self.TerminalWidth():
                    line_1 += w + " "
                    l += len(w) + 1
                else:
                    line_2 += w + " "
                    l += len(w) + 1

            # Show the dialogue
            self.DrawText(line_1, self.from_fg(C.WHITE), 1, self.TerminalHeight() - 2)
            self.DrawText(line_2, self.from_fg(C.WHITE), 1, self.TerminalHeight() - 1)

        # Change which thing is shown as 'selected' and the color based on battle phase and other things
        selected = selected_color = None

        match self.scene_type:
            # Draw the overworld
            case SceneType.OVERWORLD:
                # UI
                self.DrawHLine(self.from_fg(C.WHITE), 0, self.TerminalHeight() - 3, self.TerminalWidth())

                if not self.InDungeon():
                    self.DrawRect(self.from_fg(C.WHITE), 1, 1, self.TerminalWidth() - 3, self.TerminalHeight() - 6)

                    # Display the in-game date
                    self.DrawText(t := f"{self.day}{['st', 'nd', 'rd'][self.day - 1] if 0 < self.day <= 3 else 'th'} of {self.months[self.month]}, 1004ne", self.from_fg(C.WHITE), self.TerminalWidth() - 1 - len(t), 0)
                
                # Draw the current map
                self.current_map.draw()

                # Following chunk of code is for displaying to the player what they are standing on
                descriptions = {
                    '"': 'Plains',
                    't': 'Forest',
                    '#': 'Beach',
                    '^': 'Mountains'
                }
                tile_descriptor = self.CharAt(int(self.overworld_position.x + 2), int(self.overworld_position.y + 2)).symbol

                if tile_descriptor in descriptions:
                    self.DrawText(t := descriptions[tile_descriptor], self.from_fg(C.WHITE), self.TerminalWidth() - 1 - len(t), self.TerminalHeight() - 4)
                else:
                    trigger_positions = [(t.x, t.y) for t in self.current_map.triggers]
                    overworld_pos = (int(self.overworld_position.x), int(self.overworld_position.y))
                    
                    if overworld_pos in trigger_positions:
                        self.DrawText(t := "To: " + self.current_map.triggers[trigger_positions.index(overworld_pos)].to_map.name, self.from_fg(C.WHITE), self.TerminalWidth() - 1 - len(t), self.TerminalHeight() - 4)

                # Draw the player as an '@'
                if self.InDungeon():
                    self.DrawChar('@', (PLAYER_CLASS_COLORS[self.player_party.characters[0].char_class], self.background_color), int(self.overworld_position.x), int(self.overworld_position.y))
                else:
                    self.DrawChar('@', (PLAYER_CLASS_COLORS[self.player_party.characters[0].char_class], self.background_color), int(self.overworld_position.x + 2), int(self.overworld_position.y + 2))

            # Draw battles
            case SceneType.BATTLE:
                self.FillRect('.', (C.DARK_GRAY, self.background_color), 1, 2, self.TerminalWidth() - 3, self.TerminalHeight() - 11)
                self.DrawRect(self.from_fg(C.WHITE), 1, 1, self.TerminalWidth() - 3, self.TerminalHeight() - 11)

                self.DrawTextLines([
                    "[ ] Attack       [ ] Item",
                    "",
                    "[ ] Magic        [ ] Escape"
                ], self.from_fg(C.WHITE), 3, self.TerminalHeight() - 7)

                if self.battle_phase == 0:
                    self.DrawChar('*', self.from_fg(C.WHITE), 4 + 17 * int(self.menu_selection.x), self.TerminalHeight() - 7 + 2 * int(self.menu_selection.y))
                    selected = self.battle_characters[self.current_character]
                    selected_color = C.GREEN
                elif self.battle_phase == 1 and self.await_type == Await.ATTACK:
                    selected = self.enemy_party.characters[int(self.menu_selection.x)]
                    selected_color = C.YELLOW

                if self.battle_characters[self.current_character] in self.player_party.characters:
                    self.DrawText(
                        f"{self.battle_characters[self.current_character].hp} / {self.battle_characters[self.current_character].max_hp} HP     {self.battle_characters[self.current_character].mp} / {self.battle_characters[self.current_character].max_mp} MP",
                        self.from_fg(C.WHITE),
                        2 , self.TerminalHeight() - 9
                    )

                # Show the sprites for each character
                self.player_party.draw(self, selected, selected_color)
                self.enemy_party.draw(self, selected, selected_color)

                self.DrawHLine(self.from_fg(C.WHITE), 0, self.TerminalHeight() - 3, self.TerminalWidth())

            # TODO: implement other menus
            case SceneType.MENU:
                self.DrawHLine(self.from_fg(C.WHITE), 0, self.TerminalHeight() - 3, self.TerminalWidth())
                match self.menu:
                    case Menu.INVENTORY:
                        keys = [chr(ord('a') + i) for i in range(26)] + [chr(ord('A') + i) for i in range(26)]
                        
                        self.DrawText("Inventory " + ("(Choose Action)" if self.menu_action == None else "(Choose Item)"), self.from_fg(C.WHITE), 1, 1)
                        self.DrawText("[u] Use   [d] Drop  [i] Close Inventory", self.from_fg(C.WHITE), 1, 2)
                        
                        y = 4
                        for item in self.player_character.inventory:
                            self.DrawText(f"[{keys.pop(0)}] {item} x{self.player_character.inventory[item]}", self.from_fg(C.WHITE), 1, y)
                            y += 1
                    case Menu.SHOP:
                        keys = [chr(ord('a') + i) for i in range(26)] + [chr(ord('A') + i) for i in range(26)]
                        
                        self.DrawText("Shop " + ("(Choose Action)" if self.menu_action == None else "(Choose Item)"), self.from_fg(C.WHITE), 1, 1)
                        self.DrawText("[b] Buy   [s] Sell  [z] Close Shop", self.from_fg(C.WHITE), 1, 2)
                        self.DrawText("Party Items", self.from_fg(C.WHITE), 1, 4)
                        tposx = self.TerminalWidth() // 2 + 1
                        self.DrawText("Merchant Items", self.from_fg(C.WHITE), tposx, 4)

                        self.DrawText(f"Party Gold: {self.player_character.money}", self.from_fg(C.WHITE), 1, self.TerminalHeight() - 4)
                        self.DrawText(f"Merchant Gold: {self.merchant.money}", self.from_fg(C.WHITE), tposx, self.TerminalHeight() - 4)

                        y = 6
                        for item in self.player_character.inventory:
                            self.DrawText(f"[{keys.pop(0)}] {item} x{self.player_character.inventory[item]} ({ITEM_DICTIONARY[item].price}gp)", self.from_fg(C.WHITE), 1, y)
                            y += 1

                        y = 6
                        for item in self.merchant.inventory:
                            self.DrawText(f"[{keys.pop(0)}] {item} x{self.merchant.inventory[item]} ({ITEM_DICTIONARY[item].price}gp)", self.from_fg(C.WHITE), tposx, y)
                            y += 1
                    case _:
                        print("unimplemented menu draw")
            
            # Error
            case _:
                self.DrawText("unimplemented SceneType draw", (C.RED, self.background_color), 0, 0)

# Initialize and call 'start' on Game object
game = Game()
game.start()