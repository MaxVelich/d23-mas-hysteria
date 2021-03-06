
'''
Here we intend to provide the logic for how agents react to the panic. Also, how the panic in general progresses with time. This class is very much a work-in-progress at this moment.
'''

import math

class Panic_Dynamic:

    @staticmethod
    def average_direction_of_crowd(neighbors, pos, agent):
        """
        Return the vector toward the center of mass of the local neighbors. We took inspiration from the source below, but we rewrote the whole code.
        Reference: https://github.com/projectmesa/mesa/blob/master/examples/boid_flockers/boid_flockers/boid.py
        """

        if not neighbors:
            return []

        cohere_x = []
        cohere_y = []

        for neighbor in neighbors:
            direction = agent.model.space.get_heading(pos, neighbor.pos)
            cohere_x += [direction[0]]
            cohere_y += [direction[1]]

        average_x = sum(cohere_x) / len(neighbors)
        average_y = sum(cohere_y) / len(neighbors)
        
        norm = math.sqrt(average_x * average_x + average_y * average_y)
        if norm == 0:
            return (0,0)

        average_x /= norm
        average_y /= norm

        return (average_x, average_y)

    @staticmethod
    def change_panic_level(neighbourhood, pos, parameters):
        """
        Return the changed panic level, based on agents' neighbourhood 
        """

        panic = 0

        if parameters == [0, 0]:
            return 0

        if neighbourhood > parameters[1]:
            return 2

        if neighbourhood > parameters[0]:
            panic = 1

        return panic
