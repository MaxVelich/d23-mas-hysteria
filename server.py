
'''
This script serves as a temporary starting point for our development journey. Here we initialize the model, the canvas and start up the server.
'''

from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from src.model.entities.Hazard import Hazard
from src.model.entities.Obstacle import Obstacle
from src.model.entities.Exit import Exit

from model import Model_Controller
from src.view.Canvas_Controller import Canvas_Controller
from src.view.Portrayals import Portrayals

#Uncomment these 2 lines if you get a NotImplementedError for server.launch()
#(Confirmed to work for windows 10)
import asyncio
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

config_free_space = { "dimensions": (500, 500),
                      "num_agents": 20,
                      "theory_of_mind": 10, 
                      "panic_dynamic": [3, 4],
                      "agent_boundaries": [175, 325, 175, 325],
                      "obstacles": [],
                      "exits": [Exit(0, 25), Exit(0, 475), Exit(500, 25), Exit(500, 475)],
                      "hazard": Hazard(50, 100)
                    }

config_two_rooms = { "dimensions": (500, 500),
                     "num_agents": 20,
                     "theory_of_mind": 5, 
                     "panic_dynamic": [3, 4],
                     "agent_boundaries": [25, 475, 115, 475],
                     "obstacles": [ Obstacle((250,300), 20,400),
                                    Obstacle((75,90), 150,20),
                                    Obstacle((250,90), 75,20),
                                    Obstacle((425,90), 150,20) ],
                     "exits": [ Exit(0, 25), Exit(500, 25) ],
                     "hazard" : Hazard(30,30)
                   }

config_supermarket = { "dimensions": (1000, 500),
                       "num_agents": 60,
                       "theory_of_mind": 5, 
                       "panic_dynamic": [3, 4],
                       "agent_boundaries": [25, 975, 25, 475],
                       "obstacles": [ Obstacle((125,20), 250,40),
                                      Obstacle((970,125), 60,250),
                                      Obstacle((175,470), 350,60),
                                      Obstacle((600,125), 400,50),
                                      Obstacle((600,250), 400,50),
                                      Obstacle((625,375), 350,50),
                                      Obstacle((150,250), 200,30) ],
                       "exits": [ Exit(0, 75), Exit(0, 425) ],
                       "hazard" : Hazard(550,200)
                   }

# Change this variable here for a different setting
current_configuration = config_two_rooms

legend = Portrayals.get_legend()
introduction = Portrayals.get_introduction()
save_plots = False
batch_run = False
batch_tom = 0
batch_panic = [0, 0]

width, height = current_configuration["dimensions"]
num_agents = current_configuration["num_agents"]

server = ModularServer(
        Model_Controller, 
        [Canvas_Controller(current_configuration["dimensions"])],
        "Panic Behaviour in Crowd Evacuation",
        {"width": width, "height": height, "save_plots": save_plots, "batch_run": batch_run,
         "batch_tom": batch_tom, "batch_panic": batch_panic, "configuration": current_configuration,
         "N": UserSettableParameter('number', 'Number of Agents', value= num_agents),
         "Legend": UserSettableParameter('static_text', value=legend)}
    )
