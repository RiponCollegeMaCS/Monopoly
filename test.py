import mb as monopoly
from timer import *
import cProfile
from random import shuffle, randint, uniform


def random_ordering():
    all_groups = ["Brown", "Light Blue", "Pink", "Orange",
                  "Red", "Yellow", "Green", "Dark Blue",
                  "Utility", "Railroad"]
    shuffle(all_groups)
    return tuple(all_groups)


def best_ordering():
    return tuple(["Railroad", "Light Blue", "Orange", "Pink", "Red",
                  "Yellow", "Green", "Dark Blue", "Utility", "Brown"])


def main(games_in_a_set=10000):
    game0 = monopoly.Game(cutoff=1000, trading_enabled=True, image_exporting=0, )

    trade_count = []
    winners = [0, 0, 0]
    for i in range(games_in_a_set):
        # Play game.
        player1 = monopoly.Player(1,
                                  buying_threshold=500,
                                  group_ordering=random_ordering(),
                                  #step_threshold=True,

        )
        player2 = monopoly.Player(2,
                                  dynamic_ordering=True,
                                  n=6,
                                  buying_threshold=500,
                                  jail_time=0
        )

        game0.new_players([player1, player2])
        results = game0.play()

        # Store length.
        winners[results['winner']] += 1
        trade_count.append(results['trade count'])

    print(winners, sum(trade_count) / games_in_a_set)


if __name__ == '__main__':
    timer()
    main()
    # cProfile.run('main2()', sort=1)
    timer()