from pyne.pyne import *
from pyne.character import ScrElement
import sys
import json
from tkinter.filedialog import askopenfilename

C = PyneEngine.Color

class Editor(PyneEngine):
    def DrawSprite(self, sprite, bg, x, y):
        for j in range(len(sprite['lines'])):
            for i in range(len(sprite['lines'][j])):
                if sprite['lines'][j][i] != " ":
                    self.DrawChar(sprite['lines'][j][i], (sprite['colors'][j][i], bg), x + i, y + j)
    
    def OnConstruct(self):
        self.sprite = [ [ScrElement('.', C.WHITE, C.BLACK) for _ in range(self.TerminalWidth())] for _ in range(self.TerminalHeight())]

        self.selected = pygame.Rect(-1, -1, 0, 0)

        self.color_key = {
            K_1: C.RED,
            K_2: C.YELLOW,
            K_3: C.GREEN,
            K_4: C.CYAN,
            K_5: C.BLUE,
            K_6: C.MAGENTA,
            K_7: C.ORANGE,
            K_8: C.WHITE,
            K_q: C.DARK_RED,
            K_w: C.DARK_YELLOW,
            K_e: C.DARK_GREEN,
            K_r: C.DARK_CYAN,
            K_t: C.DARK_BLUE,
            K_y: C.DARK_MAGENTA,
            K_u: C.BROWN,
            K_i: C.GRAY,
            K_j: C.DARK_BROWN,
            K_k: C.DARK_GRAY
        }

        self.color = C.WHITE
    
    def OnUpdate(self, delta):
        if self.MousePressed(LMB):
            self.selected.x, self.selected.y = self.MousePos()
        
        if self.MouseHeld(LMB):
            mx, my = self.MousePos()
            self.selected.w, self.selected.h = max(0, mx - self.selected.x) + 1, max(0, my - self.selected.y) + 1

        if self.HasTextCache():
            for x in range(self.selected.w):
                for y in range(self.selected.h):
                    self.sprite[y + self.selected.y][x + self.selected.x].symbol = self.TextCache()
                    self.sprite[y + self.selected.y][x + self.selected.x].fg = self.color
        
        for k in self.color_key:
            if self.KeyPressed(k) and (pygame.key.get_pressed()[K_LALT] or pygame.key.get_pressed()[K_RALT]):
                self.color = self.color_key[k]

                for x in range(self.selected.w):
                    for y in range(self.selected.h):
                        self.sprite[y + self.selected.y][x + self.selected.x].fg = self.color

        if pygame.key.get_pressed()[K_LCTRL] or pygame.key.get_pressed()[K_RCTRL]:
            if self.KeyPressed(K_s):
                lines = ["" for _ in range(len(self.sprite))]

                colors = [None for _ in range(len(self.sprite))]

                for i in range(len(self.sprite)):
                    lines[i] = "".join([c.symbol for c in self.sprite[i]])
                    colors[i] = tuple([c.fg for c in self.sprite[i]])

                json.dump({
                    "lines": lines,
                    "colors": colors
                }, open(askopenfilename(), 'w', encoding='utf-8'), indent = '\t')
            elif self.KeyPressed(K_l):
                data = json.load(open(askopenfilename(), 'r', encoding='utf-8'))

                for x in range(self.TerminalWidth()):
                    for y in range(self.TerminalHeight()):
                        symbol = data['lines'][y][x]
                        fg = data['colors'][y][x]

                        self.sprite[y][x].symbol = symbol
                        self.sprite[y][x].fg = fg

        return True
    
    def OnDraw(self):
        for x in range(self.TerminalWidth()):
            for y in range(self.TerminalHeight()):
                self.DrawChar(self.sprite[y][x].symbol, (self.sprite[y][x].fg, C.DARK_GRAY if self.selected.collidepoint(x, y) else C.BLACK), x, y)

        mx, my = self.MousePos()
        self.DrawText(f"{int(mx)},{int(my)}", (C.WHITE, C.BLACK), 0, 0)

editor = Editor(int(sys.argv[1]), int(sys.argv[2]))
editor.start()