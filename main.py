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
        camera.world_position = (0, 0, -25)
        self.model, self.texture = 'textures/custom_cube', 'textures/rubik_texture'
        self.turn1 = 5
        self.animation_time = 0.5
        self.action_trigger = True
        self.load_game()

    def load_game(self):
        self.create_cube_positions()
        self.CUBES = [Entity(model=self.model, texture=self.texture, position=pos) for pos in self.SIDE_POSITIONS]
        self.PARENT = Entity()
        if self.turn1 == 3:
            self.rotation_axes = {'LEFT': 'x', 'RIGHT': 'x', 'TOP': 'y', 'BOTTOM': 'y', 'FACE': 'z', 'BACK': 'z'}
            self.cubes_side_positons = {'LEFT': self.LEFT, 'BOTTOM': self.BOTTOM, 'RIGHT': self.RIGHT,
                                        'FACE': self.FACE, 'BACK': self.BACK, 'TOP': self.TOP}
        else:
            self.rotation_axes = {'LEFT': 'x', 'RIGHT': 'x', 'TOP': 'y', 'BOTTOM': 'y', 'FACE': 'z', 'BACK': 'z',
                                  'LEFT1': 'x', 'RIGHT1': 'x', 'TOP1': 'y', 'BOTTOM1': 'y', 'FACE1': 'z', 'BACK1': 'z'}
            self.cubes_side_positons = {'LEFT': self.LEFT, 'BOTTOM': self.BOTTOM, 'RIGHT': self.RIGHT,
                                        'FACE': self.FACE,
                                        'BACK': self.BACK, 'TOP': self.TOP,
                                        'LEFT1': self.LEFT1, 'BOTTOM1': self.BOTTOM1,
                                        'RIGHT1': self.RIGHT1, 'TOP1': self.TOP1, 'FACE1': self.FACE1,
                                        'BACK1': self.BACK1}

    def toggle_animation_trigger(self):
        self.action_trigger = not self.action_trigger

    def rotate_side(self, side_name):
        self.action_trigger = False
        cube_positions = self.cubes_side_positons[side_name]
        rotation_axis = self.rotation_axes[side_name]
        self.reparent_to_scene()
        for cube in self.CUBES:
            if cube.position in cube_positions:
                cube.parent = self.PARENT
                eval(f'self.PARENT.animate_rotation_{rotation_axis}(90, duration=self.animation_time)')
        invoke(self.toggle_animation_trigger, delay=self.animation_time + 0.11)

    def reparent_to_scene(self):
        for cube in self.CUBES:
            if cube.parent == self.PARENT:
                world_pos, world_rot = round(cube.world_position, 1), cube.world_rotation
                cube.parent = scene
                cube.position, cube.rotation = world_pos, world_rot
        self.PARENT.rotation = 0

    def create_cube_positions(self):
        if self.turn1 == 3:
            self.LEFT = {Vec3(-1, y, z) for y in range(-1, 2) for z in range(-1, 2)}
            self.BOTTOM = {Vec3(x, -1, z) for x in range(-1, 2) for z in range(-1, 2)}
            self.FACE = {Vec3(x, y, -1) for x in range(-1, 2) for y in range(-1, 2)}
            self.BACK = {Vec3(x, y, 1) for x in range(-1, 2) for y in range(-1, 2)}
            self.RIGHT = {Vec3(1, y, z) for y in range(-1, 2) for z in range(-1, 2)}
            self.TOP = {Vec3(x, 1, z) for x in range(-1, 2) for z in range(-1, 2)}
            self.SIDE_POSITIONS = self.LEFT | self.BOTTOM | self.FACE | self.BACK | self.RIGHT | self.TOP
        else:
            self.LEFT1 = {Vec3(-1, y, z) for y in range(-2, 3) for z in range(-2, 3)}
            self.BOTTOM1 = {Vec3(x, -1, z) for x in range(-2, 3) for z in range(-2, 3)}
            self.RIGHT1 = {Vec3(1, y, z) for y in range(-2, 3) for z in range(-2, 3)}
            self.TOP1 = {Vec3(x, 1, z) for x in range(-2, 3) for z in range(-2, 3)}
            self.FACE1 = {Vec3(x, y, -1) for x in range(-2, 3) for y in range(-2, 3)}
            self.BACK1 = {Vec3(x, y, 1) for x in range(-2, 3) for y in range(-2, 3)}
            self.LEFT = {Vec3(-2, y, z) for y in range(-2, 3) for z in range(-2, 3)}
            self.BOTTOM = {Vec3(x, -2, z) for x in range(-2, 3) for z in range(-2, 3)}
            self.FACE = {Vec3(x, y, -2) for x in range(-2, 3) for y in range(-2, 3)}
            self.BACK = {Vec3(x, y, 2) for x in range(-2, 3) for y in range(-2, 3)}
            self.RIGHT = {Vec3(2, y, z) for y in range(-2, 3) for z in range(-2, 3)}
            self.TOP = {Vec3(x, 2, z) for x in range(-2, 3) for z in range(-2, 3)}
            self.SIDE_POSITIONS = self.LEFT | self.BOTTOM | self.FACE | self.BACK | self.RIGHT | self.TOP | \
                                  self.LEFT1 | self.BOTTOM1 | self.RIGHT1 | self.TOP1 | self.FACE1 | self.BACK1

    def input(self, key):
        if self.turn1 == 3:
            keys = dict(zip('asdzxcewqr', 'LEFT BOTTOM RIGHT TOP FACE BACK'.split()))
        else:
            keys = dict(
                zip('qwerasdfzxcv', 'LEFT BOTTOM RIGHT TOP FACE BACK LEFT1 BOTTOM1 RIGHT1 TOP1 FACE1 BACK1'.split()))
        if key in keys:
            if self.action_trigger:
                self.rotate_side(keys[key])
        super().input(key)


if __name__ == '__main__':
    game = Game()
    game.run()
