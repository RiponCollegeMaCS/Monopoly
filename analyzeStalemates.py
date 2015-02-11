# Save a dictionary into a pickle file.
import pickle
from timer import *
from monopoly import *
from row_reduction import *

def main():
    all_inventories = []
    current_proportion = 1
    repeat_counter = 0
    for i in range(2700):
        game = pickle.load(open('results/stalemates/long/game' + str(i) + '.pickle', "rb"))
        inventory = [[],[]]

        for property in game.active_players[0].inventory:
            inventory[0].append(property.id)

        for property in game.active_players[1].inventory:
            inventory[1].append(property.id)

        inventory[0].sort()
        inventory[1].sort()
        inventory.sort()

        if inventory in all_inventories:
            repeat_counter +=1
            current_proportion = (i +1 - repeat_counter)/(i+1)
        else:
            all_inventories.append(inventory)
            current_proportion = (i +1 - repeat_counter)/(i+1)

        print(current_proportion)


if __name__ == '__main__':
    timer()
    main()
    timer()