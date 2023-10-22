import sys
import pygame as pg
import pygame.midi

from interface import main
from midi import midi


if __name__=='__main__':
    pg.init()
    pg.midi.init()
    main()
    pg.midi.quit()
    pg.quit()
    sys.exit()
