from monopoly import *
from timer import *
import csv
import copy
import math


def random_ordering():
    all_groups = ["Brown", "Light Blue", "Pink", "Orange",
                  "Red", "Yellow", "Green", "Dark Blue",
                  "Utility", "Railroad"]
    shuffle(all_groups)
    return tuple(all_groups)



def all_short_random_neighbors1(ordering):
    all_random_neighbors = []
    for index1 in range(0, 10):
        for index2 in range(index1, 10):
            if index1 != index2:
                list_ordering = list(ordering)
                temp = list_ordering[index1]
                list_ordering[index1] = list_ordering[index2]
                list_ordering[index2] = temp
                all_random_neighbors.append(tuple(list_ordering))

    shuffle(all_random_neighbors)

    return all_random_neighbors






def play_set(ordering, number_of_games, results_q):
    results_list = []
    game0 = Game(cutoff=1000, trading_enabled=True)
    for i in range(number_of_games):
        # Play game.
        player1 = Player(1, buying_threshold=500, group_ordering=ordering, step_threshold=True)
        player2 = Player(2, buying_threshold=500, group_ordering=random_ordering(), step_threshold=True)
        game0.new_players([player1, player2])
        results = game0.play()
        results_list.append(results['winner'])  # Store the game's result.

    results_q.put(results_list.count(1))



    

def progressive_success_indicator(ordering, radius = 0.01, procs=4):
    game0 = monopoly.Game(cutoff=1000, trading_enabled=True, image_exporting=0)

    base_games = 1000
    counter = 0
    wins = 0

    interval_size = 10

    while (counter < base_games) or interval_size > 0.01:
        counter += 1
        # Play game.
        player1 = monopoly.Player(1,
                                  buying_threshold=2000,
                                  group_ordering=ordering,
                                  step_threshold=True,

        )
        player2 = monopoly.Player(2,
                                  buying_threshold=2000,
                                  group_ordering=random_ordering(),
                                  step_threshold=True,
        )

        game0.new_players([player1, player2])
        results = game0.play()

        # Store result.
        if results['winner'] == 1:
            wins+=1
        
        p = wins / counter
        interval_size = 1.960 * math.sqrt((p * (1 - p)) / counter)

        #print(counter, p, interval_size)
    
    return p




    return success


def write_row(row):
    with open('hillClimb_step_threshold.csv', 'a', newline='') as csvfile:
        output_file = csv.writer(csvfile, quotechar=',')
        output_file.writerow(row)


def neighbors(ordering):
    return  all_short_random_neighbors1(ordering)
    #return insertion_neighbors(ordering)


def hill_climb():
    ordering_archive = []
    success_archive = []

    while True:
        print('Start!')
        write_row(["Start!"])
        counter = 0
        old_ordering = random_ordering()
        old_success = progressive_success_indicator(old_ordering)  # lookup_success(old_ordering, ordering_archive, success_archive)
        print(old_ordering, old_success)
        #write_row([old_ordering, old_success])

        all_neighbors = neighbors(old_ordering)

        while counter < (len(all_neighbors) - 1):
            new_ordering = all_neighbors[counter]
            new_success = progressive_success_indicator(new_ordering)

            counter += 1

            if new_success > old_success:
                old_ordering = new_ordering
                old_success = new_success
                print(old_ordering, old_success, counter)
                write_row([old_ordering, old_success])

                all_neighbors = neighbors(old_ordering)
                counter = 0

        print('No better neighbors.')


def brute_force():
    groups = ["Brown", "Pink", "Red", "Yellow", "Green", "Dark Blue", "Utility"]
    import itertools

    all_orderings = itertools.permutations(groups)
    for addon in all_orderings:
        ordering = ["Railroad", "Orange", "Light Blue"]
        ordering.extend(addon)

        print(ordering, success_indicator(ordering))


def main():
    hill_climb()
    # brute_force()


if __name__ == '__main__':
    # timer()
    main()
    # timer()
