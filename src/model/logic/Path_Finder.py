
'''
This class is responsible for managing the path finding of the agents. We discretize/quantize the continuous space here, and then run A* on the resulting walkable (since we have obstacles) graph.

This class still has a long way to go! Currently, we recalculate the route for each agent after each step -> Very bad for performance
'''

from src.model.logic.A_star import A_Star
from src.model.utils.Geometry import Geometry

import numpy as np

class Path_Finder:

    def __init__(self, world_dim, obstacles, exits, mesh_size = 25):
        self.world_dim = world_dim
        self.obstacles = obstacles
        self.exits = exits
        self.mesh_size = mesh_size

    ### PUBLIC INTERFACE

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

    def get_next_step(self, agent_position, goal = (20, 480)):
        '''
        This will not make it in the final version. It produces the next step an agent should take in order to find an exit. Here, we basically run A* on the graph we generate above. Then we try to match the agent's position to the next nearest node on the graph, then we run A*.
        '''

        nearest_point = self.__find_nearest_mesh_point(agent_position)

        if nearest_point[0] == goal[0] and nearest_point[1] == goal[1]:
            return agent_position

        path = self.__find_path((nearest_point[0], nearest_point[1]), goal)
        
        first_next_node = path[0]
        if agent_position[0] == first_next_node[0] and agent_position[1] == first_next_node[1]:
            next_point = path[1]
        else:
            next_point = first_next_node
        
        return next_point

    ### PRIVATE INTERFACE

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

    def __find_nearest_mesh_point(self, point):
        '''
        We need to first let the agent 'get on the grid'. Therefore, we find the nearest node on the graph here.
        '''

        distances = []
        for p in self.nodes:
            distance = Geometry.euclidean_distance(p, point)
            distances += [distance]

        index_nearest_point = np.argmin(distances)

        return self.nodes[index_nearest_point]

    def __find_path(self, start, goal):
        '''
        Here we run A* on the graph, though A* itself is in a separate class.
        '''

        edges = self.__prepare_edges_for_path_finding()
        a_star = A_Star(edges)
        return a_star.find_path(start, goal)

    def __prepare_edges_for_path_finding(self):
        '''
        From the Delaunay method, we find triangles. Though, we need to convert these into edges (i.e. [point_1, point_2]). Also, we can remove bidirectional-duplicates, since we we do not have any directed edges (i.e. [point_1,point_2] == [point_2, point_1]).
        '''

        edges = []
        for triangle in self.walkable_space:
            for i in range(0,3):
                first_node = self.nodes[int(triangle[i])]
                second_node = self.nodes[int(triangle[(i+1) % 3])]
                edges += [ [first_node[0], first_node[1], second_node[0], second_node[1] ] ]

        filtered = []
        for edge in edges:
            
            if len(filtered) == 0:
                filtered += [edge]
                continue
            
            already_in_filtered = False
            for temp in filtered:
                
                if edge[0] == temp[2] and edge[1] == temp[3] and edge[2] == temp[0] and edge[3] == temp[1]:
                    already_in_filtered = True
                    break

            if not already_in_filtered:
                filtered += [edge]

        return filtered
