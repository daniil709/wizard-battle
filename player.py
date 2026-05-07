from character import *
from magicball import Magicball


class Player(Character):
    def __init__(self, coords: tuple, folder: str = 'lightning wizard', first_player=True):
        super().__init__(coords, folder)

        self.charge_indicator = pg.Surface((self.charge_power, 10))
        self.charge_indicator.fill('red')
        self.charge_mode = False

        if first_player:
            self.coords = LEFT_SIDE_COORDS
            self.current_animation = self.idle_animation_left
            self.side = 'left'
            self.key_left = pg.K_a
            self.key_right = pg.K_d
            self.key_down = pg.K_s
            self.key_charge = pg.K_SPACE
        else:
            self.coords = RIGHT_SIDE_COORDS
            self.current_animation = self.idle_animation_right
            self.side = 'right'
            self.key_left = pg.K_LEFT
            self.key_right = pg.K_RIGHT
            self.key_down = pg.K_DOWN
            self.key_charge = pg.K_RCTRL

    def load_animations(self):
        super().load_animations()
        self.charge = [load_image(f'images/{self.folder}/charge.png', CHARACTER_WIDTH, CHARACTER_HEIGHT)]
        self.charge.append(pg.transform.flip(self.charge[0], True, False))

        self.down = [load_image(f'images/{self.folder}/down.png', CHARACTER_WIDTH, CHARACTER_HEIGHT)]
        self.down.append(pg.transform.flip(self.down[0], True, False))

    def update(self):
        super().update()  # Оставляем, он нужен для базовой логики
        keys = pg.key.get_pressed()
        direction = 0

        if keys[self.key_left]:
            direction = -1
            self.side = 'left'
        elif keys[self.key_right]:
            direction = 1
            self.side = "right"

        self.handle_movement(direction)

        if keys[self.key_down]:
            self.animation_mode = False
            self.charge_mode = False
            self.image = self.down[self.side != 'right']

        # Обработка SPACE
        if keys[self.key_charge]:
            if not self.attack_mode:  # Если не в режиме атаки
                self.animation_mode = False
                self.image = self.charge[self.side != 'right']
                self.charge_mode = True
        else:
            # Клавиша отпущена
            if self.charge_mode:
                self.charge_mode = False
                self.attack_mode = True  # Активируем атаку

    def handle_animation(self):
        super().handle_animation()
        if not self.charge_mode and self.charge_power > 0:
            self.attack_mode = True

        if self.charge_mode:
            self.charge_power += 1
            self.charge_indicator = pg.Surface((self.charge_power, 10))
            self.charge_indicator.fill('red')
            if self.charge_power == 100:
                self.attack_mode = True

        if self.attack_mode and self.charge_power > 0:
            fireball_position = self.rect.topright if self.side == 'right' else self.rect.topleft
            self.magic_balls.add(Magicball(fireball_position, self.side, self.charge_power, self.folder))
            self.charge_power = 0
            self.charge_mode = False
            self.image = self.attack[self.side != 'right']
            self.timer = pg.time.get_ticks()
