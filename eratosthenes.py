from monopoly import *
from multiprocessing import *
import time  # Timer function

# Timer code.
timeList = []


def timer():
    timeList.append(time.time())
    if len(timeList) % 2 == 0:
        print('Time elapsed: ' + str(round(timeList[-1] - timeList[-2], 4)) + ' seconds.')
        timeList.pop()
        timeList.pop()


def generate_random_opponent():
    list_of_groups = ["Brown", "Light Blue", "Pink", "Orange", "Red", "Yellow", "Green", "Dark Blue",
                      "Railroad", "Utility"]

    player = Player(2, buying_threshold=randint(1, 1001),
                    max_houses=randint(3, 5),
                    jail_time=randint(0, 3),
                    smart_jail_strategy=choice([True, False]),
                    complete_monopoly=choice([True, False]),
                    group_preferences=sample(list_of_groups, choice([0, 1, 2, 3])))

    return player


def play_set(base_player, number_of_games, results_q):
    for i in range(number_of_games):
        # Create players.
        player1 = base_player
        player1.reset_values()
        opponent = generate_random_opponent()  # The random opponent.

        # Play the game.
        current_game = Game([player1, opponent])  # Create the game.
        current_game_result = current_game.play()  # Play the game.
        results_q.put(current_game_result[0])  # Store the game's result.


def success_indicator(base_player, number_of_games=1000, procs=2):
    q_list = [Queue() for i in range(procs)]  # List of Queues.  Process i will store its results in Queue i.
    if __name__ == '__main__':  # Technicality
        proc_list = [Process(target=play_set, args=(base_player, int(number_of_games / procs), q_list[i])) for i in
                     range(procs)]  # List of processes.
        for i in range(procs):  # Start all processes.
            proc_list[i].start()
        for i in range(procs):  # Wait for all processes to finish.
            proc_list[i].join()
        results_list = []
        for i in range(procs):  # Put all results from all processes together in a single list.
            while q_list[i].empty() == False:
                results_list.append(q_list[i].get())
        success_rate = results_list.count(1) / number_of_games  # Compute success rate as usual.
        return success_rate


# main
def main():
    grandma = Player(1, max_houses=5, jail_time=3, smart_jail_strategy=False, complete_monopoly=False,
                     buying_threshold=1000, group_preferences=("Brown", "Light Blue"))
    newbie = Player(1, max_houses=5, jail_time=3, smart_jail_strategy=False, complete_monopoly=False,
                    buying_threshold=500, group_preferences=("Green", "Dark Blue"))
    seasoned_competitor = Player(1, max_houses=3, jail_time=3, smart_jail_strategy=True, complete_monopoly=True,
                                 buying_threshold=150, group_preferences=("Orange", "Red"))
    super_aggressive = Player(1, max_houses=5, jail_time=0, smart_jail_strategy=False, complete_monopoly=False,
                              buying_threshold=1, group_preferences=())
    success_rate = success_indicator(base_player=grandma, number_of_games=10000, procs=2)
    print(success_rate)


timer()
main()
timer()


