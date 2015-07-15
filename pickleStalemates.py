# Save a dictionary into a pickle file.
import csv
import pickle
from timer import *
from m import *
from copy import deepcopy
from multiprocessing import *
import math


def play_set(sample_size, game, results_q):
    game_winners = []

    for i in range(sample_size):
        game_to_play = deepcopy(game)


        # Add 10000 more turns.
        game_to_play.cutoff = 20000

        # Reset money.
        for player in game_to_play.active_players:
            player.money = 1500
            player.position = 0

        # Play the game.
        results = game_to_play.play()
        game_winners.append(results['winner'])

    results_q.put(game_winners)


def stability(game, total_sample_size=1000):
    procs = 1
    results_q = Queue()  # Queue for results.
    proc_list = []  # List of processes.
    for i in range(procs):
        proc_list.append(Process(target=play_set, args=(int(total_sample_size / procs), game, results_q)))

    for proc in proc_list:  # Start all processes.
        proc.start()

    for proc in proc_list:  # Wait for all processes to finish.
        proc.join()

    results_list = []

    # Gather the results from each process.
    while not results_q.empty():
        results_list.extend(results_q.get())

    results = [results_list.count(0) / total_sample_size,
               results_list.count(1) / total_sample_size,
               results_list.count(2) / total_sample_size]

    return results


def write_row(row):
    with open('results/stalemates/discrete_trading_stability.csv', 'a', newline='') as csvfile:
        output_file = csv.writer(csvfile, quotechar=',')
        output_file.writerow(row)


def random_ordering():
    all_groups = ["Brown", "Light Blue", "Pink", "Orange",
                  "Red", "Yellow", "Green", "Dark Blue",
                  "Utility", "Railroad"]
    shuffle(all_groups)
    return tuple(all_groups)


def main():
    main_counter = 0
    game_counter = 0

    while main_counter < 10:
        game_counter += 1
        # Play game.
        player1 = Player(1, group_ordering=random_ordering(), buying_threshold=500)
        player2 = Player(2, group_ordering=random_ordering(), buying_threshold=500)
        game0 = Game([player1, player2], cutoff=10000, trading_enabled=True)
        results = game0.play()


        # Pickle if there is a tie.
        if results['winner'] == 0:

            # Pickle it...like a cucumber!
            pickle.dump(game0, open('results/stalemates/discrete_trading/game' + str(main_counter) + '.pickle', 'wb'))
            print("------", main_counter, "------")
            print(results['monopolies'], game_counter)
            main_counter += 1

            matrix = numpy.loadtxt(open("data/longtime.csv", "rb"), delimiter=",")
            odds = matrix[0]

            rent_power = []
            for player in game0.active_players:
                money_changes = [0] * 41

                # Rents the player will get.
                for property in player.inventory:
                    money_changes[property.id] = game0.calculate_rent(property)

                # Rents the player will pay.
                for property in game0.other_player(player).inventory:
                    money_changes[property.id] = -game0.calculate_rent(property)

                money_changes[40] = (-50)  # For the last entry, "In Jail"

                # Community Chest
                cc_change = 455 + (10 * (game0.num_active_players - 1)) - game0.community_chest_repairs(player)
                cc_change /= 14  # Weighted by the 14 cards that change money.
                money_changes[2] = cc_change
                money_changes[17] = cc_change
                money_changes[33] = cc_change

                # Chance
                c_change = 235 - (50 * (game0.num_active_players - 1)) - game0.chance_repairs(player)
                c_change /= 6  # Weighted by the 6 card that change money
                money_changes[7] = c_change
                money_changes[22] = c_change
                money_changes[36] = c_change

                # Fixed spaces.
                money_changes[4] = -75  # Luxury Tax
                money_changes[38] = -200  # Income Tax

                ######
                expected_value = numpy.dot(odds, money_changes)
                expected_value += (1 / 6.09) * 200

                money_changes_sq = [pow(i, 2) for i in money_changes]
                variance = numpy.dot(odds, money_changes_sq) + ((200 ^ 2) * (1 / 6.09)) - pow(expected_value, 2)
                stdev = math.sqrt(variance)


                rent_power.append([expected_value, stdev])

            print(rent_power)

            # Find stability.
            stab = stability(game0, total_sample_size=100)
            write_row(stab)
            print(stab)


if __name__ == '__main__':
    timer()
    main()
    timer()


