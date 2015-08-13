import mb_auctions as monopoly
import math
from random import shuffle


def random_ordering():
    all_groups = ["Brown", "Light Blue", "Pink", "Orange",
                  "Red", "Yellow", "Green", "Dark Blue",
                  "Utility", "Railroad"]
    shuffle(all_groups)
    return tuple(all_groups)


def best_ordering():
    other_groups = ["Pink", "Red",
                    "Yellow", "Green",
                    "Dark Blue", "Utility", "Brown"]
    shuffle(other_groups)

    return tuple(["Railroad", "Light Blue", "Orange"] + other_groups)


def main():
    game0 = monopoly.Game(cutoff=1000, trading_enabled=True, image_exporting=0, shuffle=False)
    num_players = 3

    base_games = 1000
    counter = 0
    winners = [0] * (num_players + 1)
    interval_size = 10
    length = []

    while (counter < base_games) or interval_size > 0.01:
        counter += 1
        # Play game.
        players = []
        for i in range(1, num_players + 1):
            players.append(monopoly.Player(i,
                                           buying_threshold=1500,
                                           group_ordering=random_ordering(),
                                           step_threshold=True
            )
            )

        game0.new_players(players)
        results = game0.play()

        # Store length.
        winners[results['winner']] += 1

        if results['winner'] != 0:
            length.append(results['length'])

        p = winners[1] / counter
        interval_size = 1.960 * math.sqrt((p * (1 - p)) / counter)

        # print(counter, p, interval_size)

    for i in range(num_players + 1):
        print("player", i, winners[i] / counter)

    print(sum(length) / (counter - winners[0]))
    print(counter)


main()