
'''
This class models the agents, or people in our case. This class is a decendent of the Agent class of MESA. This class lacks quite a lot still.
'''

from mesa import Agent
from src.model.logic.Panic_Dynamic import Panic_Dynamic
from src.model.logic.Path_Finder import Path_Finder
from src.model.utils.Geometry import Geometry

import random
from src.model.logic.Theory_Of_Mind import Theory_Of_Mind as ToM

class Person(Agent):

    def __init__(self, unique_id, model, tom):

        super().__init__(unique_id, model)
        self.panic = 0
        self.velocity = 1
        self.speed = 5
        self.vision = 40
        self.next_move = None
        self.theory_of_mind = tom # 0 = ToM0, 1 = ToM1
        self.escaped = False

    def prepare_path_finding(self):

        self.path_finder = Path_Finder(self.model.world_mesh)

        exits = [ exit.pos for exit in self.model.exits ]
        self.goal = Geometry.find_closest_point_of_set_of_points(self.pos, exits)

        if (self.theory_of_mind == 1):
            print("my ToM level is: " + str(self.theory_of_mind))
            print("I have " + str(len(self.neighbors())) + " neighbors")

            if ToM.agent_should_switch_goal(exits, self.pos, self.neighbors(), self.goal):
                for other_exit in exits:
                    if not other_exit == self.goal:
                        self.goal = other_exit
                        break

        self.path_finder.set_goal(self.pos, self.goal)

    def step(self):

        if self.check_if_at_exit():
            return

        self.panic, self.speed = Panic_Dynamic.change_panic_level(len(self.neighbors()), self.model.hazards, self.pos, self.vision)

        if self.panic == 2:
            self.velocity = Panic_Dynamic.cohere(self.neighbors(), self.pos, self)

        self.move()

    def move(self):

        '''
        In order to move, the agent moves according to a path finding algorithm. This method is not finished yet, since it is very inefficient and unrealistic at this moment, though it makes for a demo.
        '''

        if self.panic == 2:
            panic_move = self.make_panic_move()
            if self.check_if_next_move_is_clear(panic_move):
                self.model.space.move_agent(self, panic_move)
        else: 
            normal_move = self.make_normal_move()
            if self.check_if_next_move_is_clear(normal_move):
                self.model.space.move_agent(self, normal_move)

    def make_panic_move(self):
        new_position = (self.pos[0] + self.velocity[0], self.pos[1] + self.velocity[1])
        closest_node = self.path_finder.closest_node_except_one(new_position, self.pos)
        return closest_node

    def make_normal_move(self):
        if self.next_move is None:
            self.next_move = self.path_finder.get_next_step(self.pos)

        if self.next_move[0] == self.pos[0] and self.next_move[1] == self.pos[1]:
            self.next_move = self.path_finder.get_next_step(self.pos)

        delta_pos_x = self.next_move[0] - self.pos[0]
        delta_pos_y = self.next_move[1] - self.pos[1]

        return (self.pos[0] + delta_pos_x * self.speed, self.pos[1] + delta_pos_y * self.speed)

    def neighbors(self):
        
        neighbors = []
        for agent in self.model.space.get_neighbors(self.pos, self.vision):
            if not agent == self:
                neighbors.append(agent)

        return neighbors

    def check_if_next_move_is_clear(self, current_position):

        can_move = True
        for other_agent in self.neighbors():
            if current_position == other_agent.pos:
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

