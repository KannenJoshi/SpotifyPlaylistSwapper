import pygame as pg


done = False
playlists = []
bindings = []


def events():
    """
    Handle Keyboard & Mouse Events
    """
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True


def midi():
    """
    Handle Midi Events
    """
    pass


def update():
    """
    Update anything
    """
    pass


def draw():
    """
    Draw to screen
    """
    # Draw options and selectors
    pg.display.flip()


def main():
    screen = pg.display.set_mode((1,366, 768), pg.HWSURFACE)
    clock = pg.time.Clock()

    all = pg.sprite.Group()
    playlist_buttons = pg.sprite.Group()
    bindings_buttons = pg.sprite.Group()

    while not done:
        events()
        midi()
        update()
        draw()
        clock.tick(30)
