from os import listdir
import pandas as pd
from matplotlib import pyplot as plt


def get_battle_score(filename: str, lines: list[str]) -> tuple[bool, int, int]:
    """Based on the lines in a battle's log file, returns a tuple containing:
    whether SearchBot won, number of SearchBot faints,
    number of opponent faints."""
    player_str = None
    player_won = None
    for line in lines:
        # determine which player number SearchBot is
        if player_str is None and "|player|p1|SearchBot" in line:
            player_str = "p1"
        if player_str is None and "|player|p2|SearchBot" in line:
            player_str = "p2"
        # determine who won
        if player_won is None and "W: 1\tL: 0" in line:
            player_won = True
        if player_won is None and "W: 0\tL: 1" in line:
            player_won = False
        # stop when player number and winner have been found
        if player_str is not None and player_won is not None:
            break

    # sanity check for player number and winner
    if player_str is None:
        raise ValueError("unable to determine SearchBot's player number in battle {f}".format(
            f=filename))
    if player_won is None:
        raise ValueError("unable to determine winner in battle {f}".format(
            f=filename))

    # one is p1, the other is p2
    if player_str == "p1":
        opponent_str = "p2"
    elif player_str == "p2":
        opponent_str = "p1"
    else:
        raise ValueError("unexpected SearchBot player_str ({s}) in battle {f}".format(
            s=player_str, f=filename))

    # find how many Pokemon fainted on each side
    player_faint_str = "|faint|" + player_str
    opponent_faint_str = "|faint|" + opponent_str
    player_faints = 0
    opponent_faints = 0
    for line in lines:
        if player_faint_str in line:
            player_faints += 1
        if opponent_faint_str in line:
            opponent_faints += 1

    # sanity check: winner should have 0-5 faints, loser should have exactly 6 faints
    if player_won and not (0 <= player_faints <= 5) and opponent_faints != 6:
        raise ValueError("unexpected score: player won with {p} player faints and {o} opponent faints in battle{f}".format(
            p=player_faints, o=opponent_faints, f=filename))
    elif not player_won and not (0 <= opponent_faints <= 5) and player_faints != 6:
        raise ValueError("unexpected score: opponent won with {p} player faints and {o} opponent faints in battle{f}".format(
            p=player_faints, o=opponent_faints, f=filename))

    return player_won, player_faints, opponent_faints


def process_match_logs():
    matches = {"random team search vs mostdamage": ["MostDamage", "Random Team"],
                   "random team search vs safest": ["Safest", "Random Team"],
                   "same team search vs mostdamage": ["MostDamage", "Same Team"],
                   "same team search vs safest": ["Safest", "Same Team"]}

    cols = ["Opponent", "Match Type", "SearchBot Won", "Num SearchBot Faints", "Num Opponent Faints"]
    df = pd.DataFrame(columns=cols)

    for match_type in matches.keys():
        print("MATCH TYPE:", match_type)
        prefix = "csc 480 project data/logs/" + match_type + "/"
        logs = [l for l in listdir(prefix) if l.endswith(".log") and not "record" in l]  # this should have all the logs except the record log file
        logs.sort()
        print("logs:", logs)
        assert(len(logs) == 100)  # we had 100-game matches so there should be 100 battle log files

        for filename in logs:
            with open(prefix + filename) as f:
                lines = f.readlines()
                results = matches[match_type] + list(get_battle_score(filename, lines))
                # add results to the dataframe as a new row (it seems to prepend)
                df.loc[-1] = results
                df.index = df.index + 1
                df = df.sort_index()
        print("finished looking through logs for this match")
        print("\n")
    print(df)
    print("\n\n")
    return df


def get_avg_faints(df: pd.DataFrame) -> tuple[list[str], list[float]]:
    print("SCORE RESULTS:")
    avg_faints = []
    num_battles = []

    # wins against MostDamageBot
    df2 = df[(df["Opponent"] == "MostDamage") & (df["SearchBot Won"].astype(str) == "True")]
    avg_faints.append(df2.loc[:, "Num SearchBot Faints"].mean())
    num_battles.append(len(df2))
    print("In SearchBot's {w} wins against MostDamageBot, it lost an average of {p} Pokemon".format(w=num_battles[-1], p=avg_faints[-1]))

    # losses against MostDamageBot
    df2 = df[(df["Opponent"] == "MostDamage") & (df["SearchBot Won"].astype(str) == "False")]
    avg_faints.append(df2.loc[:, "Num Opponent Faints"].mean())
    num_battles.append(len(df2))
    print("In SearchBot's {l} losses against MostDamageBot, it knocked out an average of {p} Pokemon".format(l=num_battles[-1], p=avg_faints[-1]))

    # wins against SafestBot
    df2 = df[(df["Opponent"] == "Safest") & (df["SearchBot Won"].astype(str) == "True")]
    avg_faints.append(df2.loc[:, "Num SearchBot Faints"].mean())
    num_battles.append(len(df2))
    print("In SearchBot's {w} wins against SafestBot, it lost an average of {p} Pokemon".format(w=num_battles[-1], p=avg_faints[-1]))

    # losses against SafestBot
    df2 = df[(df["Opponent"] == "Safest") & (df["SearchBot Won"].astype(str) == "False")]
    avg_faints.append(df2.loc[:, "Num Opponent Faints"].mean())
    num_battles.append(len(df2))
    print("In SearchBot's {l} losses against SafestBot, it knocked out an average of {p} Pokemon".format(l=num_battles[-1], p=avg_faints[-1]))

    names = ["In Wins vs. MostDamage", "In Losses vs. MostDamage",
             "In Wins vs. Safest", "In Losses vs. Safest"]
    for i in range(len(names)):
        names[i] = "{n} ({m})".format(n=names[i], m=num_battles[i])
    return names, avg_faints


def main():
    df = process_match_logs()
    names, avg_faints = get_avg_faints(df)

    fig = plt.figure(figsize=(10, 7))
    plt.rc("font", size=8)
    plt.ylim(0, 6)

    plt.title("SearchBot Knockouts")
    plt.xlabel("Match Type")
    plt.ylabel("Avg. Number of Pokemon Knocked Out By Loser")

    plt.bar(names, avg_faints, color=["green" if "Wins" in n else "red" for n in names])
    plt.show()


if __name__ == "__main__":
    main()
