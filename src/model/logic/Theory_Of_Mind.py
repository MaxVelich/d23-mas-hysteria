'''
This class will incorporate the Theory of Mind aspect of the agents
'''

from src.model.utils.Utilities import Utilities

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
    def agent_should_switch_goal(exits, agent_position, neighbors, current_goal):
        """
        determine which exits the neighbors of a given agents are most likely to use
        """
        goals_of_agents = []
        if neighbors:
            for i in neighbors:
                goal = Utilities.find_closest_point_of_set_of_points(i.pos, exits)
                goals_of_agents += [goal]

            if goals_of_agents.count(current_goal) >= len(neighbors)/2:
                return True

        return False
