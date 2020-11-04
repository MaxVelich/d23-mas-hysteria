
'''
Here we model the Hazard object. It doesn't do much at this point...
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