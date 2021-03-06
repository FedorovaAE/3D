from ursina import *
from ursina import camera, mouse


class Game(Ursina):
    def __init__(self, count_sid):
        super().__init__()
        window.full_screen = True
        # b = Button(text='hello world!', color=color.azure, origin=(-7.5, 0), icon='sword', scale=.25)
        # b.on_click = application.quit  # assign a function to the button.
        # b.tooltip = Tooltip('exit')
        Entity(model='quad', scale=60, texture='white_cube', texture_scale=(60, 60), rotation_x=90, y=-5,
               color=color.violet)
        Entity(model='sphere', scale=100, texture='textures/1', double_sided=True)
        EditorCamera()
        camera.world_position = (0, 0, -25)
        self.model, self.texture = 'textures/custom_cube', 'textures/rubik_texture'
        self.action_trigger = True
        self.action_mode = True
        self.massage = Text(origin=(0, 19), color=color.white)
        self.count_side = count_sid
        self.load_game()

    def load_game(self):
        self.create_cube_positions()
        self.CUBES = [Entity(model=self.model, texture=self.texture, position=pos) for pos in self.SIDE_POSITIONS]
        self.PARENT = Entity()
        if self.count_side == 3:
            self.rotation_axes = {'LEFT': 'x', 'RIGHT': 'x', 'TOP': 'y', 'BOTTOM': 'y', 'FACE': 'z', 'BACK': 'z'}
            self.cubes_side_positions = {'LEFT': self.LEFT, 'BOTTOM': self.BOTTOM, 'RIGHT': self.RIGHT,
                                        'FACE': self.FACE, 'BACK': self.BACK, 'TOP': self.TOP}
        else:
            self.rotation_axes = {'LEFT': 'x', 'RIGHT': 'x', 'TOP': 'y', 'BOTTOM': 'y', 'FACE': 'z', 'BACK': 'z',
                                  'LEFT1': 'x', 'RIGHT1': 'x', 'TOP1': 'y', 'BOTTOM1': 'y', 'FACE1': 'z', 'BACK1': 'z'}
            self.cubes_side_positions = {'LEFT': self.LEFT, 'BOTTOM': self.BOTTOM, 'RIGHT': self.RIGHT,
                                         'FACE': self.FACE, 'BACK': self.BACK, 'TOP': self.TOP, 'LEFT1': self.LEFT1,
                                         'BOTTOM1': self.BOTTOM1, 'RIGHT1': self.RIGHT1, 'TOP1': self.TOP1,
                                         'FACE1': self.FACE1, 'BACK1': self.BACK1}
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
        if self.count_side == 3:
            self.LEFT_sensor = self.create_sensor('LEFT', (-0.99, 0, 0), (1.01, 3.01, 3.01))
            self.FACE_sensor = self.create_sensor('FACE', (0, 0, -0.99), (3.01, 3.01, 1.01))
            self.BACK_sensor = self.create_sensor('BACK', (0, 0, 0.99), (3.01, 3.01, 1.01))
            self.RIGHT_sensor = self.create_sensor('RIGHT', (0.99, 0, 0), (1.01, 3.01, 3.01))
            self.TOP_sensor = self.create_sensor('TOP', (0, 1, 0), (3.01, 1.01, 3.01))
            self.BOTTOM_sensor = self.create_sensor('BOTTOM', (0, -1, 0), (3.01, 1.01, 3.01))
        else:
            self.LEFT1_sensor = self.create_sensor('LEFT1', (-0.99, 0, 0), (1.02, 5.02, 5.02))
            self.FACE1_sensor = self.create_sensor('FACE1', (0, 0, -0.99), (5.01, 5.02, 1.02))
            self.BACK1_sensor = self.create_sensor('BACK1', (0, 0, 0.99), (5.02, 5.02, 1.02))
            self.RIGHT1_sensor = self.create_sensor('RIGHT1', (0.99, 0, 0), (1.02, 5.02, 5.02))
            self.TOP1_sensor = self.create_sensor('TOP1', (0, 0.99, 0), (5.02, 1.02, 5.02))
            self.BOTTOM1_sensor = self.create_sensor('BOTTOM1', (0, -0.99, 0), (5.02, 1.02, 5.02))
            self.LEFT_sensor = self.create_sensor('LEFT', (-1.98, 0, 0), (1.02, 5.02, 5.02))
            self.FACE_sensor = self.create_sensor('FACE', (0, 0, -1.98), (5.02, 5.02, 1.02))
            self.BACK_sensor = self.create_sensor('BACK', (0, 0, 1.98), (5.02, 5.02, 1.02))
            self.RIGHT_sensor = self.create_sensor('RIGHT', (1.98, 0, 0), (1.2, 5.02, 5.02))
            self.TOP_sensor = self.create_sensor('TOP', (0, 2, 0), (5.02, 1.02, 5.02))
            self.BOTTOM_sensor = self.create_sensor('BOTTOM', (0, -2, 0), (5.02, 1.02, 5.02))


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
        if self.count_side == 3:
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
        if key in 'mouse1 mouse3' and self.action_mode and self.action_trigger:
            for hit_info in mouse.collisions:
                collider_name = hit_info.entity.name
                if (key == 'mouse1' and collider_name in 'LEFT RIGHT FACE BACK LEFT1 RIGHT1 FACE1 BACK1' or
                        key == 'mouse3' and collider_name in 'TOP BOTTOM TOP1 BOTTOM1'):
                    self.rotate_side(collider_name)
                    break
        if key == 'mouse2':
            self.toggle_game_mode()
        if key == 'escape':
            sys.exit()
        super().input(key)
