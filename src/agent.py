from mesa import Agent
import random


class PersonAgent(Agent):
    """ An agent with fixed initial wealth."""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.panic = random.randint(1, 3)

    def step(self):
        self.move()

    def move(self):

        new_position = (self.pos[0] + 1, self.pos[1] + 2)
        self.model.space.move_agent(self, new_position)
