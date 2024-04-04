import strategies as st
from evaluator import EvaluationEngine as e1
from evaluator_round_2 import EvaluationEngine as e2
from agent import BaseAgent
from random import randint

for i in range(1):
  print(e2( 
    st.TitForTat(1,3),
    # st.Alternator(1),
    st.SneakyDefector(2)
    # st.AngryMan_v6(2,min_forgiveness=3),
    ).printGame()) 