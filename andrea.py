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


def play_current_game_series(strategy, number_of_games=1000):
    current_game_series_results = []
    for i in range(number_of_games):
        # Create players.
        base_player = Player(1, strategy)  # The main player.
        opponent = Player(2, randint(1, 1000))  # The random opponent.

        # Play the game.
        current_game = Game([base_player, opponent])  # Create the game.
        current_game_results = current_game.play()  # Play the game.
        current_game_series_results.append(current_game_results[0])  # Store the game's result.

    success_indicator = current_game_series_results.count(1) / number_of_games
    return success_indicator


def one_dim_climb():
    perturbations = [-5, 5]  # Possible perturbations.

    old_strategy = 100
    old_success_indicator = play_current_game_series(old_strategy)

    for series in range(100):
        new_strategy = old_strategy + choice(perturbations)

        # Play series of games.
        new_success_indicator = play_current_game_series(new_strategy)

        # Print pair.
        print([new_strategy, new_success_indicator])

        if new_success_indicator > old_success_indicator:
            old_strategy = new_strategy
            old_success_indicator = new_success_indicator


def play_game_series(number_of_games=1000, leap=50):
    print("Playing...")

    for player1_threshold in range(leap, 1001, leap):
        for player2_threshold in range(leap, 1001, leap):
            results_list = []
            length_list = []
            for i in range(number_of_games):
                player1 = Player(1, player1_threshold)
                player2 = Player(2, player2_threshold)
                current_game = Game(list_of_players=[player1, player2])
                current_game_results = current_game.play()
                results_list.append(current_game_results[0])
                length_list.append(current_game_results[1])

            success_indicator = results_list.count(1) / number_of_games
            print([player1_threshold, player2_threshold, success_indicator, sum(length_list) / len(length_list)])


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


def find_n(length = 0.05):
    n = 0

    s_squared = 0
    x_bar_old = 0
    for i in range(100):
        n += 1

        # Create players.
        base_player = Player(1)  # The main player.
        opponent = generate_random_opponent()  # The random opponent.

        # Play the game.
        current_game = Game([base_player, opponent])  # Create the game.
        current_game_results = current_game.play()  # Play the game.

        if i == 1:
            x_bar_old = current_game_results[0]

        if i > 1:
            x_bar_new = x_bar_old + ((current_game_results[0] - x_bar_old) / n)
            s_squared = ((1 - (1 / (n - 1))) * s_squared) + (n * (pow(x_bar_new - x_bar_old, 2)))
            x_bar_old = x_bar_new

    while 0 == 0:
        n += 1
        # Create players.
        base_player = Player(1)  # The main player.
        opponent = generate_random_opponent()  # The random opponent.

        # Play the game.
        current_game = Game([base_player, opponent])  # Create the game.
        current_game_results = current_game.play()  # Play the game.

        x_bar_new = x_bar_old + ((current_game_results[0] - x_bar_old) / n)
        s_squared = ((1 - (1 / (n - 1))) * s_squared) + (n * (pow(x_bar_new - x_bar_old, 2)))
        x_bar_old = x_bar_new

        test_number = (2 * 1.960 * pow(s_squared, 0.5) * pow(n, -0.5))
        print([n, test_number])

        if test_number < length:
            print('done:', n)
            a = input('pause')
            return


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


def test_proc():
    number_of_games = 1000
    winner_list = []
    for i in range(number_of_games):
        player1 = Player(1, max_houses=3, jail_time=3,
                         smart_jail_strategy=True, complete_monopoly=True, buying_threshold=100,
                         group_preferences=("Orange", "Red"))
        player2 = Player(2, max_houses=5, jail_time=3,
                         smart_jail_strategy=False, complete_monopoly=False, buying_threshold=500,
                         group_preferences=())
        game_object = Game([player1, player2])
        results = game_object.play()
        winner_list.append(results[0])

    print(winner_list.count(1) / number_of_games)



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
    success_rate = success_indicator(base_player=seasoned_competitor, number_of_games=10000, procs=4)
    print(success_rate)
    #find_n(length=0.01)


def new_function():
    grandma = Player(1, max_houses=5, jail_time=3, smart_jail_strategy=False, complete_monopoly=False,
                     buying_threshold=1000, group_preferences=("Brown", "Light Blue"))
    newbie = Player(2, max_houses=5, jail_time=3, smart_jail_strategy=False, complete_monopoly=False,
                    buying_threshold=500, group_preferences=("Green", "Dark Blue"))
    game_object = Game([grandma, newbie])
    print(game_object.play())


timer()
main()
timer()


