
'''
This script serves as a temporary starting point for our development journey. Here we initialize the model, the canvas and start up the server.
'''

from mesa.visualization.ModularVisualization import ModularServer

from src.model.Model_Controller import Model_Controller
from src.view.Canvas_Controller import Canvas_Controller

#Uncomment these 2 lines if you get a NotImplementedError for server.launch()
#(Confirmed to work for windows 10)
#import asyncio
#asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

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


