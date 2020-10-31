
'''
This class is responsible for managing the path finding of the agents. We discretize/quantize the continuous space here, and then run A* on the resulting walkable (since we have obstacles) graph.

This class still has a long way to go! Currently, we recalculate the route for each agent after each step -> Very bad for performance
'''

from src.model.logic.A_star import A_Star
from src.model.utils.Geometry import Geometry
from src.model.utils.Utilities import Utilities

import numpy as np

class Path_Finder:

    def __init__(self, world_mesh):
        self.nodes, self.edges = world_mesh

    def set_goal(self, current_pos, goal):

        print("new goal " + str(goal) + " has been set --- recalculating route...")
        self.plan = self.__find_path(current_pos, goal, self.edges)

    def plan_detour(self, current_pos, goal, except_set_of_nodes):

        filtered_edges = []

        for edge in self.edges:

            include_edge = True
            for node in except_set_of_nodes:

                edge_point_1 = (edge[0], edge[1])
                edge_point_2 = (edge[2], edge[3])

                if Utilities.check_if_points_are_approximately_the_same(edge_point_1, node):
                    include_edge = False
                elif Utilities.check_if_points_are_approximately_the_same(edge_point_2, node):
                    include_edge = False
            
            if include_edge:
                filtered_edges += [ edge ]

        self.plan = self.__find_path(current_pos, goal, filtered_edges)
    
    def try_to_find_side_step_move(self, position, denied_next_move, neighbors_positions):

        nearest_point = self.__find_nearest_mesh_point(position)
        successors = self.find_connected_nodes(nearest_point)
        free_successors = []

        for node in successors:
            if node in neighbors_positions:
                break
            else:
                free_successors += [ node ]

        if free_successors == []:
            return None

        closest_successor = Utilities.find_closest_point_of_set_of_points(denied_next_move, free_successors)
        return closest_successor

    def get_next_step(self, agent_position):
        '''
        This will not make it in the final version. It produces the next step an agent should take in order to find an exit. Here, we basically run A* on the graph we generate above. Then we try to match the agent's position to the next nearest node on the graph, then we run A*.
        '''

        if self.plan == None:
            return None

        nearest_point = self.__find_nearest_mesh_point(agent_position)
        first_next_node = self.plan[0]

        if Utilities.check_if_points_are_approximately_the_same(agent_position, first_next_node):
            self.plan.pop(0)
            next_point = self.plan[0]
        else:
            next_point = first_next_node

        return next_point

    def find_connected_nodes(self, from_position):

        successors = []
        for edge in self.edges:
            
            edge_point_1 = (edge[0], edge[1])
            edge_point_2 = (edge[2], edge[3])

            if Utilities.check_if_points_are_approximately_the_same(edge_point_1, from_position):
                successors += [ edge_point_2 ]
            elif Utilities.check_if_points_are_approximately_the_same(edge_point_2, from_position):
                successors += [ edge_point_1 ]

        return list(set(successors))

    ### PRIVATE INTERFACE

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

    def __find_path(self, start, goal, edges):
        '''
        Here we run A* on the graph, though A* itself is in a separate class.
        '''
        
        start = self.__find_nearest_mesh_point(start)
        
        a_star = A_Star(edges)
        path = a_star.find_path(start, goal)

        return path