from mesa.visualization.ModularVisualization import ModularServer

from src.agent import *
from src.model import *
from src.visualization import *

width = 500
height = 500
N = 20
agentradius = 6

#TODO: Completely rework SimpleCanvas so its a viewclass for model
#                               DrawModel(model) 
# completely independant model and drawing
def AgentPortrayal(agent):
    portrayal = {"Shape": "circle",
                 "Color": "blue",
                 "Filled": "true",
                 "Layer": 0,
                 "r": agentradius}

    if agent.panic == 1:
        portrayal["Color"] = "orange"
        portrayal["Layer"] = 2
        portrayal["r"] = agentradius * 1.02

    elif agent.panic == 2:
        portrayal["Color"] = "red"
        portrayal["Layer"] = 1
        portrayal["r"] = agentradius * 1.04

    return portrayal


def ExitPortrayal(exit):
    portrayal = {"Shape": "rect",
                 "Color": "green",
                 "Filled": "true",
                 "Layer": 0,
                 "w": 0.025,
                 "h": 0.025}

    return portrayal


canvas = SimpleCanvas(AgentPortrayal, ExitPortrayal, width, height)
server = ModularServer(
    EvacuationModel, [canvas], "Evacuation", {"width": width, "height": height, "N": N})
