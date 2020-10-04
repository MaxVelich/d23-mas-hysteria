
'''
This class performs the A* graph path finding algorithm. 

90% of this class is NOT written by us. We took the code straight from the following source. We adjusted it to our needs, and will probably change it a lot more in the future.
https://leetcode.com/problems/shortest-path-in-binary-matrix/discuss/313347/a-search-in-python
'''

from queue import PriorityQueue

from src.model.utils.Geometry import Geometry

class A_Star:

    def __init__(self, graph):
        self.graph = graph

    def find_path(self, start, goal):
        
        visited = set()
        came_from = dict()
        distance = { start: 0 }
        frontier = PriorityQueue()
        frontier.put((0, start))

        while not frontier.empty():
            
            node = frontier.get()

            if node[1] in visited:
                continue
            
            if goal == node[1]:
                return self.reconstruct_path(came_from, start, node[1])

            visited.add(node[1])
            successors = self.get_successor(node[1])
            
            for successor in successors:
                
                priority = 1 + Geometry.euclidean_distance(successor, goal) + distance[node[1]]
                frontier.put((priority, successor))

                if (successor not in distance or distance[node[1]] + 1 < distance[successor]):
                    distance[successor] = distance[node[1]] + 1
                    came_from[successor] = node[1]

    def get_successor(self, node):

        successors = []
        for edge in self.graph:
            if int(edge[0]) == int(node[0]) and int(edge[1]) == int(node[1]):
                successors += [(int(edge[2]), int(edge[3]))]
            elif int(edge[2]) == int(node[0]) and int(edge[3]) == int(node[1]):
                successors += [(int(edge[0]), int(edge[1]))]

        return successors

    def reconstruct_path(self, came_from, start, end):

        reverse_path = [end]
        while end != start:
            end = came_from[end]
            reverse_path.append(end)
        return list(reversed(reverse_path))