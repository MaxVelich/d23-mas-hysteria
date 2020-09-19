
class Portrayals:

    def get_Agent_Portrayal(self, state):

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

    def get_Exit_Portrayal(self):
        
        portrayal = {"Shape": "rect",
                        "Color": "green",
                        "Filled": "true",
                        "Layer": 0,
                        "w": 0.025,
                        "h": 0.025}

        return portrayal