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


# Search through the graph of players for the best one.
def hill_climb(steps=1000, set_length=100):
    # Define the initial player.
    old_player = Player(1, max_houses=5, jail_time=0, smart_jail_strategy=False,
                        complete_monopoly=False, buying_threshold=10, group_preferences=())

    print("Initial strategy parameters:", [old_player.max_houses, old_player.jail_time, old_player.smart_jail_strategy,
                                           old_player.complete_monopoly, old_player.buying_threshold,
                                           old_player.group_preferences])

    # Find initial success indicator.
    old_success_rate = success_indicator(base_player=old_player, number_of_games=set_length, procs=4)
    print("Initial success indicator:", old_success_rate)

    # Climb!
    for i in range(steps):
        neighbors = []  # Create a list to store neighbors in.

        # Add neighbors to the list.
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

        neighbor_counter = 0

        # Cycle through neighbors.
        keep_going = True
        for neighbor in neighbors:
            while keep_going:
                # Find success indicator for neighbor.
                new_success_rate = success_indicator(base_player=neighbor, number_of_games=set_length, procs=4)

                # The neighbor does better.
                if new_success_rate > old_success_rate:
                    keep_going = False
                    print(new_success_rate, "(better)")
                    print("New strategy parameters:",
                          [neighbor.max_houses, neighbor.jail_time, neighbor.smart_jail_strategy,
                           neighbor.complete_monopoly, neighbor.buying_threshold, neighbor.group_preferences])
                    old_player = neighbor
                    old_success_rate = new_success_rate

                # The neighbor does not do better.
                else:
                    neighbor_counter += 1
                    neighbor.success_indicator = new_success_rate  # Store success indicator.

                    # No neighbor is better.
                    if neighbor_counter == len(neighbors):
                        print("No neighbor is better. Moving to best neighbor.")

                        # Find the best neighbor.
                        sorted_neighbors = sorted(neighbors, key=lambda x: x.success_indicator, reverse=True)
                        best_neighbor = sorted_neighbors[0]
                        print("Best neighbor's success indicator:", best_neighbor.success_indicator)
                        print("Best neighbor's strategy parameters:",
                              [best_neighbor.max_houses, best_neighbor.jail_time, best_neighbor.smart_jail_strategy,
                               best_neighbor.complete_monopoly, best_neighbor.buying_threshold,
                               best_neighbor.group_preferences])
                        old_player = best_neighbor
                        old_success_rate = best_neighbor.success_indicator


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
    success_rate = success_indicator(base_player=grandma, number_of_games=1000, procs=4)
    '''game_object = Game([grandma, newbie])
    print(game_object.play())'''
    print(success_rate)
    # find_n(length=0.01)


if __name__ == '__main__':
    timer()
    for i in range(10):
        print("Starting hill climb.")
        hill_climb(steps=100, set_length=1000)
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