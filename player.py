from character import *


class Player(Character):
    def __init__(self, coords: tuple, folder):
        super().__init__(coords, folder)

        self.charge_indicator = pg.Surface((self.charge_power, 10))
        self.charge_indicator.fill('red')
        self.side = 'right'

        self.charge_mode = False
        self.attack_mode = False

    def load_animations(self):
        super().load_animations()
        self.charge = [load_image('images/fire wizard/charge.png', CHARACTER_WIDTH, CHARACTER_HEIGHT)]
        self.charge.append(pg.transform.flip(self.charge[0], True, False))

        self.down = [load_image('images/fire wizard/down.png', CHARACTER_WIDTH, CHARACTER_HEIGHT)]
        self.down.append(pg.transform.flip(self.down[0], True, False))

    def update(self):
        super().update()
        keys = pg.key.get_pressed()
        direction = 0

        if keys[pg.K_a]:
            direction = -1
            self.side = 'left'
        elif keys[pg.K_d]:
            direction = 1
            self.side = "right"

        self.handle_movement(direction, keys)

    def handle_movement(self, direction, keys):
        super().handle_movement(direction)

        if direction != 0:
            self.animation_mode = True
            self.charge_mode = False
            self.rect.x += direction
            self.current_animation = self.move_animation_left if direction == -1 else self.move_animation_right
        elif keys[pg.K_s]:
            self.animation_mode = False
            self.charge_mode = False
            self.image = self.down[self.side != 'right']
        elif keys[pg.K_SPACE]:
            self.animation_mode = False
            self.image = self.charge[self.side != 'right']
            self.charge_mode = True
        else:
            self.animation_mode = True
            self.charge_mode = False
            self.current_animation = self.idle_animation_left if self.side == 'left' else self.idle_animation_right

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
            self.charge_power = 0
            self.charge_mode = False
