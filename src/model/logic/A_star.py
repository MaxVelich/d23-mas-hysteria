
'''
This class performs the A* graph path finding algorithm. 

80% of this class is NOT written by us. We took the code from the following source. We adjusted it to our needs.
https://leetcode.com/problems/shortest-path-in-binary-matrix/discuss/313347/a-search-in-python
'''

from heapq import *

from src.model.utils.Geometry import Geometry
from src.model.utils.Utilities import Utilities

class A_Star:

    def __init__(self, graph):
        self.graph = graph

    def find_path(self, start, goal):
        
        visited = set()
        came_from = dict()
        distance = { start: 0 }
        frontier = []
        heappush(frontier, (0, start))

        while not len(frontier) == 0:
            
            node = heappop(frontier)

            if node[1] in visited:
                continue
            
            if goal == node[1]:
                return self.__reconstruct_path(came_from, start, node[1])

            visited.add(node[1])
            successors = self.__get_successor(node[1])
            
            for successor in successors:
                
                priority = 1 + Geometry.euclidean_distance(successor, goal) + distance[node[1]]
                heappush(frontier, (priority, successor))

                if (successor not in distance or distance[node[1]] + 1 < distance[successor]):
                    distance[successor] = distance[node[1]] + 1
                    came_from[successor] = node[1]

    def __get_successor(self, node):

        successors = []
        for edge in self.graph:

            edge_point_1 = (edge[0], edge[1])
            edge_point_2 = (edge[2], edge[3])

            if Utilities.check_if_points_are_approximately_the_same(edge_point_1, node):
                successors += [ edge_point_2 ]
            elif Utilities.check_if_points_are_approximately_the_same(edge_point_2, node):
                successors += [ edge_point_1 ]

        return successors

    def __reconstruct_path(self, came_from, start, end):

        reverse_path = [end]
        while end != start:
            end = came_from[end]
            reverse_path.append(end)

        return list(reversed(reverse_path))