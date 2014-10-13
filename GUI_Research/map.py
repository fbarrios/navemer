#!/usr/bin/env python

import pygame
from pygame.locals import *


def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    color_white = pygame.Color(255, 255, 255)
    background = pygame.image.load('background.jpg').convert()
    screen.blit(background, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return

            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return

            elif event.type == MOUSEBUTTONDOWN:
                x, y = event.pos
                pygame.draw.line(screen, color_white, (320,240), (x, y), 2)

        pygame.display.update()
        pygame.time.delay(10)

main()