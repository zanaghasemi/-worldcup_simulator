# Main.py

# =================== **** ===================
# DANESHJO:[SEYED MOHAMMAD ZANA GHASEMI]
# SHOMARE DANESHJOEI: [404131073]
# ONVAN PROZHE: [SHABIH SAZ JAME JAHANI]
# TARIKH TAHVIL: [ 1405/4/22 ]
# =================== **** ===================

from Worldcupsim import WorldCupSimulator


# Main program menu
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
