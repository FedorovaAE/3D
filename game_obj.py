from ursina import *
from random import randrange


class Fruit(Entity):
    def __init__(self, MAP_SIZE, **kwargs):
        super().__init__(**kwargs)
        self.MAP_SIZE = MAP_SIZE
        self.new_position()

    def new_position(self):
        self.position = (randrange(self.MAP_SIZE) + 0.5, randrange(self.MAP_SIZE) + 0.5, -0.5)


class Player:
    def __init__(self, map_size):
        self.MAP_SIZE = map_size
        self.segment_length = 1
        self.position_length = self.segment_length + 1
        self.segment_positions = [Vec3(randrange(map_size) + 0.5, randrange(map_size) + 0.5, -0.5)]
        self.segment_entities = []
        self.create_segment(self.segment_positions[0])
        self.directions = {'a': Vec3(-1, 0, 0), 'd': Vec3(1, 0, 0), 'w': Vec3(0, 1, 0), 's': Vec3(0, -1, 0)}
        self.direction = Vec3(0, 0, 0)
        self.permissions = {'a': 1, 'd': 1, 'w': 1, 's': 1}
        self.taboo_movement = {'a': 'd', 'd': 'a', 'w': 's', 's': 'w'}
        self.speed, self.score = 12, 0
        self.frame_counter = 0

    def add_segment(self):
        self.score += 1
        self.speed = max(self.speed - 1, 5)

    def create_segment(self, position):
        entity = Entity(position=position)
        Entity(model='textures/aliens', color=color.green, position=position).add_script(
            SmoothFollow(speed=12, target=entity, offset=(0, 0, 0)))
        self.segment_entities.insert(0, entity)

    def run(self):
        self.frame_counter += 1
        if not self.frame_counter % self.speed:
            self.control()
            self.segment_positions.append(self.segment_positions[-1] + self.direction)
            self.segment_positions = self.segment_positions[-self.segment_length:]
            for segment, segment_position in zip(self.segment_entities, self.segment_positions):
                segment.position = segment_position

    def control(self):
        for key in 'wasd':
            if held_keys[key] and self.permissions[key]:
                self.direction = self.directions[key]
                self.permissions = dict.fromkeys(self.permissions, 1)
                self.permissions[self.taboo_movement[key]] = 0
                break


class Villain:
    def __init__(self, map_size):
        self.MAP_SIZE = map_size
        self.segment_length = 1
        self.position_length = self.segment_length + 1
        self.segment_positions = [Vec3(randrange(map_size) + 0.5, randrange(map_size) + 0.5, -0.5)]
        self.segment_entities = []
        self.create_segment(self.segment_positions[0])
        self.directions = {'r': Vec3(-1, 0, 0), 't': Vec3(1, 0, 0), 'y': Vec3(0, 1, 0), 'u': Vec3(0, -1, 0)}
        self.direction = Vec3(1, 0, 0)
        self.permissions = {'r': 1, 't': 1, 'y': 1, 'u': 1}
        self.taboo_movement = {'r': 't', 't': 'r', 'y': 'u', 'u': 'y'}
        self.speed, self.score = 12, 0
        self.frame_counter = 0

    def add_segment(self):
        self.score += 1
        self.speed = max(self.speed - 1, 5)

    def create_segment(self, position):
        entity = Entity(position=position)
        Entity(model='sphere', color=color.blue, position=position).add_script(
            SmoothFollow(speed=12, target=entity, offset=(0, 0, 0)))
        self.segment_entities.insert(0, entity)

    def run(self):
        self.frame_counter += 1
        if not self.frame_counter % self.speed:
            self.control()
            snake = self.segment_positions
            if 1 > snake[-1][0]:
                self.direction = self.directions['t']
            elif self.MAP_SIZE - 1 < snake[-1][0]:
                self.direction = self.directions['r']
            elif 1 > snake[-1][1]:
                self.direction = self.directions['y']
            elif self.MAP_SIZE - 1 < snake[-1][1]:
                self.direction = self.directions['u']
            if 0 < snake[-1][0] < self.MAP_SIZE and 0 < snake[-1][1] < self.MAP_SIZE:
                self.segment_positions.append(self.segment_positions[-1] + self.direction)
                self.segment_positions = self.segment_positions[-self.segment_length:]
                for segment, segment_position in zip(self.segment_entities, self.segment_positions):
                    segment.position = segment_position

    def control(self):
        dict_vi = {1: 'r', 2: 't', 3: 'y', 4: 'u'}
        key = dict_vi[random.randint(1, 4)]
        if self.permissions[key]:
            self.direction = self.directions[key]
            self.permissions = dict.fromkeys(self.permissions, 1)
            self.permissions[self.taboo_movement[key]] = 0


class Boll(Entity):
    def __init__(self, speed, direction, position, **kwargs):
        super().__init__(**kwargs)
        self.speed = speed
        self.direction = direction
        self.frame_counter = 0
        self.position = position

    def run(self):
        self.speed -= 20
        if not self.frame_counter % self.speed:
            self.position += self.direction
