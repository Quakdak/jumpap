import pygame
import sys
from pygame.locals import *
import random

class Jumpap:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        self.green = pygame.image.load('sprites/platform_green.png')
        self.platforms = []


    def platforming(self):
        pass


    def run(self):
        clock = pygame.time.Clock()
        self.platforming()
        while True:
            self.screen.fill((255,255,255))
            bg = pygame.image.load("sprites/background.jpg")
            self.screen.blit(bg, (0, 0))
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()

            pygame.display.flip()
Jumpap().run()
