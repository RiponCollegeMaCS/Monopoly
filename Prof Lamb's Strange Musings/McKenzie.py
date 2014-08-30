from __future__ import division, print_function
from monopoly import *
import success
from multiprocessing import *
import time  # Timer function
import profile
import pstats



# Timer code.
timeList = []


def timer():
    timeList.append(time.time())
    if len(timeList) % 2 == 0:
        print('Time elapsed: ' + str(round(timeList[-1] - timeList[-2], 4)) + ' seconds.')
        timeList.pop()
        timeList.pop()


def ending_early():
    counter = 0
    for i in range(10000):
        base_player = Player(1, 100)  # The main player.
        opponent = Player(2, 100)  # The random opponent.

        # Play the game.
        current_game = Game([base_player, opponent])  # Create the game.
        current_game_results = current_game.play()  # Play the game.
        # print([current_game_results[0], current_game_results[2], current_game_results[1]])
        if current_game_results[0] == current_game_results[2] or current_game_results[1] < 300:
            counter += 1

    print(counter)


def test():
    grandma = Player(1, max_houses=5, jail_time=3, smart_jail_strategy=False, complete_monopoly=False,
                     buying_threshold=1000, group_preferences=("Brown", "Light Blue"))
    newbie = Player(1, max_houses=5, jail_time=3, smart_jail_strategy=False, complete_monopoly=False,
                    buying_threshold=500, group_preferences=("Green", "Dark Blue"))
    seasoned_competitor = Player(1, max_houses=3, jail_time=3, smart_jail_strategy=True, complete_monopoly=True,
                                 buying_threshold=150, group_preferences=("Orange", "Red"))
    seasoned_competitor_2 = Player(1, max_houses=3, jail_time=3, smart_jail_strategy=True, complete_monopoly=True,
                                 buying_threshold=150, group_preferences=("Orange", "Red"))
    super_aggressive = Player(1, max_houses=5, jail_time=0, smart_jail_strategy=False, complete_monopoly=False,
                              buying_threshold=1, group_preferences=())
    success_rate = success.simple_success_indicator(base_player=newbie, number_of_games=100)
    #success_rate = success.success_indicator(base_player=seasoned_competitor_2, number_of_games=100, procs=4)
    print(success_rate)
    #find_n(length=0.01)

def generate_confidence_interval():
    grandma = Player(1, max_houses=5, jail_time=3, smart_jail_strategy=False, complete_monopoly=False,
                     buying_threshold=1000, group_preferences=("Brown", "Light Blue"))
    newbie = Player(1, max_houses=5, jail_time=3, smart_jail_strategy=False, complete_monopoly=False,
                    buying_threshold=500, group_preferences=("Green", "Dark Blue"))
    seasoned_competitor = Player(1, max_houses=3, jail_time=3, smart_jail_strategy=True, complete_monopoly=True,
                                 buying_threshold=150, group_preferences=("Orange", "Red"))
    seasoned_competitor_2 = Player(1, max_houses=3, jail_time=3, smart_jail_strategy=True, complete_monopoly=True,
                                 buying_threshold=150, group_preferences=("Orange", "Red"))
    super_aggressive = Player(1, max_houses=5, jail_time=0, smart_jail_strategy=False, complete_monopoly=False,
                              buying_threshold=1, group_preferences=())
    #success_rate = success.simple_success_indicator(base_player=newbie, number_of_games=1000)
    for i in range(50):
        success_rate = success.success_indicator(base_player=seasoned_competitor_2, number_of_games=100, procs=4)
        print(success_rate)
    #find_n(length=0.01)

def basic_test():
    for i in range(100):
        grandma = Player(1, max_houses=5, jail_time=3, smart_jail_strategy=False, complete_monopoly=False,
                         buying_threshold=1000, group_preferences=("Brown", "Light Blue"))
        newbie = Player(2, max_houses=5, jail_time=3, smart_jail_strategy=False, complete_monopoly=False,
                        buying_threshold=500, group_preferences=("Green", "Dark Blue"))
        game_object = Game([grandma, newbie])
        game_object.play()
def random_generation_test():
    for i in range(1000):
        success.generate_random_opponent()


if __name__ == '__main__':
    #timer()
    #basic_test()
    profile.run('basic_test()', 'profile.tmp')
    p = pstats.Stats('profile.tmp')
    p.sort_stats('time').print_stats(50)
    #timer()


