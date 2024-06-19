from pyne.pyne import *

import random

C = PyneEngine.Color

color = (C.WHITE, C.BLACK)

blocks = [
    [
        [
            "....",
            ".##.",
            ".##.",
            "...."
        ]
    ],
    [
        [
            "....",
            ".##.",
            "..##",
            "...."
        ],
        [
            "....",
            "..#.",
            ".##.",
            ".#.."
        ]
    ],
    [
        [
            "....",
            "..##",
            ".##.",
            "...."
        ],
        [
            "....",
            ".#..",
            ".##.",
            "..#."
        ]
    ],
    [
        [
            "..#.",
            "..#.",
            "..#.",
            "..#."
        ],
        [
            "....",
            "....",
            "####",
            "...."
        ]
    ]
]

class Tetris(PyneEngine):
    def OnConstruct(self):
        self.board_w, self.board_h = 10, 20
        self.board = [[False for _ in range(self.board_w)] for _ in range(self.board_h)]
        self.current_block = random.choice(blocks)
        self.next_block = random.choice(blocks)

        self.block_pos_x = 3
        self.block_pos_y = 0

        self.block_rotation = 0

        self.tick_timer = 0
        return True
    
    def OnUpdate(self, delta):
        self.tick_timer += delta

        if self.KeyPressed(K_x):
            self.block_rotation = (self.block_rotation + 1) % len(self.current_block)

            for y in range(4):
                for x in range(4):
                    if self.current_block[self.block_rotation][y][x] == '#' and self.board[self.block_pos_y + y][self.block_pos_x + x]:
                        self.block_rotation -= 1
                        if self.block_rotation < 0:
                            self.block_rotation += len(self.current_block)
        elif self.KeyPressed(K_z):
            self.block_rotation -= 1
            if self.block_rotation < 0:
                self.block_rotation += len(self.current_block)

            for y in range(4):
                for x in range(4):
                    if self.current_block[self.block_rotation][y][x] == '#' and self.board[self.block_pos_y + y][self.block_pos_x + x]:
                        self.block_rotation = (self.block_rotation + 1) % len(self.current_block)
            
        if self.KeyPressed(K_LEFT):
            self.block_pos_x -= 1

            for y in range(4):
                for x in range(4):
                    if self.current_block[self.block_rotation][y][x] == '#' and (self.block_pos_x + x < 0 or self.board[self.block_pos_y + y][self.block_pos_x + x]):
                        self.block_pos_x += 1
                        break
            
        if self.KeyPressed(K_RIGHT):
            self.block_pos_x += 1

            for y in range(4):
                for x in range(4):
                    if self.current_block[self.block_rotation][y][x] == '#' and (self.block_pos_x + x >= self.board_w or self.board[self.block_pos_y + y][self.block_pos_x + x]):
                        self.block_pos_x -= 1
                        break
        
        if self.tick_timer > 1 / 4 or self.KeyPressed(K_DOWN):
            self.tick_timer -= 1 / 4
            self.block_pos_y += 1

            for j in range(4):
                y = 3 - j

                for x in range(4):
                    if self.current_block[self.block_rotation][y][x] == '#':
                        if self.block_pos_y + y == self.board_h or self.board[self.block_pos_y + y][self.block_pos_x + x]:
                            self.block_pos_y -= 1
                            for w in range(4):
                                for h in range(4):
                                    if self.current_block[self.block_rotation][h][w] == '#':
                                        self.board[self.block_pos_y + h][self.block_pos_x + w] = True
                            
                            self.current_block = self.next_block
                            self.next_block = random.choice(blocks)
                            self.block_pos_x = 3
                            self.block_pos_y = 0
                            self.block_rotation = 0

            print('tick')

        return True
    
    def DrawBlock(self, x, y):
        self.DrawChar('[', color, x * 2, y)
        self.DrawChar(']', color, x * 2 + 1, y)

    def OnDraw(self):
        self.Clear(' ', color)

        for j in range(self.board_h):
            for i in range(self.board_w):
                x = i + 1
                y = j + 1

                if self.board[j][i]:
                    self.DrawBlock(x, y)
                else:
                    self.DrawChar('.', color, x * 2, y)
                    self.DrawChar('.', color, x * 2 + 1, y)
                
        for i in range(4):
            for j in range(4):
                if self.current_block[self.block_rotation][j][i] == '#':
                    self.DrawBlock(self.block_pos_x + i + 1, self.block_pos_y + j + 1)

tetris = Tetris()
tetris.start()