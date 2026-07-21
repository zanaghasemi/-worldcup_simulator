from Team import Team
from Match import Match

# Knockout stage class for one elimination round
class KnockoutStage:
    """Class marboot be yek round az marhale hazfi"""

    # Initialize knockout round
    def __init__(self, round_name, matches):
        """Sazande class KnockoutStage

        Args:
            round_name (str): nam round
            matches (list): list match haye in round

        Returns:
            None
        """
        self.round_name = round_name
        self.matches = matches

    # Return winners of matches
    def get_winners(self):
        """Barande haye bazi haye in round ra barmighardanad.

        Args:
            None

        Returns:
            list: list tim haye barande
        """
        return [match.winner for match in self.matches]

    # Play all matches in this knockout round
    def play_round(self):
        """Tamam bazi haye in round ra ejra mikonad

        Args:
            None

        Returns:
            None
        """
        for match in self.matches:
            match.play()

    # Display results of a knockout round
    def display_results(self, log):
        """Natayej round hazfi ra dar surat niaz chap mikonad

        Args:
            log (bool): agar True bashad natayej chap mishavad

        Returns:
            None
        """
        if not log:
            return

        print(f"\n{self.round_name} winners:")

        if self.round_name == "Final":
            for game in self.matches:
                print(
                    f"{game.team1.name:^13} ({game.goals1})  vs  "
                    f"({game.goals2}) {game.team2.name:^13} "
                    f"--> {game.winner.name} won"
                )
            champion = self.get_winners()[0]
            print(f"\n{self.round_name} winner: {champion.name}")
            return

        half = len(self.matches) // 2

        for table_num, games in enumerate(
            (self.matches[:half], self.matches[half:]), start=1
        ):
            print(6 * "-" + f" Chart {table_num} " + 6 * "-")

            for game in games:
                print(
                    f"{game.team1.name:^13} ({game.goals1})  vs  "
                    f"({game.goals2}) {game.team2.name:^13} "
                    f"--> {game.winner.name} won"
                )

            if table_num == 1:
                print()