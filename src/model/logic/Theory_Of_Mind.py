'''
This class incorporates the logic for the theory of mind part of the agents.
'''

from src.model.utils.Utilities import Utilities

class Theory_Of_Mind:

    '''
    Here, we determine which exit the surrounding agents would most likely move towards.
    If another exit is also nearby and is being used by fewer agents, consider taking this one.
    '''

    @staticmethod
    def agent_should_switch_goal(exits, agent_position, neighbors, current_goal):

        goals_of_agents = []
        if neighbors:
            for i in neighbors:
                goal = Utilities.find_closest_point_of_set_of_points(i.pos, exits)
                goals_of_agents += [goal]

            if goals_of_agents.count(current_goal) >= len(neighbors)/2:
                return True

        return False