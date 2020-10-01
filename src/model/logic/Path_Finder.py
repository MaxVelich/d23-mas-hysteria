
'''
This class is currently empty. Here we intend to provide the logic for the agents to find a path towards an exit. We intend to not only provide algorithms for the nearest path, but also alternative routes. 
'''

class Path_Finder:

    def __init__(self, world, obstacles, exits):
        self.world = world
        self.obstacles = obstacles
        self.exits = exits

    def description(self):
        print("world:", self.world)
        print("obstacles:", self.obstacles)
        print("exits:", self.exits)
