
'''
This is a controller class, so many part of the functionality of this program are connected here. Currently, it does not do too much, except creating the environment, populating it and instantiating a bunch of important objects (e.g. Path_Finder).
'''

from src.model.entities.Person import Person
from src.model.logic.World_Manager import World_Manager
from src.model.utils.Data_Collector_Helper import Data_Collector_Helper
from src.model.utils.Geometry import Geometry

from mesa import Model
from mesa.time import RandomActivation
from mesa.space import ContinuousSpace
from mesa.datacollection import DataCollector

import random

class Model_Controller(Model):

    def __init__(self, N, width, height, configuration, save_plots):
        self.num_tom_agents = configuration["theory_of_mind"]
        self.panic_thresholds = configuration["panic_dynamic"]
        self.agent_boundaries = configuration["agent_boundaries"]
        self.obstacles = configuration["obstacles"]
        self.exits = configuration["exits"]
        self.hazard = configuration["hazard"]
        self.num_agents = configuration["num_agents"]

        self.space = ContinuousSpace(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True
        self.time = 0
        self.images = save_plots

        self.world_manager = World_Manager((width, height), self.obstacles, self.exits)
        self.world_mesh = self.world_manager.build_mesh()

        self.data_collector_helper = Data_Collector_Helper()
        self.datacollector = DataCollector(self.data_collector_helper.get_collectors())

        self.create_agent()

    def create_agent(self):

        random_unique_positions = self.find_random_agent_positions()

        # add theory of mind (or lack thereof) when agent is being created
        agent_list = [0] * (self.num_agents - self.num_tom_agents) + [1] * self.num_tom_agents
        random.shuffle(agent_list)
        for i in range(self.num_agents):
            tom = agent_list.pop()
            a = Person(i, self, tom, self.panic_thresholds)
            self.space.place_agent(a, random_unique_positions[i])
            a.prepare_path_finding()
            self.schedule.add(a)

    def find_random_agent_positions(self):

        random_unique_positions = []
        not_done = True
        while not_done:

            x_pos = random.randint(self.agent_boundaries[0], self.agent_boundaries[1])
            y_pos = random.randint(self.agent_boundaries[2], self.agent_boundaries[3])

            new_point = (x_pos, y_pos)

            not_allowed = False
            for p in random_unique_positions:
                dist = Geometry.euclidean_distance(new_point, p)
                if dist <= 16:
                    not_allowed = True

            for obstacle in self.obstacles:
                if Geometry.point_lies_within_rectangle(new_point, obstacle.get_corner_points()):
                    not_allowed = True

            danger_radius = self.hazard.danger_radius()
            if Geometry.point_lies_in_circle(new_point, self.hazard.pos, danger_radius):
                not_allowed = True

            if not not_allowed:
                random_unique_positions.append(new_point)

            if len(random_unique_positions) == 0:
                random_unique_positions.append(new_point)

            if len(random_unique_positions) == self.num_agents:
                not_done = False
        
        return random_unique_positions

    def step(self):

        self.datacollector.collect(self)

        self.schedule.step()
        self.time += 1

        if self.images:
            self.datacollector.get_model_vars_dataframe().plot()

        # Stop the simulation once all agents have exited the building
        if len(self.schedule.agents) == 0:
            if self.images:
                self.save_figures()
            print("end time: " + str(self.data_collector_helper.get_time(self)))
            self.running = False

            results = self.datacollector.get_model_vars_dataframe()
            self.data_collector_helper.save_figures(results, self.num_agents)