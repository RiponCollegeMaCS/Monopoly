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
                for jail_time in [0, 1, 3]:
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
    with open('results/brute_force_with_trades_and_hotels.csv', 'w', newline='') as csvfile:
        output_file = csv.writer(csvfile, quotechar=',')
        for buying_threshold in range(100, 501, 100):
            for jail_time in [0, 1, 3]:
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

def long_brute_force(number_of_games=10000):
    with open('results/long_brute_force_with_trades2.csv', 'w', newline='') as csvfile:
        output_file = csv.writer(csvfile, quotechar=',')
        for buying_threshold in range(520, 1001, 20):
            for jail_time in [0, 3]:
                for complete_monopoly in [0, 1, 2]:
                    for development_threshold in [0, 1, 2]:
                        player = Player(1,
                                        buying_threshold=buying_threshold,
                                        building_threshold=5,
                                        jail_time=jail_time,
                                        smart_jail_strategy=False,
                                        complete_monopoly=complete_monopoly,
                                        group_preferences=(),
                                        development_threshold=development_threshold)
                        success = success_indicator(base_player=player,procs=4,
                                                    number_of_games=number_of_games)
                        results = [success,
                                   buying_threshold,
                                   5,
                                   jail_time,
                                   False,
                                   complete_monopoly,
                                   development_threshold,
                            ()]
                        print(results)
                        output_file.writerow(results)

def threshold_brute_force(number_of_games=10000):
    with open('results/threshold_brute_force_with_trades_better_strategy2.csv', 'w', newline='') as csvfile:
        output_file = csv.writer(csvfile, quotechar=',')
        for buying_threshold in range(510, 1001, 10):
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


def characters():
    grandma = Player(1, buying_threshold=1000, building_threshold=5, jail_time=3, smart_jail_strategy=False,
                     complete_monopoly=0, group_preferences=(), development_threshold=0)
    aggressive = Player(1, buying_threshold=1, building_threshold=5, jail_time=0, smart_jail_strategy=False,
                        complete_monopoly=2, group_preferences=(), development_threshold=2)
    competitor = Player(1, buying_threshold=150, building_threshold=5, jail_time=0, smart_jail_strategy=True,
                        complete_monopoly=1, group_preferences=(), development_threshold=1)
    newbie = Player(1, buying_threshold=500, building_threshold=5, jail_time=3, smart_jail_strategy=False,
                    complete_monopoly=0, group_preferences=(), development_threshold=0)
    good  = Player(1, buying_threshold=740, building_threshold=5, jail_time=3, smart_jail_strategy=False,
                    complete_monopoly=1, group_preferences=(), development_threshold=1)
    for i in range(80):
        print(success_indicator(competitor, procs=4, number_of_games=10000))



if __name__ == '__main__':
    timer()
    short_brute_force()
    timer()