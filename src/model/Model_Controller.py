
from src.model.entities.Person import Person
from src.model.entities.Exit import Exit
from src.model.entities.Hazard import Hazard
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

        self.path_finder = Path_Finder(self.obstacles, self.exits)
        self.path_finder.build_mesh()

    def create_agent(self):
        for i in range(self.num_agents):
            a = Person(i, self)
            self.space.place_agent(a, (40, 40)) 
            self.schedule.add(a)

    def create_exit(self):
        self.exits = {
            Exit(20, 480)
        }

    def create_obstacles(self):

        self.obstacles = [
            Obstacle((75,350), 150, 40),
            Obstacle((225,350), 150, 40),
            Obstacle((425,250), 150, 40),
            Obstacle((275,250), 150, 40),
            Obstacle((75,150), 150, 40),
            Obstacle((225,150), 150, 40)
        ]

    def step(self):
        self.schedule.step()

        # Stop the simulation once all agents have exited the building
        if len(self.schedule.agents) == 0:
            self.running = False
