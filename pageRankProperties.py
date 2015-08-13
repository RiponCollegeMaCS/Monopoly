import mb as monopoly
from timer import *
from random import shuffle
import numpy
import csv
import math


def random_ordering():
    all_groups = ["Brown", "Light Blue", "Pink", "Orange",
                  "Red", "Yellow", "Green", "Dark Blue",
                  "Utility", "Railroad"]
    shuffle(all_groups)
    return tuple(all_groups)


def main(desired_radius = 0.01):
    matrix = numpy.zeros((40, 40))

    game0 = monopoly.Game(cutoff=1000, trading_enabled=True)

    props = []
    for board_space in game0.board:
        if board_space.is_property:
            props.append(board_space.id)

    main_counter = 0
    for prop1 in props:
        for prop2 in props[props.index(prop1) + 1:]:
            winners = [0, 0, 0]
            base_games = 10
            game_counter = 0
            current_radius = 10


            while (game_counter < base_games) or current_radius > desired_radius:
                # Play game.
                player1 = monopoly.Player(1, buying_threshold=1500, step_threshold=True,
                                          group_ordering=random_ordering(),
                                          initial_properties=[prop1])
                player2 = monopoly.Player(2, buying_threshold=1500, step_threshold=True,
                                          group_ordering=random_ordering(),
                                          initial_properties=[prop2])

                game0.new_players([player1, player2])
                results = game0.play()
                winners[results['winner']] += 1

                game_counter += 1

                p = winners[1] / game_counter
                current_radius = 1.960 * math.sqrt((p * (1 - p)) / game_counter)

                #print(game_counter, p, current_radius)

            main_counter += 1
            print(main_counter)

            matrix[prop1][prop2] += winners[1] / game_counter
            matrix[prop2][prop1] += winners[2] / game_counter

    matrix = normalize_columns(matrix)


    # Save matrix
    with open("PageRankStart_Matrix.csv", 'w', newline='') as csvfile:
        output_file = csv.writer(csvfile, quotechar=',')

        for row in matrix:
            output_file.writerow(row)

    eigenvalues, eigenvectors = numpy.linalg.eig(matrix)
    for i in range(len(eigenvalues)):
        print("*************************")
        print(eigenvalues[i])
        normalized_vector = normalize_data(eigenvectors[:, i])
        for element in normalized_vector:
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