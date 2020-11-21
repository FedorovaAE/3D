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
        self.model, self.texture = 'textures/custom_cube', 'textures/rubik_texture'
        self.load_game()

    def load_game(self):
        self.parent = Entity(madel='textures/custom_cube', texture='textures/parent')
        self.cube = Entity(parent=self.parent, model=self.model, texture=self.texture, position=(-1, 1, 1))
        self.rot = 0

    def input(self, key):
        if key == 'mouse1':
            self.rot += 90
            self.parent.animate_rotation_x(self.rot, duration=0.5)
        super().input(key)


if __name__ == '__main__':
    game = Game()
    game.run()
