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


def main(games_in_a_set=100000):
    matrix = numpy.zeros((40, 40))
    game_counter = 0
    game0 = monopoly.Game(cutoff=1000, trading_enabled=False)

    while game_counter < games_in_a_set:
        # Play game.
        player1 = monopoly.Player(1, buying_threshold=100)
        player2 = monopoly.Player(2, buying_threshold=100)

        game0.new_players([player1, player2])
        results = game0.play()

        if results['winner'] != 0:
            game_counter += 1
            winner = game0.active_players[0]
            loser = game0.inactive_players[0]

            for winning_prop in winner.inventory:
                for losing_prop in loser.inventory:
                    matrix[winning_prop.id][losing_prop.id] += 1

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