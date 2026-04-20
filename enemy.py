from character import *
from player import Player


class Enemy(Character):
    def __init__(self, coords: tuple, folder: str):
        super().__init__(coords, folder)

        self.current_animation = self.idle_animation_left
        self.side = 'left'
        self.move_interval = 800
        self.move_duration = 0
        self.direction = 0
        self.move_timer = pg.time.get_ticks()

    def load_animations(self):
        self.idle_animation_right = [load_image(f"images/{self.folder}/idle{i}.png", CHARACTER_WIDTH, CHARACTER_HEIGHT)
                                     for i in range(1, 4)]

        self.idle_animation_left = [pg.transform.flip(image, True, False) for image in self.idle_animation_right]

        self.move_animation_right = [load_image(f"images/{self.folder}/move{i}.png", CHARACTER_WIDTH, CHARACTER_HEIGHT)
                                     for i in range(1, 5)]

        self.move_animation_left = [pg.transform.flip(image, True, False) for image in self.move_animation_right]

        self.attack = [load_image(f"images/{self.folder}/attack.png", CHARACTER_WIDTH, CHARACTER_HEIGHT)]
        self.attack.append(pg.transform.flip(self.attack[0], True, False))

    def update(self, player: Player = None, *args):
        super().update()

        if player is not None:
            self.handle_attack_mode(player)

    def handle_attack_mode(self, player: Player = None):
        super().handle_attack_mode()

        if player is not None:
            # Дополнительная логика с player
            pass

    def handle_animation(self):
        # Сначала базовая анимация
        super().handle_animation()

        # Потом своя логика атаки
        if self.attack_mode and self.charge_power > 0:
            ball_position = self.rect.topright if self.side == "right" else self.rect.topleft
            self.magic_balls.add(Fireball(ball_position, self.side, self.charge_power, self.folder))
            self.charge_power = 0
            self.image = self.attack[self.side != "right"]
            self.timer = pg.time.get_ticks()
