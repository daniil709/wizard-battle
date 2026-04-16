import pygame as pg
from constants import *
from fireball import Fireball
from functions import load_image


class Character(pg.sprite.Sprite):
    def __init__(self, folder):
        super().__init__()

        self.idle_animation_left = []
        self.idle_animation_right = []
        self.move_animation_left = []
        self.move_animation_right = []
        self.charge = []
        self.attack = []
        self.down = []
        self.folder = folder
        self.load_animations()
        self.image = self.idle_animation_right[0]
        self.current_image = 0
        self.current_animation = self.idle_animation_right

        self.rect = self.image.get_rect()

        self.timer = pg.time.get_ticks()
        self.interval = 300
        self.animation_mode = True
        self.side = None
        self.charge_power = 0

        self.attack_mode = False
        self.attack_interval = 500
        self.magic_balls = pg.sprite.Group()

    def load_animations(self):
        self.idle_animation_right = [
            load_image(f"images/{self.folder}/idle{i}.png", CHARACTER_WIDTH, CHARACTER_HEIGHT)
            for i in range(1, 4)
        ]

        self.move_animation_right = [
            load_image(f"images/{self.folder}/move{i}.png", CHARACTER_WIDTH, CHARACTER_HEIGHT)
            for i in range(1, 4)
        ]

        self.idle_animation_left = [
            pg.transform.flip(image, True, False)
            for image in self.idle_animation_right
        ]

        self.move_animation_left = [
            pg.transform.flip(image, True, False)
            for image in self.move_animation_right
        ]

        self.attack = [load_image('images/fire wizard/attack.png', CHARACTER_WIDTH, CHARACTER_HEIGHT)]
        self.attack.append(pg.transform.flip(self.attack[0], True, False))

    def update(self):
        self.handle_attack_mode()
        self.handle_animation()

    def handle_attack_mode(self):
        if self.attack_mode:
            if pg.time.get_ticks() - self.timer > self.attack_interval:
                self.attack_mode = False
                self.timer = pg.time.get_ticks()

    def handle_movement(self, direction):
        if self.attack_mode:
            return

        if direction != 0:
            self.animation_mode = True
            self.rect.x += direction
            self.current_animation = self.move_animation_left if direction == -1 else self.move_animation_right
        else:
            self.animation_mode = True
            self.current_animation = self.idle_animation_left if self.side == 'left' else self.idle_animation_right

    def handle_animation(self):
        if self.animation_mode and not self.attack_mode:
            if pg.time.get_ticks() - self.timer > self.interval:
                self.current_image += 1
                if self.current_image >= len(self.current_animation):
                    self.current_image = 0
                self.image = self.current_animation[self.current_image]
                self.timer = pg.time.get_ticks()

        if self.attack_mode:
            fireball_position = self.rect.topright if self.side == 'right' else self.rect.topleft
            self.magic_balls.add(Fireball(fireball_position, self.side, self.charge_power))
            self.image = self.attack[self.side != 'right']
            self.timer = pg.time.get_ticks()
