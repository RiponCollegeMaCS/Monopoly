import mb as monopoly
from timer import *
from random import shuffle
import numpy
from safename import safe_name
import csv


def random_ordering():
    all_groups = ["Brown", "Light Blue", "Pink", "Orange",
                  "Red", "Yellow", "Green", "Dark Blue",
                  "Utility", "Railroad"]
    shuffle(all_groups)
    return tuple(all_groups)


def main(games_in_a_set=5000):
    matrix = numpy.zeros((40, 40))

    game0 = monopoly.Game(cutoff=1000, trading_enabled=True)
    counter = 0

    props = []
    for board_space in game0.board:
        if board_space.is_property:
            props.append(board_space.id)

    for prop1 in props:
        for prop2 in props:
            if prop1 != prop2:

                winners = [0, 0, 0]
                for i in range(games_in_a_set):
                    # Play game.
                    player1 = monopoly.Player(1, buying_threshold=500,step_threshold=True,
                                              group_ordering=random_ordering(),
                                              initial_properties=[prop1])
                    player2 = monopoly.Player(2, buying_threshold=500,step_threshold=True,
                                              group_ordering=random_ordering(),
                                              initial_properties=[prop2])

                    game0.new_players([player1, player2])
                    results = game0.play()

                    # Store length.
                    winners[results['winner']] += 1

                counter += 1
                print(counter)

                matrix[prop1][prop2] += winners[1]
                matrix[prop2][prop1] += winners[2]

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
    with open("PageRankStart_Matrix.csv", 'w', newline='') as csvfile:
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