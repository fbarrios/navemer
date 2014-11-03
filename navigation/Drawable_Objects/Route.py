from Drawable_Object import Drawable_Object

class Route(Drawable_Object):

	def __init__(self, surface, lines):
		Drawable_Object.__init__(self, surface)
		self._lines = lines

	def draw(self):
		if self.visible == True:
			# Print the lines in the order given
			for line in self._lines:
				if line.visible == True:
					line.draw()


