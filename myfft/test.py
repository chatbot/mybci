import pygame, sys, os,time
from pygame.locals import *

pygame.init()
window = pygame.display.set_mode((100,100))
pygame.display.set_caption("fuck")


chess1 = pygame.image.load("data/chess1.png")
chess2 = pygame.image.load("data/chess2.png")
screen = pygame.display.get_surface()

timeout = 1.0/int(sys.argv[1])
print timeout

i=0
while True:
    time.sleep(timeout)
    
    if i % 2 == 0:
        surf = chess1
    else:
        surf = chess2

    screen.blit(surf,(0,0))
    pygame.display.flip()
    i += 1

    
