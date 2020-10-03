
print("Test file")

from src.model.entities.Exit import Exit
from src.model.entities.Obstacle import Obstacle

from src.model.logic.Path_Finder import Path_Finder

obstacles = [
            Obstacle((50,5), 100, 10),
            Obstacle((150,5), 100, 10),
            Obstacle((250,5), 100, 10),
            Obstacle((350,5), 100, 10),
            Obstacle((450,5), 100, 10),
            Obstacle((50,495), 100, 10),
            Obstacle((150,495), 100, 10),
            Obstacle((250,495), 100, 10),
            Obstacle((350,495), 100, 10),
            Obstacle((450,495), 100, 10),
            Obstacle((5,50), 10, 100),
            Obstacle((5,150), 10, 100),
            Obstacle((5,250), 10, 100),
            Obstacle((5,350), 10, 100),
            Obstacle((5,450), 10, 100),
            Obstacle((495,50), 10, 100),
            Obstacle((495,150), 10, 100),
            Obstacle((495,250), 10, 100),
            Obstacle((495,350), 10, 100),
            Obstacle((495,450), 10, 100)
        ]

obstacles += [
            Obstacle((80,350), 150, 40),
            Obstacle((230,350), 150, 40),
            Obstacle((420,250), 150, 40),
            Obstacle((270,250), 150, 40),
            Obstacle((80,150), 150, 40),
            Obstacle((230,150), 150, 40)
        ]

# obstacles = {
#     Obstacle((150,100), 300, 10),
#     Obstacle((300,245), 10, 300),
#     Obstacle((200,350), 10, 300)
# }

path_finder = Path_Finder((500, 500), obstacles)
path_finder.build_mesh()