

class Pair:
    def __init__(self, x,y,h):
        self.x = x
        self.y = y
        self.h = h

    def __str__(self):
        return f'Position potential (h={self.h} x={self.x},y={self.y})'