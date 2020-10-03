
from src.model.entities.Person import Person
from src.model.entities.Exit import Exit
from src.model.entities.Obstacle import Obstacle

from src.model.logic.Path_Finder import Path_Finder

from mesa import Model
from mesa.time import RandomActivation
from mesa.space import ContinuousSpace

class Model_Controller(Model):

    def __init__(self, N, width, height):
        self.num_agents = N
        self.space = ContinuousSpace(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True

        self.create_obstacles()
        self.create_exit()
        self.create_agent()

        self.path_finder = Path_Finder((width, height), self.obstacles, self.exits)
        self.path_finder.build_mesh()

    def create_agent(self):
        for i in range(self.num_agents):
            a = Person(i, self)
            self.space.place_agent(a, (40, 40))
            self.schedule.add(a)

    def create_exit(self):
        self.exits = {
            Exit(40, 460, True)
        }

    def create_obstacles(self):
        self.obstacles = {
            Obstacle((150,100), 300, 10),
            Obstacle((300,245), 10, 300),
            Obstacle((200,350), 10, 300)
        }

    def step(self):
        self.schedule.step()