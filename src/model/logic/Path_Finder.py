
'''
This class is currently empty. Here we intend to provide the logic for the agents to find a path towards an exit. We intend to not only provide algorithms for the nearest path, but also alternative routes. 
'''

import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
import sys
from src.model.logic.A_star import A_Star
from src.model.utils.Utilities import Utilities

np.set_printoptions(threshold=sys.maxsize)

class Path_Finder:

    def __init__(self, world_dim, obstacles):
        self.world_dim = world_dim
        self.obstacles = obstacles

    def description(self):
        print("world_dim:", self.world_dim)
        print("obstacles:", self.obstacles)

    def build_mesh(self):

        points = []

        goal = (20, 480)
        points += [goal]

        for x in range(0,21):
            for y in range(0,21):
                points += [(x * 25, y * 25)]

        for obstacle in self.obstacles:
            points += obstacle.get_corner_points()

        self.points = np.array(points)
        tri = Delaunay(points)

        self.walkable_space = self.filter_triangles_leaving_walkable_space(tri.simplices, self.obstacles)

        # plt.triplot(self.points[:,0], self.points[:,1], self.walkable_space)
        # plt.plot(self.points[:,0], self.points[:,1], 'o')
        # plt.plot(self.path[:,0], self.path[:,1], 'o', markersize=15)
        # plt.show()

    def get_next_step(self, agent_position, goal = (20, 480)):

        nearest_point = self.find_nearest_mesh_point(agent_position)

        if nearest_point[0] == goal[0] and nearest_point[1] == goal[1]:
            return agent_position

        path = self.find_path((nearest_point[0], nearest_point[1]), goal)
        
        first_next_node = path[0]
        if agent_position[0] == first_next_node[0] and agent_position[1] == first_next_node[1]:
            next_point = path[1]
        else:
            next_point = first_next_node
        
        return next_point

    def find_nearest_mesh_point(self, point):

        distances = []
        for p in self.points:
            distance = Utilities.euclidean_distance(p, point)
            distances.append(distance)

        index_nearest_point = np.argmin(distances)

        return self.points[index_nearest_point]

    def find_path(self, start, goal):
        edges = self.prepare_edges_for_path_finding()
        a_star = A_Star(edges)
        return a_star.find_path(start, goal)

    def prepare_edges_for_path_finding(self):
        edges = np.empty([0,4])
        for triangle in self.walkable_space:
            for i in range(0,3):
                new_edge = np.array([ self.points[int(triangle[i])], self.points[int(triangle[(i+1) %3])] ])
                edges = np.append(edges, new_edge.reshape(-1,4), axis = 0)

        filtered = np.empty([0,4])
        for edge in edges:
            
            if filtered.size == 0:
                filtered = np.append(filtered, edge.reshape(-1,4), axis = 0)
                continue
            
            already_in_filtered = False
            for temp in filtered:
                
                if edge[0] == temp[2] and edge[1] == temp[3] and edge[2] == temp[0] and edge[3] == temp[1]:
                    already_in_filtered = True
                    break

            if not already_in_filtered:
                filtered = np.append(filtered, edge.reshape(-1,4), axis = 0)

        return filtered

    def filter_triangles_leaving_walkable_space(self, triangles, obstacles):
        
        filtered = np.empty([0,3])
        for triangle in triangles:
            if not self.check_if_triangle_intersects_with_any_obstacle(triangle, obstacles):
                filtered = np.append(filtered, triangle.reshape((-1,3)), axis = 0)

        return filtered

    def check_if_triangle_intersects_with_any_obstacle(self, triangle, obstacles):

        for obstacle in obstacles:
            if self.triangle_intersects_with_obstacle(triangle, obstacle):
                return True

        return False

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

        if (x > bottom_left[0] and x < top_right[0] and y < bottom_left[1] and y > top_right[1]): 
            return True

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

        if point[0] > xs[0] and point[0] < xs[-1]:
            if point[1] > ys[0] and point[1] < ys[-1]:
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
