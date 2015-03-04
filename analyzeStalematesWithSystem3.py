# Uses linear algebra for GROUPS only.
import pickle
from timer import *
from monopoly import *
import numpy


def main():
    total_variables = 8
    all_solutions = []
    main_counter = 1
    while main_counter < 1000:
        print(main_counter)
        matrix = []
        money_totals = []
        for i in range(total_variables):
            game = pickle.load(open('results/stalemates/long/game' + str(randint(0, 45000)) + '.pickle', "rb"))

            convert_group = {"Brown": 0, "Light Blue": 1, "Pink": 2, "Orange": 3,
                             "Red": 4, "Yellow": 5, "Green": 6, "Dark Blue": 7,
                             "Railroad": 8, "Utility": 9}
            properties_in_group = {"Brown": 2, "Light Blue": 3, "Pink": 3, "Orange": 3,
                                   "Red": 3, "Yellow": 3, "Green": 3, "Dark Blue": 2,
                                   "Railroad": 4, "Utility": 2}


            player1 = game.active_players[0]
            player2 = game.active_players[1]
            players = [player1, player2]

            coefficients2 = [0 for i in range(8)]

            for current_player in players:
                # Add coefficients for the completed groups.
                for group in current_player.monopolies:
                    average_rent_proportion = 0
                    for property in current_player.inventory:
                        if property.group == group:
                            if current_player.number == 1:
                                average_rent_proportion += game.calculate_rent_proportion(property=property,
                                                                                          owner=current_player)
                            elif current_player.number == 2:
                                average_rent_proportion -= game.calculate_rent_proportion(property=property,
                                                                                          owner=current_player)
                    average_rent_proportion /= properties_in_group[group]

                    # Add coefficients.
                    coefficients2[convert_group[group]] = average_rent_proportion


            # Add constant.
            matrix.append(coefficients2)

            money_totals.append((player1.money - player2.money) / (player1.money + player2.money))

        no_solution = False
        try:
            solution =  numpy.linalg.solve(matrix, money_totals)
        except Exception:
            no_solution = True
            print("No solution!")


        if not no_solution:
            min0 = min(solution)
            for i in range(len(solution)):
                solution[i] -= min0

            max0 = max(solution)
            for i in range(len(solution)):
                solution[i] /= max0

            all_solutions.append(solution)

            print(solution)
            main_counter += 1

    # Compute the average.
    averages = [0 for i in range(total_variables)]

    for i in range(len(all_solutions)):
        for j in range(total_variables):
            averages[j] += all_solutions[i][j]

    for i in range(len(averages)):
        averages[i] /= len(all_solutions)
        print(averages[i])


if __name__ == '__main__':
    timer()
    main()
    timer()