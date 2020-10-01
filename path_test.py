
print("This is just a test file.")
print("*" * 30)

from src.model.logic.Path_Finder import Path_Finder

world = (500, 500)
obstacles = [ [(0,0), (20, 0), (20,20), (0,20)] ]
exits = [ (100,100) ]

path_finder = Path_Finder(world, obstacles, exits)
path_finder.description()


from mesa.visualization.ModularVisualization import ModularServer

from src.model.Model_Controller import Model_Controller
from src.view.Canvas_Controller import Canvas_Controller

server = ModularServer(
        Model_Controller, 
        [Canvas_Controller()], 
        "Evacuation", 
        {"width": world[0], "height": world[1], "N": 1}
    )

server.launch()