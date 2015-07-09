import monopoly as monopoly
from timer import *
from random import shuffle


def random_ordering():
    all_groups = ["Brown", "Light Blue", "Pink", "Orange",
                  "Red", "Yellow", "Green", "Dark Blue",
                  "Utility", "Railroad"]
    shuffle(all_groups)
    return tuple(all_groups)


def main(games_in_a_set=1000):
    game0 = monopoly.Game(cutoff=1000, trading_enabled=True)
    for prop1 in game0.board:
        if prop1.is_property:
            winners = [0, 0, 0]
            for i in range(games_in_a_set):
                # Play game.
                player1 = monopoly.Player(1, buying_threshold=100,
                                          group_ordering=random_ordering(),
                                          initial_properties=[prop1])
                player2 = monopoly.Player(2, buying_threshold=100,
                                          group_ordering=random_ordering())

                game0.new_players([player1, player2])
                results = game0.play()

                # Store length.
                winners[results['winner']] += 1

            print(winners, prop1.name)


if __name__ == '__main__':
    timer()
    main()
    timer()