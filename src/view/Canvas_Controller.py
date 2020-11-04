'''
This class inherits from VisualizationElement provided by MESA. It's responsibility is to create and draw the environment. Here, we also handle the layout of the website to a certain degree: we create the legend as a static html div, and also adjust the layout.
'''

from mesa.visualization.ModularVisualization import VisualizationElement
from src.view.Portrayals import Portrayals

class Canvas_Controller(VisualizationElement):

    local_includes = ["src/view/visualization.js"]

    def __init__(self, dimensions):
        '''
        Via JavaScript the visualation is created. We first create the HTML code for the canvas, and for the legend, and then pass it over to the JavaScript part.
        '''

        self.dimensions = dimensions
        self.canvas_width, self.canvas_height = dimensions

        canvas = Portrayals.for_canvas(self.canvas_width, self.canvas_height)
        legend = Portrayals.for_legend()

        new_element = ("new Simple_Continuous_Module({}, {}, `{}`, `{}`)"
                        .format(self.canvas_width, self.canvas_height, canvas, legend))

        self.js_code = "elements.push(" + new_element + ");"

    def render(self, model):
        '''
        This function is called by MESA, and is responsible for providing the protrayals for all elements in the simulation.
        '''

        space_state = []

        # Portrayals for the agents
        for agent in model.schedule.agents:
            portrayal = self.__get_agent_portrayal(model.space, agent)
            space_state.append(portrayal)

        # Portrayals for the hazard
        portrayal = self.__get_hazard_portrayal(model.space, model.hazard)
        space_state.append(portrayal)

        # Portrayals for the obstacles
        for obstacle in model.obstacles:
            portrayal = self.__get_obstacle_portrayal(model.space, obstacle)
            space_state.append(portrayal)

        # Portrayals for the exits
        for exit in model.exits:
            portrayal = self.__get_exit_portrayal(model.space, exit)
            space_state.append(portrayal)

        return space_state

    ### PRIVATE INTERFACE 

    def __get_agent_portrayal(self, space, agent):
        portrayal = Portrayals.for_Agent(agent.panic, agent.theory_of_mind, agent.radius())
        return self.__placePortrayal(space, portrayal, agent)

    def __get_exit_portrayal(self, space, exit):
        portrayal = Portrayals.for_Exit(exit.width(), exit.height(), self.dimensions)
        return self.__placePortrayal(space, portrayal, exit)

    def __get_obstacle_portrayal(self, space, obstacle):
        portrayal = Portrayals.for_Obstacle(obstacle.width, obstacle.height, self.dimensions)
        return self.__placePortrayal(space, portrayal, obstacle)

    def __get_hazard_portrayal(self, space, hazard):
        portrayal = Portrayals.for_hazard(hazard.radius(), hazard.danger_radius())
        return self.__placePortrayal(space, portrayal, hazard)

    def __placePortrayal(self, space, portrayal, element):
        x, y = element.pos
        portrayal["x"] = x / self.canvas_width
        portrayal["y"] = y / self.canvas_height
        return portrayal
