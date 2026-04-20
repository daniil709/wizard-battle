from character import *


class Player(Character):
    def __init__(self, coords, folder: str):
        super().__init__(coords, folder)

        self.charge_indicator = pg.Surface((self.charge_power, 10))
        self.charge_indicator.fill('red')
        self.side = 'right'
        self.charge_mode = False

    def load_animations(self):
        super().load_animations()
        self.charge = [load_image('images/fire wizard/charge.png', CHARACTER_WIDTH, CHARACTER_HEIGHT)]
        self.charge.append(pg.transform.flip(self.charge[0], True, False))

        self.down = [load_image('images/fire wizard/down.png', CHARACTER_WIDTH, CHARACTER_HEIGHT)]
        self.down.append(pg.transform.flip(self.down[0], True, False))

    def update(self):
        super().update()  # Оставляем, он нужен для базовой логики
        keys = pg.key.get_pressed()
        direction = 0

        if keys[pg.K_a]:
            direction = -1
            self.side = 'left'
        elif keys[pg.K_d]:
            direction = 1
            self.side = "right"

        self.handle_movement(direction)

        if keys[pg.K_s]:
            self.animation_mode = False
            self.charge_mode = False
            self.image = self.down[self.side != 'right']

        # Обработка SPACE
        if keys[pg.K_SPACE]:
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
        # Сначала вызываем базовую анимацию
        super().handle_animation()

        # Потом свою логику зарядки и атаки
        if not self.charge_mode and self.charge_power > 0:
            self.attack_mode = True

        if self.charge_mode:
            self.charge_power += 1
            self.charge_indicator = pg.Surface((self.charge_power, 10))
            self.charge_indicator.fill("red")
            if self.charge_power == 100:
                self.attack_mode = True

        if self.attack_mode and self.charge_power > 0:
            fireball_position = self.rect.topright if self.side == "right" else self.rect.topleft
            self.magic_balls.add(Fireball(fireball_position, self.side, self.charge_power))
            self.charge_power = 0
            self.charge_mode = False
            self.image = self.attack[self.side != "right"]
            self.timer = pg.time.get_ticks()
