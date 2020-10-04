
'''
This class is a static helper class for everything generally geometrical. The functions below should be self-explanatory. 
'''

import math

class Geometry:

    @staticmethod
    def euclidean_distance(point_a, point_b):
        delta_x = point_a[0] - point_b[0]
        delta_y = point_a[1] - point_b[1]
        return math.sqrt(delta_x * delta_x + delta_y * delta_y)

    @staticmethod
    def line_through_two_points(point_1, point_2):
        x_1, y_1 = point_1
        x_2, y_2 = point_2

        denominator = (x_2 - x_1)
        if denominator == 0:
            k = 0
        else:
            k = (y_2 - y_1) / denominator

        d = y_1 - (k * x_1)

        return (k, d)

    @staticmethod
    def intersection_of_two_lines(line_1, line_2):
        k_1, d_1 = Geometry.line_through_two_points(line_1[0], line_1[1])
        k_2, d_2 = Geometry.line_through_two_points(line_2[0], line_2[1]) 

        if k_1 == k_2:
            return False

        x_intersect = (d_2 - d_1) / (k_1 - k_2)
        y_intersect = (k_1 * x_intersect) + d_1
        return (x_intersect, y_intersect)

    @staticmethod
    def point_lies_on_line(point, line):
        is_on_line = False

        x_1, y_1 = line[0]
        x_2, y_2 = line[1]

        xs = [x_1, x_2]
        xs.sort()
        ys = [y_1, y_2]
        ys.sort()

        if point[0] > xs[0] and point[0] < xs[-1]:
            if point[1] > ys[0] and point[1] < ys[-1]:
                is_on_line = True

        return is_on_line

    @staticmethod
    def two_lines_intersect(line_1, line_2):
        intersection = Geometry.intersection_of_two_lines(line_1, line_2)
        if intersection == False:
            return False
            
        intersection_with_line_1 = Geometry.point_lies_on_line(intersection, line_1)
        intersection_with_line_2 = Geometry.point_lies_on_line(intersection, line_2)

        if intersection_with_line_1 and intersection_with_line_2:
            return True

        return False

    @staticmethod
    def edge_intersects_with_rectangle_edges(edge, rectangle):

        for index, point in enumerate(rectangle):
            rectangle_edge = (point, rectangle[(index + 1) % 4])
            if Geometry.two_lines_intersect(edge, rectangle_edge):
                return True
            
        return False

    @staticmethod
    def point_lies_within_rectangle(point, rectangle):
        
        all_x = []
        all_y = []

        for corner in rectangle:
            (x, y) = corner
            all_x.append(x)
            all_y.append(y)
        
        all_x.sort()
        all_y.sort()

        bottom_left = (all_x[0], all_y[-1])
        top_right = (all_x[-1], all_y[0])

        x = point[0]
        y = point[1]

        if (x > bottom_left[0] and x < top_right[0] and y < bottom_left[1] and y > top_right[1]): 
            return True

        return False