from Team import Team
from Match import Match

# Group class for managing one group in the tournament
class Group:
    """Class namayande yek group az marhale grouhi"""

    # Initialize group data
    def __init__(self, name, teams):
        """Sazande class Group

        Args:
            name (str): nam group
            teams (list): list tim haye group

        Returns:
            None
        """
        self.name = name
        self.teams = teams

    # Play all matches inside the group
    def play_all_matches(self):
        """Tamam bazi haye grouh ra ejra mikonad

        Args:
            None

        Returns:
            None
        """
        for x_team in range(len(self.teams) - 1):
            for y_team in range(x_team + 1, len(self.teams)):
                match = Match(self.teams[x_team], self.teams[y_team], False)
                match.play()
                result = match.winner

                if result == "equal":
                    self.teams[x_team].point += 1
                    self.teams[y_team].point += 1
                elif result == self.teams[y_team]:
                    self.teams[y_team].point += 3
                elif result == self.teams[x_team]:
                    self.teams[x_team].point += 3

    # Return the top two teams from the group
    def advance_teams(self):
        """Do tim sadr neshin group ra baraye marhale hazfi barmighardanad

        Args:
            None

        Returns:
            tuple: (tim aval, tim dovom)
        """
        first_team = self.get_ranking()[0]
        second_team = self.get_ranking()[1]
        return first_team, second_team

    # Rank teams by points and goal difference
    def get_ranking(self):
        """Rotbe bandi tim haye grouh ra bar asas emtiaz va tafazol gol barmighardanad.

        Args:
            None

        Returns:
            list: list moratab shode timha
        """
        return sorted(
            self.teams,
            key=lambda t: (t.point, t.goal_difference(), t.goals_for),
            reverse=True,
        )