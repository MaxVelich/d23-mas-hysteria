
'''
This is a controller class, so many part of the functionality of this program are connected here. Currently, it does not do too much, except creating the environment, populating it and instantiating a bunch of important objects (e.g. Path_Finder).
'''

from src.model.entities.Person import Person
from src.model.entities.Exit import Exit
from src.model.entities.Hazard import Hazard
from src.model.entities.Obstacle import Obstacle

from src.model.logic.Path_Finder import Path_Finder
from src.model.logic.World_Manager import World_Manager

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

        self.world_manager = World_Manager((width, height), self.obstacles, self.exits)
        self.world_mesh = self.world_manager.build_mesh()

        self.create_agent()

    def create_agent(self):

        for i in range(self.num_agents):
            a = Person(i, self)
            self.space.place_agent(a, (20*(i+1), 40))
            a.prepare_path_finding()
            self.schedule.add(a)

    def create_exit(self):
        self.exits = {
            Exit(20, 480),
            Exit(480, 480)
        }

    def create_obstacles(self):

        self.obstacles = [
            Obstacle((95,350), 190, 40),
            Obstacle((405,350), 190, 40),
            Obstacle((425,250), 150, 40),
            Obstacle((75,250), 150, 40),
            Obstacle((75,150), 150, 40),
            Obstacle((425,150), 150, 40)
        ]

    def step(self):
        self.schedule.step()

        # Stop the simulation once all agents have exited the building
        if len(self.schedule.agents) == 0:
            self.running = False
