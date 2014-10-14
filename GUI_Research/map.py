#!/usr/bin/env python

import pygame
from pygame.locals import *

WINDOW_SIZE = (1006, 397)
BACKGROUND_COLOR = pygame.Color(255, 0, 0)
LINE_COLOR = pygame.Color(70, 70, 125)

REFERENCE2_R = (-58.38621971856072, -34.68458626030405)
REFERENCE2_M = (238, 68)

REFERENCE1_R = (-58.37555922960053, -34.6905536694991)
REFERENCE1_M = (485, 239)


def convert(p):
    cx = (REFERENCE1_M[0] - REFERENCE2_M[0]) / (REFERENCE1_R[0] - REFERENCE2_R[0])
    x = -cx * (REFERENCE1_R[0] - p[0]) + REFERENCE1_M[0]

    cy = (REFERENCE1_M[1] - REFERENCE2_M[1]) / (REFERENCE1_R[1] - REFERENCE2_R[1])
    y = -cy * (REFERENCE1_R[1] - p[1]) + REFERENCE1_M[1]
    return int(x), int(y)


def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    background = pygame.image.load('map.png').convert()
    screen.blit(background, (0, 0))

    for i in range(len(test_route) - 1):
        map_prev = convert(test_route[i])
        map_current = convert(test_route[i + 1])

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


test_route = [
    (-58.37555922960053, -34.6905536694991),
    (-58.37634890620792, -34.68986586444252),
    (-58.37736540162192, -34.68898622444274),
    (-58.37816347192872, -34.68829290276174),
    (-58.37854771235283, -34.68860802809196),
    (-58.37885654180224, -34.68885186966851),
    (-58.37965761692605, -34.68953774089236),
    (-58.37989992288034, -34.68935114117046),
    (-58.38008882408901, -34.68920923882282),
    (-58.38250076871115, -34.68728941643635),
    (-58.38505196700589, -34.68540042557326),
    (-58.38516405273022, -34.68532052359429),
    (-58.38532070234119, -34.68521603961083),
    (-58.38555562664, -34.6850399724274),
    (-58.38621971856072, -34.68458626030405),
    (-58.38586312503532, -34.68368402006258),
    (-58.38521456851129, -34.68214741693264),
    (-58.3851202484645, -34.68191089162801),
    (-58.38455840590086, -34.68057861530775),
    (-58.38427481268347, -34.67996137837734),
    (-58.38397808235339, -34.67935465939004),
    (-58.38372064551127, -34.67878698783745),
    (-58.38347386635837, -34.67824299950586),
    (-58.38322092440227, -34.67767608721845),
    (-58.38287888089548, -34.67690982788065),
    (-58.3824534159786, -34.67576029976117),
    (-58.38257681572532, -34.67565249951224),
    (-58.38268360005692, -34.67555633921609),
    (-58.38369772221737, -34.67473203866276),
    (-58.38463190664574, -34.67549968555901)
]

main()