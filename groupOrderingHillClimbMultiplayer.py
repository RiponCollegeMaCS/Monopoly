from mb_auctions import *
import csv
import math
import itertools


def random_strategy():
    all_groups = ["Brown", "Light Blue", "Pink", "Orange",
                  "Red", "Yellow", "Green", "Dark Blue",
                  "Utility", "Railroad"]
    shuffle(all_groups)

    all_groups.append(choice([i for i in range(500, 2001, 500)]))
    return all_groups


def neighbors(strategy):
    ordering = strategy[0:10]
    threshold = strategy[10]

    all_random_neighbors = []
    for index1 in range(0, 10):
        for index2 in range(index1, 10):
            if index1 != index2:
                list_ordering = list(ordering)
                temp = list_ordering[index1]
                list_ordering[index1] = list_ordering[index2]
                list_ordering[index2] = temp
                all_random_neighbors.append(list_ordering + [threshold])

    if threshold < 2000:
        all_random_neighbors.append(ordering + [threshold + 500])
    if threshold > 500:
        all_random_neighbors.append(ordering + [threshold - 500])

    shuffle(all_random_neighbors)

    return all_random_neighbors


def success(strategy):
    p1_ordering = strategy[0:10]
    p1_threshold = strategy[10]

    wins = 0
    game0 = Game(cutoff=1000, trading_enabled=True)
    counter = 0
    interval_size = 10
    base_games = 100
    p = 0

    while (counter < base_games) or interval_size > 0.01:
        counter += 1

        # Play game.
        p2_strategy = random_strategy()
        p2_ordering = p2_strategy[0:10]
        p2_threshold = p2_strategy[10]


        p3_strategy = random_strategy()
        p3_ordering = p3_strategy[0:10]
        p3_threshold = p3_strategy[10]

        player1 = Player(1, buying_threshold=p1_threshold, group_ordering=p1_ordering, step_threshold=True)
        player2 = Player(2, buying_threshold=p2_threshold, group_ordering=p2_ordering, step_threshold=True)
        player3 = Player(3, buying_threshold=p3_threshold, group_ordering=p3_ordering, step_threshold=True)
        game0.new_players([player1, player2, player3])
        results = game0.play()

        if results['winner'] == 1:
            wins += 1

        p = wins / counter
        interval_size = 1.960 * math.sqrt((p * (1 - p)) / counter)

        # print(counter, p, interval_size)

    return p


def write_row(row):
    with open('results/hillClimb_blah.csv', 'a', newline='') as csvfile:
        output_file = csv.writer(csvfile, quotechar=',')
        output_file.writerow(row)


def hill_climb():
    while True:
        print('Start!')
        # write_row(["Start!"])
        counter = 0
        old_ordering = random_strategy()
        old_success = success(old_ordering)
        print(old_ordering, old_success)
        #write_row([old_ordering, old_success])

        all_neighbors = neighbors(old_ordering)

        while counter < (len(all_neighbors) - 1):
            new_ordering = all_neighbors[counter]
            new_success = success(new_ordering)

            counter += 1

            if new_success > old_success:
                old_ordering = new_ordering
                old_success = new_success
                print(old_ordering, old_success, counter)
                #write_row([old_ordering, old_success])

                all_neighbors = neighbors(old_ordering)
                counter = 0

        print('No better neighbors.')


def brute_force():
    groups = ["Brown", "Pink", "Red", "Yellow", "Green", "Dark Blue", "Utility"]

    all_orderings = itertools.permutations(groups)
    for addon in all_orderings:
        ordering = ["Railroad", "Orange", "Light Blue"]
        ordering.extend(addon)

        print(ordering, success(ordering))


def main():
    hill_climb()
    # brute_force()


main()
