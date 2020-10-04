
'''
This class models the agents, or people in our case. This class is a decendent of the Agent class of MESA.
'''

from mesa import Agent
from ..logic.Panic_Dynamic import Panic_Dynamic

import random
import numpy as np

class Person(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.panic = 0
        self.velocity = 1
        self.speed = 1.0
        self.vision = 40
        self.next_move = None

    def step(self):
        nearbyAgents = self.model.space.get_neighbors(self.pos, self.vision)

        self.move()

        if self.checkIfAtExit():
            self.model.schedule.remove(self)
        else:
            self.panic, self.speed = Panic_Dynamic.change_panic_level(len(nearbyAgents))
            if self.panic == 2:
                self.velocity = Panic_Dynamic.cohere(nearbyAgents, self.pos, self) / 2

    def move(self):

        if self.next_move is None:
            self.next_move = self.model.path_finder.get_next_step(self.pos)

        if self.next_move[0] == self.pos[0] and self.next_move[1] == self.pos[1]:
            self.next_move = self.model.path_finder.get_next_step(self.pos)
        
        delta_pos_x = self.next_move[0] - self.pos[0]
        delta_pos_y = self.next_move[1] - self.pos[1]
        
        if delta_pos_x < 0:
            delta_x = -1
        elif delta_pos_x > 0:
            delta_x = 1
        else:
            delta_x = 0

        if delta_pos_y < 0:
            delta_y = -1
        elif delta_pos_y > 0:
            delta_y = 1
        else:
            delta_y = 0

        self.model.space.move_agent(self, (self.pos[0] + delta_x*5, self.pos[1] + delta_y*5))


    def checkIfAtExit(self):
        threshold = 4
        for exit in self.model.exits:
            if abs(self.pos[0] - exit.x) < threshold and abs(self.pos[1] - exit.y) < threshold:
                if exit.available:
                    return True
        return False

    def check_if_move_possible(in_direction):
        return True
