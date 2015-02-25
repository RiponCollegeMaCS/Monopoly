# Uses linear algebra.
import pickle
from timer import *
from monopoly import *
from row_reduction import *


def main():
    total_variables = 38
    all_solutions = []
    main_counter = 1
    while main_counter < 10000:
        print(main_counter)
        # start = total_variables * i
        matrix = []
        for i in range(total_variables):
            game = pickle.load(open('results/stalemates/long/game' + str(randint(0, 25000)) + '.pickle', "rb"))
            coefficients = [0 for i in range(50)]

            convert_group = {"Brown": 40, "Light Blue": 41, "Pink": 42, "Orange": 43,
                             "Red": 44, "Yellow": 45, "Green": 46, "Dark Blue": 47,
                             "Railroad": 48, "Utility": 49}
            properties_in_group = {"Brown": 2, "Light Blue": 3, "Pink": 3, "Orange": 3,
                                   "Red": 3, "Yellow": 3, "Green": 3, "Dark Blue": 2,
                                   "Railroad": 4, "Utility": 2}

            player1 = game.active_players[0]
            player2 = game.active_players[1]
            players = [player1, player2]
            for current_player in players:
                # Add railroads and utilities to the list of monopolies.
                counter = 0
                for property in current_player.inventory:
                    if property.group == "Railroad":
                        counter += 1
                if counter == 4:
                    current_player.monopolies.append("Railroad")

                counter = 0
                for property in current_player.inventory:
                    if property.group == "Utility":
                        counter += 1
                if counter == 2:
                    current_player.monopolies.append("Utility")

            for property in player1.inventory:
                if property not in player1.monopolies:
                    coefficients[property.id] += 1  # game.calculate_rent_proportion(property=property, owner=player1)
            for property in player2.inventory:
                if property not in player2.monopolies:
                    coefficients[property.id] -= 1  # game.calculate_rent_proportion(property=property, owner=player2)

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
                    coefficients[convert_group[group]] = average_rent_proportion

            # Add constant.
            coefficients.append((player1.money - player2.money) / (player1.money + player2.money))
            matrix.append(coefficients)

        toReducedRowEchelonForm(matrix)
        solution = []
        for element in matrix:
            solution.append(element[-1])

        # There actually is a solution.
        if solution[0] != 0 and solution[1] != 0:
            for i in range(len(solution)):
                solution[i] -= min(solution)
            for i in range(len(solution)):
                solution[i] /= max(solution)

            all_solutions.append(solution)
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