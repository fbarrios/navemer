
class Intersection(object):

    def __init__(self, num, x, y):
        self.id = num
        self.x = x
        self.y = y

    def get_coordinates(self):
        return self.x, self.y