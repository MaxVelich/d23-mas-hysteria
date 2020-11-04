
'''
This class models the agents, or people in our case. This class is a decendent of the Agent class of MESA. This class handles the behaviour of the agents. They set goals, plan routes and react to other agents in the environment. 
'''

from mesa import Agent
import random

from src.model.logic.Panic_Dynamic import Panic_Dynamic
from src.model.logic.Path_Finder import Path_Finder
from src.model.logic.Theory_Of_Mind import Theory_Of_Mind

from src.model.utils.Geometry import Geometry
from src.model.utils.Utilities import Utilities

class Person(Agent):

    def __init__(self, unique_id, model, tom, panic_thresholds):

        super().__init__(unique_id, model)

        self.panic = 0
        self.theory_of_mind = tom
        self.panic_thresholds = panic_thresholds

        self.escaped = False
        self.stuck_counter = 0
        self.panic_fatigue = 0

    def radius(self):
        return 8
    
    def neighbour_radius(self):
        return 40

    def prepare_path_finding(self):
        '''
        Each agents needs to find a goal and a path to the goal before starting to move. This function is called externally.
        '''

        self.goal = self.__determine_goal()
        print("Agent " + str(self.unique_id) + "'s goal was set " + str(self.goal) + " --- Route is being planned ...")
        self.path_finder.set_goal(self.pos, self.goal)

    def step(self):
        '''
        This function is called at each step of the model. Here we check if the agent is close to an exit, and record that if that is the case.
        '''

        if self.__check_if_at_exit():
            if self.theory_of_mind == 0:
                self.model.regular_times.append(self.model.time)
            else:
                self.model.tom_times.append(self.model.time)
            return        

        self.move()

    def move(self):
        '''
        In order to move, the agent moves according to a path finding algorithm. This method is not finished yet, since it is very inefficient and unrealistic at this moment, though it makes for a demo.
        '''

        # First we determine the current panic level
        self.panic = Panic_Dynamic.change_panic_level(len(self.__neighbors()), self.pos, self.panic_thresholds)

        if self.panic == 2:

            # We handle prolonged panic of the agents with a counter
            self.panic_fatigue += 1

            if self.panic_fatigue < 5:
                # As long as the agent only recently became panicked, it follow the panic move.
                move = self.__make_panic_move()
            else:
                # If it was panicked for too long, we make a normal move -- the agent calms down a bit and tries a normal move.
                move = self.__make_normal_move()
        else:

            # If the agent is not panicked, find a normal move
            move = self.__make_normal_move()
        
        # Reset the panic fatigue
        if self.panic_fatigue > 8:
            self.panic_fatigue = 0

        if not move == None:

            # If a move could be found previously, the agent needs to check if its a 'good' one
            if self.__check_if_hazard_is_nearby(move):

                if self.__check_if_hazard_blocks_goal():

                    # If there is a hazard nearby and the hazard blocks the exit, the agent needs to turn to a different goal
                    self.goal = self.__select_different_goal(self.goal)
                else:

                    # If the hazard does not block the goal, the agent can plan around the hazard
                    self.path_finder.replan_around_hazard(self.pos, self.goal, self.model.hazard)
                return

            # If no hazard is nearby, the agent can move
            self.model.space.move_agent(self, move)
            self.stuck_counter = 0 # agent was not stuck anymore, so reset the counter
        else:
            # If no move could be found, then the agents need to find an alternative route
            self.__replan(self.pos)
            self.stuck_counter += 1 # agent was stuck, so increase the counter

        # In case the agent was stuck for too long, it needs to find a different goal
        if self.stuck_counter > 5:
            self.goal = self.__select_different_goal(self.goal, True)
            self.path_finder.set_goal(self.pos, self.goal)
            self.stuck_counter = 0

    ### PRIVATE INTERFACE

    def __replan(self, from_position):
        '''
        Sometimes the agent can't move anymore due to its environment, then the agents needs to replan
        '''

        neighbors_positions = [ neighbor.pos for neighbor in self.__neighbors() ]
        self.path_finder.plan_detour(from_position, self.goal, neighbors_positions)
    
    def __make_panic_move(self):
        '''
        Here we handle how an agent treat a move when it panicks. We first get the average direction from the surrounding agents, then we try to find the next practical state the agent could occupy.
        '''

        direction = Panic_Dynamic.average_direction_of_crowd(self.__neighbors(), self.pos, self)
        new_position = (self.pos[0] + direction[0], self.pos[1] + direction[1])

        # Following the crowd might not be possible due to occupied space, then the agent needs to find the next best open spot
        neighbors_positions = [ neighbor.pos for neighbor in self.__neighbors() ]
        move = self.path_finder.try_to_find_side_step_move(new_position, self.pos, neighbors_positions)

        # If the move is valid and clear, this function returns the move
        if self.__check_if_next_move_is_clear(move):
            return move

        return None

    def __make_normal_move(self):
        '''
        Each agent has a plan stored in the path finder class. In case of a normal move, the agent simply follows the plan if possible. 
        '''

        next_move = self.path_finder.get_next_step(self.pos)
        if next_move == None or next_move == []:

            # If the next move is None, it means that the path finder could not find a path -- the path to the current goal is blocked
            return None

        if self.__check_if_next_move_is_clear(next_move):
            return next_move
        else:

            # if the next move is not empty, the agent can try to "dance around" the obstacles via side steps
            neighbors_positions = [ neighbor.pos for neighbor in self.__neighbors() ]
            side_step = self.path_finder.try_to_find_side_step_move(self.pos, next_move, neighbors_positions)

            if not side_step == None:
                return side_step

        return None

    def __check_if_hazard_is_nearby(self, move):

        hazard = self.model.hazard
        danger_radius = hazard.danger_radius()
        return Geometry.point_lies_in_circle(move, hazard.pos, danger_radius)

    def __check_if_hazard_blocks_goal(self):

        hazard = self.model.hazard
        danger_radius = hazard.danger_radius()
        return Geometry.point_lies_in_circle(self.goal, hazard.pos, danger_radius)

    def __select_different_goal(self, without_other_goal, chaotic = False):
        '''
        Sometimes, an agent needs to change its goal. This can happen deliberatly (in case of a Theory of Mind agent), or chaotically, in case the last goal was obstructed by the hazard
        '''

        exit_positions = [ exit.pos for exit in self.model.exits ]
        filtered_exits = [ exit for exit in exit_positions if not exit == without_other_goal ]

        if chaotic:
            chosen_exit = random.choice(filtered_exits)
        else:
            chosen_exit = Utilities.find_closest_point_of_set_of_points(self.pos, filtered_exits)

        return chosen_exit

    def __check_if_next_move_is_clear(self, move):

        can_move = True
        for other_agent in self.__neighbors():
            if move == other_agent.pos:
                can_move = False
        
        return can_move

    def __check_if_at_exit(self):

        for exit in self.model.exits:
            
            distance = Geometry.euclidean_distance(exit.pos, self.pos)
            if distance < exit.leavable_radius():

                # If the agent is in range of the exit, remove it from the scheduler and the environment -- the agent has left the building
                self.escaped = True
                self.model.schedule.remove(self)
                self.model.space.remove_agent(self)
                return True

        return False

    def __neighbors(self):
        
        neighbors = []
        for agent in self.model.space.get_neighbors(self.pos, self.neighbour_radius()):
            if not agent == self:
                neighbors.append(agent)

        return neighbors

    def __determine_goal(self):
        '''
        Find the closest goal, or, in case of Theory of Mind agents, find a goal that is not aimed at by the majority of the neighbours.
        '''

        self.path_finder = Path_Finder(self.model.world_mesh)

        exits = [ exit.pos for exit in self.model.exits ]
        goal = Utilities.find_closest_point_of_set_of_points(self.pos, exits)

        if self.theory_of_mind == 1:
            if Theory_Of_Mind.agent_should_switch_goal(exits, self.pos, self.__neighbors(), goal):
                for other_exit in exits:
                    if not other_exit == goal:
                        goal = other_exit
                        break
        
        return goal