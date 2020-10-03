
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

        points = np.array(points)
        tri = Delaunay(points)

        walkable_space = self.filter_triangles_leaving_walkable_space(tri.simplices, self.obstacles)
        print(walkable_space)
        
        # plt.triplot(points[:,0], points[:,1], tri.simplices)
        # plt.plot(points[:,0], points[:,1], 'o')
        # plt.show()

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

            if self.point_lies_in_rectangle(point, corners_of_obstacle):
                return True

            if self.edge_intersects_with_rectangle_edges((point, triangle[index[0] % 3]), corners_of_obstacle):
                return True

        return False

    def point_lies_in_rectangle(self, point, rectangle):
        return False

    def edge_intersects_with_rectangle_edges(self, edge, rectangle):
        return False
