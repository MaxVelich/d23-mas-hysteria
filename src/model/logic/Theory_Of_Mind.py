'''
This class will incorporate the Theory of Mind aspect of the agents
'''

from src.model.utils.Geometry import Geometry

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
    def determine_neighbor_exit_strategy(exits, agent_position, neighbors, current_goal):
        """
        determine which exits the neighbors of a given agents are most likely to use
        """
        possible_exits = []
        total_neighbors = len(neighbors)
        agent_goal = current_goal
        if neighbors:
            for i in neighbors:
                goal = Geometry.find_closest_point_of_set_of_points(i.pos, exits)
                possible_exits += [goal]

            # print("exit list is: " + str(exits))
            if agent_goal in possible_exits:
                if possible_exits.count(current_goal) >= total_neighbors/2:
                    # print("changing goal from: " + str(agent_goal))
                    agent_goal = Geometry.find_closest_point_of_set_of_points(agent_position, exits)
                    # print("to :" + str(agent_goal))

        return agent_goal
