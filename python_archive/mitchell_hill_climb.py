from success import *  # Success function.
from timer import timer  # Timer function
from copy import deepcopy  # deepcopy function to copy objects.


def find_n(length=0.05):
    n = 0

    s_squared = 0
    x_bar_old = 0
    for i in range(100):
        n += 1

        # Create players.
        base_player = Player(1)  # The main player.
        opponent = generate_random_player(2)  # The random opponent.

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
        opponent = generate_random_player(2)  # The random opponent.

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


def generate_neighbor_list(player):
    neighbors = []
    # Add neighbors to the list.
    if player.building_threshold > 0:
        perturbed_player = deepcopy(player)
        perturbed_player.building_threshold += -1
        neighbors.append(perturbed_player)

    if player.building_threshold < 5:
        perturbed_player = deepcopy(player)
        perturbed_player.building_threshold += 1
        neighbors.append(perturbed_player)

    if player.jail_time > 0:
        perturbed_player = deepcopy(player)
        perturbed_player.jail_time += -1
        neighbors.append(perturbed_player)

    if player.jail_time < 3:
        perturbed_player = deepcopy(player)
        perturbed_player.jail_time += 1
        neighbors.append(perturbed_player)

    if player.buying_threshold > 10:
        perturbed_player = deepcopy(player)
        perturbed_player.buying_threshold += -10
        neighbors.append(perturbed_player)

    if player.jail_time < 1000:
        perturbed_player = deepcopy(player)
        perturbed_player.buying_threshold += 10
        neighbors.append(perturbed_player)

    if player.smart_jail_strategy:
        perturbed_player = deepcopy(player)
        perturbed_player.smart_jail_strategy = False
        neighbors.append(perturbed_player)
    else:
        perturbed_player = deepcopy(player)
        perturbed_player.smart_jail_strategy = True
        neighbors.append(perturbed_player)

    if player.complete_monopoly:
        perturbed_player = deepcopy(player)
        perturbed_player.complete_monopoly = False
        neighbors.append(perturbed_player)
    else:
        perturbed_player = deepcopy(player)
        perturbed_player.complete_monopoly = True
        neighbors.append(perturbed_player)
    return neighbors


# Search through the graph of players for the best one.
def hill_climb(best_player, best_success_indicator, set_length=1000):
    # Generate initial random player.
    old_player = generate_random_player(1)
    old_player.group_preferences = ("orange", "red")

    print("Initial strategy parameters:", [old_player.building_threshold, old_player.jail_time, old_player.smart_jail_strategy,
                                           old_player.complete_monopoly, old_player.buying_threshold,
                                           old_player.group_preferences])

    # Find initial success indicator.
    old_success_rate = success_indicator(base_player=old_player, number_of_games=set_length, procs=4)
    print("Initial success indicator:", old_success_rate)

    if old_success_rate > best_success_indicator:
        best_player = old_player
        best_success_indicator = old_success_rate

    while 0 == 0:
        neighbors = generate_neighbor_list(old_player)  # Generate neighbors.
        shuffle(neighbors)  # Randomize neighbor opponents.

        # Cycle through neighbors.
        neighbor_counter = 0
        keep_checking_neighbors = True
        for neighbor in neighbors:
            while keep_checking_neighbors:
                # Find success indicator for neighbor.
                new_success_rate = success_indicator(base_player=neighbor, number_of_games=set_length, procs=4)

                # The neighbor does better.
                if new_success_rate > old_success_rate:
                    # Stop checking neighbors.
                    keep_checking_neighbors = False

                    # Print results.
                    print("Found better neighbor.")
                    print("New strategy parameters:",
                          [neighbor.building_threshold, neighbor.jail_time, neighbor.smart_jail_strategy,
                           neighbor.complete_monopoly, neighbor.buying_threshold, neighbor.group_preferences])
                    print("New success rate:", new_success_rate, "(better)")


                    # Archive as old player.
                    old_player = neighbor
                    old_success_rate = new_success_rate

                    # Check if this is the best player so far.
                    if new_success_rate > best_success_indicator:
                        best_player = neighbor
                        best_success_indicator = new_success_rate

                # The neighbor does not do better.
                else:
                    neighbor_counter += 1
                    # No neighbor is better.
                    if neighbor_counter == len(neighbors):
                        print("No neighbor is better. Restarting.")

                        # Stop this climb; random restart.
                        return [best_player, best_success_indicator]


def random_restart(restarts=1000, set_length=5000):
    # Initial best player.
    best_player = None
    best_success_indicator = 0

    print("Starting hill climb.")
    for i in range(restarts):
        print("-----------------------------")
        path_results = hill_climb(best_player, best_success_indicator, set_length)
        best_player = path_results[0]
        best_success_indicator = path_results[1]

    print("Done climbing.")
    print("Best success rate:", best_success_indicator)
    print("Best strategy parameters:", [best_player.building_threshold, best_player.jail_time, best_player.smart_jail_strategy,
                                        best_player.complete_monopoly, best_player.buying_threshold,
                                        best_player.group_preferences])



if __name__ == '__main__':
    timer()
    #random_restart(restarts=50, set_length=100)
    timer()

'''
New hill climbing alorgirithm with random restart. [DONE]
Finalize characters. [DONE]
Fix jail [DONE]
Making fund between turns. [DONE]
Analazye average number of turns in different games.
Different rules = different strategy?
Use 'characters' and analyze under different groups of rules.
'''
