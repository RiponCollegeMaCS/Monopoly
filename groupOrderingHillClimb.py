from mb import *
from timer import *
from multiprocessing import *
import csv
import copy


def random_ordering():
    all_groups = ["Brown", "Light Blue", "Pink", "Orange",
                  "Red", "Yellow", "Green", "Dark Blue",
                  "Utility", "Railroad"]
    shuffle(all_groups)
    return tuple(all_groups)


def random_neighbor1(ordering):
    index1 = randint(0, 9)
    index2 = index1
    while index2 == index1:
        index2 = randint(0, 9)

    list_ordering = list(ordering)

    temp = list_ordering[index1]
    list_ordering[index1] = list_ordering[index2]
    list_ordering[index2] = temp

    return tuple(list_ordering)


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


def insertion_neighbors(ordering):
    ordering = list(ordering)

    all_random_neighbors = []

    for i in range(10):
        group = ordering[i]
        short_ordering = copy.deepcopy(ordering)
        short_ordering.remove(group)

        for j in range(10):
            if i != j:
                new_ordering = copy.deepcopy(short_ordering)

                new_ordering.insert(j, group)

                all_random_neighbors.append(tuple(new_ordering))

    shuffle(all_random_neighbors)

    return all_random_neighbors


def all_short_random_neighbors2(ordering):
    all_random_neighbors = []
    for index in range(0, 9):
        list_ordering = list(ordering)
        temp = list_ordering[index]
        list_ordering[index] = list_ordering[index + 1]
        list_ordering[index + 1] = temp
        all_random_neighbors.append(tuple(list_ordering))

    return all_random_neighbors


'''def old_success_indicator(ordering, games_in_a_set=10000):
    winner_matrix = [0, 0, 0]

    for i in range(games_in_a_set):
        # Play game.
        player1 = Player(1, buying_threshold=500, group_ordering=ordering)
        player2 = Player(2, buying_threshold=500, group_ordering=random_ordering())
        game0 = Game([player1, player2], cutoff=1000, trading_enabled=True)
        results = game0.play()

        # Store length.
        winner_matrix[results['winner']] += 1

    return winner_matrix[1] / games_in_a_set'''


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


def success_indicator(ordering, number_of_games=1000, procs=4):
    results_q = Queue()  # Queue for results.
    proc_list = [Process(target=play_set, args=(ordering, int(number_of_games / procs), results_q))
                 for i in range(procs)]  # List of processes.
    for proc in proc_list:  # Start all processes.
        proc.start()
    for proc in proc_list:  # Wait for all processes to finish.
        proc.join()
    results_list = []

    # Gather the results from each process in a list of counts.
    while results_q.empty() == False:
        results_list.append(results_q.get())

    # Success rate = total count / total number of games
    success_rate = float(sum(results_list)) / float(number_of_games)

    return 100 * success_rate


def lookup_success(ordering, ordering_archive, success_archive):
    length = len(ordering_archive)
    for index in range(length):
        if ordering_archive[index] == ordering:
            print("-----used archive-----")
            return success_archive[index]

    success = success_indicator(ordering)

    ordering_archive.append(ordering)
    success_archive.append(success)

    if length >= 50:
        ordering_archive = []
        success_archive = []

    return success


def write_row(row):
    with open('results/hillClimb_blah.csv', 'a', newline='') as csvfile:
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
        old_success = success_indicator(old_ordering)  # lookup_success(old_ordering, ordering_archive, success_archive)
        print(old_ordering, old_success)
        write_row([old_ordering, old_success])

        all_neighbors = neighbors(old_ordering)

        while counter < (len(all_neighbors) - 1):
            new_ordering = all_neighbors[counter]
            new_success = success_indicator(new_ordering)

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
