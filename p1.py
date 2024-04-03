from agent import BaseAgent
from random import randint
from math import floor

class p1(BaseAgent):
    def __init__(self, id):
        super().__init__(id=id)
        self.forgiveness = 100
        self.exponent = 1;
        self.hasDefected = False
        self.current_strek = 0
        self.isEarlyDefecter = False

    # def next_move(self, state):
    #     op_id = 1 if self.id == 2 else 2
    #     itr = state["current_iter"]
    #     # if itr == 1:
    #     #     return 1
    #     # if (state["history"][itr-1][op_id] == -1 and state["history"][itr-1][self.id] == 1):
    #     #     self.decrement_forgiveness()
    #     #     decision = 1 if randint(1,100) < self.forgiveness else -1
    #     #     return decision
    #     # if (state["history"][itr-1][op_id] == 1 and state["history"][itr-1][self.id] == -1):
    #     #     decision = 1 if randint(1,100) < self.forgiveness else -1
        
    #     return -1
    ##Tit for Tat with defection
    # def next_move(self,state):
    #     op_id = 1 if self.id == 2 else 2
    #     itr = state["current_iter"]
    #     if (itr == 1):
    #         return -1;
    #     return state["history"][itr-1][op_id]
    #Tit for Tat with cooperation
    # def next_move(self,state):
    #     op_id = 1 if self.id == 2 else 2
    #     itr = state["current_iter"]
    #     if (itr == 1):
    #         return 1;
    #     return state["history"][itr-1][op_id]
    # 
    # #The Angry man
    # def next_move(self,state):
    #     op_id = 1 if self.id == 2 else 2
    #     itr = state["current_iter"]
    #     if (itr == 1):
    #         return 1;
    #     if (self.hasDefected):
    #         return -1
    #     if state["history"][itr-1][op_id] == -1:
    #         if randint(1,100) < self.forgiveness:
    #             self.decrement_forgiveness()
    #             return -1
    #         else:
    #             self.hasDefected = True
    
    #The Angry man v2
    # def next_move(self,state):
    #     op_id = 1 if self.id == 2 else 2
    #     itr = state["current_iter"]
    #     if (itr == 1):
    #         return 1;
    #     if (self.hasDefected):
    #         return -1
    #     if state["history"][itr-1][op_id] == -1:
    #         self.decrement_forgiveness()
    #         if randint(1,100) < self.forgiveness:
    #             return 1
    #         else:
    #             self.hasDefected = True
    #             return -1
    #     return 1
    
    # # The Angry man v3
    # def next_move(self,state):
    #     op_id = 1 if self.id == 2 else 2
    #     itr = state["current_iter"]
    #     if (itr == 1):
    #         return 1;
    #     if (state["history"][itr-1][op_id] == 1 and state["history"][itr-1][op_id] == 1):
    #         self.current_strek += 1
    #     if (self.hasDefected):
    #         return -1
    #     if state["history"][itr-1][op_id] == -1:
    #         for i in range(1,floor(self.current_strek / 5)+2):
    #             self.decrement_forgiveness()
    #         if randint(1,100) < self.forgiveness:
    #             return 1
    #         else:
    #             self.hasDefected = True
    #             return -1
    #     return 1
    
    # # Angry Man v4 (Best so far)
    # def next_move(self,state):
    #     op_id = 1 if self.id == 2 else 2
    #     itr = state["current_iter"]
    #     if (itr == 1):
    #         return 1;
    #     if (state["history"][itr-1][op_id] == 1 and state["history"][itr-1][op_id] == 1):
    #         self.current_strek += 1
    #     if (self.hasDefected):
    #         return -1
    #     if state["history"][itr-1][op_id] == -1:
    #         for i in range(1,floor(self.current_strek / 5)+2):
    #             if (self.forgiveness):
    #                 self.forgiveness -= 2*self.exponent*self.exponent*self.exponent #98 82 28 0
    #                 if (self.forgiveness < 0): 
    #                     self.forgiveness = 0
    #         else:
    #             self.exponent+=1
    #         if randint(1,100) < self.forgiveness:
    #             return 1
    #         else:
    #             self.hasDefected = True
    #             return -1
    #     return 1
    
    # # Angry Man v5 with hostility for immediate defectors
    # def next_move(self,state):
    #     def decrement_forgiveness():
    #         if (self.forgiveness):
    #             self.forgiveness -= 2*self.exponent*self.exponent*self.exponent #98 82 28 0
    #             if (self.forgiveness < 0): 
    #                 self.forgiveness = 0
    #             else:
    #                 self.exponent+=1
                    
                    
    #     op_id = 1 if self.id == 2 else 2
    #     itr = state["current_iter"]
    #     if (itr == 1):
    #         return 1;
                
    #     if (state["history"][itr-1][op_id] == 1 and state["history"][itr-1][op_id] == 1):
    #         self.current_strek += 1
    #     if (self.hasDefected):
    #         return -1
    #     if state["history"][itr-1][op_id] == -1:
    #         if (itr <= 2 and not self.isEarlyDefecter):
    #             if state["history"][itr-1][op_id] == -1:
    #                 self.exponent += 1
    #                 self.isEarlyDefecter = True
    #                 decrement_forgiveness()
    #             else:
    #                 [decrement_forgiveness() for i in range(1,floor(self.current_strek / 5)+2)] 
    #         else:
    #             self.exponent+=1
    #         if randint(1,100) < self.forgiveness:
    #             return 1
    #         else:
    #             self.hasDefected = True
    #             return -1
    #     return 1
    
    def next_move(self,state):
        op_id = 1 if self.id == 2 else 2
        itr = state["current_iter"]
        if (itr == 1):
            return 1;
        if (state["history"][itr-1][op_id] == 1):
            return 1;
        else:
            return -1;
    
    def decrement_forgiveness(self):
            if (self.forgiveness):
                self.forgiveness -= 2*self.exponent*self.exponent*self.exponent #98 82 28 0
                if (self.forgiveness < 0): 
                    self.forgiveness = 0
                else:
                    self.exponent+=1
        

                