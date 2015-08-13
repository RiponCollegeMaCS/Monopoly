import mb as monopoly
import math
from orderings import *


def main():
    game0 = monopoly.Game(cutoff=1000, trading_enabled=True, image_exporting=0)

    base_games = 1000

    for n in range(1, 10):
        counter = 0
        winners = [0, 0, 0]
        interval_size = 10
        trade_count = []

        while (counter < base_games) or interval_size > 0.01:
            counter += 1
            # Play game./
            player1 = monopoly.Player(1,
                                      buying_threshold=1500,
                                      group_ordering=best_ordering(),
                                      step_threshold=True,


            )
            player2 = monopoly.Player(2,
             buying_threshold=1500,
                                      group_ordering=random_ordering(),
                                      step_threshold=True,

            )

            player2 = monopoly.Player(2,
                                      buying_threshold=100,
                                      n=n,
                                      dynamic_ordering=True,
                                      #development_threshold=2
            )

            game0.new_players([player1, player2])
            results = game0.play()

            # Store length.
            winners[results['winner']] += 1

            p = winners[1] / counter
            interval_size = 1.960 * math.sqrt((p * (1 - p)) / counter)
            trade_count.append(results['trade count'])

            # print(counter, p, interval_size)

        print(winners[0] / counter, winners[1] / counter, winners[2] / counter, counter, n)
        print(sum(trade_count) / counter)


main()