import strategies as st
from evaluator import EvaluationEngine
from agent import BaseAgent
from random import randint
import copy,threading,queue

lock = threading.Lock()

def round(player1,i, player2,j, leaderboard):
    with lock:
        copy1 = copy.deepcopy(player1)
        copy2 = copy.deepcopy(player2)
    engine = EvaluationEngine(
                copy1,
                copy2,
            )
    result = engine.playGame()
    with lock:
        leaderboard[f'{i} {player1.name}'] += result[1]
    print(f'{player1.name} vs {player2.name} : {result[1]}  _  {result[2]}')
    
    

def round_robin():
    id1_players = player_initialization(1)
    num_players = len(id1_players)
    leaderboard = {f'{i}) {player.name}': 0 for i,player in enumerate(id1_players)}
    print(leaderboard)

    id2_players = player_initialization(2)
    for i in range(num_players):
        threads = []
        print("Printing rounds for :",id1_players[i].name)
        for j in range(num_players):
            t1 = threading.Thread(target=round, args=(
                id1_players[i],i,id2_players[j],j,leaderboard
            ))
            threads.append(t1)
            t1.start()
            
    for thread in threads:
        thread.join()
                    

    return leaderboard

def player_initialization(id):
  return [
      st.AngryMan_v4(id,base_exponent=1),
      st.AngryMan_v4(id,base_exponent=2),
      st.fixedCooperator(id,cooperation=21),
      st.fixedCooperator(id,cooperation=26),
      st.TitForTat(id,first_move=1,forgiveness=0),
      st.TitForTat(id,first_move=1,forgiveness=5),
      st.TitForTat(id,first_move=-1,forgiveness=0),
      st.TitForTat(id,first_move=-1,forgiveness=5),
      st.TitForTat(id,first_move=1,forgiveness=5),
      st.randomDefect(id,0),
      st.AngryMan_v6(id,min_forgiveness=5),
      st.AngryMan_v6(id,min_forgiveness=2),
      st.xCoopDefectCycle(id,26,3),
      st.xCoopDefectCycle(id,56,3),
      st.xCoopDefectCycle(id,56,5),
      st.xCoopDefectCycle(id,15,3),
    ]
  
if __name__ == "__main__":
    # Example usage
    leaderboard = round_robin()
    sorted_leaderboard = sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)

    print("Final Leaderboard:")
    for idx, (player_name, score) in enumerate(sorted_leaderboard, start=1):
        print(f"{idx}. {player_name}: {score}")
