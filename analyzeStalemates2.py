# Looks for unique stalemates and gives a summary.
import pickle
from timer import *
from monopoly import *
from row_reduction import *


def print_modes(my_list, num=0):
    total_games = len(my_list)
    all_elements = []  # Stores elements.
    counting_list = []  # Stores counts.

    for element in my_list:
        if element in all_elements:
            # Increase old entry.
            counting_list[all_elements.index(element)] += 1
        else:
            # Add new entry.
            all_elements.append(element)
            counting_list.append(1)

    master_list = []  # Stores both counts and elements.

    # Merge counts and elements.
    for i in range(len(all_elements)):
        master_list.append([all_elements[i], counting_list[i]])

    # Sort.
    sorted_results = sorted(master_list, key=lambda tup: tup[1], reverse=True)

    in_group = [2, 3, 3, 3, 3, 3, 3, 2, 4, 2]
    group_broken_counter = [0 for i in range(10)]

    # Print result.
    if not num:
        num = len(sorted_results)

    broken_counter = 0
    for i in range(num):
        broken = False
        for prop_id in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
            if sorted_results[i][0][0][prop_id] != in_group[prop_id] and sorted_results[i][0][0][prop_id] != 0:
                if prop_id not in [8, 9]:
                    broken = True
                group_broken_counter[prop_id] += 1
        if broken:
            broken_counter += 1

        print(sorted_results[i][0], sorted_results[i][1], broken)


    # Configs not found.
    all_configs = 552960
    found_configs = len(counting_list) + 1

    broken_groups = []
    for element in group_broken_counter:
        broken_groups.append(element / total_games)

    print("total games:", total_games)
    print("all configs:", all_configs)
    print("found unique configs:", found_configs)
    print("% not found:", (all_configs - found_configs) / all_configs)
    print("% broken (of all searched):", broken_counter / total_games)
    print("broken groups", broken_groups)


def find_all_subinventories():
    all_inventories = []
    for v0 in range(3):
        for v1 in range(4):
            for v2 in range(4):
                for v3 in range(4):
                    for v4 in range(4):
                        for v5 in range(4):
                            for v6 in range(4):
                                for v7 in range(3):
                                    for v8 in range(5):
                                        for v9 in range(3):
                                            inventory = [v0, v1, v2, v3, v4, v5, v6, v7, v8, v9]
                                            # inventory2 = [2 - v0, 3 - v1, 3 - v2, 3 - v3, 3 - v4, 3 - v5, 3 - v6,
                                            # 2 - v7, 4 - v8, 2 - v9]
                                            all_inventories.append(inventory)

    print('inventories found:', len(all_inventories))
    return all_inventories


def main():
    all_inventories = []
    sub_inventories = []
    total = 100
    for i in range(total):
        game = pickle.load(open('results/stalemates/long/game' + str(i) + '.pickle', "rb"))

        property_counts = [[0 for i in range(10)], [0 for i in range(10)]]
        convert_group = {"Brown": 0, "Light Blue": 1, "Pink": 2, "Orange": 3,
                         "Red": 4, "Yellow": 5, "Green": 6, "Dark Blue": 7,
                         "Railroad": 8, "Utility": 9}
        for player_id in [0, 1]:
            for property in game.active_players[player_id].inventory:
                property_counts[player_id][convert_group[property.group]] += 1

        property_counts.sort()
        sub_inventories.append(property_counts[0])
        sub_inventories.append(property_counts[1])

        all_inventories.append(property_counts)

    print_modes(all_inventories)


if __name__ == '__main__':
    timer()
    main()
    timer()