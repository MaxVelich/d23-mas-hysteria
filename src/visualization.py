#
#   https://github.com/projectmesa/mesa-examples/blob/master/examples/Flockers/flockers/SimpleContinuousModule.py
#
from mesa.visualization.ModularVisualization import VisualizationElement


class SimpleCanvas(VisualizationElement):
    local_includes = ["src/visualization.js"]
    portrayal_method = None
    canvas_height = 500
    canvas_width = 500

    # TODO: Having multiple portrayals like this is awful
    #           need to come up with a dynamic way of doing this for any object
    def __init__(self, agent_portrayal_method, exit_portrayal_method, canvas_height=500, canvas_width=500):
        '''
        Instantiate a new SimpleCanvas
        '''
        self.agent_portrayal_method = agent_portrayal_method
        self.exit_portrayal_method = exit_portrayal_method
        self.canvas_height = canvas_height
        self.canvas_width = canvas_width
        new_element = ("new Simple_Continuous_Module({}, {})".
                       format(self.canvas_width, self.canvas_height))
        self.js_code = "elements.push(" + new_element + ");"

    def render(self, model):
        space_state = []

        for obj in model.schedule.agents:
            portrayal = self.agent_portrayal_method(obj)
            x, y = obj.pos
            portrayal["x"] = ((x - model.space.x_min) /
                              (model.space.x_max - model.space.x_min))
            portrayal["y"] = ((y - model.space.y_min) /
                              (model.space.y_max - model.space.y_min))
            space_state.append(portrayal)

        for exit in model.exits:
            portrayal = self.exit_portrayal_method(exit)
            x, y = exit.pos
            portrayal["x"] = ((x - model.space.x_min) /
                              (model.space.x_max - model.space.x_min))
            portrayal["y"] = ((y - model.space.y_min) /
                              (model.space.y_max - model.space.y_min))
            space_state.append(portrayal)

        return space_state
