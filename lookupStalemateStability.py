# Counts duplicate stalemates.
import pickle
from timer import *
import csv


def main():
    with open('results/stalemateStability003.csv', 'r') as dest_f:
        data_iter = csv.reader(dest_f, delimiter=",", quotechar='"')
        data = [float(data[1]) for data in data_iter]

    i = 0
    for stabilityNumber in data:
        if stabilityNumber >= 0:
            game = pickle.load(open('results/stalemates/long/game' + str(i) + '.pickle', "rb"))

            inventory = [[], []]

            for player in game.active_players:
                for property in player.inventory:
                    inventory[player.number - 1].append(property.id)

            inventory[0].sort()
            inventory[1].sort()
            inventory.sort()

            print(inventory, stabilityNumber)
        i += 1


if __name__ == '__main__':
    timer()
    main()
    timer()