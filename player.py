from constants import MAX_WALLS

class Player:
    def __init__(self, pos, color, ai_controlled=False):
        self._pos = pos
        self.color = color
        self._walls = MAX_WALLS
        self.ai_controlled = ai_controlled
        self.listeners = {}

    def subscribe(self, props, callback):
        self.listeners[props] = callback

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = value

        callback = self.listeners["pos"]
        callback(self)

    @property
    def walls(self):
        return self._walls

    @walls.setter
    def walls(self, value):
        self._walls = value

        callback = self.listeners["walls"]
        callback()
    