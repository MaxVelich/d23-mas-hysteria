"""
Visualization of agent grid
Reference: https://mesa.readthedocs.io/en/master/tutorials/intro_tutorial.html
"""

from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

# If MoneyModel.py is where your code is:
from src.model import MoneyModel


def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Color": "red",
                 "Filled": "true",
                 "Layer": 0,
                 "r": 0.5}

    if agent.panic == 1:
        portrayal["Color"] = "green"
        portrayal["Layer"] = 2
        portrayal["r"] = 0.2

    elif agent.panic == 2:
        portrayal["Color"] = "blue"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.3
    else:
        portrayal["Color"] = "red"
        portrayal["Layer"] = 0

    return portrayal


grid = CanvasGrid(agent_portrayal, 20, 20, 500, 500)
server = ModularServer(MoneyModel,
                       [grid],
                       "Evacuation Model",
                       {"N": 100, "width": 20, "height": 20})
server.port = 8521  # The default
server.launch()

