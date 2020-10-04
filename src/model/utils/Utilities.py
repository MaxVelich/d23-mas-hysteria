
'''
This is a static Utilitiy class for all sorts of helper functions that might come up during development. Make sure to use the flag @staticmethod for readability.

Outside of this class, functions can be called by simply invoking e.g.:
Utilities.add_two_points(a,b)
'''

class Utilities:

    @staticmethod
    def add_two_points(point_a, point_b):
        (a_x, a_y) = point_a
        (b_x, b_y) = point_b
        return (a_x + b_x, a_y + b_y)