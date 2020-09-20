
'''
This class models the agents, or people in our case. This class is a decendent of the Agent class of MESA.
'''

from mesa import Agent
import random

class Person(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.panic = 0

    def step(self):
        self.move()
        if self.checkIfAtExit():
            self.model.schedule.remove(self)

        neighbourRadius = 40
        nearbyAgents = self.model.space.get_neighbors(self.pos, neighbourRadius)

        if len(nearbyAgents) > 3:
            self.panic = 1
        if len(nearbyAgents) > 7:
            self.panic = 2

    def move(self):
        speed = 1

        if self.pos[0] < self.model.space.width / 2:
            self.model.space.move_agent(
                self, (self.pos[0] + speed, self.pos[1]))
        if self.pos[1] < self.model.space.height / 2:
            self.model.space.move_agent(
                self, (self.pos[0], self.pos[1] + speed))
        if self.pos[0] > self.model.space.width / 2:
            self.model.space.move_agent(
                self, (self.pos[0] - speed, self.pos[1]))
        if self.pos[1] > self.model.space.height / 2:
            self.model.space.move_agent(
                self, (self.pos[0], self.pos[1] - speed))

    def checkIfAtExit(self):
        threshold = 4
        for exit in self.model.exits:
            if abs(self.pos[0] - exit.x) < threshold and abs(self.pos[1] - exit.y) < threshold:
                if exit.avail:
                    return True
        return False

    def check_if_move_possible(in_direction):
        return True
