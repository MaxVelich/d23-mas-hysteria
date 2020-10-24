
'''
This class is responsible for managing the path finding of the agents. We discretize/quantize the continuous space here, and then run A* on the resulting walkable (since we have obstacles) graph.

This class still has a long way to go! Currently, we recalculate the route for each agent after each step -> Very bad for performance
'''

from src.model.logic.A_star import A_Star
from src.model.utils.Geometry import Geometry

import numpy as np

class Path_Finder:

    def __init__(self, world_mesh):
        self.nodes, self.edges = world_mesh

    def set_goal(self, current_pos, goal):

        print("new goal " + str(goal) + " has been set --- recalculating route...")
        self.plan = self.__find_path(current_pos, goal, self.edges)

    def get_next_step(self, agent_position):
        '''
        This will not make it in the final version. It produces the next step an agent should take in order to find an exit. Here, we basically run A* on the graph we generate above. Then we try to match the agent's position to the next nearest node on the graph, then we run A*.
        '''

        nearest_point = self.__find_nearest_mesh_point(agent_position)
        
        first_next_node = self.plan[0]
        rounded = (round(first_next_node[0], 0), round(first_next_node[1], 0))

        if agent_position[0] == rounded[0] and agent_position[1] == rounded[1]:
            self.plan.pop(0)
            next_point = self.plan[0]
        else:
            next_point = first_next_node

        return (round(next_point[0], 0), round(next_point[1], 0))

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