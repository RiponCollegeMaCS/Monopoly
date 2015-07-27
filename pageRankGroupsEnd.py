import mb as monopoly
from timer import *
from random import shuffle
import numpy
from safename import *
import csv


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


def main(games_in_a_set=100000):
    matrix = numpy.zeros((10, 10))
    game_counter = 0
    game0 = monopoly.Game(cutoff=1000, trading_enabled=False)

    while game_counter < games_in_a_set:
        print(game_counter)
        # Play game.
        player1 = monopoly.Player(1, buying_threshold=500, group_ordering=random_ordering(), step_threshold=True)
        player2 = monopoly.Player(2, buying_threshold=500, group_ordering=random_ordering(), step_threshold=True)

        game0.new_players([player1, player2])
        results = game0.play()

        if results['winner'] != 0:
            game_counter += 1
            winner = game0.active_players[0]
            loser = game0.inactive_players[0]

            winner.add_railroads_and_utilities()
            loser.add_railroads_and_utilities()

            for winning_group in winner.monopolies:
                for losing_group in loser.monopolies:
                    matrix[group_index(winning_group)][group_index(losing_group)] += 1

    matrix = normalize_columns(matrix)

    graph_matrix = []
    group_names = ["Brown", "Light Blue", "Pink", "Orange",
                   "Red", "Yellow", "Green", "Dark Blue",
                   "Utility", "Railroad"]

    graph_matrix.append([""] + group_names)

    for i in range(len(matrix)):
        row = [group_names[i]]
        for j in matrix[i]:
            row.append(float(j))
        graph_matrix.append(row)

    # Save matrix
    with open("PageRankEndGroupsMatrix.csv", 'w', newline='') as csvfile:
        output_file = csv.writer(csvfile, quotechar=',')

        for row in graph_matrix:
            output_file.writerow(row)

    eigenvalues, eigenvectors = numpy.linalg.eig(matrix)
    print(eigenvalues[0])
    for element in normalize_data(eigenvectors[:, 0]):
        print(element)


def normalize_data(vector):
    nvector = []
    for i in range(len(vector)):
        nvector.append(pow(pow(vector[i].real, 2) + pow(vector[i].imag, 2), (1 / 2)))

    dmin = min(nvector)
    for i in range(len(nvector)):
        nvector[i] -= dmin

    dmax = max(nvector)
    for i in range(len(nvector)):
        nvector[i] /= dmax

    return nvector


def normalize_columns(matrix):
    size = len(matrix)

    for column in range(size):
        col_sum = sum(matrix[:, column])
        if col_sum != 0:
            for row in range(size):
                matrix[row][column] /= col_sum

    return matrix


if __name__ == '__main__':
    timer()
    main()
    timer()