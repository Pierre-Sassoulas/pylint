
    import sys
    import pygame
    from pygame.locals import *
    
    pygame.init()
    
    # setup the window
    DISPLAYSURF = pygame.display.set_mode((500, 400), 0, 32)
    pygame.display.set_caption("Drawing")
    
    # setup the colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    
    pixObj = pygame.PixelArray(DISPLAYSURF)
    pixObj[480][380] = BLACK
    pixObj[482][382] = BLACK
    pixObj[484][384] = BLACK
    pixObj[486][386] = BLACK
    pixObj[488][388] = BLACK
    del pixObj
    

