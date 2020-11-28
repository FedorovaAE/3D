from ursina import camera
from game_obj import *


class Game(Ursina):
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
        Entity(model='quad', scale=map_size, position=(map_size // 2, map_size // 2, 0), color=color.dark_gray)
        Entity(model=Grid(map_size, map_size), scale=map_size,
               position=(map_size // 2, map_size // 2, -0.01), color=color.white)

    def new_game(self):
        scene.clear()
        self.create_map(self.MAP_SIZE)
        self.apple = Fruit(self.MAP_SIZE, model='sphere', color=color.red)
        self.player = Player(self.MAP_SIZE)
        self.villain = Villain(self.MAP_SIZE)
        self.num_villain = [self.villain]
        self.player_boll = Boll(self.player.speed, self.player.direction, self.player.segment_positions[-1])

    def input(self, key):
        if key == '2':
            camera.rotation_x = 0
            camera.position = (self.MAP_SIZE // 2, self.MAP_SIZE // 2, -50)
        elif key == '3':
            camera.position = (self.MAP_SIZE // 2, -20.5, -20)
            camera.rotation_x = -57
        elif key == '1':
            if self.player.direction != Vec3(0, 0, 0):
                self.player_boll = Boll(self.player.speed, self.player.direction, self.player.segment_positions[-1],
                                    model='sphere', color=color.orange)
        super().input(key)

    def kill_villain(self):
        for i in range(len(self.num_villain)):
            if self.player_boll.position == self.num_villain[i].segment_positions[-1]:
                del self.num_villain[i]

    def check_fruit_eaten(self):
        if self.player.segment_positions[-1] == self.apple.position:
            self.player.add_segment()
            self.apple.new_position()
            self.create_villain()

    def create_villain(self):
        self.num_villain.append(Villain(self.MAP_SIZE))

    def check_game_over(self):
        player = self.player.segment_positions
        still_run = True
        for i in range(len(self.num_villain)):
            if self.player.segment_positions[-1] == self.num_villain[i].segment_positions[-1]:
                still_run = False
        if (0 < player[-1][0] < self.MAP_SIZE) and (0 < player[-1][1] < self.MAP_SIZE) and still_run:
            return
        print_on_screen('GAME OVER', position=(-0.7, 0.1), scale=10, duration=1)
        self.player.direction = Vec3(0, 0, 0)
        self.player.permissions = dict.fromkeys(self.player.permissions, 0)
        invoke(self.new_game, delay=1)

    def update(self):
        print_on_screen(f'Score: {self.player.score}', position=(-0.75, 0.45), scale=3, duration=1 / 20)
        print_on_screen(f': {self.villain.segment_positions[-1]}', position=(0.15, 0.45), scale=3, duration=1 / 20)
        self.kill_villain()
        self.check_fruit_eaten()
        self.check_game_over()
        self.player.run()
        self.player_boll.run()
        for i in range(len(self.num_villain)):
            self.num_villain[i].run()
        self.player_boll.run()


if __name__ == '__main__':
    game = Game()
    update = game.update
    game.run()
