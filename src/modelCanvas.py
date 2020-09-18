from mesa.visualization.ModularVisualization import VisualizationElement


class ModelCanvas(VisualizationElement):
    # Used within Mesa, source of the visualization js script
    local_includes = ["src/visualization.js"]

    # TODO: Having multiple portrayals like this is awful
    #           need to come up with a dynamic way of doing this for any object
    def __init__(self, canvas_height=500, canvas_width=500):

        self.canvas_height = canvas_height
        self.canvas_width = canvas_width

        new_element = ("new Simple_Continuous_Module({}, {})".
                       format(self.canvas_width, self.canvas_height))

        # Pushes the string into a js <Script></Script>
        self.js_code = "elements.push(" + new_element + ");"

    def render(self, model):
        space_state = []

        # Draw agents
        for agent in model.schedule.agents:
            portrayal = self.getAgentPortrayal(model, agent)
            space_state.append(portrayal)

        # Draw exits
        for exit in model.exits:
            portrayal = self.getExitPortrayal(model, exit)
            space_state.append(portrayal)

        return space_state

    # ----> Might be nice to implement so we just do a "for everything get protrayal?"
    # def getPortrayal(self, element):
    #     if element.type == 'Agent':
    #         print('retrive agents protrayal')
    #     elif element.type == 'Exit':
    #         print('retrieve exit portrayal')

    def getAgentPortrayal(self, model, agent):
        agentradius = 8
        portrayal = {"Shape": "circle",
                     "Color": "blue",
                     "Filled": "true",
                     "Layer": 0,
                     "r": agentradius}

        if agent.panic == 1:
            portrayal["Color"] = "orange"
            portrayal["Layer"] = 2
            portrayal["r"] = agentradius * 1.02

        elif agent.panic == 2:
            portrayal["Color"] = "red"
            portrayal["Layer"] = 1
            portrayal["r"] = agentradius * 1.04

        return self.placePortrayal(model, portrayal, agent)

    def getExitPortrayal(self, model, exit):
        portrayal = {"Shape": "rect",
                     "Color": "green",
                     "Filled": "true",
                     "Layer": 0,
                     "w": 0.025,
                     "h": 0.025}

        return self.placePortrayal(model, portrayal, exit)

    # Requires the element to have a pos attribute
    def placePortrayal(self, model, portrayal, element):
        x, y = element.pos
        portrayal["x"] = ((x - model.space.x_min) /
                          (model.space.x_max - model.space.x_min))
        portrayal["y"] = ((y - model.space.y_min) /
                          (model.space.y_max - model.space.y_min))
        return portrayal
