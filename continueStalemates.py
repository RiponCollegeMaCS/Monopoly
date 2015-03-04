# Tests the stability of stalemates.
import pickle
from timer import *
from monopoly import *
import numpy


def main():
    game_lengths = []
    for game_id in range(50):
        for i in range(5):
            # Resume game
            game = pickle.load(open('results/stalemates/long/game' + str(game_id) + '.pickle', "rb"))

            # Add 10000 more turns.
            game.cutoff = 20000
            for player in game.active_players:
                player.money = 1500

            results = game.play()
            game_lengths.append(results['length']-10000)

        print(game_lengths)

        '''results.append(12-new_game.hotels)
        new_game.cutoff = 20000
        results = new_game.play()

        # Pickle it...like a cucumber!
        pickle.dump(new_game, open('results/stalemates/long/continued/game' + str(i) + '.pickle', 'wb'))

    for i in range(13):
        print(i,results.count(i))'''


if __name__ == '__main__':
    timer()
    main()
    timer()