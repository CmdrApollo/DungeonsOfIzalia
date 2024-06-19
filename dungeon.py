from pyne.pyne import *
from maps import *
from utils import *
from character import *
from _types import *
from trigger import *

class Room:
    def __init__(self, x, y, w, h, ox, oy, rtype):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.ox = ox
        self.oy = oy

        self.connections = [False]*4

        self.type = rtype

class Dungeon:
    def __init__(self, x, y, difficulty, region, game):
        """
        Dungeon difficulty is a number between 0 and 1, 0 being easiest, 1 being hardest.
        Region defines the enemies found within.
        """

        self.game = game

        self.name = "Test Dungeon"

        self.difficulty = difficulty
        self.region = region

        self._number_rooms_per_floor = 5 + int( 5 * difficulty )
        self._number_floors = 2 + round( difficulty * 3 )
        self._encounters_per_floor = 3 + int( 4 * difficulty )
        self.current_encounters = self._encounters_per_floor

        self.exit_point_x = 10
        self.exit_point_y = 10

        self.floors = [Map(self.name, None, [Trigger(self.game.overworld_map, self.exit_point_x, self.exit_point_y, x, y)] if i == 0 else [], game) for i in range(self._number_floors)]
        self.current_floor = 0

        self.x = x
        self.y = y

        self.GenerateDungeon()
    
    def GenerateDungeon(self):
        tw = self.game.TerminalWidth()
        th = 25 #self.game.TerminalHeight()

        for i in range(self._number_floors):
            sprite = {
                'lines' : [[' ' for _ in range(tw)] for _ in range(th)],
                'colors': [[C.BLACK for _ in range(tw)] for _ in range(th)]
            }

            spr = [ScrElement(' ', C.WHITE, self.game.background_color) for _ in range(tw * th)]

            n_rooms = self._number_rooms_per_floor + random.randint(-1, 1)
            
            room_types = [
                RoomType.ENTER, RoomType.EXIT, RoomType.MINIBOSS
            ] + [ self.RandomRoom() for _ in range(n_rooms - 3)]

            visited = []

            rooms = []

            n_current_rooms = 0
            # Add a random offset to the number of rooms on each floor
            while n_current_rooms < n_rooms:
                w = random.randint(6, 15)
                h = random.randint(4, 5)

                if n_current_rooms == 0:
                    ri = random.randint(0, 11)
                else:
                    o = random.choice([-4, 4, 1, -1])
                    tx, ty = (ri + o) % 4, (ri + o) // 4

                    if ri + o < 0 or ri + o > 11 or (tx != ri % 4 and ty != ri // 4) or random.random() <= 0.2:
                        continue
                    else:
                        ri += o

                        if ri < 0:
                            ri += 12
                        ri %= 12

                        if ri in visited:
                            continue
                        else:
                            visited.append(ri)

                p = (ri % 4, ri // 4)

                x = p[0] * (tw // 4) + (tw // 8) - w // 2
                y = p[1] * (th // 3) + (th // 6) - h // 2

                # Rooms are stored as rectangles [x, y, w, h]
                rooms.append(Room(x, y, w, h, p[0], p[1], room_types.pop(random.randint(0, len(room_types) - 1))))
                n_current_rooms += 1
            
            for room in rooms:
                self.game.FillRect('.', (C.DARK_GRAY, self.game.background_color), room.x, room.y, room.w, room.h, scr=spr)

                char, col = '@', C.MAGENTA

                match room.type:
                    case RoomType.EXIT:
                        col = C.DARK_MAGENTA
                    case RoomType.REGULAR:
                        col = C.WHITE
                    case RoomType.SHOP:
                        col = C.CYAN
                    case RoomType.TREASURE:
                        col = C.YELLOW
                    case RoomType.MINIBOSS:
                        col = C.RED
                    case RoomType.BOSS:
                        col = C.DARK_RED
                
                self.game.DrawChar(char, (col, C.BLACK), room.x + 1, room.y + 1, scr=spr)

                dirs = [(0, -1), (1, 0), (0, 1), (-1, 0)]
                for n in range(len(dirs)):
                    o = self.HasNeighbor(room, rooms, dirs[n])
                    if o:
                        room.connections[n] = True
                        o.connections[ (n + 2) % 4 ] = True
            
            for room in rooms:
                for n in range(4):
                    if room.connections[n]:
                        match n:
                            case 0: # North
                                self.game.DrawVLine((C.DARK_GRAY, self.game.background_color), room.x + room.w // 2, room.y + room.h // 2 - th // 4, room.y + room.h // w, char='.', scr=spr)
                            case 1: # East
                                self.game.DrawHLine((C.DARK_GRAY, self.game.background_color), room.x + room.w // 2, room.y + room.h // 2, room.x + room.w // 2 + tw // 4, char='.', scr=spr)
                            case 2: # South
                                self.game.DrawVLine((C.DARK_GRAY, self.game.background_color), room.x + room.w // 2, room.y + room.h // 2, room.y + room.h // w + th // 4, char='.', scr=spr)
                            case 3: # West
                                self.game.DrawHLine((C.DARK_GRAY, self.game.background_color), room.x + room.w // 2 - tw // 4, room.y + room.h // 2, room.x + room.w // 2, char='.', scr=spr)

            for room in rooms:
                if room.type == RoomType.ENTER:
                    self.game.DrawChar('<', (C.GRAY, self.game.background_color), room.x + random.randint(1, room.w - 2), room.y + random.randint(1, room.h - 2), scr=spr)
                elif room.type == RoomType.EXIT:
                    self.game.DrawChar('>', (C.GRAY, self.game.background_color), room.x + random.randint(1, room.w - 2), room.y + random.randint(1, room.h - 2), scr=spr)


            for y in range(1, th - 1):
                for x in range(1, tw - 1):
                    dirs = [(0, -1), (0, 1), (1, 0), (-1, 0), (1, -1), (1, 1), (-1, -1), (-1, 1)]

                    for n in range(8):
                        nx = x + dirs[n][0]
                        ny = y + dirs[n][1]
                        if spr[ny * tw + nx].symbol == ' ' and spr[y * tw + x].symbol == '.':
                            self.game.DrawChar('#', (C.GRAY, self.game.background_color), nx, ny, scr=spr)

            for y in range(th):
                for x in range(tw):
                    c = spr[y * tw + x]
                    sprite['lines'][y][x] = c.symbol
                    sprite['colors'][y][x] = c.fg

            self.floors[i].sprite = sprite
    
    def RandomRoom(self):
        r = random.random()

        if r <= 0.7:
            return RoomType.REGULAR
        if r <= 0.9:
            return RoomType.SHOP
        
        return RoomType.TREASURE

    def HasNeighbor(self, room, rooms, direction):
        for r in rooms:
            if r != room:
                if room.ox + direction[0] == r.ox and room.oy + direction[1] == r.oy:
                    return r
        return None

    def OnMove(self):
        if self.current_encounters > 0:
            player = self.game.player_party.characters[0] # MC

            if random.random() ** 2 >= player.luck / 10:
                # Encounter!

                # Hit the music!
                self.game.PlaySong('battle_start', 0)
                self.game.GetAudioHandler()._music_channel.queue(self.game.GetAudioHandler().sounds['battle_theme'])

                self.current_encounters -= 1
                
                ## Construct Enemy Party

                self.game.enemy_party.characters = [
                    Character("Goblin", Race.GOBLIN, Class.FIGHTER, self.game) for _ in range(1)#random.randint(1, 2))
                ]

                ## Start the battle
                
                self.game.OnBattleStart()