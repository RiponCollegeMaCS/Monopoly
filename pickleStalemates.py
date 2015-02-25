# Save a dictionary into a pickle file.
import pickle
from timer import *
from monopoly import *
# game002 = pickle.load( open( "entry.pickle", "rb" ) )

def main():
    main_counter = 20183
    while main_counter < 50000:
        # Play game.
        player1 = Player(1)
        player2 = Player(2)
        game0 = Game([player1, player2], cutoff=10000, trading_enabled=True)
        results = game0.play()

        # Pickle if there is a tie.
        if results['winner'] == 0:
            # Pickle it...like a cucumber!
            pickle.dump(game0, open('results/stalemates/long/game' + str(main_counter) + '.pickle', 'wb'))
            main_counter += 1


if __name__ == '__main__':
    timer()
    main()
    timer()