
'''
Here we intend to provide the logic for how agents react to the panic. Also, how the panic in general progresses with time. This class is very much a work-in-progress at this moment.
'''

import math


class Panic_Dynamic:

    def __init__():
        pass

    @staticmethod
    def cohere(neighbors, pos, agent):
        """
        Return the vector toward the center of mass of the local neighbors.
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
        
        norm = math.sqrt(average_x*average_x + average_y*average_y)
        if norm == 0:
            return (0,0)

        average_x /= norm
        average_y /= norm

        return (average_x, average_y)

    @staticmethod
    def change_panic_level(neighbourhood, hazards, pos, vision, threshold):
        """
        Return the changed panic level, based on nearby agents and vision of hazard
        :param neighbourhood:
        :return:
        """
        panic = 0
        speed = 0.8

        if neighbourhood > 4:
            return (2, speed)

        if neighbourhood > 3:
            panic = 1
        # else:
        #     # Check if a hazard is in vision
        #     for h in hazards:
        #         if (h.x - pos[0] <= vision) or (h.y - pos[1] <= vision):
        #             panic = 2
        #             speed = 1
        #             break

        return panic, speed
