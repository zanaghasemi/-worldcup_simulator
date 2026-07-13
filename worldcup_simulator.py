# =================== **** ===================
# DANESHJO:[SEYED MOHAMMAD ZANA GHASEMI]
# SHOMARE DANESHJOEI: [404131073]
# ONVAN PROZHE: [SHABIH SAZ JAME JAHANI]
# TARIKH TAHVIL: [ 1405/4/22 ]
# =================== **** ===================

import random
import numpy as np
import pandas as pd


class WorldCupSimulator:
    """Class asli baraye modiriat shabih sazi jame jahani"""

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

        for i in data:
            self.teams.append(
                Team(name=i[0], attack=int(i[1]), defence=int(i[2]), rank=int(i[3]))
            )

        if len(self.teams) != 32:
            raise ValueError("data has to be 32 rows")

        print(f"file {file_name} uploaded")
        return True

    def run_group_stage(self, log=True):
        """Marhale groupi ra ejra mikonad va dar surat niaz natayej ra chap mikonad

        Args:
            log (bool): agar True bashad natayej group-ha chap mishavad

        Returns:
            None
        """
        if not self.groups:
            print("first select option 2 (Seed and Draw)")
            return

        for team in self.teams:
            team.reset_status()

        for i in self.groups:
            i.play_all_matches()

            if log:
                print(6 * "-" + f" Group {i.name} " + 6 * "-")

            team_list = i.get_ranking()

            if log:
                for j in range(4):
                    print(
                        f"{j + 1}. {team_list[j].name:13}: "
                        f"{team_list[j].point:2} PTS | "
                        f"{team_list[j].goal_difference():+2} GD | "
                        f"{team_list[j].goals_for:2} GF"
                    )
                print()

        self.group_game_num += 1

    def seed_and_draw_groups(self):
        """Timha ra bar asas rank seed bandi va dar group ha draw mikonad

        Args:
            None

        Returns:
            dict: dictionary group ha va tim haye gharar gerefte dar har group
        """
        seed = {"seed1": [], "seed2": [], "seed3": [], "seed4": []}

        for i in self.teams:
            if 1 <= i.rank <= 8:
                seed["seed1"].append(i)
            elif 9 <= i.rank <= 16:
                seed["seed2"].append(i)
            elif 17 <= i.rank <= 24:
                seed["seed3"].append(i)
            elif 25 <= i.rank <= 32:
                seed["seed4"].append(i)

        random.shuffle(seed["seed1"])
        random.shuffle(seed["seed2"])
        random.shuffle(seed["seed3"])
        random.shuffle(seed["seed4"])

        group = {"A": [], "B": [], "C": [], "D": [], "E": [], "F": [], "G": [], "H": []}

        for _, g_name in enumerate(group.keys()):
            group[g_name].append(seed["seed1"].pop())
            group[g_name].append(seed["seed2"].pop())
            group[g_name].append(seed["seed3"].pop())
            group[g_name].append(seed["seed4"].pop())

        self.groups = []

        for group_name in group.keys():
            self.groups.append(Group(group_name, group[group_name]))

        return group

    def setup_knockout_bracket(self):
        """Bracket marhale hazfi ra bar asas natayej group ha misazad

        Args:
            None

        Returns:
            list: list az match haye round of 16
        """
        matches_total = []
        ch1 = []
        ch2 = []
        i = 0

        for group in self.groups:
            g = group.advance_teams()

            if i % 2 == 0:
                ch1.append(g[1])
            else:
                ch2.append(g[0])
            i += 1

        for group in self.groups:
            g = group.advance_teams()

            if i % 2 == 0:
                ch1.append(g[0])
            else:
                ch2.append(g[1])
            i += 1

        i = 0

        for t1, t2 in zip(ch1, ch2):
            matches_total.append(Match(t1, t2, True))

        self.round_of_16 = KnockoutStage("Round of 16", matches_total)
        return matches_total

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

        def work(winners_list):
            temp_li = []
            for i in range(0, len(winners_list), 2):
                temp_li.append(Match(winners_list[i], winners_list[i + 1], True))
            return temp_li

        list_team_win = self.round_of_16.get_winners()
        list_quarterfinals_matches = work(list_team_win)
        self.quarterfinals = KnockoutStage("Quarter Finals", list_quarterfinals_matches)
        self.quarterfinals.play_round()
        self.quarterfinals.display_results(log)

        list_team_win = self.quarterfinals.get_winners()
        list_semifinal_matches = work(list_team_win)
        self.semifinals = KnockoutStage("Semi Finals", list_semifinal_matches)
        self.semifinals.play_round()
        self.semifinals.display_results(log)

        list_team_win = self.semifinals.get_winners()
        self.final = KnockoutStage(
            "Final", [Match(list_team_win[0], list_team_win[1], True)]
        )
        self.final.play_round()
        self.final.display_results(log)

    def run_full_simulation(self):
        """Yek shabih sazi kamel shamel paksazi group stage va knockout ra ejra mikonad

        Args:
            None

        Returns:
            None
        """
        self.clearing(self.group_game_num != 0)
        self.run_group_stage()
        self.run_knockout_bracket()

    def most_likely_champion(self, num_simulations=1000):
        """Ba chand bar shabih sazi, ehtemali tarin ghahreman ra namayesh midahad

        Args:
            num_simulations (int): tedad dafe-haye shabih-sazi

        Returns:
            None
        """
        final_result = {}

        for team in self.teams:
            final_result[team.name] = 0

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

    def clearing(self, seed):
        """Vaziat simulation qabli ra pak mikonad

        Args:
            seed (bool): agar False bashad groupha dobare draw mishavand

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


class Team:
    """Class marboot be yek tim melli football"""

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

    def goal_difference(self):
        """Tafazol gol tim ra barmighrdanad

        Args:
            None

        Returns:
            int: tafazol gol
        """
        return self.goals_for - self.goals_against

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


class Group:
    """Class namayande yek group az marhale grouhi"""

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

    def play_all_matches(self):
        """Tamam bazi haye group ra ejra mikonad

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

    def get_ranking(self):
        """Rotbe bandi tim haye group ra bar asas emtiaz va tafazol gol barmighardanad

        Args:
            None

        Returns:
            list: list moratab shode timha
        """
        group_result = sorted(
            self.teams,
            key=lambda t: (t.point, t.goal_difference(), t.goals_for),
            reverse=True,
        )
        return group_result


class KnockoutStage:
    """Class marboot be yek round az marhale hazfi"""

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

    def get_winners(self):
        """Barande haye match haye in round ra barmighardanad
        Args:
            None

        Returns:
            list: list tim haye barande
        """
        winners_team_name = [match.winner for match in self.matches]
        return winners_team_name

    def play_round(self):
        """Tamam matchhaye in round ra ejra mikonad

        Args:
            None

        Returns:
            None
        """
        for match in self.matches:
            match.play()

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


class Match:
    """Class marboot be yek bazi bein do tim"""

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


def main():
    """Tabe asli barname va menu karbar

    Args:
        None

    Returns:
        None
    """
    f = False
    obj = WorldCupSimulator()
    help_text = (
        "\n1- load csv file\n"
        "2- seed and draw groups\n"
        "3- group game\n"
        "4- (group + final) game\n"
        "5- simulate 1000\n"
        "6- showing last bracket\n"
        "7- exit\n"
    )

    while True:
        print(help_text)

        try:
            num = int(input(": "))
        except ValueError:
            print("type a number\n")
            continue

        if not 1 <= num <= 7:
            print("enter a number between 1 and 7.")
            continue

        if num == 1:
            file_path = "worldcup_2026_teams.csv"
            f = obj.load_teams_from_csv(file_path)

        elif num in (2, 3, 4, 5, 6):
            if not f:
                print("first upload the csv file")
                continue

            if num == 2:
                result = obj.seed_and_draw_groups()
                for item in result:
                    print(f"Group {item}: ", end="")
                    for i in range(4):
                        print(f"{result[item][i].name:^15} | ", end="")
                    print()
                    print(81 * "-")

            elif num == 3:
                obj.run_group_stage()

            elif num == 4:
                obj.run_full_simulation()

            elif num == 5:
                while True:
                    try:
                        simulations = int(input("number of simulations: "))
                        if simulations <= 0:
                            print("number must be positive")
                            continue
                        obj.most_likely_champion(simulations)
                        break
                    except ValueError:
                        print("enter a number type int")

            elif num == 6:
                obj.display_bracket()

        elif num == 7:
            break


if __name__ == "__main__":
    main()
