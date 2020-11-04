
'''
This is the general implementation of an obstacle object in the environment that agents cannot pass through. This could be furniture or a wall, but also other types of obstruction.
'''

class Obstacle:

    def __init__(self, center, width, height):
        self.pos = center
        self.width = width
        self.height = height

    def get_corner_points(self):
        corners = []
        corners += [(self.pos[0]-(self.width/2),self.pos[1]-(self.height/2))] # top_left
        corners += [(self.pos[0]+(self.width/2),self.pos[1]-(self.height/2))] # top_right
        corners += [(self.pos[0]-(self.width/2),self.pos[1]+(self.height/2))] # bottom_left
        corners += [(self.pos[0]+(self.width/2),self.pos[1]+(self.height/2))] # bottom_right
        return corners