# Save a dictionary into a pickle file.
import pickle
from timer import *
from monopoly import *


def main():
    main_counter = 0
    running_average = 0
    game_lengths = []
    game_counter = 0
    while main_counter < 10:
        game_counter += 1
        # Play game.
        player1 = Player(1)
        player2 = Player(2)
        game0 = Game([player1, player2], cutoff=10000, trading_enabled=True, hotel_upgrade=True, building_sellback=True)
        results = game0.play()

        #game_lengths.append(results['length'])
        #running_average = sum(game_lengths) / len(game_lengths)

        if results['length'] > 1000:
            print('long game:', results['length'])

        #print(results['length'])


        # Pickle if there is a tie.
        if results['winner'] == 0:
            # Pickle it...like a cucumber!
            pickle.dump(game0, open('results/stalemates/building_sellback/game' + str(main_counter) + '.pickle', 'wb'))
            print("!!!!!!found", main_counter)
            main_counter += 1


if __name__ == '__main__':
    timer()
    main()
    timer()