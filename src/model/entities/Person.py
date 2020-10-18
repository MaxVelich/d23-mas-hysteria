
'''
This class models the agents, or people in our case. This class is a decendent of the Agent class of MESA. This class lacks quite a lot still.
'''

from mesa import Agent
from src.model.logic.Panic_Dynamic import Panic_Dynamic
from src.model.logic.Path_Finder import Path_Finder
from src.model.logic.Theory_Of_Mind import Theory_Of_Mind as ToM

class Person(Agent):

    def __init__(self, unique_id, model, tom):

        super().__init__(unique_id, model)
        self.panic = 0
        self.velocity = 1
        self.speed = 1.0
        self.vision = 40
        self.next_move = None
        # 0 = ToM0, 1 = ToM1
        self.theory_of_mind = tom

    def prepare_path_finding(self):
        
        self.path_finder = Path_Finder(self.model.world_mesh)
        self.goal = self.path_finder.find_nearest_goal(self.pos)
        if(self.theory_of_mind == 1):
            print("my ToM level is: " + str(self.theory_of_mind))
            neighbors = self.model.space.get_neighbors(self.pos, self.vision)
            print("I have " + str(len(neighbors)) + " neighbors")
            ToM.determine_neighbor_exit_strategy(self.path_finder, neighbors)
            # TODO: See Theory_Of_Mind

        self.path_finder.set_goal(self.pos, self.goal)

    def step(self):

        near_by_agents = self.model.space.get_neighbors(self.pos, self.vision)

        self.move()

        if self.check_if_at_exit():
            self.model.schedule.remove(self)
        else:
            self.panic, self.speed = Panic_Dynamic.change_panic_level(len(near_by_agents))
            if self.panic == 2:
                self.velocity = Panic_Dynamic.cohere(near_by_agents, self.pos, self) / 2

    def move(self):
        '''
        In order to move, the agent moves according to a path finding algorithm. This method is not finished yet, since it is very inefficient and unrealistic at this moment, though it makes for a demo.
        '''

        if self.next_move is None:
            self.next_move = self.path_finder.get_next_step(self.pos)

        if self.next_move[0] == self.pos[0] and self.next_move[1] == self.pos[1]:
            self.next_move = self.path_finder.get_next_step(self.pos)
        
        print(self.next_move)

        delta_pos_x = self.next_move[0] - self.pos[0]
        delta_pos_y = self.next_move[1] - self.pos[1]
        
        if delta_pos_x < 0:
            delta_x = -1
        elif delta_pos_x > 0:
            delta_x = 1
        else:
            delta_x = 0

        if delta_pos_y < 0:
            delta_y = -1
        elif delta_pos_y > 0:
            delta_y = 1
        else:
            delta_y = 0

        self.model.space.move_agent(self, (self.pos[0] + delta_x*5, self.pos[1] + delta_y*5))

    def check_if_at_exit(self):

        threshold = 4
        for exit in self.model.exits:
            if abs(self.pos[0] - exit.x) < threshold and abs(self.pos[1] - exit.y) < threshold:
                return True
        return False
