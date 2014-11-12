from success import *  # Success function.
from timer import timer  # Timer function
import csv  # The csv module to output results.


def brute_force(number_of_games=10000):
    with open('brute_force000.csv', 'w', newline='') as csvfile:
        output_file = csv.writer(csvfile, quotechar=',')

        list_of_preferences = [(), ("Brown", "Light Blue"), ("Pink", "Orange"), ("Red", "Yellow"),
                                   ("Green", "Dark Blue")]

        for buying_threshold in range(100, 501, 100):
            for building_threshold in [0, 1, 2, 3, 4, 5]:
                for jail_time in [0, 1, 2, 3]:
                    for smart_jail_strategy in [True, False]:
                        for complete_monopoly in [0, 1, 2]:
                            for development_threshold in [0, 1, 2]:
                                for group_preferences in list_of_preferences:
                                    player = Player(1,
                                                    buying_threshold=buying_threshold,
                                                    building_threshold=building_threshold,
                                                    jail_time=jail_time,
                                                    smart_jail_strategy=smart_jail_strategy,
                                                    complete_monopoly=complete_monopoly,
                                                    group_preferences=group_preferences,
                                                    development_threshold=development_threshold)
                                    success = success_indicator(base_player=player,
                                                                number_of_games=number_of_games,
                                                                procs=4)
                                    results = [success,
                                               buying_threshold,
                                               building_threshold,
                                               jail_time,
                                               smart_jail_strategy,
                                               complete_monopoly,
                                               development_threshold,
                                               group_preferences]
                                    print(results)
                                    output_file.writerow(results)


def short_brute_force(number_of_games=10000):
    with open('brute_force000.csv', 'w', newline='') as csvfile:
        output_file = csv.writer(csvfile, quotechar=',')
        for buying_threshold in range(100, 501, 100):
            for jail_time in [0, 1, 2, 3]:
                for smart_jail_strategy in [True, False]:
                    for complete_monopoly in [0, 1, 2]:
                        for development_threshold in [0, 1, 2]:
                            player = Player(1,
                                            buying_threshold=buying_threshold,
                                            building_threshold=5,
                                            jail_time=jail_time,
                                            smart_jail_strategy=smart_jail_strategy,
                                            complete_monopoly=complete_monopoly,
                                            group_preferences=(),
                                            development_threshold=development_threshold)
                            success = success_indicator(base_player=player,procs=4,
                                                        number_of_games=number_of_games)
                            results = [success,
                                       buying_threshold,
                                       5,
                                       jail_time,
                                       smart_jail_strategy,
                                       complete_monopoly,
                                       development_threshold,
                                ()]
                            print(results)
                            output_file.writerow(results)


if __name__ == '__main__':
    timer()
    short_brute_force()
    timer()