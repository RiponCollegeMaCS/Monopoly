from timer import *
from monopoly import *


def random_property_values():
    return [randint(200, 500) for i in range(40)]


def main():
    games_in_a_set = 1000
    winner_matrix = [0, 0, 0]

    p1_values = random_property_values()
    print(p1_values)
    for i in range(games_in_a_set):
        player1 = Player(1, buying_threshold=100, property_values=p1_values)
        player2 = Player(2, buying_threshold=100, property_values=random_property_values())

        # Play game.
        game0 = Game([player1, player2], cutoff=1000, property_trading=True)
        results = game0.play()

        # Store winner.
        winner_matrix[results['winner']] += 1

    print(winner_matrix)


if __name__ == '__main__':
    timer()
    main()
    timer()