# Import various commands
import csv
from timer import *
from monopoly import *
from row_reduction import *


def main():
    main_counter = 0
    all_sets = []
    with open('results/with_trades/games_that_do_not_end/list002.csv', 'w', newline='') as csvfile:
        output_file4 = csv.writer(csvfile, quotechar=',')

        # Individual trial.
        while main_counter < 5000:
            # Play game.
            player1 = Player(1)
            player2 = Player(2)
            game0 = Game([player1, player2], cutoff=1000, trading_enabled=True)
            results = game0.play()

            # Investigate further if there is a tie.
            if results['winner'] == 0:
                inventory = [[],[]]

                for element in results['players'][0].inventory:
                    inventory[0].append(element.id)
                inventory[0].sort()

                for element in results['players'][1].inventory:
                    inventory[1].append(element.id)
                inventory[1].sort()

                p1_string = ""
                for element in inventory[0]:
                    p1_string += str(element)
                    p1_string += ";"

                p2_string = ""
                for element in  inventory[1]:
                    p2_string += str(element)
                    p2_string += ";"

                write_me = [p1_string, p2_string, results['players'][0].money, results['players'][1].money]

                if inventory[0] in all_sets or inventory[1] in all_sets:
                    print('repeat')
                    write_me.append("Repeat")

                all_sets.append(inventory[0])
                all_sets.append(inventory[1])

                print(write_me)
                output_file4.writerow(write_me)
                main_counter += 1


if __name__ == '__main__':
    timer()
    main()
    timer()