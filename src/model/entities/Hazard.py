
'''
Here we model the Hazard object. It has a danger radius that prohibits agents to walk into. 
'''

class Hazard():

    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
        self.pos = (x, y)

    def radius(self):
        return 20

    def danger_radius(self):
        return 100