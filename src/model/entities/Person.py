
'''
This class models the agents, or people in our case. This class is a decendent of the Agent class of MESA. This class lacks quite a lot still.
'''

from mesa import Agent

from src.model.logic.Panic_Dynamic import Panic_Dynamic
from src.model.logic.Path_Finder import Path_Finder
from src.model.utils.Geometry import Geometry
from src.model.utils.Utilities import Utilities

import random
from src.model.logic.Theory_Of_Mind import Theory_Of_Mind as ToM

class Person(Agent):

    def __init__(self, unique_id, model, tom):

        super().__init__(unique_id, model)

        self.neighbout_radius = 40
        self.escaped = False
        # self.next_move = None
        
        self.panic = 0
        
        self.theory_of_mind = tom

    def prepare_path_finding(self):

        self.goal = self.determine_goal()
        self.path_finder.set_goal(self.pos, self.goal)

    def determine_goal(self):

        self.path_finder = Path_Finder(self.model.world_mesh)

        exits = [ exit.pos for exit in self.model.exits ]
        goal = Geometry.find_closest_point_of_set_of_points(self.pos, exits)

        if (self.theory_of_mind == 1):
            if ToM.agent_should_switch_goal(exits, self.pos, self.neighbors(), goal):
                for other_exit in exits:
                    if not other_exit == goal:
                        goal = other_exit
                        break
        
        return goal

    def step(self):

        if self.check_if_at_exit():
            return        

        self.move()

    def move(self):
        '''
        In order to move, the agent moves according to a path finding algorithm. This method is not finished yet, since it is very inefficient and unrealistic at this moment, though it makes for a demo.
        '''

        self.panic = Panic_Dynamic.change_panic_level(len(self.neighbors()), self.pos)

        if self.panic == 2:
            move = self.make_panic_move()
        else:
            move = self.make_normal_move()

        if not move == None:
            self.model.space.move_agent(self, move)
        
    def make_panic_move(self):

        direction = Panic_Dynamic.average_direction_of_crowd(self.neighbors(), self.pos, self)
        new_position = (self.pos[0] + direction[0], self.pos[1] + direction[1])
        move = self.path_finder.closest_node_except_one(new_position, self.pos)

        if self.check_if_next_move_is_clear(move):
            return move

        return None

    def make_normal_move(self):

        next_move = self.path_finder.get_next_step(self.pos)
        
        if next_move == None or next_move == []:
            return None

        delta_pos_x = next_move[0] - self.pos[0]
        delta_pos_y = next_move[1] - self.pos[1]

        move = (self.pos[0] + delta_pos_x, self.pos[1] + delta_pos_y)

        if self.check_if_next_move_is_clear(move):
            return move
        else:
            side_step = self.try_to_find_side_step_move(move)
            if not side_step == None:
                neighbors_positions = [ neighbor.pos for neighbor in self.neighbors() ]
                self.path_finder.plan_detour(side_step, self.goal, neighbors_positions)
                return side_step

        return None

    def try_to_find_side_step_move(self, denied_next_move):

        successors = self.path_finder.find_connected_nodes(self.pos)

        free_successors = []
        neighbors = self.neighbors()
        neighbors_positions = [ neighbor.pos for neighbor in neighbors ]

        for node in successors:
            if node in neighbors_positions:
                break
            else:
                free_successors += [ node ]

        if free_successors == []:
            return None

        minimum = (0, -1)

        for index, node in enumerate(free_successors):

            distance = Geometry.euclidean_distance(node, denied_next_move)

            if minimum[1] == -1:
                minimum = (index, distance)

            if minimum[1] > distance:
                minimum = (index, distance)

        return free_successors[minimum[0]]

    def neighbors(self):
        
        neighbors = []
        for agent in self.model.space.get_neighbors(self.pos, self.neighbout_radius):
            if not agent == self:
                neighbors.append(agent)

        return neighbors

    def check_if_next_move_is_clear(self, move):

        can_move = True
        for other_agent in self.neighbors():
            if move == other_agent.pos:
                can_move = False
        
        return can_move

    def check_if_at_exit(self):

        threshold = 30
        for exit in self.model.exits:
            
            distance = Geometry.euclidean_distance(exit.pos, self.pos)
            if distance < threshold:
                self.escaped = True
                self.model.schedule.remove(self)
                self.model.space.remove_agent(self)
                return True

        return False

