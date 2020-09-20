
'''
This class models the Exit object. This is the objects agents want to rush to in case of an emergency.
'''

class Exit:

    def __init__(self, x = 0, y = 0, available = False):
        self.x = x
        self.y = y
        self.pos = (x, y)
        self.available = available

    def is_visible(from_position, distance = 100):
        return True