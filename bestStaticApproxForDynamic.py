import mb as monopoly
import numpy
from orderings import *
import csv
import copy


def main():
    with open('pageRank_DynamicGraph.csv', 'w', newline='') as csvfile:
        output_file = csv.writer(csvfile, quotechar=',')
        game0 = monopoly.Game(cutoff=1000, trading_enabled=True, image_exporting=0)
        groups = ["Brown", "Light Blue", "Pink", "Orange",
                  "Red", "Yellow", "Green", "Dark Blue",
                  "Utility", "Railroad"]

        counter = 0

        matrix = numpy.zeros((10, 10))

        for i in range(100000):
            counter += 1
            # Play game.
            player1 = monopoly.Player(1,
                                      buying_threshold=100,
                                      n=6,
                                      dynamic_ordering=True,
            )

            player2 = monopoly.Player(2,
                                      buying_threshold=1500,
                                      group_ordering=random_ordering(),
                                      step_threshold=True,

            )

            game0.new_players([player1, player2])
            results = game0.play()

            for trade in game0.trades:
                # print(trade[1].group, trade[0].group)
                g1to2 = groups.index(trade[0].group)
                g2to1 = groups.index(trade[1].group)
                matrix[g2to1][g1to2] += 1

            if counter % 1000 == 0:
                print(matrix)
                print(counter)
                new_matrix = normalize_columns(copy.deepcopy(matrix))
                eigenvalues, eigenvectors = numpy.linalg.eig(new_matrix)

                big_vector = eigenvectors[:, 0]  # Grab e-vector.
                small_vector = [x for x in big_vector if x != 0]  # Remove 0s

                # Write to file.
                ranking = normalize_data(small_vector)
                for i in range(10):
                    print(ranking[i], groups[i])
                output_file.writerow([counter] + ranking)

    numpy.savetxt("tradeMatrix.csv", matrix, delimiter=",")

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
    with open("adjTradeMatrix.csv", 'w', newline='') as csvfile:
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


main()