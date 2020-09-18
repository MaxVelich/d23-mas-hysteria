from mesa.visualization.ModularVisualization import ModularServer

from src.agent import *
from src.model import *
from src.modelCanvas import *

'''
Model Parameters
'''
width = 500
height = 500
N = 200


#canvas = ModelCanvas(width, height)
canvas = ModelCanvas()
server = ModularServer(EvacuationModel, [canvas], "Evacuation",
                       {"width": width, "height": height, "N": N})
