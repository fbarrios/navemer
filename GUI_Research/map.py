#!/usr/bin/env python

import pygame
from pygame.locals import *


def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    color_white = pygame.Color(255, 255, 255)
    background = pygame.image.load('background.jpg').convert()
    screen.blit(background, (0, 0))

    pygame.draw.line(screen, color_white, (60, 10), (400, 400), 4)

    while True:
        for event in pygame.event.get():
            if event.type in (QUIT, KEYDOWN):
                return

        pygame.display.update()
        pygame.time.delay(10)

main()