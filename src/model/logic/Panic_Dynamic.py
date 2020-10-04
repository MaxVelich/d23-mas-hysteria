
'''
Here we intend to provide the logic for how agents react to the panic. Also, how the panic in general progresses with time. This class is very much a work-in-progress at this moment.
'''

import numpy as np

class Panic_Dynamic:

    def __init__():
        pass

    @staticmethod
    def cohere(neighbors, pos, agent):
        """
        Return the vector toward the center of mass of the local neighbors.
        Reference: https://github.com/projectmesa/mesa/blob/master/examples/boid_flockers/boid_flockers/boid.py
        """
        cohere = np.zeros(2)

        cohere_factor = 1.0
        if neighbors:
            # The velocity of the agent is determined based on the neighbouring agents
            # Returning an average direction
            for neighbor in neighbors:
                cohere += agent.model.space.get_heading(pos, neighbor.pos)
            cohere /= len(neighbors)

        velocity = (cohere * cohere_factor)
        velocity /= np.linalg.norm(velocity)
        return velocity.any()

    @staticmethod
    def change_panic_level(neighbourhood):
        """
        Return the changed panic level, based on nearby agents and vision of hazard
        :param neighbourhood:
        :return:
        """
        panic = 0
        speed = 1.0
        if neighbourhood > 3:
            panic = 1

        if neighbourhood > 7:
            panic = 2
            speed = 1

        return panic, speed
