'''
This class provides the appearance of the entities in the environment via static methods.
'''

class Portrayals:

    @staticmethod
    def for_Agent(state, tom):

        radius = 8

        portrayal = {"Shape": "circle",
                     "Color": "blue",
                     "Filled": "true",
                     "Layer": 0,
                     "r": radius,
                     "border": 0,
                     "border_color": None}

        if state == 1:
            portrayal["Color"] = "orange"
            portrayal["Layer"] = 2
            portrayal["r"] = radius * 1.02

        elif state == 2:
            portrayal["Color"] = "red"
            portrayal["Layer"] = 1
            portrayal["r"] = radius * 1.04

        if tom == 1:
            portrayal["border"] = 10
            portrayal["border_color"] = "Indigo"

        return portrayal

    @staticmethod
    def for_Exit():

        portrayal = {"Shape": "rect",
                     "Color": "green",
                     "Filled": "true",
                     "Layer": 1,
                     "w": 0.025,
                     "h": 0.025}

        return portrayal

    @staticmethod
    def for_hazard(danger_radius):
        portrayal = {"Shape": "circle",
                     "Color": "FireBrick",
                     "Filled": "false",
                     "Layer": 0,
                     "r": 20,
                     "border": danger_radius,
                     "border_color": "Gainsboro"}

        return portrayal

    @staticmethod
    def for_Obstacle(width, height, dimensions):

        portrayal = {"Shape": "rect",
                     "Color": "black",
                     "Filled": "true",
                     "Layer": 0,
                     "w": width / dimensions[0],
                     "h": height / dimensions[1]
                     }

        return portrayal