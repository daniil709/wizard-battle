import pygame as pg

pg.init()

font = pg.font.Font(None, 40)


def load_image(file, width, height):
    image = pg.image.load(file).convert_alpha()
    image = pg.transform.scale(image, (width, height))
    return image


def text_render(text, color):
    return font.render(str(text), True, color)
