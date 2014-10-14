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


# Constants used for convert from KML coordinates to map pixels.
REFERENCE2_R = (-58.38621971856072, -34.68458626030405)
REFERENCE2_M = (238, 68)
REFERENCE1_R = (-58.37555922960053, -34.6905536694991)
REFERENCE1_M = (485, 239)


# Converts a point in coordinates to a point in the map.
def convert_to_pixels(p):
    cx = (REFERENCE1_M[0] - REFERENCE2_M[0]) / (REFERENCE1_R[0] - REFERENCE2_R[0])
    x = -cx * (REFERENCE1_R[0] - p[0]) + REFERENCE1_M[0]

    cy = (REFERENCE1_M[1] - REFERENCE2_M[1]) / (REFERENCE1_R[1] - REFERENCE2_R[1])
    y = -cy * (REFERENCE1_R[1] - p[1]) + REFERENCE1_M[1]
    return int(x), int(y)


def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption(WINDOW_CAPTION)
    background = pygame.image.load(MAP_FILE).convert()
    screen.blit(background, (0, 0))

    # Draws a random route taken from the navigation module.
    route = get_random_route()
    for i in range(len(route) - 1):
        map_prev = convert_to_pixels(route[i])
        map_current = convert_to_pixels(route[i + 1])
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