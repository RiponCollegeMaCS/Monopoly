import mb as monopoly
from timer import *
from random import shuffle, randint
import numpy
import csv
from safename import *


def random_ordering():
    all_groups = ["Brown", "Light Blue", "Pink", "Orange",
                  "Red", "Yellow", "Green", "Dark Blue",
                  "Utility", "Railroad"]
    shuffle(all_groups)
    return tuple(all_groups)


def main(games_in_a_set=10000):
    matrix = numpy.zeros((28, 28))
    game_counter = 0
    game0 = monopoly.Game(cutoff=1000, trading_enabled=True)

    while game_counter < games_in_a_set:
        print(game_counter)
        # Play game.
        player1 = monopoly.Player(1,  # dynamic_ordering=True,
                                  # c=1, n=randint(1, 13))
                                  buying_threshold=500, group_ordering=random_ordering(), step_threshold=True)
        player2 = monopoly.Player(2,  # dynamic_ordering=True,
                                  # c=1, n=randint(1, 13))
                                  buying_threshold=500, group_ordering=random_ordering(), step_threshold=True)

        game0.new_players([player1, player2])
        results = game0.play()

        if results['winner'] != 0:
            game_counter += 1
            winner = game0.active_players[0]
            loser = game0.inactive_players[0]

            for winning_prop in winner.inventory:
                for losing_prop in loser.inventory:
                    matrix[winning_prop.prop_id][losing_prop.prop_id] += 1

    matrix = normalize_columns(matrix)

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
    with open("PageRankEndMatrix.csv", 'w', newline='') as csvfile:
        output_file = csv.writer(csvfile, quotechar=',')

        for row in graph_matrix:
            output_file.writerow(row)

    eigenvalues, eigenvectors = numpy.linalg.eig(matrix)
    for i in range(len(eigenvalues)):
        print("*************************")
        print(eigenvalues[i])
        for element in eigenvectors[:, i]:
            if element.real != 0:
                print(element.real)


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