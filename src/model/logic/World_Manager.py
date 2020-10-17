
from src.model.utils.Geometry import Geometry

import numpy as np

class World_Manager:

    def __init__(self, world_dim, obstacles, exits, mesh_size = 25):

        print("World Manager instantiated!")

        self.world_dim = world_dim
        self.obstacles = obstacles
        self.exits = exits
        self.mesh_size = mesh_size

    def build_mesh(self):
        '''
        In order to run A* on the world, we need to make state spaces discrete. We use Delaunay's algrithm in order to find triangles across all nodes. Then, we filter those triangle depending on if they fall on walkable space or not.
        '''

        self.nodes = self.__prepare_nodes_of_graph()

        from scipy.spatial import Delaunay
        triangles = Delaunay(self.nodes)

        self.walkable_space = self.__find_walkable_space(triangles.simplices, self.obstacles)

        # UNCOMMENT IF YOU WANT TO SEE THE MESH OF THE GRAPH
        # import matplotlib.pyplot as plt
        # self.nodes = np.array(self.nodes)
        # plt.triplot(self.nodes[:,0], self.nodes[:,1], self.walkable_space)
        # plt.plot(self.nodes[:,0], self.nodes[:,1], 'o')
        # plt.show()

        return (self.nodes, self.walkable_space)

    def __prepare_nodes_of_graph(self):
        '''
        Here we setup all nodes we need for the graph. We use 'artificial' nodes to cover empty space, the corner points of rectangle obstacles, and the exits' positions.
        '''

        nodes = []

        for x in range(0, int(self.world_dim[0] / self.mesh_size) + 1):
            for y in range(0, int(self.world_dim[1] / self.mesh_size) + 1):
                nodes += [(x * self.mesh_size, y * self.mesh_size)]

        for obstacle in self.obstacles:
            nodes += obstacle.get_corner_points()

        for exit in self.exits:
            nodes += [ exit.pos ]

        return nodes

    def __find_walkable_space(self, triangles, obstacles):
        '''
        If one of the triangles intersects with an obstacle we need to remove it so that the agent can't walk over it -- like a ghost. The two methods following this one are helper functions.
        '''
        
        filtered = np.empty([0,3])
        for triangle in triangles:
            if not self.__triangle_intersects_with_any_obstacle(triangle, obstacles):
                filtered = np.append(filtered, triangle.reshape((-1,3)), axis = 0)

        return filtered

    def __triangle_intersects_with_any_obstacle(self, triangle, obstacles):

        for obstacle in obstacles:
            if self.__triangle_intersects_with_obstacle(triangle, obstacle):
                return True

        return False

    def __triangle_intersects_with_obstacle(self, triangle, obstacle):

        for index, point in np.ndenumerate(triangle):
            
            corners_of_obstacle = obstacle.get_corner_points()
            point = self.nodes[point]

            if Geometry.point_lies_within_rectangle(point, corners_of_obstacle):
                return True

            edge = (point, self.nodes[triangle[(index[0]+1) % 3]])
            if Geometry.edge_intersects_with_rectangle_edges(edge, corners_of_obstacle):
                return True

        return False