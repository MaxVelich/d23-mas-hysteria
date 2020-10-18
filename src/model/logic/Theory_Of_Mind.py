'''
This class will incorporate the Theory of Mind aspect of the agents
'''

class Theory_Of_Mind:

    def __init__(self):
        pass

    '''
    Plan:
    use something similar to the cohere function in the Panic_Dynamic
    i.e. determine which exit the surrounding agents would most likely move towards (see __find_nearest_goal in pathfinder.py)
    If another exit is also nearby and is being used by fewer agents, consider taking this one 
    '''