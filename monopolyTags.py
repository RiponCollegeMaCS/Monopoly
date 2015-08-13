import mb as monopoly
import math
from random import shuffle, randint


def random_ordering():
    all_groups = ["Brown", "Light Blue", "Pink", "Orange",
                  "Red", "Yellow", "Green", "Dark Blue",
                  "Utility", "Railroad"]
    shuffle(all_groups)
    return tuple(all_groups)


def best_ordering():
    other_groups = ["Pink", "Red",
                    "Yellow", "Green",
                    "Dark Blue", "Utility", "Brown"]
    shuffle(other_groups)

    return tuple(["Railroad", "Light Blue", "Orange"] + other_groups)


def main():
    game0 = monopoly.Game(cutoff=1000, trading_enabled=False, record_predicted_winners=True)

    base_games = 100
    counter = 0
    winners = [0, 0, 0]
    interval_size = 10
    matching_counter = 0
    monopolies_formed_counter = 0
    formation_times = []
    prediction = [0] * 100
    turn_prediction = [0] * 1000
    turn_counter_list = [0] * 1000

    while (counter < base_games) or interval_size > 0.01:
        counter += 1
        # Play game.
        player1 = monopoly.Player(1, buying_threshold=100)
        # group_ordering=random_ordering())
        player2 = monopoly.Player(2, buying_threshold=100)
        # group_ordering=random_ordering())

        game0.new_players([player1, player2])
        results = game0.play()

        winners[results['winner']] += 1
        p = winners[1] / counter
        interval_size = 1.960 * math.sqrt((p * (1 - p)) / counter)


        # It was not a tie.
        if results['winner'] != 0:

            for percent in range(1, 101):
                index = round((percent / 100) * results['length'])
                if game0.predicted_winners[index - 1] == results['winner']:
                    prediction[percent - 1] += 1

            for turn in range(results['length']):
                turn_counter_list[turn] += 1
                if game0.predicted_winners[turn] == results['winner']:
                    turn_prediction[turn] += 1

            # If monopolies formed see if the winner got the first one.
            if game0.first_monopoly:
                monopolies_formed_counter += 1
                if game0.first_monopoly == results['winner']:
                    matching_counter += 1

                    # if results['winning_player'].monopoly_tags:
                    # proportion = results['winning_player'].monopoly_tags[0] / results['length']
                    # formation_times.append(proportion)

    print("*" * 10)

    # finite_games = winners[1] + winners[2]
    # for element in prediction:
    # print(element / finite_games)

    print("*" * 10)

    for i in range(1000):
        if turn_counter_list[i] > 0:
            print(turn_prediction[i] / turn_counter_list[i])
        else:
            print(0)

    print("*" * 10)

    print("games played:", counter)
    print("win %s:", winners[0] / counter, winners[1] / counter, winners[2] / counter)
    print("winner had first monopoly:", matching_counter / monopolies_formed_counter, "of", monopolies_formed_counter,
          "games")


main()