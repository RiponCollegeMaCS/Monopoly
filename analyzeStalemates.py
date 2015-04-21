# Counts duplicate stalemates.
import pickle
from timer import *
from monopoly import *
#from row_reduction import *


def main():
    all_inventories = []
    current_proportion = 1
    repeat_counter = 0
    total = 17000
    for i in range(total):
        game = pickle.load(open('results/stalemates/long/game' + str(i) + '.pickle', "rb"))
        inventory = [[], []]

        for property in game.active_players[0].inventory:
            inventory[0].append(property.id)

        for property in game.active_players[1].inventory:
            inventory[1].append(property.id)

        inventory[0].sort()
        inventory[1].sort()
        inventory.sort()
        repeats_found = []

        if inventory in all_inventories:
            if inventory in repeats_found:
                repeat_counter += 1
            else:
                repeats_found.append(inventory)
                repeat_counter += 2

        if inventory in all_inventories:
            repeat_counter += 1
        else:
            all_inventories.append(inventory)

        current_proportion = repeat_counter / (i + 1)
        print(current_proportion)


if __name__ == '__main__':
    timer()
    main()
    timer()