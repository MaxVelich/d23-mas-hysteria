
from mesa.visualization.ModularVisualization import ModularServer

from src.Model_Controller import Model_Controller
from src.view.Canvas_Controller import Canvas_Controller

width = 500
height = 500
N = 1

server = ModularServer(
        Model_Controller, 
        [Canvas_Controller()], 
        "Evacuation", 
        {"width": width, "height": height, "N": N}
    )

server.launch()