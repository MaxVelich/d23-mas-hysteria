
'''
This script serves as a temporary starting point for our development journey. Here we initialize the model, the canvas and start up the server.
'''

from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from model import Model_Controller
from src.view.Canvas_Controller import Canvas_Controller
from src.view.Portrayals import Portrayals

#Uncomment these 2 lines if you get a NotImplementedError for server.launch()
#(Confirmed to work for windows 10)
# import asyncio
# asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

width = 500
height = 1000
N = 80
theory_of_mind = 5  # How many of the agents will apply theory of mind
panic_dynamic = [2, 7]  # Threshold for number of neighbours before panic sets in
legend = Portrayals.get_legend()
introduction = Portrayals.get_introduction()
save_plots = False

server = ModularServer(
        Model_Controller, 
        [Canvas_Controller(height, width)],
        "Panic Behaviour in Crowd Evacuation",
        {"width": width, "height": height, "save_plots": save_plots,
         "theory_of_mind": theory_of_mind, "panic_dynamic": panic_dynamic,
         "N": UserSettableParameter('number', 'Number of Agents', value=N),
         "Legend": UserSettableParameter('static_text', value=legend)}
    )
