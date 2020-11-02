'''
This class inherits from VisualizationElement provided by MESA. It's responsibility is to create and draw the environment.
'''

from mesa.visualization.ModularVisualization import VisualizationElement
from src.view.Portrayals import Portrayals

class Canvas_Controller(VisualizationElement):

    local_includes = ["src/view/visualization.js"]

    def __init__(self, dimensions):

        self.canvas_height, self.canvas_width = dimensions

        new_element = ("new Simple_Continuous_Module({}, {})"
                        .format(self.canvas_height, self.canvas_width))

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

        # for hazard in model.hazards:
        portrayal = self.getHazardPortrayal(model.space, model.hazard)
        space_state.append(portrayal)

        return space_state

    def getAgentPortrayal(self, space, agent):
        portrayal = Portrayals.for_Agent(agent.panic, agent.theory_of_mind)
        return self.placePortrayal(space, portrayal, agent)

    def getExitPortrayal(self, space, exit):
        portrayal = Portrayals.for_Exit()
        return self.placePortrayal(space, portrayal, exit)

    def getObstaclePortrayal(self, space, obstacle):
        portrayal = Portrayals.for_Obstacle(obstacle.width, obstacle.height, (self.canvas_width, self.canvas_height))
        return self.placePortrayal(space, portrayal, obstacle)

    def getHazardPortrayal(self, space, hazard):
        portrayal = Portrayals.for_hazard(hazard.danger_radius())
        return self.placePortrayal(space, portrayal, hazard)

    def placePortrayal(self, space, portrayal, element):
        x, y = element.pos
        portrayal["x"] = x/self.canvas_width
        portrayal["y"] = y/self.canvas_height
        return portrayal
