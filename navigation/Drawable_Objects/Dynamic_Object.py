from Drawable_Object import Drawable_Object
import pygame

''' 
Class Dynamic Object
Object that move around the surface
'''

class Dynamic_Object(Drawable_Object):

	def __init__(self, surface, pos, image_name):
		Drawable_Object.__init__(self, surface)
		self._image = pygame.image.load(image_name).convert()
		# Tuple (x,y)
		self._pos = pos
		# Minimize the image
		self._image = pygame.transform.scale(self._image, (40,40))


	def set_pos(self,pos):
		self._pos = pos

	def move(self):
		raise NotImplementedError("Please Implement this method")


	def draw(self):
		self._surface.blit(self._image, self._pos)


