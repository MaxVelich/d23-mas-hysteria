from mesa.visualization.ModularVisualization import ModularServer

from src.agent import *
from src.model import *
from visualization import *

width = 200
height = 200
N = 15


def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Color": "green",
                 "Filled": "true",
                 "Layer": 0,
                 "r": 10}

    if agent.panic == 1:
        portrayal["Color"] = "orange"
        portrayal["Layer"] = 2
        portrayal["r"] = 13

    elif agent.panic == 2:
        portrayal["Color"] = "red"
        portrayal["Layer"] = 1
        portrayal["r"] = 15

    return portrayal


boid_canvas = SimpleCanvas(agent_portrayal, width, height)
server = ModularServer(
    EvacuationModel, [boid_canvas], "matters?", {"width": width, "height": height, "N": N})
#{ 100, 100, 100,5, 10, 2}
