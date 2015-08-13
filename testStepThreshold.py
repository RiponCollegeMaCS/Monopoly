import mb as monopoly
import math
from random import shuffle, randint


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
    game0 = monopoly.Game(cutoff=1000, trading_enabled=True, image_exporting=0)

    for thresh in range(150, 1501, 150):
        base_games = 1000
        counter = 0
        winners = [0, 0, 0]
        interval_size = 10

        while (counter < base_games) or interval_size > 0.01:
            counter += 1
            # Play game.
            player1 = monopoly.Player(1,
                                      buying_threshold=1500,
                                      group_ordering=random_ordering(),
                                      step_threshold=True,

            )
            player2 = monopoly.Player(2,
                                      buying_threshold=thresh,
                                      group_ordering=random_ordering(),
                                      step_threshold=False
            )

            game0.new_players([player1, player2])
            results = game0.play()

            # Store length.
            winners[results['winner']] += 1

            p = winners[1] / counter
            interval_size = 1.960 * math.sqrt((p * (1 - p)) / counter)

            # print(counter, p, interval_size)

        print(winners[0] / counter, winners[1] / counter, winners[2] / counter, counter, thresh)


main()