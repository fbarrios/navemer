'''
Class Drawable_Object_Storage
	Object that store all the 
'''

class Drawable_Object_Storage(object):

	def __init__(self):
		# Dictionary that storage Drawable Objects
		self._object_storage = {}

	def add_object(self, drawable_object):
		self._object_storage[drawable_object.id()] = drawable_object

	def get_object(self, object_id):
		try:
			return self._object_storage[object_id]
		except:
			return -1

	def remove_object(self, object_id):
		try:
			del self._object_storage[object_id]
		except:
			print "Object could not be destroyed. Doesn't belong to the Storage"

	def draw_objects(self):
		for drawable_object in self._object_storage.itervalues():
			if drawable_object.visible == True:
				drawable_object.draw()