from agent import BaseAgent
from random import randint
import threading, copy

class p2(BaseAgent):
    def __init__(self, id):
        super().__init__(id=id)
        self.forgiveness = 20

    def next_move(self, state):
        op_id = 1 if self.id == 2 else 2
        i = randint(1, 100)
        if i>5:
            return -1
        return 1
    
    # # Tit for Tat with defection
    # def next_move(self,state):
    #     op_id = 1 if self.id == 2 else 2
    #     itr = state["current_iter"]
    #     if (itr == 1):
    #         return -1;
    #     return state["history"][itr-1][op_id]
    
    # Tit for Tat with cooperation
    def next_move(self,state):
        op_id = 1 if self.id == 2 else 2
        itr = state["current_iter"]
        if (itr == 1):
            return 1;
        if (state["history"][itr-1][op_id] == 1):
            return 1;
        else:
            return -1;
        
    # # Tit for Tat with cooperation and forgiveness
    # def next_move(self,state):
    #     op_id = 1 if self.id == 2 else 2
    #     itr = state["current_iter"]
    #     if (itr == 1):
    #         return 1;
    #     if (state["history"][itr-1][op_id] == 1):
    #         return 1;
    #     else:
    #         if (randint(1,100) < self.forgiveness):
    #             return 1
    #         else:
    #             return -1;
    
    # # Always Defect
    # def next_move(self,state):
    #     op_id = 1 if self.id == 2 else 2
    #     itr = state["current_iter"]
    #     # if (itr == 1):
    #     #     return 1;
    #     return -1
    
    # Always Defect
    # def next_move(self,state):
    #     op_id = 1 if self.id == 2 else 2
    #     itr = state["current_iter"]
    #     # if (itr == 1):
    #     #     return 1;
    #     return -1
    
    ## 21 times cooperator
    # def next_move(self,state):
    #     op_id = 1 if self.id == 2 else 2
    #     itr = state["current_iter"]
    #     if (itr <= 26):
    #         return 1;
    #     return 1


                

