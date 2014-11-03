from Drawable_Object import Drawable_Object
import pygame
import random

class Line(Drawable_Object):

	def __init__(self, surface, start, end, width = 5, color = None):
		Drawable_Object.__init__(self, surface)

		self._start = start
		self._end = end
		self._width = width
		self._color = color

	@property
	def start(self):
		return self._start

	@start.setter
	def start(self, start):
		self._start = start

	@property
	def end(self):
		return self._end

	@end.setter
	def end(self, end):
		self._end = end

	@property
	def width(self):
		return self._width

	@width.setter
	def width(self, width):
		self._width = width

	def draw(self):
		if self._color == None:
			self._color = pygame.Color(random.randint(0,255),
					  				   random.randint(0,255),
								 	   random.randint(0,255))
		pygame.draw.line(self._surface, 
						 self._color, 
						 self._start,
						 self._end,
						 self._width)

