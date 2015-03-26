# Tests the stability of stalemates.
import pickle
from timer import *
from monopoly import *
from copy import deepcopy
from multiprocessing import *
import csv


def play_set(sample_size, game, results_q):
    game_lengths = []

    for i in range(sample_size):
        game_to_play = deepcopy(game)

        # Add 10000 more turns.
        game_to_play.cutoff = 20000

        # Reset money.
        for player in game_to_play.active_players:
            player.money = 1500

        # Play the game.
        results = game_to_play.play()
        game_lengths.append(results['length'] - 10000)

    results_q.put(game_lengths.count(10000))


def main():
    with open('results/stalemateStability004.csv', 'w', newline='') as csvfile:
        output_file = csv.writer(csvfile, quotechar=',')
        total_sample_size = 1000
        for game_id in range(100,200):
            # Load in game data.
            game = pickle.load(open('results/stalemates/long/game' + str(game_id) + '.pickle', "rb"))

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
                results_list.append(results_q.get())

            results = [game_id,sum(results_list) / total_sample_size]
            print(results)
            output_file.writerow(results)




        '''results.append(12-new_game.hotels)
        new_game.cutoff = 20000
        results = new_game.play()

        # Pickle it...like a cucumber!
        pickle.dump(new_game, open('results/stalemates/long/continued/game' + str(i) + '.pickle', 'wb'))

    for i in range(13):
        print(i,results.count(i))'''



if __name__ == '__main__':
    main()