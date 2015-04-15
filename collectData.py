import csv
from timer import *
from monopoly import *


def main():
    games_in_a_set = 10000
    cutoff = 1000
    length_matrix = []

    for i in range(games_in_a_set):
        # Play game.
        player1 = Player(1)
        player2 = Player(2)
        game0 = Game([player1, player2], cutoff=cutoff)
        results = game0.play()

        # Store length.
        length_matrix.append(results['length'])

    with open('results/simple_runs/blah.csv', 'w', newline='') as csvfile:
        output_file = csv.writer(csvfile, quotechar=',')
        # Write to file.
        for i in range(cutoff):
            output_file.writerow()


if __name__ == '__main__':
    timer()
    main()
    timer()