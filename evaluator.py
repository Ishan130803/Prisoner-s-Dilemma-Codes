import time, threading, random, math, json, copy
from agent import BaseAgent
import p1,p2
from random import randint
import pprint
from threading import Lock

lock = Lock()



class EvaluationEngine:
  program_names = ['agent1', 'agent2']
  COOP = 1
  DEFECT = -1
  

  coop_win = lambda x: 20 + 5 * (x // 5)
  betrayal_win = lambda x: 45
  betrayal_lose = lambda x: -10 * (x // 5)
  defect = lambda x: -5 * (x // 5)
  payoff_matrx = [[coop_win, coop_win], [betrayal_win, betrayal_lose], [defect, defect]]

  def __init__(self, player1, player2):
    self.player_threads = []
    self.streak = 0
    self.history = {}
    self.iteration = 1
    self.score = {1: 0, 2: 0}
    self.rounds = randint(150,200)
    self.time_limit = 0.01  # seconds
    self.error = -0.1
    self.player1 = player1
    self.player2 = player2  
    self.players: list[BaseAgent] = [self.player1, self.player2]
    self.move_queue = [0, 0]
    

    

  def threaded_player_call(self, player, streak, iteration):
      with lock:
         state = {"current_iter": iteration, "history": self.history, "streak": streak}
         state = copy.deepcopy(state)
      move = self.players[player].next_move(state)
      # print(f"Player {player}:", move, iteration, history)
      if not iteration in self.history:
          self.move_queue[player] = move


  def event_loop(self):
      while self.iteration <= self.rounds:
          # Starts threads to wait for agents to update move_queue and then waits for time limit
          t1 = threading.Thread(target=self.threaded_player_call, args=(0, self.streak, self.iteration))
          t2 = threading.Thread(target=self.threaded_player_call, args=(1, self.streak, self.iteration))
          t1.start(); t2.start()
          time.sleep(self.time_limit)

          # If TLE on first then random, else repeat last move
          if not self.move_queue[0] or self.move_queue[0] not in [EvaluationEngine.COOP, EvaluationEngine.DEFECT]:
              if self.iteration == 1:
                  self.move_queue[0] = random.choice([EvaluationEngine.COOP, EvaluationEngine.DEFECT])
              else:
                  self.move_queue[0] = self.history[self.iteration - 1][1]

          if not self.move_queue[1] or self.move_queue[1] not in [EvaluationEngine.COOP, EvaluationEngine.DEFECT]:
              if self.iteration == 1:
                  self.move_queue[1] = random.choice([EvaluationEngine.COOP, EvaluationEngine.DEFECT])
              else:
                  self.move_queue[1] = self.history[self.iteration - 1][2]

          # errors in communication with agents
          is_err1 = random.random() < self.error
          is_err2 = random.random() < self.error

          if is_err1:
              self.move_queue[0] = -self.move_queue[0]
          if is_err2:
              self.move_queue[1] = -self.move_queue[1]

          """
          Payoff matrix calculations
          Streak is not reset to 0 if rift in communication is caused by errors
          """

          if self.move_queue[0] == EvaluationEngine.COOP and self.move_queue[1] == EvaluationEngine.COOP:
              self.score[1] += self.payoff_matrx[0][0](self.streak)
              self.score[2] += self.payoff_matrx[0][1](self.streak)
              self.streak += 1
          elif self.move_queue[0] == EvaluationEngine.DEFECT and self.move_queue[1] == EvaluationEngine.COOP:
              self.score[1] += self.payoff_matrx[1][0](self.streak)
              self.score[2] += self.payoff_matrx[1][1](self.streak)
              self.streak = math.ceil(self.streak / 2) if (is_err1 or is_err2) else 0
          elif self.move_queue[0] == EvaluationEngine.COOP and self.move_queue[1] == EvaluationEngine.DEFECT:
              self.score[1] += self.payoff_matrx[1][1](self.streak)
              self.score[2] += self.payoff_matrx[1][0](self.streak)
              self.streak = math.ceil(self.streak / 2) if (is_err1 or is_err2) else 0
          else:
              self.score[1] += self.payoff_matrx[2][0](self.streak)
              self.score[2] += self.payoff_matrx[2][1](self.streak)
              self.streak = math.ceil(self.streak / 2) if (is_err1 and is_err2) else 0
          with lock:
                self.history[self.iteration] = {
                    1: self.move_queue[0],
                    2: self.move_queue[1],
                    "score": copy.deepcopy(self.score),
                }
          move_queue = [0, 0]

          self.iteration += 1
          t1.join(); t2.join()
  def playGame(self):
      self.event_loop()
      return self.history[self.rounds]['score']
  def printGame(self):
      self.event_loop()
      pprint.pprint(self.history)
      
          
# engine = EvaluationEngine(p1.p1(1),p2.p2(2))
# engine.event_loop()


# print(rounds,history[rounds])
# print(json.dumps(history, indent=2))
