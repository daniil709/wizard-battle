from character import *
import random
from magicball import Magicball


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

    def update(self, player=None, *args):
        super().update()

        if player is not None:
            self.handle_attack_mode(player)

        self.movement()

    def movement(self):
        if self.attack_mode:
            return

        self.animation_mode = True
        self.current_animation = self.idle_animation_left if self.side == 'left' else self.move_animation_right

        now = pg.time.get_ticks()  # взять количество тиков +

        if now - self.move_timer < self.move_duration:
            # включить режим анимации +
            self.animation_mode = True
            # подвинуть по X координате на direction +
            self.rect.x += self.direction
            self.current_animation = self.move_animation_left if self.direction == -1 else self.move_animation_right
        else:
            if random.randint(1, 5) == 1 and now - self.move_timer > self.move_interval:
                self.move_timer = pg.time.get_ticks()
                self.move_duration = random.randint(400, 1500)  # случайное число от 400 до 1500 +
                self.direction = random.choice([-1, 1])

            else:
                # включить режим анимации +
                self.animation_mode = True
                self.current_animation = self.idle_animation_left if self.side == "left" else self.idle_animation_right

        if self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        elif self.rect.left <= 0:
            self.rect.left = 0

    def handle_attack_mode(self, player=None):
        super().handle_attack_mode()

        if player is not None:
            if not self.attack_mode:
                attack_probability = 1

                if player.charge_mode:
                    attack_probability += 2

                if random.randint(1, 100) <= attack_probability:
                    self.attack_mode = True
                    self.charge_power = random.randint(1, 100)

                    if player.rect.centerx < self.rect.centerx:
                        self.side = 'left'
                    else:
                        self.side = 'right'

                    self.animation_mode = False
                    self.image = self.attack[self.side != 'right']

            if self.attack_mode:
                if pg.time.get_ticks() - self.timer > self.attack_interval:
                    self.attack_mode = False
                    self.timer = pg.time.get_ticks()

    def handle_animation(self):
        super().handle_animation()

        if self.animation_mode and self.charge_power > 0:
            ball_position = self.rect.topright if self.side == 'right' else self.rect.topleft
            self.magic_balls.add(Magicball(ball_position, self.side, self.charge_power, self.folder))
            self.charge_power = 0
            self.image = self.attack[self.side != 'right']
            self.timer = pg.time.get_ticks()
