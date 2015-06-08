from timer import *
from monopoly import *


def main():
    games_in_a_set = 1000
    cutoff = 1000


    for thresh in range(10, 501, 10):
        length_matrix = []
        for i in range(games_in_a_set):
            # Play game.
            player1 = Player(1, buying_threshold=thresh)
            player2 = Player(2, buying_threshold=thresh)
            game0 = Game([player1, player2],
                         cutoff=cutoff,
                         trading_enabled=False,
            )

            results = game0.play()

            # Store length.
            length_matrix.append(results['length'])

        # Open file.
        print(thresh, sum(length_matrix) / games_in_a_set)


if __name__ == '__main__':
    timer()
    main()
    timer()