# Save a dictionary into a pickle file.
import csv
import pickle
from timer import *
from monopoly import *
from copy import deepcopy
from multiprocessing import *


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


def stability(game):
    total_sample_size = 10000
    procs = 4
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
    game_lengths = []
    game_counter = 0
    while main_counter < 10:
        game_counter += 1
        # Play game.
        order = random_ordering()
        player1 = Player(1, group_ordering=order)
        player2 = Player(2, group_ordering=tuple(reversed(list(order))))
        game0 = Game([player1, player2], cutoff=10000,
                     new_trading=True)  # trading_enabled=True, hotel_upgrade=True, building_sellback=True)
        results = game0.play()

        # game_lengths.append(results['length'])
        #running_average = sum(game_lengths) / len(game_lengths)
        #print(running_average)

        #print(results['length'])


        # Pickle if there is a tie.
        if results['winner'] == 0:
            # Pickle it...like a cucumber!
            pickle.dump(game0, open('results/stalemates/discrete_trading/game' + str(main_counter) + '.pickle', 'wb'))
            print("!!!!!!found", main_counter)
            print(results['monopolies'], game_counter)
            main_counter += 1

            # Find stability.
            stab = stability(game0)
            write_row(stab)
            print(stab)


if __name__ == '__main__':
    timer()
    main()
    timer()