# Takes groups of properties away from stalemates.
import pickle
from timer import *
from monopoly import *
from copy import deepcopy
from multiprocessing import *
import csv
from lookupStalemateStability import stability


def play_set(sample_size, game, results_q):
    game_winners = []

    for i in range(sample_size):
        game_to_play = deepcopy(game)

        # Add 10000 more turns.
        game_to_play.cutoff = 20000

        # Reset money.
        for player in game_to_play.active_players:
            player.money = 1500

        # Play the game.
        results = game_to_play.play()
        game_winners.append(results['winner'])

    results_q.put(game_winners)


def main():
    groups = ['Railroad', 'Utility', 'Brown', 'Light Blue', 'Pink', 'Orange', 'Red', 'Yellow', 'Green', 'Dark Blue']
    groups.remove('Green')
    groups.remove('Red')
    with open('results/subtractiveMeasure21.csv', 'w', newline='') as csvfile:
        output_file = csv.writer(csvfile, quotechar=',')
        for group in groups:
            total_sample_size = 1000
            game_to_find = 1
            games_found = 0

            game_id = 21
            while games_found < game_to_find:
                if stability(game_id) >= 0.95:
                    # Load in game data.
                    game = pickle.load(open('results/stalemates/long/game' + str(game_id) + '.pickle', "rb"))

                    # Look for group.
                    properties_to_remove = []
                    player_found = False
                    group_found = False
                    for player in game.active_players:
                        player.add_railroads_and_utilities()
                        for monopoly in player.monopolies:
                            if monopoly == group:
                                group_found = True
                                player_found = player
                                for property in player.inventory:
                                    if property.group == group:
                                        properties_to_remove.append(property)
                    if not group_found:
                        print(group, "not found")

                    if group_found:
                        print(group, "found")

                        # Remove group from player's list of monopolies.
                        player_found.monopolies.remove(group)

                        house_counter = 0
                        hotel_counter = 0
                        # Reset property's methods.
                        for property in properties_to_remove:
                            if property.buildings == 5:
                                game.hotels += 1
                                hotel_counter += 1
                            else:
                                game.houses += property.buildings
                                house_counter += property.buildings

                            property.buildings = 0
                            property.mortgaged = False

                            game.unowned_properties.append(property)
                            player_found.inventory.remove(property)
                            property.buildings = 0

                        games_found += 1

                        procs = 4
                        results_q = Queue()  # Queue for results.
                        proc_list = []  # List of processes.
                        for i in range(procs):
                            proc_list.append(
                                Process(target=play_set, args=(int(total_sample_size / procs), game, results_q)))
                        for proc in proc_list:  # Start all processes.
                            proc.start()
                        for proc in proc_list:  # Wait for all processes to finish.
                            proc.join()
                        # Gather the results from each process.
                        results_list = []
                        while not results_q.empty():
                            results_list.extend(results_q.get())

                        results = [game_id,
                                   results_list.count(0),
                                   results_list.count(1),
                                   results_list.count(2),
                                   group,
                                   house_counter,
                                   hotel_counter,
                                   player_found.number]
                        print(results)
                        output_file.writerow(results)
                game_id += 1


if __name__ == '__main__':
    timer()
    main()
    timer()