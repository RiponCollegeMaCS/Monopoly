import mb as monopoly
from timer import *
from random import shuffle, randint


def random_ordering():
    all_groups = ["Brown", "Light Blue", "Pink", "Orange",
                  "Red", "Yellow", "Green", "Dark Blue",
                  "Utility", "Railroad"]
    shuffle(all_groups)
    return tuple(all_groups)


def best_ordering():
    return tuple(["Railroad", "Light Blue", "Orange", "Pink", "Red",
                  "Yellow", "Green", "Dark Blue", "Utility", "Brown"])


def test(games_in_a_set=1):
    game0 = monopoly.Game(cutoff=1000, trading_enabled=True, image_exporting=0)
    for i in range(games_in_a_set):
        # Play game.
        player1 = monopoly.Player(1,
                                  dynamic_ordering=True,
                                  n=18,
                                  c=0,

        )
        player2 = monopoly.Player(2,
                                  dynamic_ordering=True,
                                  n=6,
                                  c=0,
        )

        game0.new_players([player1, player2])
        results = game0.play()


def main(games_in_a_set=1000):
    game0 = monopoly.Game(cutoff=1000, trading_enabled=True, image_exporting=0)
    for n in [6]:
        for thresh in range(1,250,25):

            trade_count = []
            winners = [0, 0, 0]

            for i in range(games_in_a_set):
                # Play game.
                player1 = monopoly.Player(1,
                                          buying_threshold=thresh,
                                          dynamic_ordering=True,
                                          n=n,
                )
                player2 = monopoly.Player(2,
                                          dynamic_ordering=True,
                                          buying_threshold=randint(1,500),
                                          n=randint(1, 18),
                )

                game0.new_players([player1, player2])
                results = game0.play()

                # Store length.
                winners[results['winner']] += 1
                trade_count.append(results['trade count'])

            print(winners, n, thresh, sum(trade_count) / games_in_a_set)
            # print("avg. trades", sum(trade_count) / games_in_a_set)
            # print("max trades", max(trade_count))
            # print("min trades", min(trade_count))


main()