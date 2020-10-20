
'''
This is a controller class, so many part of the functionality of this program are connected here. Currently, it does not do too much, except creating the environment, populating it and instantiating a bunch of important objects (e.g. Path_Finder).
'''

from src.model.entities.Person import Person
from src.model.entities.Exit import Exit
from src.model.entities.Hazard import Hazard
from src.model.entities.Obstacle import Obstacle

from src.model.logic.Path_Finder import Path_Finder
from src.model.logic.World_Manager import World_Manager

from src.model.utils.Geometry import Geometry

from mesa import Model
from mesa.time import RandomActivation
from mesa.space import ContinuousSpace

import random

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

        random_unique_positions = []
        not_done = True
        while not_done:
            x_pos = random.randint(20, 480)
            y_pos = random.randint(20, 55)
            new_point = (x_pos, y_pos)

            not_allowed = False
            for p in random_unique_positions:
                dist = Geometry.euclidean_distance(new_point, p)
                if dist <= 16:
                    not_allowed = True

            if not not_allowed:
                random_unique_positions.append(new_point)

            if len(random_unique_positions) == 0:
                random_unique_positions.append(new_point)

            if len(random_unique_positions) == self.num_agents:
                not_done = False


        for i in range(self.num_agents):
            a = Person(i, self)
            
            self.space.place_agent(a, random_unique_positions[i])

            a.prepare_path_finding()
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
