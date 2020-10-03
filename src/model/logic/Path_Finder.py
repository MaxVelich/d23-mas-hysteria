
'''
This class is currently empty. Here we intend to provide the logic for the agents to find a path towards an exit. We intend to not only provide algorithms for the nearest path, but also alternative routes. 
'''

import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay

class Path_Finder:

    def __init__(self, world_dim, obstacles, exits):
        self.world_dim = world_dim
        self.obstacles = obstacles
        self.exits = exits

    def description(self):
        print("world_dim:", self.world_dim)
        print("obstacles:", self.obstacles)
        print("exits:", self.exits)

    def build_mesh(self):

        points = [
            (0,0), (0, 99), (0, 199), (0, 299), (0, 399), (0, 499),
            (99, 0), (199, 0), (299, 0), (399, 0), (499, 0),
            (99, 499), (199, 499), (299, 499), (399, 499), (499, 499),
            (499,0), (499, 99), (499, 199), (499, 299), (499, 399)
        ]
        # points = []
        for obstacle in self.obstacles:
            points += obstacle.get_corner_points()

        self.points = np.array(points)
        tri = Delaunay(points)

        print(self.points.shape)

        walkable_space = self.filter_triangles_leaving_walkable_space(tri.simplices, self.obstacles)
        print(len(walkable_space))
        
        print(tri.simplices.shape)
        print(walkable_space.shape)

        plt.triplot(self.points[:,0], self.points[:,1], walkable_space)
        plt.plot(self.points[:,0], self.points[:,1], 'o')
        plt.show()

    def filter_triangles_leaving_walkable_space(self, triangles, obstacles):
        
        filtered = np.empty([0,3])
        for triangle in triangles:
            for obstacle in obstacles:
                if not self.triangle_intersects_with_obstacle(triangle, obstacle):
                    filtered = np.append(filtered, triangle.reshape((-1,3)), axis = 0)
                else:
                    break
        
        return filtered

    def triangle_intersects_with_obstacle(self, triangle, obstacle):

        for index, point in np.ndenumerate(triangle):
            
            corners_of_obstacle = obstacle.get_corner_points()
            point = self.points[point]

            if self.point_lies_in_rectangle(point, corners_of_obstacle):
                return True

            edge = (point, self.points[triangle[(index[0]+1) % 3]])
            if self.edge_intersects_with_rectangle_edges(edge, corners_of_obstacle):
                return True

        return False

    def point_lies_in_rectangle(self, point, rectangle):

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

        if (x > bottom_left[0] and x < top_right[0] and y > bottom_left[1] and y < top_right[1]): 
            return True
        else: 
            return False

        return False

    def edge_intersects_with_rectangle_edges(self, edge, rectangle):

        for index, point in enumerate(rectangle):
            rectangle_edge = (point, rectangle[(index + 1) % 4])
            if self.check_if_two_lines_intersect(edge, rectangle_edge):
                return True
            
        return False


    def check_if_two_lines_intersect(self, line_1, line_2):

        intersection = self.get_intersection_of_two_lines(line_1, line_2)
        if intersection == False:
            return False
            
        intersection_with_line_1 = self.check_if_point_lies_on_line(intersection, line_1)
        intersection_with_line_2 = self.check_if_point_lies_on_line(intersection, line_2)

        if intersection_with_line_1 and intersection_with_line_2:
            return True

        return False

    def check_if_point_lies_on_line(self, point, line):

        is_on_line = False

        x_1, y_1 = line[0]
        x_2, y_2 = line[1]

        xs = [x_1, x_2]
        xs.sort()
        ys = [y_1, y_2]
        ys.sort()

        if point[0] >= xs[0] and point[0] <= xs[-1]:
            if point[1] >= ys[0] and point[1] <= ys[-1]:
                is_on_line = True

        return is_on_line

    def get_intersection_of_two_lines(self, line_1, line_2):
        
        k_1, d_1 = self.get_line_parameters_through_points(line_1[0], line_1[1])
        k_2, d_2 = self.get_line_parameters_through_points(line_2[0], line_2[1]) 

        if k_1 == k_2:
            return False

        x_intersect = (d_2 - d_1) / (k_1 - k_2)
        y_intersect = (k_1 * x_intersect) + d_1
        return (x_intersect, y_intersect)

    def get_line_parameters_through_points(self, point_1, point_2):

        x_1, y_1 = point_1
        x_2, y_2 = point_2

        denominator = (x_2 - x_1)
        if denominator == 0:
            k = 0
        else:
            k = (y_2 - y_1) / denominator

        d = y_1 - (k * x_1)

        return (k, d)

