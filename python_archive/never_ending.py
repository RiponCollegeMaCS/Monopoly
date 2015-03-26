# Import various commands
import csv
from timer import *
from monopoly import *


def main():
    total_games = 0
    winner_matrix = [0, 0, 0]
    length_matrix = []
    never_ending_counter = 0
    inventory_record = []
    all_percents = []
    main_counter = 0

    with open('results/with_trades/games_that_do_not_end/results_table.csv', 'w', newline='') as csvfile:
        output_file4 = csv.writer(csvfile, quotechar=',')

        with open('results/with_trades/games_that_do_not_end/with_trades.csv', 'w', newline='') as csvfile:
            output_file0 = csv.writer(csvfile, quotechar=',')

            while main_counter < 100:
                player1 = Player(1)
                player2 = Player(2)

                # Play game.
                game0 = Game([player1, player2], cutoff=1000, trading_enabled=True)
                results = game0.play()
                total_games += 1

                # Store info.
                winner_matrix[results['winner']] += 1
                length_matrix.append(results['length'])

                # Write to file.
                output_file0.writerow([results['started'], results['winner'], results['length']])

                # Investigate further if there is a tie.
                if results['winner'] == 0:
                    main_counter += 1

                    # Find the player's properties.
                    properties = [[],[]]
                    for property in results['players'][0].inventory:
                        properties[0].append(property.id)
                    for property in results['players'][1].inventory:
                        properties[1].append(property.id)

                    properties[0].sort()
                    properties[1].sort()
                    properties.sort()

                    if properties[0] in inventory_record or properties[1] in inventory_record:
                        print('duplicate')
                    else:
                        never_ending_counter += 1
                        inventory_record.append(properties[0])
                        inventory_record.append(properties[1])

                        print(properties[0], properties[1])

                        # Store money changes in a file.
                        with open('results/with_trades/games_that_do_not_end/money_changes' + str(
                                never_ending_counter) + '.csv', 'w', newline='') as csvfile:
                            output_file1 = csv.writer(csvfile, quotechar=',')
                            goto = min(len(results['players'][0].money_changes), len(results['players'][1].money_changes))
                            for i in range(goto):
                                output_file1.writerow([results['players'][0].money_changes[i],
                                                       results['players'][1].money_changes[i]])

                        game_lengths = []
                        with open('results/with_trades/games_that_do_not_end/test' + str(never_ending_counter) + '.csv',
                                  'w', newline='') as csvfile:
                            output_file2 = csv.writer(csvfile, quotechar=',')

                            for i in range(1000):
                                player1 = Player(1, initial_inventory=properties[0])
                                player2 = Player(2, initial_inventory=properties[1])

                                # Play game.
                                game0 = Game([player1, player2], cutoff=1000, trading_enabled=True)
                                results = game0.play()

                                # Save results.
                                game_lengths.append(results['length'])

                                # Write to file.
                                output_file2.writerow([results['started'], results['winner'], results['length']])

                        percents = []
                        for i in range(1, 1001):
                            counter = 0
                            for element in game_lengths:
                                if element < i:
                                    counter += 1
                            percents.append(1 - (counter / 1000))
                        all_percents.append(percents)

                        p1_string = ""
                        for element in properties[0]:
                            p1_string += str(element)
                            p1_string += ";"

                        p2_string = ""
                        for element in properties[1]:
                            p2_string += str(element)
                            p2_string += ";"

                        output_file4.writerow([p1_string, str(p2_string), len(properties[0]),len(properties[1]), percents[-1]])

    with open('results/with_trades/games_that_do_not_end/graph.csv', 'w', newline='') as csvfile:
        output_file3 = csv.writer(csvfile, quotechar=',')
        # Write to file.
        zipped_percents = zip(*all_percents)
        for element in zipped_percents:
            output_file3.writerow(element)

    # Print out winners (The ith slot represents the ith person's wins; 0=tie).
    print('winner_matrix', winner_matrix)
    # Print out average game length.
    print('average length', sum(length_matrix) / total_games)

if __name__ == '__main__':
    timer()
    main()
    timer()