import PLmonopoly as monopoly
from timer import *
import cProfile
from random import shuffle

def random_ordering():
    all_groups = ["Brown", "Light Blue", "Pink", "Orange",
                  "Red", "Yellow", "Green", "Dark Blue",
                  "Utility", "Railroad"]
    shuffle(all_groups)
    return tuple(all_groups)

def old_success_indicator(games_in_a_set=100):
    counter = 0
    game0 = monopoly.Game(cutoff=1000, ranking_trading=True)

    for i in range(games_in_a_set):
        # Play game.
        player1 = monopoly.Player(1, buying_threshold=500, group_ordering=random_ordering())
        player2 = monopoly.Player(2, buying_threshold=500, group_ordering=random_ordering())

        game0.new_players([player1, player2])
        results = game0.play()

        # Store length.
        counter += results['length']

    return counter / games_in_a_set


if __name__ == '__main__':
    timer()
    #print(old_success_indicator())
    cProfile.run('old_success_indicator()',sort=1)
    timer()