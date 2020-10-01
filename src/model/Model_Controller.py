
from src.model.entities.Person import Person
from src.model.entities.Exit import Exit
from src.model.entities.Obstacle import Obstacle

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
        self.create_obstacles()
        self.create_exit()

    def create_agent(self):
        for i in range(self.num_agents):
            a = Person(i, self)

            self.space.place_agent(a, (20, 20))

            self.schedule.add(a)

    def create_exit(self):
        self.exits = {
            Exit(480, 480, True)
        }

    def create_obstacles(self):
        self.obstacles = {
            Obstacle((150,100), 150, 100),
            Obstacle((350,200), 150, 100),
            Obstacle((110,260), 100, 150)
        }

    def step(self):
        self.schedule.step()
