from timer import *
from monopoly import *
import random


def random_player(id):
    player = Player(id, buying_threshold=100, evolving_threshold=random.uniform(0, 0.5))
    return player


def main():
    games_in_a_set = 1000

    for evolving_thresh in range(0, 50, 1):
        winner_matrix = [0, 0, 0]
        et = evolving_thresh / 100
        for i in range(games_in_a_set):
            player1 = Player(1, buying_threshold=100, evolving_threshold=et)
            player2 = random_player(2)
            # Play game.
            game0 = Game([player1, player2], cutoff=1000)
            results = game0.play()

            # Store winner.
            winner_matrix[results['winner']] += 1

        print(evolving_thresh, winner_matrix)


if __name__ == '__main__':
    timer()
    main()
    timer()