from mesa import Model
from src.agent import PersonAgent

from mesa.time import RandomActivation
from mesa.space import ContinuousSpace

from mesa.datacollection import DataCollector


def compute_gini(model):
    agent_wealths = [agent.wealth for agent in model.schedule.agents]
    x = sorted(agent_wealths)
    N = model.num_agents
    B = sum(xi * (N - i) for i, xi in enumerate(x)) / (N * sum(x))
    return 1 + (1 / N) - 2 * B


class EvacuationModel(Model):

    def __init__(self, N, width, height):
        self.num_agents = N
        self.space = ContinuousSpace(
            width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True

        # Create agents
        for i in range(self.num_agents):
            a = PersonAgent(i, self)

            # Add the agent to a random space cell
            x = self.random.randrange(self.space.width)
            y = self.random.randrange(self.space.height)
            self.space.place_agent(a, (x, y))

            self.schedule.add(a)

        # self.datacollector = DataCollector(
            #model_reporters={"Gini": compute_gini},
            # agent_reporters={"Wealth": "wealth"})

    def step(self):
        # self.datacollector.collect(self)
        self.schedule.step()
