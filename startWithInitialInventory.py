# Starts games with each property.
from timer import *
from monopoly import *

def main():
    prop_ids = [1, 3, 5, 6, 8, 9, 11, 12, 13, 14, 15, 16, 18, 19,
                21, 23, 24, 25, 26, 27, 28, 29, 31, 32, 34, 35,
                37, 39]
    for prop_id in prop_ids:
        game_winners = []
        for i in range(1000):
            players = [Player(1, initial_inventory=[prop_id]), Player(2)]
            game = Game(players, cutoff=10000, trading_enabled=False)
            results = game.play()
            game_winners.append(results['winner'])

        print([prop_id, game_winners.count(0), game_winners.count(1), game_winners.count(2)])


if __name__ == '__main__':
    timer()
    main()
    timer()