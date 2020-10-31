
'''
This is a static Utilitiy class for all sorts of helper functions that might come up during development. Make sure to use the flag @staticmethod for readability.

Outside of this class, functions can be called by simply invoking e.g.:
Utilities.add_two_points(a,b)
'''

from src.model.utils.Geometry import Geometry

class Utilities:

    @staticmethod
    def add_two_points(point_a, point_b):
        (a_x, a_y) = point_a
        (b_x, b_y) = point_b
        return (a_x + b_x, a_y + b_y)

    @staticmethod
    def check_if_points_are_approximately_the_same(point_a, point_b):

        rounding_factor = 1

        a_1 = round(point_a[0], rounding_factor)
        a_2 = round(point_a[1], rounding_factor)
        
        b_1 = round(point_b[0], rounding_factor)
        b_2 = round(point_b[1], rounding_factor)

        if a_1 == b_1 and a_2 == b_2:
            return True
        
        return False

    @staticmethod
    def find_closest_point_in_points(point, points):

        minimum = (0, -1)
        for index, node in enumerate(points):
            distance = Geometry.euclidean_distance(node, point)

            if minimum[1] == -1:
                minimum = (index, distance)

            if minimum[1] > distance:
                minimum = (index, distance)

        return points[minimum[0]]