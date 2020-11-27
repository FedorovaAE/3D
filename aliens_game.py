from ursina import *
from ursina import camera
from game_obj import *


class GameAliens(Ursina):
    def __init__(self):
        super().__init__()
        window.color = color.black
        Light(type='ambient', color=(0.5, 0.5, 0.5, 1))
        Light(type='directional', color=(0.5, 0.5, 0.5, 1), direction=(1, 1, 1))
        self.MAP_SIZE = 20
        self.new_game()
        camera.position = (self.MAP_SIZE // 2, -20.5, -20)
        camera.rotation_x = -57

    def create_map(self, map_size):
        Entity(model='quad', scale=map_size, position=(map_size // 2, map_size // 2, 0), color=color.violet)
        Entity(model=Grid(map_size, map_size), scale=map_size, position=(map_size // 2, map_size // 2, -0.01),
               color=color.white)

    def new_game(self):
        scene.clear()
        self.create_map(self.MAP_SIZE)
        self.fruit = Fruit(self.MAP_SIZE, model='sphere', color=color.red)


game = GameAliens()
game.run()
