import strategies as st
from evaluator import EvaluationEngine as e1
from evaluator_round_2 import EvaluationEngine as e2
from agent import BaseAgent
from random import randint
import copy, threading, queue
import pandas as pd

lock = threading.Lock()


def round(player1, i, player2, j, leaderboard):
    with lock:
        copy1 = copy.deepcopy(player1)
        copy2 = copy.deepcopy(player2)
        copy1.id = 1
        copy2.id = 2
    engine = e2(
        copy1,
        copy2,
    )
    result = engine.playGame()
    with lock:
        leaderboard[f"{i}) {player1.name}"] += result[1]
        leaderboard[f"{j}) {player2.name}"] += result[2]

    # print(f'{i}__ {player1.name} vs {i}__ {player2.name} : {result[1]}  _  {result[2]}')


def round_robin(players, leaderboard):
    num_players = len(players)

    # print(leaderboard)

    id2_players = player_initialization(2)
    threads = []
    for i in range(num_players):
        for j in range(i, num_players):
            t1 = threading.Thread(
                target=round, args=(players[i], i, players[j], j, leaderboard)
            )
            threads.append(t1)
            t1.start()

    for thread in threads:
        thread.join()

    return leaderboard


def player_initialization(id):
    return [
        st.AngryMan_v4(id, base_exponent=1),
        st.TitForTat(id, first_move=1, forgiveness=0),
        st.TitForTat(id, first_move=1, forgiveness=5),
        st.TitForTat(id, first_move=1, forgiveness=10),
        st.TitForTat(id, first_move=1, forgiveness=15),
        st.randomDefect(id, 0),
        st.randomDefect(id, 0),
        st.randomDefect(id, 0),
        st.AngryMan_v6(id, min_forgiveness=5),
        st.AngryMan_v6(id, min_forgiveness=2),
        st.AngryMan_v7(id, min_forgiveness=0),
        st.TitForTatwDishonesty(id, 10),
        # st.TitForTatwDishonesty(id, 12),
        # st.TitForTatwDishonesty(id, 14),
        # st.TitForTatwDishonesty(id, 16),
        # st.TitForTatwDishonesty(id, 18),
        # st.TitForTatwDishonesty(id, 20),
        # st.TitForTatwDishonesty(id, 8),
        # st.TitForTatwDishonesty(id, 6),
        # st.TitForTatwDishonesty(id, 4),
        # st.TitForTatwDishonesty(id, 2),
        # st.TitForTatwDishonesty(id, 0),
        # st.TitForTatwDishonesty(id, 20),
        # st.RandomForgivenessTitForTat(id),
        st.SneakyDefector(id, 3),
        st.SneakyDefector(id, 4),
        st.SneakyDefector(id, 5),
        st.SneakyDefector(id, 6),
        st.SneakyDefector(id, 7),
        st.SneakyDefector(id, 8),
        st.SneakyDefector(id, 9),
        st.RandomForgivenessTitForTat(id),
    ]


if __name__ == "__main__":
    # Example usage
    df = pd.read_csv("Data.csv")
    players = player_initialization(1)
    leaderboard = {f"{i}) {player.name}": 0 for i, player in enumerate(players)}
    print(leaderboard.keys())
    # df = pd.DataFrame(columns = leaderboard.keys())
    for i in range(1):
        for i in leaderboard:
            leaderboard[i] = 0
        leaderboard = round_robin(players, leaderboard)
        df.loc[len(df)] = pd.Series(leaderboard)
        sorted_leaderboard = sorted(
            leaderboard.items(), key=lambda x: x[1], reverse=True
        )
        df.to_csv("Data.csv", index=False)
        print("Final Leaderboard:")
        for idx, (player_name, score) in enumerate(sorted_leaderboard, start=1):
            print(f"{idx}. {player_name}: {score}")
