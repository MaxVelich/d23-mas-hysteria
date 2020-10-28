
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
        # 0 = ToM0, 1 = ToM1
        self.theory_of_mind = tom
        self.escaped = False
        self.threshold = model.panic_threshold

    def prepare_path_finding(self):

        self.path_finder = Path_Finder(self.model.world_mesh)
        self.goal = self.path_finder.find_goal(self.pos, None)
        if self.theory_of_mind == 1:
            # print("my ToM level is: " + str(self.theory_of_mind))
            neighbors = self.model.space.get_neighbors(self.pos, self.vision)
            # print("I have " + str(len(neighbors)) + " neighbors")
            if len(neighbors) > 2:
                self.goal = ToM.determine_neighbor_exit_strategy(self.path_finder, self.pos, neighbors, self.goal)

        self.path_finder.set_goal(self.pos, self.goal)

        self.in_motion = False

    def step(self):

        if self.check_if_at_exit():
            self.escaped = True
            if self.theory_of_mind == 0:
                self.model.regular_times.append(self.model.get_time(self.model))
            else:
                self.model.tom_times.append(self.model.get_time(self.model))
            self.model.schedule.remove(self)
            self.model.space.remove_agent(self)
            return

        self.near_by_agents = self.model.space.get_neighbors(self.pos, self.vision)

        self.move()


        # self.panic, self.speed = Panic_Dynamic.change_panic_level(len(self.near_by_agents))

        self.panic, self.speed = Panic_Dynamic.change_panic_level(len(self.near_by_agents), self.model.hazards, self.pos, self.vision, self.threshold)

        if self.panic == 2:
            self.velocity = Panic_Dynamic.cohere(self.near_by_agents, self.pos, self)

        # TODO: Dynamic goal changing based on Theory of Mind

    def move(self):

        '''
        In order to move, the agent moves according to a path finding algorithm. This method is not finished yet, since it is very inefficient and unrealistic at this moment, though it makes for a demo.
        '''

        if self.panic == 2:
            new_position = (self.pos[0] + self.velocity[0], self.pos[1] + self.velocity[1])
            closest_node = self.path_finder.closest_node_except_one(new_position, self.pos)
            
            can_move = True
            for other_agent in self.near_by_agents:
                if not other_agent == self:
                    
                    if closest_node == other_agent.pos:
                        can_move = False

            if can_move:
                self.model.space.move_agent(self, closest_node)
            
        else: 
            if self.next_move is None:
                self.next_move = self.path_finder.get_next_step(self.pos)

            if self.next_move[0] == self.pos[0] and self.next_move[1] == self.pos[1]:
                self.next_move = self.path_finder.get_next_step(self.pos)
                self.in_motion = False

            delta_pos_x = self.next_move[0] - self.pos[0]
            delta_pos_y = self.next_move[1] - self.pos[1]

            self.speed = 1
            new_position = (self.pos[0] + delta_pos_x * self.speed, self.pos[1] + delta_pos_y * self.speed)
            
            can_move = True
            for other_agent in self.near_by_agents:
                if not other_agent == self:
                    
                    if new_position == other_agent.pos:
                        can_move = False

            if can_move:
                self.model.space.move_agent(self, new_position)
            else:
                self.do_sidestep()

    def do_sidestep(self):

        delta_pos_x = self.next_move[0] - self.pos[0]
        delta_pos_y = self.next_move[1] - self.pos[1]
        new_position = (self.pos[0] + delta_pos_x * -1, self.pos[1] + delta_pos_y * -1)

        can_move = True
        for other_agent in self.near_by_agents:
            if not other_agent == self:
                
                if new_position == other_agent.pos:
                    can_move = False

        if can_move:
            self.model.space.move_agent(self, new_position)


    def check_if_at_exit(self):

        threshold = 30
        for exit in self.model.exits:
            
            distance = Geometry.euclidean_distance(exit.pos, self.pos)
            if distance < threshold:
                return True

        return False

