
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
        edges = self.__prepare_edges_for_path_finding()

        return (self.nodes, edges)

    def visualize_mesh(self):

        import matplotlib.pyplot as plt
        self.nodes = np.array(self.nodes)
        plt.triplot(self.nodes[:,0], self.nodes[:,1], self.walkable_space)
        plt.plot(self.nodes[:,0], self.nodes[:,1], 'o')
        plt.show()

    def __prepare_nodes_of_graph(self):
        '''
        Here we setup all nodes we need for the graph. We use 'artificial' nodes to cover empty space, the corner points of rectangle obstacles, and the exits' positions.
        '''

        nodes = []
        offset = self.mesh_size / 2

        for x in range(0, int(self.world_dim[0] / self.mesh_size) + 1):
            for y in range(0, int(self.world_dim[1] / self.mesh_size) + 1):

                node_x = x * self.mesh_size
                node_y = y * self.mesh_size

                nodes += [(node_x, node_y)]
                
                if node_x + offset < self.world_dim[0]:
                    if node_y + offset < self.world_dim[1]:
                        nodes += [(node_x + offset, node_y + offset)]

        nodes_to_remove = []
        for obstacle in self.obstacles:
            for node in nodes:
                if self.__check_if_node_is_within_obstacle(node, obstacle):
                    nodes_to_remove += [node]

        for removable_node in nodes_to_remove:
            if removable_node in nodes:
                nodes.remove(removable_node)

        return nodes

    def __check_if_node_is_within_obstacle(self, node, obstacle):

        corner_points = obstacle.get_corner_points()
        if Geometry.point_lies_within_rectangle(node, corner_points):
            return True

        return False

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