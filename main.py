from ursina import *
from ursina import camera


class Game(Ursina):
    def __init__(self):
        super().__init__()
        window.full_screen = True
        Entity(model='quad', scale=60, texture='white_cube', texture_scale=(60, 60), rotation_x=90, y=-5,
               color=color.light_gray)
        Entity(model='sphere', scale=100, texture='textures/1', double_sided=True)
        EditorCamera()
        camera.world_position = (0, 0, -15)
        self.load_game()

    def load_game(self):
        pass

    def input(self, key):
        super().input(key)


if __name__ == '__main__':
    game = Game()
    game.run()
