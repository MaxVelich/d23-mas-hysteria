
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
        speed = self.speed

        if self.pos[0] < self.model.space.width / 2:
            self.model.space.move_agent(
                self, (self.pos[0] + self.velocity * speed, self.pos[1]))
        if self.pos[1] < self.model.space.height / 2:
            self.model.space.move_agent(
                self, (self.pos[0], self.pos[1] + self.velocity * speed))
        if self.pos[0] > self.model.space.width / 2:
            self.model.space.move_agent(
                self, (self.pos[0] - self.velocity * speed, self.pos[1]))
        if self.pos[1] > self.model.space.height / 2:
            self.model.space.move_agent(
                self, (self.pos[0], self.pos[1] - self.velocity * speed))

    def checkIfAtExit(self):
        threshold = 4
        for exit in self.model.exits:
            if abs(self.pos[0] - exit.x) < threshold and abs(self.pos[1] - exit.y) < threshold:
                if exit.available:
                    return True
        return False

    def check_if_move_possible(in_direction):
        return True
