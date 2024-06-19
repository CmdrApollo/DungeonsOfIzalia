class Map:
    def __init__(self, name, sprite, triggers, game):
        self.name = name
        self.sprite = sprite
        self.triggers = triggers
        self.game = game
    
    def draw(self):
        # Show the sprite map and the name of the map
        if self.game.InDungeon():
            self.game.DrawSprite(self.sprite, self.game.background_color, 0, 0)
        else:
            self.game.DrawSprite(self.sprite, self.game.background_color, 2, 2)
            self.game.DrawText(self.name, (self.game.Color.WHITE, self.game.background_color), 1, 0)