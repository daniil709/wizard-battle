from enemy import *
from functions import load_image, text_render
from player import Player
from constants import *
import pygame as pg


class Game:
    def __init__(self, mode, enemy, player):

        self.mode = mode
        self.winner = None
        self.enemy = enemy

        # Создание окна
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("Битва магов")

        self.background = load_image("images/background.png", SCREEN_WIDTH, SCREEN_HEIGHT)

        if self.mode == 'one player':
            self.player = Player(LEFT_SIDE_COORDS)

            self.enemy = Enemy(RIGHT_SIDE_COORDS, enemy)
        elif self.mode == 'two players':
            self.player = Player(LEFT_SIDE_COORDS, player)
            self.enemy = Player(RIGHT_SIDE_COORDS, enemy, first_player=False)

        self.clock = pg.time.Clock()
        self.is_running = True
        self.run()

    def run(self):
        while self.is_running:
            self.event()
            self.update()
            self.draw()
            self.clock.tick(FPS)

    def event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.is_running = False

            if event.type == pg.KEYDOWN and self.winner is not None:
                self.is_running = False

    def update(self):
        if self.winner is None:
            self.player.update()

            if self.mode == 'two players':
                self.enemy.update()
            else:
                self.enemy.update(self.player)

            self.player.magic_balls.update()
            self.enemy.magic_balls.update()

            if self.mode == 'one player':
                hits = pg.sprite.spritecollide(self.enemy, self.player.magic_balls, True,
                                               pg.sprite.collide_rect_ratio(0.3))

                for hit in hits:
                    self.enemy.health -= hit.power

                if self.player.image not in self.player.down:
                    hits = pg.sprite.spritecollide(self.player, self.enemy.magic_balls, True,
                                                   pg.sprite.collide_rect_ratio(0.3))

                    for hit in hits:
                        self.player.health -= hit.power

                if self.player.health <= 0:
                    self.winner = self.enemy
                elif self.enemy.health <= 0:
                    self.winner = self.player

            if self.mode == 'two players':
                if self.player.image not in self.player.down:
                    hits = pg.sprite.spritecollide(self.player, self.enemy.magic_balls, True,
                                                   pg.sprite.collide_rect_ratio(0.3))

                    for hit in hits:
                        self.player.health -= hit.power
                if self.enemy.image not in self.enemy.down:
                    hits = pg.sprite.spritecollide(self.enemy, self.player.magic_balls, True,
                                                   pg.sprite.collide_rect_ratio(0.3))

                    for hit in hits:
                        self.enemy.health -= hit.power

                if self.player.health <= 0:
                    self.winner = self.enemy
                elif self.enemy.health <= 0:
                    self.winner = self.player

    def draw(self):
        # Отрисовка интерфейса
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.player.image, self.player.rect)
        self.screen.blit(self.enemy.image, self.enemy.rect)

        if self.player.charge_mode:
            self.screen.blit(self.player.charge_indicator, (self.player.rect.left + 120, self.player.rect.top))

        if self.mode == 'two players' and self.enemy.charge_mode:
            self.screen.blit(self.enemy.charge_indicator, (self.enemy.rect.left + 120, self.enemy.rect.top))

        self.player.magic_balls.draw(self.screen)
        self.enemy.magic_balls.draw(self.screen)
        # print(self.player.fireballs.draw(self.screen))

        pg.draw.rect(self.screen, 'green', (10, 10, self.player.health, 20))
        pg.draw.rect(self.screen, 'black', (10, 10, 200, 20), 2)

        pg.draw.rect(self.screen, 'green', (SCREEN_WIDTH - 210, 10, self.enemy.health, 20))
        pg.draw.rect(self.screen, 'black', (SCREEN_WIDTH - 210, 10, 200, 20), 2)

        if self.mode == 'one player':
            if self.winner == self.player:
                text = text_render("ПОБЕДА", 'green')
                text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                self.screen.blit(text, text_rect)
            elif self.winner == self.enemy:
                text = text_render("ПОРАЖЕНИЕ", 'red')
                text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                self.screen.blit(text, text_rect)
        elif self.mode == 'two players':
            if self.winner == self.player:
                text = text_render("ПОБЕДА. МАГ В ЛЕВОМ УГЛУ", 'black')
                text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                self.screen.blit(text, text_rect)
            elif self.winner == self.enemy:
                text = text_render("ПОБЕДА. МАГ В ПРАВОМ УГЛУ", 'black')
                text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                self.screen.blit(text, text_rect)

        pg.display.flip()
