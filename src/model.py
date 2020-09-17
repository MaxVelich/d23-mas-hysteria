from mesa import Model
from agent import PersonAgent

from mesa.time import RandomActivation
from mesa.space import ContinuousSpace

from mesa.datacollection import DataCollector


def compute_gini(model):
    agent_wealths = [agent.wealth for agent in model.schedule.agents]
    x = sorted(agent_wealths)
    N = model.num_agents
    B = sum(xi * (N - i) for i, xi in enumerate(x)) / (N * sum(x))
    return 1 + (1 / N) - 2 * B

# TODO: modify so its not toroidal. Restrict agents to inbounds
class EvacuationModel(Model):

    def __init__(self, N, width, height):
        self.num_agents = N
        self.space = ContinuousSpace(
            width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True

        # Create agents
        self.create_agent()
        self.create_exit()
        # self.datacollector = DataCollector(
        #model_reporters={"Gini": compute_gini},
        # agent_reporters={"Wealth": "wealth"})

    def create_agent(self):
        for i in range(self.num_agents):
            a = PersonAgent(i, self)

            # Add the agent to a random space cell
            x = self.random.randrange(self.space.width)
            y = self.random.randrange(self.space.height)
            self.space.place_agent(a, (x, y))

            self.schedule.add(a)

    def create_exit(self):
        self.exits = {Exit(self.space.width / 2, self.space.height / 2, True)}

    def step(self):
        # self.datacollector.collect(self)
        self.schedule.step()

class Exit():

    def __init__(self, x=0, y=0, avail=False):
        self.x = x
        self.y = y
        self.pos = (x, y)
        self.avail = avail

    def isVisible(frompos, distance=100):
        return True
