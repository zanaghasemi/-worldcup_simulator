from Match import Match
from Group import Group
from Team import Team
from KnockoutStage import KnockoutStage
import random
import pandas as pd

# Main class for managing the World Cup simulation
class WorldCupSimulator:
    """Class asli baraye modiriat shabih sazi jame jahani"""

    # Initialize the simulator
    def __init__(self):
        """Sazande class WorldCupSimulator

        Args:
            None

        Returns:
            None
        """
        self.group_game_num = 0
        self.teams = []
        self.groups = []
        self.round_of_16 = None
        self.quarterfinals = None
        self.semifinals = None
        self.final = None

    # Load teams from a CSV file
    def load_teams_from_csv(self, file_name):
        """Etelaat timha ra az file CSV load mikonad

        Args:
            file_name (str): esm ya masir file CSV

        Returns:
            bool: agar file ba movafaghiat load shavad True, dar gheir in surat False
        """
        try:
            data = pd.read_csv(file_name).values
        except FileNotFoundError:
            print("the file not found")
            return False

        self.teams = []
        for row in data:
            self.teams.append(
                Team(
                    name=row[0],
                    attack=int(row[1]),
                    defence=int(row[2]),
                    rank=int(row[3]),
                )
            )

        if len(self.teams) != 32:
            raise ValueError("data has to be 32 rows")

        print(f"file {file_name} uploaded")
        return True

    # Run the group stage matches
    def run_group_stage(self, log=True):
        """Marhale grouhi ra ejra mikonad va dar surat niaz natayej ra chap mikonad

        Args:
            log (bool): agar True bashad natayej grouh ha chap mishavad

        Returns:
            None
        """
        if not self.groups:
            print("first select option 2 (Seed and Draw)")
            return

        for team in self.teams:
            team.reset_status()

        for group in self.groups:
            group.play_all_matches()

            if log:
                print(6 * "-" + f" Group {group.name} " + 6 * "-")

            team_list = group.get_ranking()

            if log:
                for index in range(4):
                    print(
                        f"{index + 1}. {team_list[index].name:13}: "
                        f"{team_list[index].point:2} PTS | "
                        f"{team_list[index].goal_difference():+2} GD | "
                        f"{team_list[index].goals_for:2} GF"
                    )
                print()

        self.group_game_num += 1

    # Seed teams and draw them into groups
    def seed_and_draw_groups(self):
        """Timha ra bar asas rank seed bandi va dar group ha gharar midahad

        Args:
            None

        Returns:
            dict: dictionary grouh ha va tim haye gharar gerefte dar har grouh
        """
        seed = {"seed1": [], "seed2": [], "seed3": [], "seed4": []}

        for team in self.teams:
            if 1 <= team.rank <= 8:
                seed["seed1"].append(team)
            elif 9 <= team.rank <= 16:
                seed["seed2"].append(team)
            elif 17 <= team.rank <= 24:
                seed["seed3"].append(team)
            elif 25 <= team.rank <= 32:
                seed["seed4"].append(team)

        random.shuffle(seed["seed1"])
        random.shuffle(seed["seed2"])
        random.shuffle(seed["seed3"])
        random.shuffle(seed["seed4"])

        group = {"A": [], "B": [], "C": [], "D": [], "E": [], "F": [], "G": [], "H": []}

        for group_name in group.keys():
            group[group_name].append(seed["seed1"].pop())
            group[group_name].append(seed["seed2"].pop())
            group[group_name].append(seed["seed3"].pop())
            group[group_name].append(seed["seed4"].pop())

        self.groups = []
        for group_name in group.keys():
            self.groups.append(Group(group_name, group[group_name]))

        return group

    # Build the knockout bracket based on group results
    def setup_knockout_bracket(self):
        """Bracket marhale hazfi ra bar asas natayej grouh ha misazad

        Args:
            None

        Returns:
            list: list az bazi haye round of 16
        """
        matches_total = []
        ch1 = []
        ch2 = []
        i = 0

        for group in self.groups:
            first, second = group.advance_teams()

            if i % 2 == 0:
                ch1.append(second)
            else:
                ch2.append(first)
            i += 1

        for group in self.groups:
            first, second = group.advance_teams()

            if i % 2 == 0:
                ch1.append(first)
            else:
                ch2.append(second)
            i += 1

        for team1, team2 in zip(ch1, ch2):
            matches_total.append(Match(team1, team2, True))

        self.round_of_16 = KnockoutStage("Round of 16", matches_total)
        return matches_total

    # Run the knockout stages from round of 16 to final
    def run_knockout_bracket(self, log=True):
        """Marhale hazfi az round of 16 ta final ra ejra mikonad

        Args:
            log (bool): agar True bashad natayej har round chap mishavad

        Returns:
            None
        """
        self.setup_knockout_bracket()
        self.round_of_16.play_round()
        self.round_of_16.display_results(log)

        # Create next round matches from winners
        def make_matches(winners_list):
            """Az barandeha bazi haye round baadi ra misazad"""
            temp_list = []
            for i in range(0, len(winners_list), 2):
                temp_list.append(Match(winners_list[i], winners_list[i + 1], True))
            return temp_list

        winners = self.round_of_16.get_winners()
        quarter_matches = make_matches(winners)
        self.quarterfinals = KnockoutStage("Quarter Finals", quarter_matches)
        self.quarterfinals.play_round()
        self.quarterfinals.display_results(log)

        winners = self.quarterfinals.get_winners()
        semi_matches = make_matches(winners)
        self.semifinals = KnockoutStage("Semi Finals", semi_matches)
        self.semifinals.play_round()
        self.semifinals.display_results(log)

        winners = self.semifinals.get_winners()
        self.final = KnockoutStage("Final", [Match(winners[0], winners[1], True)])
        self.final.play_round()
        self.final.display_results(log)

    # Run a full simulation from group stage to final
    def run_full_simulation(self):
        """Yek shabih sazi kamel shamel grouh stage va knockout ra ejra mikonad

        Args:
            None

        Returns:
            None
        """
        self.clearing(self.group_game_num != 0)
        self.run_group_stage()
        self.run_knockout_bracket()

    # Simulate many times and show most likely champion
    def most_likely_champion(self, num_simulations=1000):
        """Ba chand bar shabih sazi, ehtemali tarin ghahreman ra namayesh midahad

        Args:
            num_simulations (int): tedad dafe-haye shabih sazi

        Returns:
            None
        """
        final_result = {team.name: 0 for team in self.teams}

        for _ in range(num_simulations):
            self.clearing(False)
            self.run_group_stage(False)
            self.run_knockout_bracket(False)
            final_team = self.final.get_winners()[0]
            final_result[final_team.name] += 1

        print("\nMost Likely final_result:\n")

        sorted_champions = sorted(
            final_result.items(), key=lambda x: x[1], reverse=True
        )

        for team_name, wins in sorted_champions:
            percent = (wins / num_simulations) * 100
            print(f"{team_name:15} --> {percent:.2f}%")

    # Display the last knockout bracket
    def display_bracket(self):
        """Bracket akharin marhale hazfi shode ra chap mikonad

        Args:
            None

        Returns:
            None
        """
        if self.round_of_16 is None:
            print("bracket not found")
            return

        print("\n")
        print(6 * "-" + " 1/8 " + 6 * "-")

        for match in self.round_of_16.matches:
            print(
                f"{match.team1.name:^11} ({match.goals1}) vs "
                f"({match.goals2}) {match.team2.name:^11} "
                f"-> {match.winner.name} won"
            )

        if self.quarterfinals:
            print("\n")
            print(6 * "-" + " 1/4 " + 6 * "-")
            for match in self.quarterfinals.matches:
                print(
                    f"{match.team1.name:^11} ({match.goals1}) vs "
                    f"({match.goals2}) {match.team2.name:^11} "
                    f"-> {match.winner.name} won"
                )

        if self.semifinals:
            print("\n")
            print(6 * "-" + " Semi Final " + 6 * "-")
            for match in self.semifinals.matches:
                print(
                    f"{match.team1.name:^11} ({match.goals1}) vs "
                    f"({match.goals2}) {match.team2.name:^11} "
                    f"-> {match.winner.name} won"
                )

        if self.final:
            print("\n")
            print(6 * "-" + " Final " + 6 * "-")
            match = self.final.matches[0]

            if match.goals1 == match.goals2:
                print(
                    f"{match.team1.name:^11} ({match.goals1}) vs "
                    f"({match.goals2}) {match.team2.name:^11} "
                    f"--> Penalty: ({match.team1.penalty}-{match.team2.penalty})"
                )
            else:
                print(
                    f"{match.team1.name:^11} ({match.goals1}) vs "
                    f"({match.goals2}) {match.team2.name:^11}"
                )

            print(f"\n\nFinal Winner: {match.winner.name}")

    # Reset previous simulation data
    def clearing(self, seed):
        """Vaziat simulation qabli ra pak mikonad

        Args:
            seed (bool): agar False bashad grouh ha dobare sakhte mishavand

        Returns:
            None
        """
        for team in self.teams:
            team.reset_status()

        if not seed:
            self.seed_and_draw_groups()

        self.round_of_16 = None
        self.quarterfinals = None
        self.semifinals = None
        self.final = None