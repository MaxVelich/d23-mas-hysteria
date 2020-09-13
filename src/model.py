
from mesa import Model
from src.agent import MoneyAgent

from mesa.time import RandomActivation
from mesa.space import MultiGrid

class MoneyModel(Model):

    def __init__(self, N, width, height):
        
        self.num_agents = N
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)

        # Create agents
        for i in range(self.num_agents):
            a = MoneyAgent(i, self)
            self.schedule.add(a)

            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

    def step(self):

        self.schedule.step()
