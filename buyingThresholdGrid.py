import m as monopoly
import itertools
import numpy


def main3(games_in_a_set=1000):
    result_matrix = numpy.zeros((10, 10))
    threshold_pairs = list(itertools.product(range(10), range(10)))
    game0 = monopoly.Game(cutoff=1000, trading_enabled=False)

    for pair in threshold_pairs:
        if result_matrix[pair[0]][pair[1]] == 0:
            threshold1 = (pair[0] + 1) * 50
            threshold2 = (pair[1] + 1) * 50

            winners = [0, 0, 0]
            for i in range(games_in_a_set):
                # Play game.
                player1 = monopoly.Player(1, buying_threshold=threshold1)
                player2 = monopoly.Player(2, buying_threshold=threshold2)
                game0.new_players([player1, player2])
                results = game0.play()

                # Store length.
                winners[results['winner']] += 1

            result_matrix[pair[0]][pair[1]] = winners[1]
            result_matrix[pair[1]][pair[0]] = winners[2]

            print(threshold1, threshold2, winners)

    numpy.savetxt("buyingThresholdMatrix.csv", result_matrix, delimiter=",")


main3()