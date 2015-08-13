import mb as monopoly
import math
from random import shuffle, randint
import numpy


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


def generate_rules():
    rules = []
    for r1 in [True, False]:
        for r2 in [True, False]:
            for r3 in [True, False]:
                for r4 in [True, False]:
                    for r5 in [True, False]:
                        for r6 in [True, False]:
                            rules.append([r1, r2, r3, r4, r5, r6])

    return rules


def main():
    rule_sets = generate_rules()
    base_games = 100
    desired_radius = 1

    for rule_set in rule_sets:
        game0 = monopoly.Game(cutoff=1000, trading_enabled=rule_set[5],
                              free_parking_pool=rule_set[0],
                              double_on_go=rule_set[1],
                              no_rent_in_jail=rule_set[2],
                              trip_to_start=rule_set[3],
                              snake_eyes_bonus=rule_set[4],
        )

        counter = 0
        lengths_sum = 0
        lengths = []
        interval_size = desired_radius + 100
        stalemates = 0

        while (counter < base_games) or interval_size > desired_radius:
            # Play game.
            player1 = monopoly.Player(1,
                                      buying_threshold=1500,
                                      group_ordering=random_ordering(),
                                      step_threshold=True,

            )
            player2 = monopoly.Player(2,
                                      buying_threshold=1500,
                                      group_ordering=random_ordering(),
                                      step_threshold=True
            )

            game0.new_players([player1, player2])
            results = game0.play()

            # Store length.
            length = results['length']

            if length == 1000:
                stalemates += 1
            else:
                counter += 1
                lengths.append(length)
                lengths_sum += length

                interval_size = 1.960 * (numpy.std(lengths) / math.sqrt(counter))

                # print(counter, lengths_sum / counter, interval_size)

        print(lengths_sum / counter, stalemates / counter, numpy.std(lengths), counter, rule_set)


main()