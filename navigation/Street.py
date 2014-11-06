
'''
class Street
This object models the street as a set of intersections. The idea behind the
class is to compare streets to check if the streets intersect themselves in some 
point.
'''

class Street(object):
	def __init__(self, name):
		self._intersections = set()
		self._name = name

	def get_name(self):
		return self._name

	def add_intersection(self, intersection_id):
		self._intesertions.add(intersection_id)

	def get_intersections(self):
		return self._intersections

	def intersect_street(self, street):
		return self._intersections.intersect( street.get_intersections() )