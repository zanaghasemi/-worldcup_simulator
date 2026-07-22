# Match.py

# =================== **** ===================
# DANESHJO:[SEYED MOHAMMAD ZANA GHASEMI]
# SHOMARE DANESHJOEI: [404131073]
# ONVAN PROZHE: [SHABIH SAZ JAME JAHANI]
# TARIKH TAHVIL: [ 1405/4/22 ]
# =================== **** ===================

from Team import Team


# Match class for simulating a single game
class Match:
    """Class marboot be yek bazi bein do tim"""

    # Initialize a match
    def __init__(self, team1, team2, is_knockout):
        """Sazande class Match

        Args:
            team1 (Team): tim aval
            team2 (Team): tim dovom
            is_knockout (bool): aya bazi hazfi ast ya na

        Returns:
            None
        """
        self.team1 = team1
        self.team2 = team2
        self.goals1 = 0
        self.goals2 = 0
        self.winner = None
        self.is_knockout = is_knockout

    # Play the match and store the result
    def play(self):
        """Bazi ra ejra karde va natije ra zakhire mikonad

        Args:
            None

        Returns:
            None
        """
        result = self.team1.simulate_match(self.team2, self.is_knockout)
        self.goals1 = result[0]
        self.goals2 = result[1]
        self.winner = result[2]
