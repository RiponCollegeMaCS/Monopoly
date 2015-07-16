import m as monopoly
from timer import *
from random import shuffle
import numpy


def random_ordering():
    all_groups = ["Brown", "Light Blue", "Pink", "Orange",
                  "Red", "Yellow", "Green", "Dark Blue",
                  "Utility", "Railroad"]
    shuffle(all_groups)
    return tuple(all_groups)


def main(games_in_a_set=1000):
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
                    player1 = monopoly.Player(1, buying_threshold=100,
                                              group_ordering=random_ordering(),
                                              initial_properties=[prop1])
                    player2 = monopoly.Player(2, buying_threshold=100,
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