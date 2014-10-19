#!/usr/bin/env python
# -*- coding: latin-1

import random
import pygame
from pygame.locals import *
from city import City
from point import MapPoint

# Miscellaneous constants.
MAP_FILE = "city/map.png"
WINDOW_SIZE = 1006, 397
WINDOW_CAPTION = "Sistema de Navegacion para Emergencias"
DEFAULT_LINE_COLOR = pygame.Color(70, 70, 125)


def main():
    city = City()
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption(WINDOW_CAPTION)
    background = pygame.image.load(MAP_FILE).convert()
    screen.blit(background, (0, 0))

    # Draws a random route taken from the navigation module.
    init_point = city.get_random_intersection()
    end_point = city.get_random_intersection()
    draw_route(screen, city.get_route_between_intersections(init_point, end_point))
    init_point = end_point

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return

            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return

            elif event.type == MOUSEBUTTONDOWN:
                clicked_point = MapPoint(event.pos[0], event.pos[1])
                end_point = city.get_closest_intersection_to_point(clicked_point.convert_to_kml_point())
                route = city.get_route_between_intersections(init_point, end_point)
                draw_route(screen, route, line_color=get_random_color())
                init_point = end_point

        pygame.display.update()
        pygame.time.delay(10)


def draw_route(screen, route, line_color=None):
    for i in range(len(route) - 1):
        map_prev = route[i].point.convert_to_map_point().get_tuple()
        map_current = route[i + 1].point.convert_to_map_point().get_tuple()

        if line_color is None:
            line_color = DEFAULT_LINE_COLOR

        pygame.draw.line(screen, line_color, map_prev, map_current, 4)


def get_random_color():
    return pygame.Color(random.randint(0, 255),random.randint(0, 255), random.randint(0, 255))

main()