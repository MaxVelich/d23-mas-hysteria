
'''
This class is currently empty. It will provide a general implementation of an obstacle object in the environment that agents cannot pass through. This could be furniture or a wall, but also other types of obstruction such as smoke (which would allow agents to pass through at e.g. lower speeds).
'''

class Obstacle:

    def __init__(self, center, width, height):
        self.pos = center
        self.width = width
        self.height = height

    def get_corner_points(self):
        corners = []
        corners += [(self.pos[0]-(self.width/2),self.pos[1]-(self.height/2))]
        corners += [(self.pos[0]+(self.width/2),self.pos[1]-(self.height/2))]
        corners += [(self.pos[0]-(self.width/2),self.pos[1]+(self.height/2))]
        corners += [(self.pos[0]+(self.width/2),self.pos[1]+(self.height/2))]
        return corners