'''
This class inherits from VisualizationElement provided by MESA. It's responsibility is to create and draw the environment.
'''

from mesa.visualization.ModularVisualization import VisualizationElement
from src.view.Portrayals import Portrayals

class Canvas_Controller(VisualizationElement):

    local_includes = ["src/view/visualization.js"]

    def __init__(self, canvas_height=500, canvas_width=500):

        self.canvas_height = canvas_height
        self.canvas_width = canvas_width

        new_element = ("new Simple_Continuous_Module({}, {})"
                        .format(self.canvas_width, self.canvas_height))

        self.js_code = "elements.push(" + new_element + ");"

    def render(self, model):
        space_state = []

        for agent in model.schedule.agents:
            portrayal = self.getAgentPortrayal(model.space, agent)
            space_state.append(portrayal)

        for obstacle in model.obstacles:
            portrayal = self.getObstaclePortrayal(model.space, obstacle)
            space_state.append(portrayal)

        for exit in model.exits:
            portrayal = self.getExitPortrayal(model.space, exit)
            space_state.append(portrayal)

        return space_state

    def getAgentPortrayal(self, space, agent):
        portrayal = Portrayals.for_Agent(agent.panic)
        return self.placePortrayal(space, portrayal, agent)

    def getExitPortrayal(self, space, exit):
        portrayal = Portrayals.for_Exit()
        return self.placePortrayal(space, portrayal, exit)

    def getObstaclePortrayal(self, space, obstacle):
        portrayal = Portrayals.for_Obstacle(obstacle.width, obstacle.height)
        return self.placePortrayal(space, portrayal, obstacle)

    def placePortrayal(self, space, portrayal, element):
        x, y = element.pos
        portrayal["x"] = x/self.canvas_width
        portrayal["y"] = y/self.canvas_height
        return portrayal
