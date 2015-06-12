import csv
from timer import *
from monopoly import *

def random_ordering():
    all_groups = ["Brown", "Light Blue", "Pink", "Orange",
                  "Red", "Yellow", "Green", "Dark Blue",
                  "Utility", "Railroad"]
    shuffle(all_groups)
    return tuple(all_groups)


def main():
    games_in_a_set = 1000
    cutoff = 1000
    length_matrix = []

    for i in range(games_in_a_set):
        # Play game.
        player1 = Player(1, group_ordering=random_ordering())
        player2 = Player(2,group_ordering=random_ordering())
        game0 = Game([player1, player2], cutoff=cutoff,
                     trading_enabled=True,
                     new_trading=True,
                     hotel_upgrade=False,
                     building_sellback=False,

                     free_parking_pool=False,
                     double_on_go=False,
                     no_rent_in_jail=False,
                     trip_to_start=False,
                     snake_eyes_bonus=False
        )
        results = game0.play()

        # Store length.
        length_matrix.append(results['length'])

    print(sum(length_matrix)/len(length_matrix))
    # Open file.
    with open('results/blah.csv', 'w', newline='') as csvfile:
        output_file = csv.writer(csvfile, quotechar=',')

        # Write to file.
        for i in range(1, cutoff):
            counter = 0
            for element in length_matrix:
                if element > i:
                    counter += 1

            output_file.writerow([counter / games_in_a_set])
            print(counter / games_in_a_set)


if __name__ == '__main__':
    timer()
    main()
    timer()