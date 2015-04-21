import csv
from timer import *
from monopoly import *


def main():
    games_in_a_set = 100
    house_rules = ["Control", "Frozen Assets", "Dash for the Cash", "See the Sights", "Free Parking Fast Cash",
                   "Lucky Roller",
                   "All"]
    all_length_lists = []
    hotel_upgrade = False
    trading_enabled = False

    for rule in house_rules:
        length_list = []
        with open('results/house_rules/000000' + rule + '.csv', 'w', newline='') as csvfile002:
            output_file002 = csv.writer(csvfile002, quotechar=',')

            for i in range(games_in_a_set):
                player1 = Player(1)
                player2 = Player(2)

                # Play game.
                if rule == "Control":
                    game0 = Game([player1, player2], cutoff=1000, trading_enabled=trading_enabled,
                                 hotel_upgrade=hotel_upgrade)
                elif rule == "Frozen Assets":
                    game0 = Game([player1, player2], cutoff=1000, trading_enabled=trading_enabled,
                                 hotel_upgrade=hotel_upgrade, no_rent_in_jail=True)
                elif rule == "Dash for the Cash":
                    game0 = Game([player1, player2], cutoff=1000, trading_enabled=trading_enabled,
                                 hotel_upgrade=hotel_upgrade, double_on_go=True)
                elif rule == "See the Sights":
                    game0 = Game([player1, player2], cutoff=1000, trading_enabled=trading_enabled,
                                 hotel_upgrade=hotel_upgrade, trip_to_start=True)
                elif rule == "Free Parking, Fast Cash":
                    game0 = Game([player1, player2], cutoff=1000, trading_enabled=trading_enabled,
                                 hotel_upgrade=hotel_upgrade, free_parking_pool=True)
                elif rule == "Lucky Roller":
                    game0 = Game([player1, player2], cutoff=1000, trading_enabled=trading_enabled,
                                 hotel_upgrade=hotel_upgrade, snake_eyes_bonus=True)
                else:
                    game0 = Game([player1, player2], cutoff=1000, trading_enabled=trading_enabled,
                                 hotel_upgrade=hotel_upgrade,
                                 free_parking_pool=True,
                                 double_on_go=True,
                                 no_rent_in_jail=True,
                                 trip_to_start=True,
                                 snake_eyes_bonus=True)

                results = game0.play()
                length_list.append(results['length'])

                # Write to file.
                output_file002.writerow([results['started'], results['winner'], results['length']])

        all_length_lists.append(length_list)
        print("Done with", rule)

    with open('results/house_rules/all_data.csv', 'w', newline='') as csvfile001:
        output_file001 = csv.writer(csvfile001, quotechar=',')

        output_file001.writerow(house_rules)

        for i in range(games_in_a_set):
            row = []
            for length_list in all_length_lists:
                row.append(length_list[i])
            output_file001.writerow(row)

    print('done')


if __name__ == '__main__':
    timer()
    main()
    timer()