# Import various commands
import csv
from timer import *
from monopoly import *
from row_reduction import *


def main():
    run_id = 0

    with open('results/with_trades/games_that_do_not_end/weights/weights_new001.csv', 'w', newline='') as csvfile:
        output_file4 = csv.writer(csvfile, quotechar=',')

        # Tracking total number of trials.
        while run_id < 100:
            matrix = []
            main_counter = 0
            all_rows = []

            # Individual trial.
            while main_counter < 8:
                # Play game.
                player1 = Player(1)
                player2 = Player(2)
                game0 = Game([player1, player2], cutoff=1000, trading_enabled=True)
                results = game0.play()

                # Investigate further if there is a tie.
                if results['winner'] == 0:
                    # Convert group name to number.
                    group_numbers = {'Brown': 0, 'Light Blue': 1, 'Pink': 2, 'Orange': 3,
                                     'Red': 4, 'Yellow': 5, 'Green': 6, 'Dark Blue': 7,
                                     'Railroad': 8, 'Utility': 9}
                    group_caps = [2, 3, 3, 3, 3, 3, 3, 2, 4, 2]

                    # The coefficients for the current matrix row.
                    coefficients = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

                    # Add in coefficients.
                    '''for property in results['players'][0].inventory:
                        coefficients[group_numbers[property.group]] += 1

                    for index,element in enumerate(coefficients):
                        if element != group_caps[index]:
                            coefficients[index] = 0

                    for property in results['players'][1].inventory:
                        coefficients[group_numbers[property.group]] -= 1

                    for index,element in enumerate(coefficients):
                        if element != -group_caps[index]:
                            coefficients[index] = 0

                    coefficients.pop()
                    coefficients.pop()'''

                    for group in results['players'][0].monopolies:
                        if coefficients[group_numbers[group]] == 0:
                            coefficients[group_numbers[group]] += 1

                    for group in results['players'][1].monopolies:
                        if coefficients[group_numbers[group]] == 0:
                            coefficients[group_numbers[group]] -= 1

                    if coefficients in all_rows:
                        print('repeat')
                    else:
                        all_rows.append(coefficients)

                        # Add the constant.
                        total_money = results['players'][0].money + results['players'][1].money
                        coefficients.append((results['players'][0].money - results['players'][1].money) / total_money)

                        matrix.append(coefficients)
                        print(coefficients)
                        main_counter += 1

            # Row reduce matrix.
            toReducedRowEchelonForm(matrix)
            result_row = []
            for element in matrix:
                result_row.append(element[-1])
            print(matrix)

            output_file4.writerow(result_row)
            print(result_row)

            run_id += 1


if __name__ == '__main__':
    timer()
    main()
    timer()