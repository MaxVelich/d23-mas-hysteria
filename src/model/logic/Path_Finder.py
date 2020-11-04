
'''
This class is responsible for managing the path finding of the agents. We discretize/quantize the continuous space here, and then run A* on the resulting walkable (since we have obstacles) graph. This class also offers different ways to find alternative routes around obstacles, hazards and other agents. It also offers panick-y side-step ways to quickly get out of a stuck situation. 
'''

from src.model.logic.A_star import A_Star
from src.model.utils.Geometry import Geometry
from src.model.utils.Utilities import Utilities

import numpy as np

class Path_Finder:

    def __init__(self, world_mesh):
        self.nodes, self.edges = world_mesh

    def set_goal(self, current_pos, goal):
        '''
        When a goal is set, the agent plans the route. This function can also be used to replan a route with a new goal.
        '''

        self.plan = self.__find_path(current_pos, goal, self.edges)

    def plan_detour(self, current_pos, goal, except_set_of_nodes):
        '''
        This function acts similar to the above, however it first removes a set of nodes (and their edges) from the set of possible nodes. This way, the agent can plan around e.g. other agents.
        '''

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

    def replan_around_hazard(self, agent_position, goal, hazard):
        '''
        Also, similar to the above function, but this method removes the nodes and edges that lie within the danger radius of the hazard first, and then calculates the route.
        '''
        
        danger_radius = hazard.danger_radius()

        filtered_nodes = []
        for node in self.nodes:
            if Geometry.point_lies_in_circle(node, hazard.pos, danger_radius):
                filtered_nodes += [ node ]

        self.plan_detour(agent_position, goal, filtered_nodes)
    
    def try_to_find_side_step_move(self, position, denied_next_move, neighbors_positions):
        '''
        This function represents a quick detour alternative. The agent does not plan a new router, instead it just makes a side step if one is possible, and then persues its original plan. 
        '''

        nearest_point = self.__find_nearest_mesh_point(position)
        successors = self.__find_connected_nodes(nearest_point)
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

    ### PRIVATE INTERFACE

    def __find_connected_nodes(self, from_position):
        '''
        Find all nodes that are connected to the position (from_position).
        '''

        successors = []
        for edge in self.edges:
            
            edge_point_1 = (edge[0], edge[1])
            edge_point_2 = (edge[2], edge[3])

            if Utilities.check_if_points_are_approximately_the_same(edge_point_1, from_position):
                successors += [ edge_point_2 ]
            elif Utilities.check_if_points_are_approximately_the_same(edge_point_2, from_position):
                successors += [ edge_point_1 ]

        return list(set(successors))

    def __find_nearest_mesh_point(self, point):
        '''
        We need to let the agents 'get on the grid'. Therefore, we find the nearest node on the graph here.
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