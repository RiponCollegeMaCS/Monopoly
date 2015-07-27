import mb as monopoly
from timer import *
from random import shuffle
import numpy
import copy
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
    with open('pageRank_GroupGraph3.csv', 'w', newline='') as csvfile:
        output_file = csv.writer(csvfile, quotechar=',')
        matrix = numpy.zeros((10, 10))
        game_counter = 0
        game0 = monopoly.Game(cutoff=1000, trading_enabled=True)

        while game_counter < games_in_a_set:
            # Play game.
            player1 = monopoly.Player(1, buying_threshold=100, group_ordering=random_ordering())
            player2 = monopoly.Player(2, buying_threshold=100, group_ordering=random_ordering())

            game0.new_players([player1, player2])
            results = game0.play()

            if results['winner'] != 0:
                game_counter += 1
                winner = game0.active_players[0]
                loser = game0.inactive_players[0]

                winner.add_railroads_and_utilities()
                loser.add_railroads_and_utilities()

                #print(winner.monopolies, loser.monopolies)
                for winning_group in winner.monopolies:
                    for losing_group in loser.monopolies:
                        matrix[group_index(winning_group)][group_index(losing_group)] += 1

            if game_counter % 100 == 0:
                print(game_counter)
                new_matrix = normalize_columns(copy.deepcopy(matrix))
                eigenvalues, eigenvectors = numpy.linalg.eig(new_matrix)

                big_vector = eigenvectors[:, 0]  # Grab e-vector.
                small_vector = [x for x in big_vector if x != 0]  # Remove 0s

                # Write to file.
                output_file.writerow([game_counter] + normalize_data(small_vector))


        new_matrix = normalize_columns(copy.deepcopy(matrix))
        graph_matrix = []
        group_names = ["Brown", "Light Blue", "Pink", "Orange",
                       "Red", "Yellow", "Green", "Dark Blue",
                       "Utility", "Railroad"]

        graph_matrix.append([""] + group_names)

        for i in range(len(new_matrix)):
            row = [group_names[i]]
            for j in new_matrix[i]:
                row.append(float(j))
            graph_matrix.append(row)

        # Save matrix
        with open("PageRankEndGroupsMatrix.csv", 'w', newline='') as csvfile:
            output_file = csv.writer(csvfile, quotechar=',')

            for row in graph_matrix:
                output_file.writerow(row)



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