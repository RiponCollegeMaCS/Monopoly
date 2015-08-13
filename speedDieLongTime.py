import mb_auctions_speeddie as monopoly
import math
from random import shuffle, randint


def random_ordering():
    all_groups = ["Brown", "Light Blue", "Pink", "Orange",
                  "Red", "Yellow", "Green", "Dark Blue",
                  "Utility", "Railroad"]
    shuffle(all_groups)
    return tuple(all_groups)


def best_ordering():
    other_groups = ["Pink", "Red",
                    "Yellow", "Green",
                    "Dark Blue", "Utility", "Brown"]
    shuffle(other_groups)

    return tuple(["Railroad", "Light Blue", "Orange"] + other_groups)


def main():
    game0 = monopoly.Game(cutoff=1000, trading_enabled=True, image_exporting=0, speed_die=True)

    base_games = 10000
    board_vector = [0] * 40
    counter = 0

    while (counter < base_games):
        counter += 1
        # Play game.
        player1 = monopoly.Player(1,
                                  buying_threshold=1500,
                                  group_ordering=best_ordering(),
                                  step_threshold=True,
                                  position=randint(0,40)

        )
        player2 = monopoly.Player(2,
                                  buying_threshold=1500,
                                  group_ordering=random_ordering(),
                                  step_threshold=True,
                                  position=randint(0,40)

        )

        game0.new_players([player1, player2])
        results = game0.play()

        for property in game0.board:
            board_vector[property.id] += property.visits

    for count in board_vector:
        print(count)

    print("*", sum(board_vector), counter)


main()