
'''
This class models the Exit object. This is the objects agents want to rush to in case of an emergency.
'''

class Exit:

    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
        self.pos = (x, y)

    def height(self):
        return 30

    def width(self):
        return 15