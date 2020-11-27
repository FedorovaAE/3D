from ursina import *
from random import randrange


class Fruit(Entity):
    def __init__(self, map_size, **kwargs):
        super().__init__(**kwargs)
        self.MAP_SIZE = map_size
        self.new_position()

    def new_position(self):
        self.position = (randrange(self.MAP_SIZE) + 0.5, randrange(self.MAP_SIZE) + 0.5, -0.5)
