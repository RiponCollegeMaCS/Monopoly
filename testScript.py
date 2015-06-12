import monopoly
from timer import *

def old_success_indicator(games_in_a_set=1000):
    counter = 0
    for i in range(games_in_a_set):
        # Play game.
        player1 = monopoly.Player(1, buying_threshold=500)
        player2 = monopoly.Player(2, buying_threshold=500)
        game0 = monopoly.Game([player1, player2], cutoff=1000, new_trading=True)
        results = game0.play()

        # Store length.
        if results['winner'] == 1:
            counter += 1

    return counter / games_in_a_set

if __name__ == '__main__':
    timer()
    print(old_success_indicator())
    timer()