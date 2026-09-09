from constants import MAX_WALLS

class Player:
    def __init__(self, pos, color, ai_controlled=False):
        self.pos = pos
        self.color = color
        self.walls = MAX_WALLS
        self.ai_controlled = ai_controlled