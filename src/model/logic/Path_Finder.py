
'''
TODO: independence from numpy
TODO: dependency interjection
TODO: Utils functions to streamline
TODO: private functions
'''

import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
import sys
from src.model.logic.A_star import A_Star
from src.model.utils.Utilities import Utilities
from src.model.utils.Geometry import Geometry

class Path_Finder:

    def __init__(self, obstacles, exits):
        self.obstacles = obstacles
        self.exits = exits

    def build_mesh(self):

        self.points = np.array(self.prepare_nodes_of_graph())
        tri = Delaunay(self.points)

        self.walkable_space = self.filter_triangles_leaving_walkable_space(tri.simplices, self.obstacles)

        # plt.triplot(self.points[:,0], self.points[:,1], self.walkable_space)
        # plt.plot(self.points[:,0], self.points[:,1], 'o')
        # plt.show()

    def prepare_nodes_of_graph(self):
        nodes = []

        for x in range(0,21):
            for y in range(0,21):
                nodes += [(x * 25, y * 25)]

        for obstacle in self.obstacles:
            nodes += obstacle.get_corner_points()

        for exit in self.exits:
            nodes += [exit.pos]

        return nodes

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

            if Geometry.point_lies_within_rectangle(point, corners_of_obstacle):
                return True

            edge = (point, self.points[triangle[(index[0]+1) % 3]])
            if Geometry.edge_intersects_with_rectangle_edges(edge, corners_of_obstacle):
                return True

        return False