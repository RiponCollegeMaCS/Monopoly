from success import *
import time  # Timer function
from copy import deepcopy

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


def find_n(length=0.05):
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


def simple_success_indicator(base_player, number_of_games):
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

    success_indicator = results_list.count(1) / number_of_games
    return success_indicator


def new_climb(steps=5000, set_length=100):
    # The initial player.
    old_player = Player(1, max_houses=5, jail_time=0, smart_jail_strategy=False,
                        complete_monopoly=False, buying_threshold=10, group_preferences=())

    # Find initial success indicator.
    old_success_rate = success_indicator(base_player=old_player, number_of_games=set_length, procs=2)
    print("initial success indicator:", old_success_rate)

    # Climb!
    for i in range(steps):
        neighbors = []

        if old_player.max_houses > 0:
            perturbed_player = deepcopy(old_player)
            perturbed_player.max_houses += -1
            neighbors.append(perturbed_player)

        if old_player.max_houses < 5:
            perturbed_player = deepcopy(old_player)
            perturbed_player.max_houses += 1
            neighbors.append(perturbed_player)

        if old_player.jail_time > 0:
            perturbed_player = deepcopy(old_player)
            perturbed_player.jail_time += -1
            neighbors.append(perturbed_player)

        if old_player.jail_time < 3:
            perturbed_player = deepcopy(old_player)
            perturbed_player.jail_time += 1
            neighbors.append(perturbed_player)

        if old_player.buying_threshold > 10:
            perturbed_player = deepcopy(old_player)
            perturbed_player.buying_threshold += -10
            neighbors.append(perturbed_player)

        if old_player.jail_time < 1000:
            perturbed_player = deepcopy(old_player)
            perturbed_player.buying_threshold += 10
            neighbors.append(perturbed_player)

        if old_player.smart_jail_strategy:
            perturbed_player = deepcopy(old_player)
            perturbed_player.smart_jail_strategy = False
            neighbors.append(perturbed_player)
        else:
            perturbed_player = deepcopy(old_player)
            perturbed_player.smart_jail_strategy = True
            neighbors.append(perturbed_player)

        if old_player.complete_monopoly:
            perturbed_player = deepcopy(old_player)
            perturbed_player.complete_monopoly = False
            neighbors.append(perturbed_player)
        else:
            perturbed_player = deepcopy(old_player)
            perturbed_player.complete_monopoly = True
            neighbors.append(perturbed_player)

        shuffle(neighbors)  # Randomize neighbor opponents.

        success_of_neighbors = []

        keep_going = True
        for neighbor in neighbors:
            while keep_going:
                new_success_rate = success_indicator(base_player=neighbor, number_of_games=set_length, procs=2)
                if new_success_rate > old_success_rate:
                    keep_going = False
                    print(new_success_rate, "(better)")
                    print("strategy parameters:", neighbor.max_houses, neighbor.jail_time, neighbor.smart_jail_strategy,
                          neighbor.complete_monopoly, neighbor.buying_threshold, neighbor.group_preferences)
                    old_player = neighbor
                    old_success_rate = new_success_rate
                else:
                    success_of_neighbors.append(new_success_rate)
                    if len(success_of_neighbors) == len(neighbors):
                        print("No neighbor is better.")


def hill_climb(steps=5000, set_length=5000):
    # The initial player.
    old_player = Player(1, max_houses=5, jail_time=0, smart_jail_strategy=False,
                        complete_monopoly=False, buying_threshold=1, group_preferences=())

    # Find initial success indicator.
    old_success_rate = simple_success_indicator(base_player=old_player, number_of_games=set_length)
    print(old_success_rate)

    # Climb!
    for i in range(steps):
        new_player = old_player  # Create a new player.

        try_again = True
        while try_again:
            random_selection = randint(1, 8)
            try_again = False

            if random_selection == 1:
                if old_player.max_houses > 0:
                    new_player.max_houses += -1
                else:
                    try_again = True

            elif random_selection == 2:
                if old_player.max_houses < 5:
                    new_player.max_houses += 1
                else:
                    try_again = True

            elif random_selection == 3:
                if old_player.jail_time > 0:
                    new_player.jail_time += -1
                else:
                    try_again = True

            elif random_selection == 4:
                if old_player.jail_time < 3:
                    new_player.jail_time += 1
                else:
                    try_again = True

            elif random_selection == 5:
                if old_player.smart_jail_strategy:
                    new_player.smart_jail_strategy = False
                else:
                    new_player.smart_jail_strategy = True

            elif random_selection == 6:
                if old_player.complete_monopoly:
                    new_player.complete_monopoly = False
                else:
                    new_player.complete_monopoly = True

            elif random_selection == 7:
                if old_player.buying_threshold > 10:
                    new_player.buying_threshold += -10
                else:
                    try_again = True

            elif random_selection == 8:
                if old_player.buying_threshold < 1000:
                    new_player.buying_threshold += 10
                else:
                    try_again = True

        new_success_rate = simple_success_indicator(base_player=new_player, number_of_games=set_length)

        if new_success_rate > old_success_rate:
            print(new_success_rate, "(better)")
            print(new_player.max_houses, new_player.jail_time, new_player.smart_jail_strategy,
                  new_player.complete_monopoly, new_player.buying_threshold, new_player.group_preferences)
            old_success_rate = new_success_rate
            old_player = new_player
        else:
            random_number = randint(1, 100)
            if random_number <= 5:
                print(new_success_rate, "(changing anyway)")
                print(new_player.max_houses, new_player.jail_time, new_player.smart_jail_strategy,
                      new_player.complete_monopoly, new_player.buying_threshold, new_player.group_preferences)
                old_success_rate = new_success_rate
                old_player = new_player
            else:
                print(new_success_rate, "(not better)")


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
    success_rate = success_indicator(base_player=grandma, number_of_games=1000, procs=2)
    print(success_rate)
    # find_n(length=0.01)


def new_function():
    grandma = Player(1, max_houses=5, jail_time=3, smart_jail_strategy=False, complete_monopoly=False,
                     buying_threshold=1000, group_preferences=("Brown", "Light Blue"))
    newbie = Player(2, max_houses=5, jail_time=3, smart_jail_strategy=False, complete_monopoly=False,
                    buying_threshold=500, group_preferences=("Green", "Dark Blue"))
    game_object = Game([grandma, newbie])
    print(game_object.play())


if __name__ == '__main__':
    timer()
    new_climb()
    timer()


def gma_test():
    grandma = Player(1, max_houses=3, jail_time=3, smart_jail_strategy=False, complete_monopoly=False,
                     buying_threshold=1000, group_preferences=("Brown", "Light Blue"))

    new_grandma = deepcopy(grandma)

    if grandma.max_houses < 5:
        new_grandma.max_houses += 1

    print(grandma.max_houses)

    print(new_grandma.max_houses)


'''
New hill climbing alorgirithm with random restart.
Finalize set players.
Analazye average number of different games.
Different rules = different strategy?
Use 'characters' and analyze under different groups of rules.
'''