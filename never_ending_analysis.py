# Import various commands
import csv
from timer import *
from monopoly import *


def main():
    test_results = [[],[]]
    with open('results/with_trades/games_that_do_not_end/results_table.csv', "rt") as f:
        reader = csv.reader(f)
        for i in reader:
            test_results[0].append(i[0].split(';'))
            test_results[1].append(i[1].split(';'))

        print(test_results)


if __name__ == '__main__':
    timer()
    main()
    timer()