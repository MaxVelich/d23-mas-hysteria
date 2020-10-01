
'''
This class provides the appearance of the entities in the environment via static methods.
'''

class Portrayals:

    @staticmethod
    def for_Agent(state):

        radius = 8

        portrayal = {"Shape": "circle",
                        "Color": "blue",
                        "Filled": "true",
                        "Layer": 0,
                        "r": radius}

        if state == 1:
            portrayal["Color"] = "orange"
            portrayal["Layer"] = 2
            portrayal["r"] = radius * 1.02

        elif state == 2:
            portrayal["Color"] = "red"
            portrayal["Layer"] = 1
            portrayal["r"] = radius * 1.04

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
    def for_Obstacle(width, height):

        portrayal = {"Shape": "rect",
                        "Color": "red",
                        "Filled": "true",
                        "Layer": 0,
                        "w": width/500,
                        "h": height/500
                        }

        return portrayal