import csv
from timer import *
from success import *
from monopoly import *


def main():
    games_in_a_set = 10000
    ending_reason = {}
    winner_matrix = [0, 0, 0]
    length_matrix = []
    didnotend = 0
    didend = 0

    with open('results/all_house_rules.csv', 'w', newline='') as csvfile:
        output_file = csv.writer(csvfile, quotechar=',')

        for i in range(games_in_a_set):
            player1 = Player(1, buying_threshold=500,
                             jail_time=3,
                             smart_jail_strategy=False,
                             complete_monopoly=0,
                             development_threshold=0,
                             group_preferences=(),
                             building_threshold=5,
            )
            player2 = Player(2, buying_threshold=500,
                             jail_time=3,
                             smart_jail_strategy=False,
                             complete_monopoly=0,
                             development_threshold=0,
                             group_preferences=(),
                             building_threshold=5,
            )
            # Play game.
            game0 = Game([player1, player2],
                         cutoff=1000,
                         auctions_enabled=True,
                         free_parking_pool=True,
                         double_on_go=True,
                         no_rent_in_jail=True,
                         trip_to_start=True,
                         snake_eyes_bonus=True,
                         )
            results = game0.play()

            # Store winner.
            winner_matrix[results['winner']] += 1

            # Store length.
            length_matrix.append(results['length'])

            # Store how the game ended in a dictionary.
            entry_name = results['end behavior']
            if results['monopolies'] == ['Brown'] or results['monopolies'] == []:
                if results['winner'] == 0:
                    didnotend += 1
                else:
                    didend += 1

            if entry_name in ending_reason:
                ending_reason[entry_name] += 1
            else:
                ending_reason[entry_name] = 1

            # Write to file.
            output_file.writerow([results['winner'], results['length']])

    # Print out ways that the games ended.
    for i, j in ending_reason.items():
        print(i, ";", j)

    # Print out what happened when no monopolies formed (or just brown)
    print('didend', didend)
    print('didnotend', didnotend)

    # Print out winners (The ith slot represents the ith person's wins; 0=tie).
    print('winner_matrix', winner_matrix)


if __name__ == '__main__':
    timer()
    main()
    timer()