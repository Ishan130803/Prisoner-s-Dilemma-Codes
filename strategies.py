from agent import BaseAgent
from random import randint
from math import floor


class TitForTat(BaseAgent):
    def __init__(self, id, forgiveness=20, first_move=1, name="TitForTat"):
        super().__init__(id=id)
        self.forgiveness = forgiveness
        self.first_move = first_move
        self.name = f"{name}__first_move_{first_move}__forgiveness_{forgiveness}"

    def next_move(self, state):
        op_id = 1 if self.id == 2 else 2
        itr = state["current_iter"]
        if itr == 1:
            return self.first_move
        mylastMove = state["history"][itr - 1][self.id]
        oplastMove = state["history"][itr - 1][op_id]
        if oplastMove == -1:
            if randint(1, 100) <= self.forgiveness:
                return 1
            else:
                return -1
        return 1


class randomDefect(BaseAgent):
    def __init__(self, id, percent=80, name="randomDefect"):
        super().__init__(id=id)
        self.percent = percent
        self.name = f"{name}__r_{percent}"

    def next_move(self, state):
        op_id = 1 if self.id == 2 else 2
        i = randint(1, 100)
        if i > self.percent:
            return -1
        return 1


class fixedCooperator(BaseAgent):
    def __init__(self, id, cooperation=21, name="fixedCooperator"):
        super().__init__(id=id)
        self.cooperation = cooperation
        self.name = f"{name}__{cooperation}"

    def next_move(self, state):
        op_id = 1 if self.id == 2 else 2
        itr = state["current_iter"]
        if itr <= self.cooperation:
            return 1
        return -1


class AngryMan_v4(BaseAgent):
    def __init__(
        self,
        id,
        base_forgiveness=100,
        base_exponent=1,
        base_streak=0,
        name="AngryMan_v4",
    ):
        super().__init__(id=id)
        self.forgiveness = 100
        self.exponent = base_exponent
        self.hasDefected = False
        self.current_strek = 0
        self.isEarlyDefecter = False
        self.name = (
            f"{name}_bf_{base_forgiveness}__be_{base_exponent}__bs_{base_streak}"
        )

    def next_move(self, state):
        op_id = 1 if self.id == 2 else 2
        itr = state["current_iter"]
        if itr == 1:
            return 1
        if (
            state["history"][itr - 1][op_id] == 1
            and state["history"][itr - 1][op_id] == 1
        ):
            self.current_strek += 1
        if self.hasDefected:
            return -1
        if state["history"][itr - 1][op_id] == -1:
            for i in range(1, floor(self.current_strek / 5) + 2):
                if self.forgiveness:
                    self.forgiveness -= (
                        2 * self.exponent * self.exponent * self.exponent
                    )  # 98 82 28 0
                    if self.forgiveness < 0:
                        self.forgiveness = 0
                    else:
                        self.exponent += 1
            if randint(1, 100) < self.forgiveness:
                return 1
            else:
                self.hasDefected = True
                return -1
        return 1


class Tester(BaseAgent):
    def __init__(
        self, id, base_forgiveness=100, base_exponent=1, base_streak=0, name="Tester"
    ):
        super().__init__(id=id)
        self.forgiveness = 100
        self.exponent = base_exponent
        self.hasDefected = False
        self.current_strek = 0
        self.isEarlyDefecter = False
        self.name = (
            f"{name}_bf_{base_forgiveness}__be_{base_exponent}__bs_{base_streak}"
        )
        self.cooperation_ratio = 1
        self.cooperation_count = 1
        self.counted_round = 1
        self.defection_tolerance = 0.7
        self.titfortat_forgiveness = 0.1

    def next_move(self, state):
        op_id = 1 if self.id == 2 else 2
        itr = state["current_iter"]

        if itr == 1:
            return 1

        mylastMove = state["history"][itr - 1][self.id]
        oplastMove = state["history"][itr - 1][op_id]
        if mylastMove == 1 and oplastMove == 1:
            self.current_strek += 1
            self.counted_round += 1
            self.cooperation_count += 1
            self.cooperation_ratio = self.cooperation_count / self.counted_round

        elif mylastMove == -1 and oplastMove == 1:
            self.cooperation_count += 2
            self.counted_round += 1
            self.cooperation_ratio = (
                1
                if self.cooperation_count / self.counted_round > 1
                else self.cooperation_count / self.counted_round
            )

        elif mylastMove == 1 and oplastMove == -1:
            self.counted_round += 1
            self.cooperation_ratio = self.cooperation_count / self.counted_round

        if self.cooperation_ratio < 0.7 and itr > 10:
            if self.hasDefected:
                return -1
            if oplastMove == -1:
                for i in range(1, floor(self.current_strek / 5) + 2):
                    if self.forgiveness:
                        self.forgiveness -= (
                            2 * self.exponent * self.exponent * self.exponent
                        )  # 98 82 28 0
                        if self.forgiveness < 0:
                            self.forgiveness = 0
                        else:
                            self.exponent += 1
                self.current_strek = 0
                if randint(1, 100) < self.forgiveness:
                    return 1
                else:
                    self.hasDefected = True
                    return -1
            return 1
        else:
            if oplastMove == -1:
                if randint(1, 100) < self.titfortat_forgiveness:
                    return 1
                else:
                    return -1
            return 1


class AngryMan_v5(BaseAgent):
    def __init__(
        self,
        id,
        base_forgiveness=100,
        base_exponent=1,
        min_forgiveness=10,
        base_streak=0,
        name="AngryMan_v5",
    ):
        super().__init__(id=id)
        self.forgiveness = 100
        self.exponent = base_exponent
        self.current_strek = 0
        self.name = (
            f"{name}_bf_{base_forgiveness}__be_{base_exponent}__bs_{base_streak}"
        )
        self.isHonest = True
        self.honest_probability = 0
        self.dishonest_probability = 0
        self.min_forgiveness = min_forgiveness
        self.isTitForTat = False

    def next_move(self, state):
        op_id = 1 if self.id == 2 else 2
        itr = state["current_iter"]
        if itr == 1:
            return 1
        history = state["history"]
        mylastMove = history[itr - 1][self.id]
        oplastMove = history[itr - 1][op_id]
        if itr == 2:
            if oplastMove == -1:
                self.dishonest_probability += 1
                self.forgiveness = self.min_forgiveness

        if mylastMove == 1 and oplastMove == 1:
            self.honest_probability += 1

        if self.honest_probability > 30:
            self.isTitForTat = True

        if itr >= 2 and oplastMove == -1 and history[itr - 2][self.id] == 1:
            self.dishonest_probability += 1
            if self.dishonest_probability >= 2:
                self.hasDefected = True
                self.isHonest = False
        else:
            self.dishonest_probability = 0

        if not self.isHonest:
            return -1

        if oplastMove == -1:
            if self.forgiveness > self.min_forgiveness:
                self.forgiveness -= (
                    2 * self.exponent * self.exponent * self.exponent
                )  # 98 82 28 0
            if self.forgiveness < self.min_forgiveness:
                self.forgiveness = self.min_forgiveness
            else:
                self.exponent += 1
            if randint(1, 100) < self.forgiveness:
                return 1
            else:
                return -1
        return 1


class AngryMan_v6(BaseAgent):
    def __init__(
        self,
        id,
        base_forgiveness=100,
        base_exponent=1,
        min_forgiveness=10,
        base_streak=0,
        name="AngryMan_v6",
    ):
        super().__init__(id=id)
        self.forgiveness = 100
        self.exponent = base_exponent
        self.hasDefected = False
        self.current_strek = 0
        self.streak = 0
        self.name = (
            f"{name}_bf_{base_forgiveness}__be_{base_exponent}__bs_{base_streak}"
        )
        self.isHonest = True
        self.min_forgiveness = min_forgiveness
        self.min_base_forgive = min_forgiveness

        self.tft_prob = 0
        self.istft = False

        self.dishonest_probability = 0  # 10
        self.honest_probability = 0  # 11
        self.dumb = 0  # 01
        self.retaliation = 0  # 10
        self.deadlock = 0  # 00

        self.dumb_displayed = False

        self.taken_advantage = False
        self.total_dishonesty = 0
        self.recently_forgave = False

    def next_move(self, state):
        op_id = 1 if self.id == 2 else 2
        itr = state["current_iter"]
        if itr == 1:
            return 1
        history = state["history"]
        mylastMove = history[itr - 1][self.id]
        oplastMove = history[itr - 1][op_id]

        if self.dumb_displayed and oplastMove == 1:
            self.dumb += 1
            self.dumb_displayed = False
        else:
            self.dumb_displayed = False

        if itr == 2:
            if oplastMove == -1:
                self.dishonest_probability += 1
                self.forgiveness = self.min_forgiveness
        if mylastMove == 1 and oplastMove == 1:
            self.current_strek += 1
            self.streak %= 5
        else:
            self.current_strek = 0

        if itr > 2 and history[itr - 2][self.id] == 1 and oplastMove == 1:
            self.honest_probability += 1
            self.recently_forgave = False if self.recently_forgave else True
            if self.honest_probability % 5 == 0:
                self.dishonest_probability -= (
                    1 if self.dishonest_probability > -1 else 0
                )

        if itr > 2 and oplastMove == -1 and history[itr - 2][self.id] == 1:
            self.dishonest_probability += 1
            self.total_dishonesty += 1
            if self.dishonest_probability >= 2:
                self.isHonest = False
        elif self.dishonest_probability > 0:
            self.dishonest_probability = 0

        if itr > 2 and oplastMove == 1 and history[itr - 2][self.id] == -1:
            self.dumb += 1
            self.dumb_displayed = True
            if self.dumb >= 2:
                self.taken_advantage = True
                self.dumb = 0

        if itr > 2 and oplastMove == -1 and history[itr - 2][self.id] == -1:
            self.retaliation += 1
            self.taken_advantage = False
            self.dumb -= 5 if self.dumb - 5 >= 0 else 0

        if itr > 2 and oplastMove == -1 and mylastMove == -1:
            self.dumb -= 1
            self.deadlock += 1
            self.total_dishonesty -= 1 if self.total_dishonesty > 0 else 0
            if (
                self.honest_probability > 40
                and self.deadlock >= 2
                and not self.recently_forgave
            ):
                self.recently_forgave = True
                return 1
            self.dumb = 0
        else:
            self.deadlock = 0

        if self.taken_advantage:
            return -1
        # if (self.honest_probability > 30):
        #     self.istft = True

        if not self.isHonest and self.honest_probability < 30:
            return -1

        if oplastMove == -1:
            # if (self.forgiveness > self.min_forgiveness):
            #     self.forgiveness -= 2*self.exponent*self.exponent*self.exponent #98 82 28 0
            # if (self.forgiveness < self.min_forgiveness):
            #     self.forgiveness = self.min_forgiveness
            # else:
            #     self.exponent+=1
            if randint(1, 100) < self.min_forgiveness:
                return 1
            else:
                return -1
        return 1


class Alternator(BaseAgent):
    def __init__(self, id, name="Alternator"):
        super().__init__(id=id)
        self.name = f"{name}"

    def next_move(self, state):
        op_id = 1 if self.id == 2 else 2
        itr = state["current_iter"]

        if itr % 2 == 0:
            return -1
        return 1


class xCoopDefectCycle(BaseAgent):
    def __init__(self, id, period=16, forgiveness=2, name="xCoopDefectCycle"):
        super().__init__(id=id)
        self.name = f"{name}"
        self.period = period
        self.coop = 1
        self.forgiveness = forgiveness

    def next_move(self, state):
        op_id = 1 if self.id == 2 else 2
        itr = state["current_iter"]
        history = state["history"]
        if itr == 1:
            return 1
        mylastMove = history[itr - 1][self.id]
        oplastMove = history[itr - 1][op_id]

        if mylastMove == 1 and oplastMove == 1:
            self.coop += 1
        if self.coop % self.period == 0:
            self.coop = 1
            return -1
        if oplastMove == -1:
            if randint(1, 100) < self.forgiveness:
                return 1
            else:
                return -1
        else:
            return 1


class TitForTatWdld(BaseAgent):
    def __init__(self, id, forgiveness=20, name="TitForTatWdld"):
        super().__init__(id=id)
        self.forgiveness = forgiveness
        self.name = f"{name}__forgiveness_{forgiveness}"
        self.honest_probability = 0  # 11
        self.deadlock = 0  # 00
        self.current_strek = 0
        self.streak = 0
        self.retaliation_cycle = False
        self.dishonest_probability = 0
        self.total_dishonesty = 0

    def next_move(self, state):
        op_id = 1 if self.id == 2 else 2
        itr = state["current_iter"]
        if itr == 1:
            return 1
        history = state["history"]
        mylastMove = state["history"][itr - 1][self.id]
        oplastMove = state["history"][itr - 1][op_id]
        print(
            self.honest_probability, self.dishonest_probability, self.total_dishonesty
        )

        if oplastMove == -1:
            self.total_dishonesty += 1

        if self.total_dishonesty >= 4:
            self.forgiveness = 0
        if (
            itr > 4
            and history[itr - 3][self.id] == 1
            and history[itr - 2][op_id] == 1
            and history[itr - 2][self.id] == -1
            and history[itr - 1][op_id] == -1
        ):
            self.retaliation_cycle = True
            self.forgiveness = 0
            return 1

        if mylastMove == 1 and oplastMove == 1:
            self.current_strek += 1
            self.streak = self.current_strek // 5
        else:
            self.current_strek = 0
            self.streak = 0

        if itr > 2 and oplastMove == -1 and mylastMove == -1:
            self.deadlock += 1
            if self.honest_probability > 20 and self.deadlock >= 2:
                self.honest_probability = 0
                return 1
        else:
            self.deadlock = 0

        if itr > 2 and history[itr - 2][self.id] == 1 and oplastMove == 1:
            self.honest_probability += 1

        if itr > 2 and oplastMove == -1 and history[itr - 2][self.id] == 1:
            self.dishonest_probability += 1
            self.total_dishonesty += 1
            if self.dishonest_probability >= 2:
                self.forgiveness = 0

        if oplastMove == -1:
            if randint(1, 100) <= self.forgiveness:
                return 1
            else:
                return -1
        return 1

# Forgiveness reduces exponentially after 
# It actievely searches for tft and breaks the deadlocks which form due to TFT 
# Defection
class AngryMan_v7(BaseAgent):
    def __init__(
        self,
        id,
        base_forgiveness=100,
        base_exponent=1,
        min_forgiveness=10,
        base_streak=0,
        name="AngryMan_v7",
    ):
        super().__init__(id=id)
        self.forgiveness = 100
        self.exponent = base_exponent
        self.hasDefected = False
        self.current_strek = 0
        self.streak = 0
        self.name = f"{name}_bf_{min_forgiveness}"
        self.isHonest = True
        self.min_forgiveness = min_forgiveness
        self.min_base_forgive = min_forgiveness

        self.tft_prob = 0
        self.istft = False

        self.dishonest_probability = 0  # 10
        self.honest_probability = 0  # 11
        self.retaliation = 0  # 10
        self.deadlock = 0  # 00

        self.total_dishonesty = 0
        self.recently_forgave = False

    def next_move(self, state):
        op_id = 1 if self.id == 2 else 2
        itr = state["current_iter"]
        if itr == 1:
            return 1
        history = state["history"]
        mylastMove = history[itr - 1][self.id]
        oplastMove = history[itr - 1][op_id]

        if itr == 2:
            if oplastMove == -1:
                self.dishonest_probability += 1
                self.forgiveness = self.min_forgiveness
        if mylastMove == 1 and oplastMove == 1:
            self.current_strek += 1
            self.streak %= 5
        else:
            self.current_strek = 0

        if itr > 2 and history[itr - 2][self.id] == 1 and oplastMove == 1:
            self.honest_probability += 1
            self.recently_forgave = False if self.recently_forgave else True
            if self.honest_probability % 5 == 0:
                self.dishonest_probability -= (
                    1 if self.dishonest_probability > -1 else 0
                )

        if itr > 2 and oplastMove == -1 and history[itr - 2][self.id] == 1:
            self.dishonest_probability += 1
            self.total_dishonesty += 1
            if self.dishonest_probability >= 2:
                self.isHonest = False
        elif self.dishonest_probability > 0:
            self.dishonest_probability = 0

        if itr > 2 and oplastMove == -1 and history[itr - 2][self.id] == -1:
            self.retaliation += 1

        if itr > 2 and oplastMove == -1 and mylastMove == -1:
            self.deadlock += 1
            self.total_dishonesty -= 1 if self.total_dishonesty > 0 else 0
            if (
                self.honest_probability > 40
                and self.deadlock >= 2
                and not self.recently_forgave
            ):
                self.recently_forgave = True
                return 1
        else:
            self.deadlock = 0

        if not self.isHonest and self.honest_probability < 30:
            return -1

        if oplastMove == -1:
            if randint(1, 100) < self.min_forgiveness:
                return 1
            else:
                return -1
        return 1


import random


class TitForTatwDishonesty(BaseAgent):
    def __init__(self, id, forgiveness=20, first_move=1, name="TitForTatwDishonesty"):
        super().__init__(id=id)
        self.forgiveness = forgiveness
        self.first_move = first_move
        self.name = f"{name}__forgiveness_{forgiveness}"
        self.dishonesty = 0

    def next_move(self, state):
        op_id = 1 if self.id == 2 else 2
        itr = state["current_iter"]
        if itr == 1:
            return self.first_move

        history = state["history"]
        mylastMove = state["history"][itr - 1][self.id]
        oplastMove = state["history"][itr - 1][op_id]

        if itr == 2:
            if oplastMove == -1:
                self.dishonesty += 1

        if itr > 2 and history[itr - 2][self.id] == 1 and oplastMove == 1:
            self.dishonesty = 0

        if itr > 2 and history[itr - 2][self.id] == 1 and oplastMove == -1:
            self.dishonesty += 1
            if self.dishonesty >= 3:
                self.forgiveness = 0

        if oplastMove == -1:
            if randint(1, 100) <= self.forgiveness:
                return 1
            else:
                return -1
        return 1


class RandomForgivenessTitForTat(BaseAgent):
    def __init__(self, id):
        super().__init__(id=id)
        self.forgiveness = random.randint(15, 20)
        self.first_move = 1
        self.dishonesty = 0
        self.name = "RandomForgivenessTitForTat"

    def next_move(self, state):
        op_id = 1 if self.id == 2 else 2
        itr = state["current_iter"]
        if itr == 1:
            return self.first_move

        history = state["history"]
        mylastMove = state["history"][itr - 1][self.id]
        oplastMove = state["history"][itr - 1][op_id]

        if itr == 2:
            if oplastMove == -1:
                self.dishonesty += 1

        if itr > 2 and history[itr - 2][self.id] == 1 and oplastMove == 1:
            self.dishonesty = 0

        if itr > 2 and history[itr - 2][self.id] == 1 and oplastMove == -1:
            self.dishonesty += 1
            if self.dishonesty >= 3:
                self.forgiveness = 0

        if oplastMove == -1:
            if random.randint(1, 100) <= self.forgiveness:
                return 1
            else:
                return -1
        return 1


class DefectiveTFT(BaseAgent):
    def __init__(self, id):
        super().__init__(id=id)
        self.forgiveness = random.randint(15, 20)
        self.first_move = 1
        self.name = "Agent"

    def next_move(self, state):
        op_id = 1 if self.id == 2 else 2
        itr = state["current_iter"]
        if itr == 1:
            return self.first_move

        history = state["history"]
        mylastMove = state["history"][itr - 1][self.id]
        oplastMove = state["history"][itr - 1][op_id]
        streak = state["streak"]

        if itr == 2:
            if oplastMove == -1:
                self.dishonesty += 1

        if itr > 2 and history[itr - 2][self.id] == 1 and oplastMove == 1:
            self.dishonesty = 0

        if itr > 2 and history[itr - 2][self.id] == 1 and oplastMove == -1:
            self.dishonesty += 1
            if self.dishonesty >= 3:
                self.forgiveness -= 5

        if oplastMove == -1:
            if random.randint(1, 100) <= self.forgiveness:
                return 1
            else:
                return -1
        return 1


class SneakyDefector(BaseAgent):
    def __init__(self, id, defection_threshold = 3):
        super().__init__(id=id)
        self.forgiveness = random.randint(15, 20)
        self.first_move = 1
        self.name = "SneakyDefector"
        self.dishonesty = 0
        self.defection_threshold = defection_threshold

    def next_move(self, state):
        op_id = 1 if self.id == 2 else 2
        itr = state["current_iter"]
        if itr == 1:
            return self.first_move

        history = state["history"]
        mylastMove = state["history"][itr - 1][self.id]
        oplastMove = state["history"][itr - 1][op_id]
        streak = state["streak"]

        if streak // 5 >= self.defection_threshold:
            return -1

        if itr == 2:
            if oplastMove == -1:
                self.dishonesty += 1

        if itr > 2 and history[itr - 2][self.id] == 1 and oplastMove == 1:
            self.dishonesty = 0

        if itr > 2 and history[itr - 2][self.id] == 1 and oplastMove == -1:
            self.dishonesty += 1
            if self.dishonesty >= 3:
                self.forgiveness -= 5

        if oplastMove == -1:
            if random.randint(1, 100) <= self.forgiveness:
                return 1
            else:
                return -1
        return 1
