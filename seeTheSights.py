import mb as monopoly
from random import shuffle
from confidence import mean_confidence_interval

def random_ordering():
    all_groups = ["Brown", "Light Blue", "Pink", "Orange",
                  "Red", "Yellow", "Green", "Dark Blue",
                  "Utility", "Railroad"]
    shuffle(all_groups)
    return tuple(all_groups)


def best_ordering():
    return tuple(["Railroad", "Light Blue", "Orange", "Pink", "Red",
                  "Yellow", "Green", "Dark Blue", "Utility", "Brown"])


def main(games_in_a_set=100000):
    for shuffle in [True, False]:
        game0 = monopoly.Game(cutoff=1000, trading_enabled=False, image_exporting=0, shuffle=shuffle, trip_to_start=True)

        trade_count = []
        winners = [0, 0, 0]
        wins1 = []
        wins2 = []
        for i in range(games_in_a_set):
            # Play game.
            player1 = monopoly.Player(1,
                                      buying_threshold=500,
                                      group_ordering=random_ordering(),

            )
            player2 = monopoly.Player(2,
                                      buying_threshold=500,
                                      group_ordering=random_ordering(),
            )

            game0.new_players([player1, player2])
            results = game0.play()

            # Store length.
            winners[results['winner']] += 1
            if results['winner'] == 1:
                wins1.append(1)
                wins2.append(0)
            elif results['winner'] == 2:
                wins1.append(0)
                wins2.append(1)
            else:
                wins1.append(0)
                wins2.append(0)

            trade_count.append(results['trade count'])

        print(mean_confidence_interval(wins1))
        print(mean_confidence_interval(wins2))
        print(winners, shuffle, sum(trade_count) / games_in_a_set)


main()