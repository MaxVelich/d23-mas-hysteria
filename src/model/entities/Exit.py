
class Exit():

    def __init__(self, x=0, y=0, avail=False):
        self.x = x
        self.y = y
        self.pos = (x, y)
        self.avail = avail

    def isVisible(frompos, distance=100):
        return True