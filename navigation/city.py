
import csv
from random import randrange
from pygraph.classes.digraph import digraph as pydigraph
from pygraph.algorithms.minmax import shortest_path

from intersection import Intersection
from block import Block
from Street import Street

BLOCKS_FILE = "city/blocks.csv"
INTERSECTIONS_FILE = "city/intersections.csv"


class City(object):

    def __init__(self):
        self.city = get_city()
        self.intersection_count = len(self.city.nodes())
        # Dictionary where the streets will be stored
        self.streets = {}
        self.load_streets()


    def get_random_intersection(self):
        int_id = randrange(1, self.intersection_count)
        return self.city.node_attributes(int_id)[0][1]


    def get_route_between_intersections(self, i1, i2):
        n1 = i1.id
        n2 = i2.id
        span, dists = shortest_path(self.city, n1)

        path = [n2]
        node_prev = n2
        while node_prev != n1:
            if node_prev not in span:
                return []

            node_curr = span[node_prev]
            path.append(node_curr)
            node_prev = node_curr

        path.reverse()

        route = []
        for intersection in path:
            intersection = self.city.node_attributes(intersection)[0][1]
            route.append(intersection)

        return route


    def get_random_route(self):
        i1 = self.get_random_intersection()
        i2 = self.get_random_intersection()
        return self.get_route_between_intersections(i1, i2)


    def get_closest_intersection_to_point(self, point):
        closest_intersection = None
        closest_distance = float("inf")

        for intersection in self.city.nodes():
            intersection = self.city.node_attributes(intersection)[0][1]
            distance = intersection.point.distance(point)

            if distance < closest_distance:
                closest_distance = distance
                closest_intersection = intersection

        return closest_intersection


    def load_streets(self):
        with open(BLOCKS_FILE) as fp:
            blocks_file = csv.reader(fp)

            for record in blocks_file:
                # For every record, get the intersections and add 
                # them to the streets. If the street doesn't exists, create it

                name = record[1]
                intersection_id_1 = int(record[4])
                intersection_id_2 = int(record[5])

                street = None
                try:
                    street = self.streets[name]
                except:
                    street = Street(name)
                    self.streets[name] = street

                street.add_intersection(intersection_id_1)
                street.add_intersection(intersection_id_2)


    def get_streets(self):
        return self.streets


    # Return the streets names that intersect with the street given as a parameter
    def get_streets_names_who_intersect_with_a_street(self, rhs_street):
        streets_names = set()

        for street in self.streets.itervalues():
            if rhs_street.get_name() != street:
                # Check if the streets has an intersection
                if len( rhs.street.intersect_street(street)) != 0:
                    streets_name.add( street.get_name() )

        return streets_names


# Loads the city as a graph in memory.
def get_city():
    city = pydigraph()

    load_intersections(city)
    load_blocks(city)

    return city


def load_intersections(city):
    with open(INTERSECTIONS_FILE) as fp:
        intersections_file = csv.reader(fp)

        for record in intersections_file:
            num = int(record[0])
            x = float(record[3])
            y = float(record[4])

            intersection = Intersection(num, x, y)

            city.add_node(num)
            city.add_node_attribute(num, ("intersection", intersection))


def load_blocks(city):
    with open(BLOCKS_FILE) as fp:
        blocks_file = csv.reader(fp)

        for record in blocks_file:
            num = int(record[0])
            name = record[1]
            block_type = int(record[2])
            single_hand = True if record[3] == "0" else False
            intersection_id_1 = int(record[4])
            intersection_id_2 = int(record[5])
            block = Block(num, name, block_type, single_hand, intersection_id_1, intersection_id_2)

            edge = (intersection_id_1, intersection_id_2)
            city.add_edge(edge, block_type, name, ("block", block))

            if not block.single_hand:
                edge = (intersection_id_2, intersection_id_1)
                city.add_edge(edge, block_type, name, ("block", block))
