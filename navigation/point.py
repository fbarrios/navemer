
from math import sqrt

# Constants used for convert from KML coordinates to map pixels.
REFERENCE2_R = (-58.38621971856072, -34.68458626030405)
REFERENCE2_M = (238, 68)
REFERENCE1_R = (-58.37555922960053, -34.6905536694991)
REFERENCE1_M = (485, 239)


class Point(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        return sqrt(dx ** 2 + dy ** 2)

    def get_tuple(self):
        return self.x, self.y

    def __str__(self):
        return "({x}, {y})".format(x=self.x, y=self.y)

    def __repr__(self):
        return str(self)


class KMLPoint(Point):

    """ Converts a point in KML coordinates to a point in the Model.
    """
    def convert_to_map_point(self):
        cx = (REFERENCE1_M[0] - REFERENCE2_M[0]) / (REFERENCE1_R[0] - REFERENCE2_R[0])
        x = -cx * (REFERENCE1_R[0] - self.x) + REFERENCE1_M[0]

        cy = (REFERENCE1_M[1] - REFERENCE2_M[1]) / (REFERENCE1_R[1] - REFERENCE2_R[1])
        y = -cy * (REFERENCE1_R[1] - self.y) + REFERENCE1_M[1]
        return MapPoint(x, y)


class MapPoint(Point):

    """ Converts a point in the map to a point in KML coordinates.
    """
    def convert_to_kml_point(self):
        return KMLPoint(0, 0)
