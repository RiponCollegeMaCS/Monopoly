import mb as monopoly
from timer import *
from random import shuffle
import numpy
import copy
import csv
from safename import safe_name
import math


def random_ordering():
    all_groups = ["Brown", "Light Blue", "Pink", "Orange",
                  "Red", "Yellow", "Green", "Dark Blue",
                  "Utility", "Railroad"]
    shuffle(all_groups)
    return tuple(all_groups)


def main(games_in_a_set=100000):
    with open('pageRankEnd_Graph.csv', 'w', newline='') as csvfile:
        output_file = csv.writer(csvfile, quotechar=',')

        matrix = numpy.zeros((28, 28))
        game_counter = 0
        game0 = monopoly.Game(cutoff=1000, trading_enabled=True)

        keep_going = True
        while keep_going:
            # Play game.
            player1 = monopoly.Player(1, buying_threshold=1500, group_ordering=random_ordering(), step_threshold=True)
            player2 = monopoly.Player(2, buying_threshold=1500, group_ordering=random_ordering(), step_threshold=True)

            game0.new_players([player1, player2])
            results = game0.play()

            if results['winner'] != 0:
                game_counter += 1
                winner = game0.active_players[0]
                loser = game0.inactive_players[0]

                for winning_prop in winner.inventory:
                    for losing_prop in loser.inventory:
                        matrix[winning_prop.prop_id][losing_prop.prop_id] += 1

            if game_counter % 100 == 0:
                print(game_counter)
                new_matrix = normalize_columns(copy.deepcopy(matrix))
                eigenvalues, eigenvectors = numpy.linalg.eig(new_matrix)

                e_vector = eigenvectors[:, 0]  # Grab e-vector.

                # Write to file.
                output_file.writerow([game_counter] + normalize_data(e_vector))
                if game_counter == games_in_a_set:
                    for element in normalize_data(e_vector):
                        print(element)

                keep_going = False
                for i in range(28):
                    for j in range(28):
                        p = matrix[i][j] / game_counter
                        radius = 1.960 * math.sqrt((p * (1 - p)) / game_counter)
                        if radius > 0.01:
                            keep_going = True

        graph_matrix = []
        prop_names = []

        for prop in game0.board:
            if prop.is_property:
                prop_names.append(safe_name(prop.name))

        graph_matrix.append([""] + prop_names)

        for i in range(len(matrix)):
            row = [prop_names[i]]
            for j in matrix[i]:
                row.append(float(j))
            graph_matrix.append(row)

        # Save matrix
        with open("PageRankEnd_Matrix.csv", 'w', newline='') as csvfile:
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