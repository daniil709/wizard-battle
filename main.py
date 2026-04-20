from enemy import *

from functions import load_image
from player import Player
from constants import *


class Game:
    def __init__(self):

        # Создание окна
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("Битва магов")

        self.background = load_image("images/background.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.player = Player((100, SCREEN_HEIGHT // 2), 'fire wizard')
        self.enemy = Enemy((SCREEN_WIDTH - 100, SCREEN_HEIGHT // 2), 'lightning wizard')
        self.clock = pg.time.Clock()
        self.run()

    def run(self):
        while True:
            self.event()
            self.update()
            self.draw()
            self.clock.tick(FPS)

    def event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()

    def update(self):
        self.player.update()
        self.enemy.update(self.player)
        self.player.magic_balls.update()

    def draw(self):
        # Отрисовка интерфейса
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.player.image, self.player.rect)
        self.screen.blit(self.enemy.image, self.enemy.rect)

        if self.player.charge_mode:
            self.screen.blit(self.player.charge_indicator, (self.player.rect.left + 120, self.player.rect.top))

        self.player.magic_balls.draw(self.screen)

        pg.display.flip()


if __name__ == "__main__":
    Game()
