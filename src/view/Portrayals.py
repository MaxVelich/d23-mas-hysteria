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
                        "Layer": 0,
                        "w": 0.025,
                        "h": 0.025}

        return portrayal

    @staticmethod
    def for_hazard():
        portrayal = {"Shape": "rect",
                     "Color": "gold",
                     "Filled": "true",
                     "Layer": 0,
                     "w": 0.025,
                     "h": 0.025}

        return portrayal

    @staticmethod
    def get_legend():
        legend = '''
              <div style="width=0px;">
              <legend style="float:left; font-size:15px; margin-top:5px; width=10px">Model Legend:</legend>
              <div style='float: left;height: 15px;width: 15px;margin-bottom: 15px;margin-right: 5px;border: 1px solid
                black;clear: both;background-color:blue'></div> <p style="font-size:16px; margin-bottom: 15px">Panic level: Low </p>
              <div style='float: left;height: 15px;width: 15px;margin-bottom: 15px;margin-right: 5px;border: 1px solid
                black;clear: both;background-color:orange'></div> <p style="font-size:16px; margin-bottom: 15px"> Panic level: Medium </p>
              <div style='float: left;height: 15px;width: 15px;margin-bottom: 15px;margin-right: 5px;border: 1px solid
                black;clear: both;background-color:red'></div> <p style="font-size:16px; margin-bottom: 15px"> Panic level: High </p>
              <div style='float: left;height: 15px;width: 15px;margin-bottom: 15px;margin-right: 5px;border: 1px solid
                black;clear: both;background-color:green'></div> <p style="font-size:16px; margin-bottom: 15px"> Exit</p>
              </div>
        '''

        return legend

    @staticmethod
    def get_introduction():
        introduction = '''
        This is a simulation built for understanding panic behaviour of people in a crowd evacuation. 
        To run the model, just press Start! 
        '''
