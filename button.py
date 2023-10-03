import pygame as pg

WIDTH = HEIGHT = 50

class Button(pg.sprite.Sprite):
    def __init__(self, x, y, id):
        self.rect = pg.Rect(x, y, WIDTH, HEIGHT)
