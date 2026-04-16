import pygame as pg
from constants import *
from functions import load_image, text_render


class Fireball(pg.sprite.Sprite):
    def __init__(self, coord, side, power):
        super().__init__()

        self.image = load_image('images/fire wizard/magicball.png', 200, 150)
        self.side = side
        self.power = power // 2
        self.rect = self.image.get_rect()
        self.rect.center = (coord[0], coord[1] + 120)

        if self.side == 'right':
            self.image = pg.transform.flip(self.image, True, False)

    def update(self):
        if self.side == 'left':
            self.rect.x -= 4
            if self.rect.right <= 0:
                self.kill()
        else:
            self.rect.x += 4
            if self.rect.left >= SCREEN_WIDTH:
                self.kill()
