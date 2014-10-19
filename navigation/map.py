#!/usr/bin/env python
# -*- coding: latin-1

import pygame
from pygame.locals import *
from navigation import get_random_route

# Miscellaneous constants.
MAP_FILE = "city/map.png"
WINDOW_SIZE = 1006, 397
WINDOW_CAPTION = "Sistema de Navegacion para Emergencias"
LINE_COLOR = pygame.Color(70, 70, 125)


def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption(WINDOW_CAPTION)
    background = pygame.image.load(MAP_FILE).convert()
    screen.blit(background, (0, 0))

    # Draws a random route taken from the navigation module.
    route = get_random_route()
    for i in range(len(route) - 1):
        map_prev = route[i].convert_to_map_point().get_tuple()
        map_current = route[i + 1].convert_to_map_point().get_tuple()
        pygame.draw.line(screen, LINE_COLOR, map_prev, map_current, 4)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return

            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return

            elif event.type == MOUSEBUTTONDOWN:
                print event.pos
                pygame.draw.line(screen, LINE_COLOR, (320, 240), event.pos, 2)

        pygame.display.update()
        pygame.time.delay(10)


main()