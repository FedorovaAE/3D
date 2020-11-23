from ursina import *
from ursina import camera, mouse


class Game(Ursina):
    def __init__(self):
        super().__init__()
        window.full_screen = True
        Entity(model='quad', scale=60, texture='white_cube', texture_scale=(60, 60), rotation_x=90, y=-5,
               color=color.violet)
        Entity(model='sphere', scale=100, texture='textures/1', double_sided=True)
        EditorCamera()
        camera.world_position = (0, 0, -25)
        self.model, self.texture = 'textures/custom_cube', 'textures/rubik_texture'
        self.action_trigger = True
        self.action_mode = True
        self.massage = Text(origin=(0, 19), color=color.white)
        # self.count_side = 3
        self.load_game()

    def load_game(self):
        self.create_cube_positions()
        self.CUBES = [Entity(model=self.model, texture=self.texture, position=pos) for pos in self.SIDE_POSITIONS]
        self.PARENT = Entity()
        self.rotation_axes = {'LEFT': 'x', 'RIGHT': 'x', 'TOP': 'y', 'BOTTOM': 'y', 'FACE': 'z', 'BACK': 'z'}
        self.cubes_side_positions = {'LEFT': self.LEFT, 'BOTTOM': self.BOTTOM, 'RIGHT': self.RIGHT,
                                     'FACE': self.FACE, 'BACK': self.BACK, 'TOP': self.TOP}
        self.animation_time = 0.5
        self.toggle_game_mode()
        self.create_sensors()
        self.random_state(rotations=3)

    def random_state(self, rotations=3):
        [self.rotate_side_without_animation(random.choice(list(self.rotation_axes))) for i in range(rotations)]

    def rotate_side_without_animation(self, side_name):
        cube_positions = self.cubes_side_positions[side_name]
        rotation_axis = self.rotation_axes[side_name]
        self.reparent_to_scene()
        for cube in self.CUBES:
            if cube.position in cube_positions:
                cube.parent = self.PARENT
                exec(f'self.PARENT.rotation_{rotation_axis} = 90')

    def create_sensors(self):
        self.LEFT_sensor = self.create_sensor('LEFT', (-0.99, 0, 0), (1.01, 3.01, 3.01))
        self.FACE_sensor = self.create_sensor('FACE', (0, 0, -0.99), (3.01, 3.01, 1.01))
        self.BACK_sensor = self.create_sensor('BACK', (0, 0, 0.99), (3.01, 3.01, 1.01))
        self.RIGHT_sensor = self.create_sensor('RIGHT', (0.99, 0, 0), (1.01, 3.01, 3.01))
        self.TOP_sensor = self.create_sensor('TOP', (0, 1, 0), (3.01, 1.01, 3.01))
        self.BOTTOM_sensor = self.create_sensor('BOTTOM', (0, -1, 0), (3.01, 1.01, 3.01))

    def create_sensor(self, name, pos, scale):
        return Entity(name=name, position=pos, model='cube', color=color.dark_gray, scale=scale, collider='box',
                      visible=False)

    def toggle_game_mode(self):
        self.action_mode = not self.action_mode
        msg = dedent(f"{'Крутите кубик ' if self.action_mode else 'Режим просмотра '}"
                     f"(Изменить режим - нажми колесико мышки)").strip()
        self.massage.text = msg

    def toggle_animation_trigger(self):
        self.action_trigger = not self.action_trigger

    def rotate_side(self, side_name):
        self.action_trigger = False
        cube_positions = self.cubes_side_positions[side_name]
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
        self.LEFT = {Vec3(-1, y, z) for y in range(-1, 2) for z in range(-1, 2)}
        self.BOTTOM = {Vec3(x, -1, z) for x in range(-1, 2) for z in range(-1, 2)}
        self.FACE = {Vec3(x, y, -1) for x in range(-1, 2) for y in range(-1, 2)}
        self.BACK = {Vec3(x, y, 1) for x in range(-1, 2) for y in range(-1, 2)}
        self.RIGHT = {Vec3(1, y, z) for y in range(-1, 2) for z in range(-1, 2)}
        self.TOP = {Vec3(x, 1, z) for x in range(-1, 2) for z in range(-1, 2)}
        self.SIDE_POSITIONS = self.LEFT | self.BOTTOM | self.FACE | self.BACK | self.RIGHT | self.TOP

    def input(self, key):
        if key in 'mouse1 mouse3' and self.action_mode and self.action_trigger:
            for hit_info in mouse.collisions:
                collider_name = hit_info.entity.name
                if (key == 'mouse1' and collider_name in 'LEFT RIGHT FACE BACK' or
                        key == 'mouse3' and collider_name in 'TOP BOTTOM'):
                    self.rotate_side(collider_name)
                    break
        if key == 'mouse2':
            self.toggle_game_mode()
        super().input(key)


if __name__ == '__main__':
    game = Game()
    game.run()
