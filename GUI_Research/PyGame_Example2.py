#!/usr/bin/env python

import sys, pygame
from GameObject import GameObject
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((640, 480))
player = pygame.image.load('ball.bmp').convert()
background = pygame.image.load('background.jpg').convert()
screen.blit(background, (0, 0))
objects = []

for x in range(10): 		#create 10 objects
	o = GameObject(player, x, x)
 	objects.append(o)

while 1:
	for event in pygame.event.get():
		if event.type in (QUIT, KEYDOWN):
			sys.exit()

	for o in objects:
		screen.blit(background, o.pos, o.pos)

	for o in objects:
		o.move()
		screen.blit(o.image, o.pos)

	pygame.display.update()
	pygame.time.delay(10)