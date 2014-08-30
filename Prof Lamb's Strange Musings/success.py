from monopoly import *
from multiprocessing import *

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
    results_list = []
    for i in range(number_of_games):
        # Create players.
        player1 = base_player
        player1.reset_values()
        opponent = generate_random_opponent()  # The random opponent.

        # Play the game.
        current_game = Game([player1, opponent])  # Create the game.
        current_game_result = current_game.play()  # Play the game.
        results_list.append(current_game_result[0])  # Store the game's result.
    results_q.put(results_list.count(1))

def success_indicator(base_player, number_of_games=1000, procs=2):
    results_q = Queue() # Queue for results.
    proc_list = [Process(target=play_set, args=(base_player, int(number_of_games / procs), results_q)) for i in
                 range(procs)]  # List of processes.
    for proc in proc_list:  # Start all processes.
        proc.start()
    for proc in proc_list:  # Wait for all processes to finish.
        proc.join()
    results_list = []
    while results_q.empty() == False: #Gather the results from each process in a list of counts.
        results_list.append(results_q.get())
    success_rate = float(sum(results_list)) / float(number_of_games) # Success rate = total count / total number of games
    return success_rate

def simple_success_indicator(base_player, number_of_games=1000):
    results_list = []
    for i in range(number_of_games):
        # Create players.
        player1 = base_player
        player1.reset_values()
        opponent = generate_random_opponent()  # The random opponent.

        # Play the game.
        current_game = Game([player1, opponent])  # Create the game.
        current_game_result = current_game.play()  # Play the game.
        results_list.append(current_game_result[0])  # Store the game's result.
    success_rate = float(results_list.count(1)) / float(number_of_games)
    return success_rate