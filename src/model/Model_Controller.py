
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

        self.path_finder = Path_Finder((width, height), self.obstacles)
        self.path_finder.build_mesh()

    def create_agent(self):
        for i in range(self.num_agents):
            a = Person(i, self)
            self.space.place_agent(a, (400, 40)) 
            self.schedule.add(a)

    def create_exit(self):
        self.exits = {
            Exit(40, 460, True)
        }

    def create_obstacles(self):

        self.obstacles = [
            Obstacle((50,5), 100, 10),
            Obstacle((150,5), 100, 10),
            Obstacle((250,5), 100, 10),
            Obstacle((350,5), 100, 10),
            Obstacle((450,5), 100, 10),
            Obstacle((50,495), 100, 10),
            Obstacle((150,495), 100, 10),
            Obstacle((250,495), 100, 10),
            Obstacle((350,495), 100, 10),
            Obstacle((450,495), 100, 10),
            Obstacle((5,50), 10, 100),
            Obstacle((5,150), 10, 100),
            Obstacle((5,250), 10, 100),
            Obstacle((5,350), 10, 100),
            Obstacle((5,450), 10, 100),
            Obstacle((495,50), 10, 100),
            Obstacle((495,150), 10, 100),
            Obstacle((495,250), 10, 100),
            Obstacle((495,350), 10, 100),
            Obstacle((495,450), 10, 100)
        ]

        self.obstacles += [
            Obstacle((80,350), 150, 40),
            Obstacle((230,350), 150, 40),
            Obstacle((420,250), 150, 40),
            Obstacle((270,250), 150, 40),
            Obstacle((80,150), 150, 40),
            Obstacle((230,150), 150, 40)
        ]

    def step(self):
        self.schedule.step()