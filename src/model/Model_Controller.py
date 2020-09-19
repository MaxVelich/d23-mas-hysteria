
from mesa import Model
from mesa.time import RandomActivation
from mesa.space import ContinuousSpace
from mesa.datacollection import DataCollector

from src.model.entities.Person import Person
from src.model.entities.Exit import Exit

class Model_Controller(Model):

    def __init__(self, N, width, height):
        self.num_agents = N
        self.space = ContinuousSpace(
            width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True

        self.create_agent()
        self.create_exit()

    def create_agent(self):
        for i in range(self.num_agents):
            a = Person(i, self)

            x = self.random.randrange(self.space.width)
            y = self.random.randrange(self.space.height)
            self.space.place_agent(a, (x, y))

            self.schedule.add(a)

    def create_exit(self):
        self.exits = {Exit(self.space.width / 2+50, self.space.height / 2, True)}

    def step(self):
        self.schedule.step()
