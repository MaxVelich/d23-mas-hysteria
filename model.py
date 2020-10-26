
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

from mesa.datacollection import DataCollector

import matplotlib.pyplot as plt
import time

import numpy as np

class Model_Controller(Model):

    def __init__(self, N, width, height):
        self.num_agents = N
        self.space = ContinuousSpace(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True
        self.time = 0
        self.exits = []
        self.obstacles = []
        self. hazards = []

        self.create_obstacles()
        self.create_exit()
        self.create_hazard()

        self.world_manager = World_Manager((width, height), self.obstacles, self.exits)
        self.world_mesh = self.world_manager.build_mesh()
        self.datacollector = DataCollector(
            {
                "Active": lambda m: self.count_active_agents(m, False),
                "Escaped": lambda m: self.count_active_agents(m, True),
                "Low Panic": lambda m: self.count_panic(m, 0),
                "Medium Panic": lambda m: self.count_panic(m, 1),
                "High Panic": lambda m: self.count_panic(m, 2),
                "ToM0": lambda m: self.count_tom(m, 0),
                "ToM1": lambda m: self.count_tom(m, 1)
            }
        )

        self.create_agent()

    def create_agent(self):

        random_unique_positions = []
        not_done = True
        while not_done:
            x_pos = random.randint(20, 350)
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
            # add theory of mind (or lack thereof) when agent is being created
            tom = 0
            if random.random() <= 0.2:
                tom = 1
            a = Person(i, self, tom)
            self.space.place_agent(a, (20*(i+1), 40))
            a.prepare_path_finding()
            self.schedule.add(a)

    def create_exit(self):
        self.exits = [
            Exit(34.5, 494.5),
            #Exit(240, 480),
            Exit(448.5, 494.5)
        ]

    def create_obstacles(self):

        # self.obstacles = [
        #     Obstacle((95,350), 190, 40),
        #     Obstacle((405,350), 190, 40),
        #     Obstacle((425,250), 150, 40),
        #     Obstacle((75,250), 150, 40),
        #     Obstacle((75,150), 150, 40),
        #     Obstacle((425,150), 150, 40)
        # ]

        self.obstacles = [
            Obstacle((95,350), 190, 40),
            Obstacle((405,350), 190, 40),
            Obstacle((425,250), 150, 40),
            Obstacle((75,250), 150, 40),
            Obstacle((75,150), 150, 40),
            Obstacle((225,150), 150, 40),
            # Obstacle((450,375), 150, 250),
            # Obstacle((450,125), 150, 250),
            # Obstacle((50,250), 100, 200)
        ]

    def create_hazard(self):

        self.hazards = [Hazard(400, 100)]

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
        self.time += 1
        self.datacollector.get_model_vars_dataframe().plot()

        # Stop the simulation once all agents have exited the building
        if len(self.schedule.agents) == 0:
            self.running = False
            self.save_figures()

    def save_figures(self):
        results = self.datacollector.get_model_vars_dataframe()

        dpi = 100
        fig, axes = plt.subplots(figsize=(1920 / dpi, 1080 / dpi), dpi=dpi, nrows=1, ncols=3)

        status_results = results.loc[:, ['Active', 'Escaped']]
        status_plot = status_results.plot(ax=axes[0])
        status_plot.set_title("Agent Status")
        status_plot.set_xlabel("Simulation Step")
        status_plot.set_ylabel("Count")

        panic_results = results.loc[:, ['Low Panic', 'Medium Panic', 'High Panic']]
        panic_plot = panic_results.plot(ax=axes[1])
        panic_plot.set_title("Panic levels")
        panic_plot.set_xlabel("Simulation Step")
        panic_plot.set_ylabel("Count")

        tom_results = results.loc[:, ['ToM0', 'ToM1']]
        tom_plot = tom_results.plot(ax=axes[2])
        tom_plot.set_title("ToM levels")
        tom_plot.set_xlabel("Simulation Step")
        tom_plot.set_ylabel("Count")

        timestr = time.strftime("%Y%m%d-%H%M%S")
        plt.suptitle("Number of Agents: " + str(self.num_agents), fontsize=16)
        plt.savefig(timestr + ".png")
        plt.close(fig)

    @staticmethod
    def count_active_agents(model, status=False):
        """
        Count how many agents are still active in the model
        """
        count = 0
        for agent in model.schedule.agents:
            if isinstance(agent, Person):
                if agent.escaped == status:
                    count += 1
        return count

    @staticmethod
    def count_panic(model, panic):
        """
        Count how many agents have a particular panic level
        """
        count = 0
        for agent in model.schedule.agents:
            if isinstance(agent, Person):
                if agent.panic == panic:
                    count += 1
        return count

    @staticmethod
    def count_tom(model, tom=1):
        """
        Count how many agents have a particular level of Theory of Mind
        """
        count = 0
        for agent in model.schedule.agents:
            if isinstance(agent, Person):
                if agent.theory_of_mind == tom:
                    count += 1
        return count

    @staticmethod
    def get_time(model):
        return model.time