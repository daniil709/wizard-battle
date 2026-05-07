import random
import pygame as pg
import pygame_menu
from main import Game
from constants import *

pg.init()


class Menu:
    def __init__(self):
        self.surface = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        font = pygame_menu.font.FONT_FIRACODE_BOLD
        pygame_menu.themes.THEME_SOLARIZED.widget_font = font
        self.menu = pygame_menu.Menu(
            height=SCREEN_HEIGHT,
            width=SCREEN_WIDTH,
            theme=pygame_menu.themes.THEME_SOLARIZED,
            title='Wizard battle',
        )

        self.menu.add.label('Главное меню')
        self.menu.add.text_input('Ваше имя:', default='Name', onchange=self.set_name)
        self.menu.add.label('Режим на одного')
        self.menu.add.selector(
            'Ваш враг: ',
            [('Маг молний', 1), ('Маг земли', 2), ('Маг огня', 3), ('Случайный', 4)],
            onchange=self.set_enemy
        )
        self.menu.add.button('Играть', self.start_one_player_game)
        self.menu.add.label('Режим на двоих')
        self.menu.add.selector(
            'Левый игрок: ',
            [('Маг молний', 1), ('Маг земли', 2), ('Маг огня', 3), ('Случайный', 4)],
            onchange=self.set_left_player
        )
        self.menu.add.selector(
            'Правый игрок: ',
            [('Маг молний', 1), ('Маг земли', 2), ('Маг огня', 3), ('Случайный', 4)],
            onchange=self.set_right_player
        )
        self.menu.add.button('Играть', self.start_two_player_game)
        self.menu.add.button('Выйти', pygame_menu.events.EXIT)

        self.players = ["lightning wizard", "earth monk", "fire wizard"]
        self.left_player = self.players[0]
        self.right_player = self.players[0]
        self.enemy = "lightning wizard"

        self.run()

    def set_name(self, value):
        print("Ваше имя: ", value)

    def set_enemy(self, selected, value):
        if value in range(1, 4):
            self.enemy = ENEMIES[value - 1]
        else:
            self.enemy = random.choice(ENEMIES)

    def set_left_player(self, selected, value):
        if value in range(1, 4):
            self.left_player = self.players[value - 1]
        else:
            self.left_player = random.choice(self.players)

    def set_right_player(self, selected, value):
        if value in range(1, 4):
            self.right_player = self.players[value - 1]
        else:
            self.right_player = random.choice(self.players)

    def start_one_player_game(self):
        Game("one player", self.enemy, 'fire wizard')

    def start_two_player_game(self):
        Game("two players", self.left_player, self.right_player)

    def run(self):
        self.menu.mainloop(self.surface)


if __name__ == '__main__':
    menu_app = Menu()
