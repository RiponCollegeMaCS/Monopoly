from success import *  # Success function.
from timer import timer  # Timer function
import csv  # The csv module to output results.


def threshold_brute_force(number_of_games=1000):
    with open('results/threshold_brute_force_with_trades_with_hotels_better_strategy.csv', 'w', newline='') as csvfile:
        output_file = csv.writer(csvfile, quotechar=',')
        for buying_threshold in range(0, 1001, 10):
            player = Player(1,
                            buying_threshold=buying_threshold,
                            building_threshold=5,
                            jail_time=0,
                            smart_jail_strategy=True,
                            complete_monopoly=1,
                            group_preferences=(),
                            development_threshold=2)
            success = success_indicator(base_player=player,procs=4,
                                        number_of_games=number_of_games)
            results = [success,
                       buying_threshold,
                       5,
                       0,
                       True,
                       1,
                       2,
                ()]
            print(results)
            output_file.writerow(results)




if __name__ == '__main__':
    timer()
    threshold_brute_force()
    timer()