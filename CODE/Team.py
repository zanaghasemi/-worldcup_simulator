# Team.py

# =================== **** ===================
# DANESHJO:[SEYED MOHAMMAD ZANA GHASEMI]
# SHOMARE DANESHJOEI: [404131073]
# ONVAN PROZHE: [SHABIH SAZ JAME JAHANI]
# TARIKH TAHVIL: [ 1405/4/22 ]
# =================== **** ===================

import numpy as np
import random


# Team class for storing national team data
class Team:
    """Class marboot be yek tim melli football"""

    # Initialize a team object
    def __init__(self, name, attack, defence, rank):
        """Sazande class Team

        Args:
            name (str): nam tim
            attack (int): ghodrat hamle
            defence (int): ghodrat defa
            rank (int): rank jahani ya seed tim

        Returns:
            None
        """
        self.name = name
        self.attack = attack
        self.defence = defence
        self.rank = rank
        self.penalty = 0
        self.point = 0
        self.goals_for = 0
        self.goals_against = 0

    # Return goal difference
    def goal_difference(self):
        """Tafazol gol tim ra barmighardanad

        Args:
            None

        Returns:
            int: tafazol gol
        """
        return self.goals_for - self.goals_against

    # Reset group stage stats
    def reset_status(self):
        """Amar group stage tim ra reset mikonad

        Args:
            None

        Returns:
            None
        """
        self.goals_for = 0
        self.goals_against = 0
        self.point = 0

    # Simulate a match against another team
    def simulate_match(self, opponent, is_knockout=False):
        """Natije bazi ba tim harif ra shabih sazi mikonad

        Args:
            opponent (Team): tim harif
            is_knockout (bool): aya bazi marhale hazfi ast ya na

        Returns:
            tuple: (goals_self, goals_opponent, winner)
        """
        if type(is_knockout) is not bool:
            raise ValueError("is_knockout must be bool")

        self.penalty = 0
        opponent.penalty = 0

        def expected_goals(team, rival):
            return (team.attack * 1.5 + (100 - rival.defence) * 0.8) / 100

        goals_self = np.random.poisson(expected_goals(self, opponent))
        goals_opponent = np.random.poisson(expected_goals(opponent, self))

        winner = None

        if goals_self != goals_opponent:
            winner = self if goals_self > goals_opponent else opponent
        elif not is_knockout:
            winner = "equal"
        else:
            goals_self += np.random.poisson(expected_goals(self, opponent) / 3)
            goals_opponent += np.random.poisson(expected_goals(opponent, self) / 3)

            if goals_self != goals_opponent:
                winner = self if goals_self > goals_opponent else opponent
            else:
                chance_self = 0.75 + (self.attack - opponent.defence) / 250
                chance_opp = 0.75 + (opponent.attack - self.defence) / 250

                for _ in range(5):
                    self.penalty += random.random() < chance_self
                    opponent.penalty += random.random() < chance_opp

                while self.penalty == opponent.penalty:
                    self.penalty += random.random() < chance_self
                    opponent.penalty += random.random() < chance_opp

                winner = self if self.penalty > opponent.penalty else opponent

        self.goals_for += goals_self
        self.goals_against += goals_opponent
        opponent.goals_for += goals_opponent
        opponent.goals_against += goals_self

        return goals_self, goals_opponent, winner
