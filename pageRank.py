import monopoly as monopoly
from timer import *
from random import shuffle
import numpy


def random_ordering():
    all_groups = ["Brown", "Light Blue", "Pink", "Orange",
                  "Red", "Yellow", "Green", "Dark Blue",
                  "Utility", "Railroad"]
    shuffle(all_groups)
    return tuple(all_groups)


def group_index(group):
    all_groups = ["Brown", "Light Blue", "Pink", "Orange",
                  "Red", "Yellow", "Green", "Dark Blue",
                  "Utility", "Railroad"]
    return all_groups.index(group)


def main(games_in_a_set=1000):
    matrix = numpy.zeros((10, 10))
    groups = ["Brown", "Light Blue", "Pink", "Orange",
              "Red", "Yellow", "Green", "Dark Blue",
              "Utility", "Railroad"]

    game0 = monopoly.Game(cutoff=1000, trading_enabled=False)
    counter = 0
    for group1 in groups:
        for group2 in groups:
            if group1 != group2:

                winners = [0, 0, 0]
                for i in range(games_in_a_set):
                    # Play game.
                    player1 = monopoly.Player(1, buying_threshold=100,
                                              #group_ordering=random_ordering(),
                                              initial_group=group1)
                    player2 = monopoly.Player(2, buying_threshold=100,
                                              #group_ordering=random_ordering(),
                                              initial_group=group2)

                    game0.new_players([player1, player2])
                    results = game0.play()

                    # Store length.
                    winners[results['winner']] += 1

                counter += 1
                print(counter)

                matrix[group_index(group1)][group_index(group2)] += winners[1]
                matrix[group_index(group2)][group_index(group1)] += winners[2]

    matrix = normalize_columns(matrix)

    eigenvalues, eigenvectors = numpy.linalg.eig(matrix)
    for i in range(len(eigenvalues)):
        print("***")
        print(eigenvalues[i])
        print(eigenvectors[:, i])


def normalize_columns(matrix):
    size = len(matrix)

    for column in range(size):
        col_sum = sum(matrix[:, column])
        for row in range(size):
            matrix[row][column] /= col_sum

    return matrix


if __name__ == '__main__':
    timer()
    main()
    timer()