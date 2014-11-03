import itertools

class Drawable_Object(object):
	newid = itertools.count().next

	def __init__(self, surface, visible = True):
		# Get a unique object ID
		self._id = Drawable_Object.newid()
		# Surface where the Object will be drew
		self._surface = surface
		# True indicates that the object will be dr
		self._visible = visible

	def id(self):
		return self._id

	@property
	def visible(self):
		return self._visible

	@visible.setter
	def visible(self, visible):
		self._visible = visible

	def draw(self):
		# TODO: Replace with the ABC module??
		raise NotImplementedError("Please Implement this method")
