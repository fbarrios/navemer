
import csv
from random import randrange
from pygraph.classes.digraph import digraph as pydigraph
from pygraph.algorithms.minmax import shortest_path

from intersection import Intersection
from block import Block

BLOCKS_FILE = "city/blocks.csv"
INTERSECTIONS_FILE = "city/intersections.csv"


class City(object):

    def __init__(self):
        self.city = get_city()

    def get_random_route(self):
        node_count = len(self.city.nodes())
        n1 = randrange(1, node_count)
        n2 = randrange(1, node_count)

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
            route.append(intersection.point)

        return route


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
