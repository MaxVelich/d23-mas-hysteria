'''
This class will incorporate the Theory of Mind aspect of the agents
'''

from src.model.logic.Path_Finder import Path_Finder

class Theory_Of_Mind:

    def __init__(self):
        pass

    '''
    Plan:
    use something similar to the cohere function in the Panic_Dynamic
    i.e. determine which exit the surrounding agents would most likely move towards (see __find_nearest_goal in pathfinder.py)
    If another exit is also nearby and is being used by fewer agents, consider taking this one 
    '''

    @staticmethod
    def determine_neighbor_exit_strategy(path_finder, neighbors):
        """
        determine which exits the neighbors of a given agents are most likely to use
        """
        exits = []
        if(neighbors):
            for i in neighbors:
                print("neighbor at location " + str(i.pos))
                exit = Path_Finder.find_nearest_goal(path_finder, i.pos)
                print("exit for neighbor is " + str(exit))

        # TODO: change exit if too many neighbors use exit
        return exits