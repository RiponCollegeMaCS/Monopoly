# Uses linear algebra for JUST PROPERTIES.
import pickle
from timer import *
from monopoly import *
import numpy


def main():
    total_variables = 28
    all_solutions = []
    main_counter = 1
    while main_counter < 1000:
        print(main_counter)
        matrix = []
        money_totals = []
        for i in range(total_variables):
            game = pickle.load(open('results/stalemates/long/game' + str(randint(0, 45000)) + '.pickle', "rb"))
            coefficients1 = [0 for i in range(28)]

            convert_group = {"Brown": 0, "Light Blue": 1, "Pink": 2, "Orange": 3,
                             "Red": 4, "Yellow": 5, "Green": 6, "Dark Blue": 7,
                             "Railroad": 8, "Utility": 9}
            properties_in_group = {"Brown": 2, "Light Blue": 3, "Pink": 3, "Orange": 3,
                                   "Red": 3, "Yellow": 3, "Green": 3, "Dark Blue": 2,
                                   "Railroad": 4, "Utility": 2}
            prop_id = {1: 1, 3: 2, 5: 3, 6: 4, 8: 5, 9: 6, 11: 7, 12: 8, 13: 9, 14: 10, 15: 11, 16: 12, 18: 13, 19: 14,
                       21: 15, 23: 16, 24: 17, 25: 18, 26: 19, 27: 20, 28: 21, 29: 22, 31: 23, 32: 24, 34: 25, 35: 26,
                       37: 27, 39: 28}

            player1 = game.active_players[0]
            player2 = game.active_players[1]
            players = [player1, player2]

            for property in player1.inventory:
                coefficients1[prop_id[property.id]-1] += game.calculate_rent_proportion(property=property, owner=player1)
            for property in player2.inventory:
                coefficients1[prop_id[property.id]-1] -= game.calculate_rent_proportion(property=property, owner=player2)

            matrix.append(coefficients1)
            money_totals.append(player1.money - player2.money)
            # money_totals.append((player1.money - player2.money) / (player1.money + player2.money))

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