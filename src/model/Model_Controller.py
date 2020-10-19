
from src.model.entities.Person import Person
from src.model.entities.Exit import Exit
from src.model.entities.Hazard import Hazard

from mesa import Model
from mesa.time import RandomActivation
from mesa.space import ContinuousSpace
from mesa.datacollection import DataCollector


def get_count(model):
    return model.num_agents


class Model_Controller(Model):

    def __init__(self, N, width, height):
        self.num_agents = N
        self.space = ContinuousSpace(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True
        self.count = 0

        self.create_agent()

        self.create_exit()

        self.create_hazard()

        self.path_finder = Path_Finder((width, height), self.obstacles, self.exits)
        self.path_finder.build_mesh()

        self.datacollector = DataCollector(model_reporters={"Gini": get_count})

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

    def create_obstacles(self):

        self.obstacles = [
            Obstacle((75,350), 150, 40),
            Obstacle((225,350), 150, 40),
            Obstacle((425,250), 150, 40),
            Obstacle((275,250), 150, 40),
            Obstacle((75,150), 150, 40),
            Obstacle((225,150), 150, 40)
        ]

    def create_hazard(self):

        self.hazards = [Hazard(400, 100)]

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
        self.count += 1

        # Stop the simulation once all agents have exited the building
        if len(self.schedule.agents) == 0:
            self.running = False
