import strategies as st
from evaluator import EvaluationEngine
from agent import BaseAgent
from random import randint

for i in range(1):
  print(EvaluationEngine( 
    st.TitForTat(1,100),
    st.TitForTat(1,100)
    # st.Alternator(1),
    # st.AngryMan_v6(2,min_forgiveness=3),
    ).printGame())