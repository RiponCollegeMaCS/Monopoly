# Compare "rent power".
import pickle
from timer import *
from monopoly import *
from row_reduction import *


def main():
    all_totals = []
    total = 17000
    for i in range(total):
        game = pickle.load(open('results/stalemates/long/game' + str(i) + '.pickle', "rb"))

        rent_totals = [0, 0]
        players = [game.active_players[0], game.active_players[1]]

        for player_id in [0, 1]:
            for property in players[player_id].inventory:
                rent_totals[player_id] += game.calculate_rent(property=property, owner=players[player_id])

        diff = rent_totals[1] - rent_totals[0]

        rent_totals.append(diff)
        print(rent_totals)
        all_totals.append(rent_totals)


if __name__ == '__main__':
    timer()
    main()
    timer()