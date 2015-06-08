from timer import *
from monopoly import *


def random_group_values():
    group_values = {"Brown": randint(500, 1000),
                    "Light Blue": randint(500, 1000),
                    "Pink": randint(500, 1000),
                    "Orange": randint(500, 1000),
                    "Red": randint(500, 1000),
                    "Yellow": randint(500, 1000),
                    "Green": randint(500, 1000),
                    "Dark Blue": randint(500, 1000),
                    "Utility": randint(500, 1000),
                    "Railroad": randint(500, 1000)
    }
    return group_values


def main():
    games_in_a_set = 1000
    winner_matrix = [0, 0, 0]

    for i in range(games_in_a_set):
        player1 = Player(1, buying_threshold=100,
                         group_values={"Brown": 100, "Light Blue": 600, "Pink": 700, "Orange": 1000,
                                       "Red": 1000, "Yellow": 1000, "Green": 100, "Dark Blue": 1000,
                                       "Utility": 100, "Railroad": 1000})
        player2 = Player(2, buying_threshold=100,
                         group_values=random_group_values())

        # Play game.
        game0 = Game([player1, player2], cutoff=1000, complex_trading2=True)
        results = game0.play()

        # Store winner.
        winner_matrix[results['winner']] += 1

    print(winner_matrix)


if __name__ == '__main__':
    timer()
    main()
    timer()