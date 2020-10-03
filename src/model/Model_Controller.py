
from src.model.entities.Person import Person
from src.model.entities.Exit import Exit
from src.model.entities.Hazard import Hazard

from mesa import Model
from mesa.time import RandomActivation
from mesa.space import ContinuousSpace


class Model_Controller(Model):

    def __init__(self, N, width, height):
        self.num_agents = N
        self.space = ContinuousSpace(width, height, True)
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
        self.exits = {
            Exit(self.space.width / 2, self.space.height / 2, True)
        }

    def step(self):
        self.schedule.step()

        # Stop the simulation once all agents have exited the building
        if len(self.schedule.agents) == 0:
            self.running = False
