from success import *
from timer import timer
import csv  # The csv module to output results.


def generate_random_player_ALT(number):
    player = Player(number, buying_threshold=100,#randint(1, 500),
                    building_threshold=5,#choice([2, 3, 4, 5]),
                    development_threshold=choice([0, 1, 2]),
                    complete_monopoly=choice([0, 1, 2]),
                    jail_time=choice([0, 1, 2, 3]),
                    smart_jail_strategy=choice([True, False]),
                    group_preferences=())

    return player


# def players():
# grandma = Player(2, building_threshold=5, jail_time=3, smart_jail_strategy=False, complete_monopoly=2,
# buying_threshold=1000, group_preferences=("Brown", "Light Blue"), development_threshold=2)
# '''newbie = Player(2, building_threshold=5, jail_time=3, smart_jail_strategy=False, complete_monopoly=0,
# buying_threshold=500, group_preferences=("Green", "Dark Blue"))
# seasoned_competitor = Player(1, building_threshold=3, jail_time=3, smart_jail_strategy=True, complete_monopoly=1,
#                                  buying_threshold=150, group_preferences=("Orange", "Red"))
#     super_aggressive = Player(1, building_threshold=5, jail_time=0, smart_jail_strategy=False, complete_monopoly=2,
#                               buying_threshold=1, group_preferences=())'''
#
#     good_player = Player(1, building_threshold=5, jail_time=0, smart_jail_strategy=True, complete_monopoly=1,
#                          buying_threshold=100, group_preferences=(), development_threshold=1)
#     '''    grandma = Player(2, building_threshold=5, jail_time=3, smart_jail_strategy=False, complete_monopoly=0,
#                      buying_threshold=1000, group_preferences=(), development_threshold=0)
#     good_player = Player(1, building_threshold=5, jail_time=0, smart_jail_strategy=True, complete_monopoly=2,
#                          buying_threshold=100, group_preferences=(), development_threshold=2)'''
#     for i in range(20):
#         success_rate = success_indicator(base_player=good_player, static_opponent=grandma, number_of_games=1000,
#                                          procs=4)
#         print(success_rate)


def main():
    good_player1 = Player(1, building_threshold=5, jail_time=0, smart_jail_strategy=True, complete_monopoly=1,
                          buying_threshold=100, group_preferences=(), development_threshold=1)
    grandma = Player(2, building_threshold=5, jail_time=3, smart_jail_strategy=False, complete_monopoly=0,
                     buying_threshold=1000, group_preferences=(), development_threshold=0)

    number_of_games = 1000
    results_list = []

    for i in range(number_of_games):
        player1 = good_player1  # generate_random_player(1)
        player1.reset_values()
        player2 = generate_random_player(2)
        player2.reset_values()
        game_object = Game([player1, player2], cutoff=1000)
        result = game_object.play()
        results_list.append(result[0])

    print(results_list.count(1) * 100 / len(results_list), "%")
    # print("player", result[0], "won")
    # if result[1] == 1000:

    # results_list.append(result[0])
    # print(len(results_list))

    # print((sum(results_list) / len(results_list)))

    # success_rate = success_indicator(base_player=grandma1, static_opponent=grandma2, number_of_games=5000, procs=4)
    # print(success_rate)


def monopoly_test():
    player1 = Player(1, building_threshold=5, jail_time=3, smart_jail_strategy=False, complete_monopoly=0,
                     buying_threshold=1000, group_preferences=(), development_threshold=0)
    player2 = Player(2, building_threshold=5, jail_time=3, smart_jail_strategy=False, complete_monopoly=0,
                     buying_threshold=1000, group_preferences=(), development_threshold=0)

    ended_early_no_monopolies = 0
    finished_games_with_no_monopolies = 0
    results = []

    with open('results1.csv', 'w', newline='') as csvfile:
        output_file = csv.writer(csvfile, quotechar=',')

        for i in range(1000):
            monopolies = []
            player1 = generate_random_player_ALT(1)
            player1.reset_values()
            player2 = generate_random_player_ALT(2)
            player2.reset_values()
            game_object = Game([player1, player2], cutoff=1000, auctions_enabled=True)
            result = game_object.play()
            monopolies.extend(result[2])
            monopolies.extend(result[3])


            results.append(result[0])
            #print("player",result[0],"won")

            if result[0] == 0:
                if monopolies == [] or monopolies == ["Brown"]:
                    ended_early_no_monopolies += 1
                else:
                    print("resultant monos:",result[2], result[3], result[4], result[5])



            if result[0] != 0:
                if monopolies == [] or monopolies == ["Brown"]:
                    finished_games_with_no_monopolies += 1




                    # output_file.writerow(result)

    print("ended early:", results.count(0))
    print("ended early & no monopolies or just brown:", ended_early_no_monopolies)
    print("finished_games_with_no_monopolies:", finished_games_with_no_monopolies)


if __name__ == '__main__':
    timer()
    monopoly_test()
    timer()
