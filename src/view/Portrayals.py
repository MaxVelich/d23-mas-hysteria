'''
This class provides the appearance of the entities in the environment via static methods. It also generates the HTML for the canvas.
'''

class Portrayals:

    @staticmethod
    def for_Agent(state, tom, radius):

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
    def for_Exit(width, height, dimensions):

        portrayal = {"Shape": "rect",
                     "Color": "green",
                     "Filled": "true",
                     "Layer": 0,
                     "w": width / dimensions[1],
                     "h": height / dimensions[0]
                     }

        return portrayal

    @staticmethod
    def for_hazard(radius, danger_radius):
        portrayal = {"Shape": "circle",
                     "Color": "FireBrick",
                     "Filled": "false",
                     "Layer": 0,
                     "r": radius,
                     "border": danger_radius,
                     "border_color": "Gainsboro"}

        return portrayal

    @staticmethod
    def for_Obstacle(width, height, dimensions):

        print(width, height, dimensions)

        portrayal = {"Shape": "rect",
                     "Color": "black",
                     "Filled": "true",
                     "Layer": 0,
                     "w": width / dimensions[1],
                     "h": height / dimensions[0]
                     }

        return portrayal

    @staticmethod
    def for_canvas(width, height):
        return '''
          <div id='canvas_site' style='margin: 0px; padding: 0px; border-width: 0px; width:100%; text-align: center;'>
            <canvas id='canvas_id' width=' ''' + str(width) + ''' ' height=' ''' + str(height) + '''' style='border-width: 3px; border-style: solid; border-radius: 8px' />
          </div>
        '''

    @staticmethod
    def for_legend():
        legend_file = open("src/view/legend.html", "rt")
        legend = legend_file.read()
        legend_file.close()
        return legend