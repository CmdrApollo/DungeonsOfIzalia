class Trigger:
    def __init__(self, to_map, x, y, target_x, target_y):
        self.to_map = to_map
        self.x = x
        self.y = y
        
        self.target_x, self.target_y = target_x, target_y