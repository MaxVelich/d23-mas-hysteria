
'''
This is a controller class, so many part of the functionality of this program are connected here. This includes the creation of the world and its canvas. Also, here the agents are placed on the canvas. This class is also responsible for setting up the data collection in order to get results from the simulations. Lastly, it handles the step function, i.e. it handles what should happen at each time step.
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

    def __init__(self, N, num_tom, width, height, configuration, save_plots, batch_run, batch_tom, batch_panic):
        self.panic_thresholds = configuration["panic_dynamic"]
        self.agent_boundaries = configuration["agent_boundaries"]
        self.obstacles = configuration["obstacles"]
        self.exits = configuration["exits"]
        self.hazard = configuration["hazard"]
        
        self.num_agents = N
        self.num_tom_agents = num_tom

        if batch_run:
            self.num_tom_agents = batch_tom
            self.panic_thresholds = batch_panic

        self.space = ContinuousSpace(width, height, True)
        self.schedule = RandomActivation(self)

        self.world_manager = World_Manager((width, height), self.obstacles, self.exits)
        self.world_mesh = self.world_manager.build_mesh()
        self.create_agents()

        self.time = 0
        self.running = True
        self.regular_times = []
        self.tom_times = []
        self.data_collector_helper = Data_Collector_Helper()
        self.datacollector = DataCollector(self.data_collector_helper.get_collectors())
        self.images = save_plots

        self.report_status()

    def report_status(self):
        print("There are " + str(self.num_agents) + " agents of which " + str(self.num_tom_agents) + " have Theory of Mind")
        print("Agents' panic thresholds are " + str(self.panic_thresholds))

    def create_agents(self):
        '''
        Create the agents, and place them at random spots on the canvas. Also, here the theory of mind is set.
        '''

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
        '''
        Find a position that is random, but also doesn't fall in an obstructed are, or in a hazard area, or just not onto another agent.
        '''

        random_unique_positions = []
        not_done = True
        while not_done:

            # Find a random position within the given bounds
            x_pos = random.randint(self.agent_boundaries[0], self.agent_boundaries[1])
            y_pos = random.randint(self.agent_boundaries[2], self.agent_boundaries[3])

            new_point = (x_pos, y_pos)
            not_allowed = False

            # Check for other agent's positions, so they don't overlap
            for p in random_unique_positions:
                dist = Geometry.euclidean_distance(new_point, p)
                if dist <= 16:
                    not_allowed = True

            # Check for obstacles
            for obstacle in self.obstacles:
                if Geometry.point_lies_within_rectangle(new_point, obstacle.get_corner_points()):
                    not_allowed = True

            # Check for hazards
            danger_radius = self.hazard.danger_radius()
            if Geometry.point_lies_in_circle(new_point, self.hazard.pos, danger_radius):
                not_allowed = True

            # If all of the previous conditions didn't trigger, add it to the list
            if not not_allowed:
                random_unique_positions.append(new_point)

            if len(random_unique_positions) == 0:
                random_unique_positions.append(new_point)

            # When the list is big enough, stop
            if len(random_unique_positions) == self.num_agents:
                not_done = False
        
        return random_unique_positions

    def step(self):
        '''
        At each step, the scheduler needs to perform a step (hence all the agents as well). Here, we also deal with collecting the time information of the simulation, and create figures.
        '''

        self.datacollector.collect(self)

        self.schedule.step()
        self.time += 1

        if self.images:
            self.datacollector.get_model_vars_dataframe().plot()

        # Stop the simulation once all agents have exited the building
        if len(self.schedule.agents) == 0:

            if self.images:
                self.data_collector_helper.save_figures()

            print("end time: " + str(self.data_collector_helper.get_time(self)))
            self.running = False

            if self.images:
                results = self.datacollector.get_model_vars_dataframe()
                self.data_collector_helper.save_figures(results, self.num_agents)