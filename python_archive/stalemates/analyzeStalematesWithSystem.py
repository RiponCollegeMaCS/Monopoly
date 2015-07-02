# Uses linear algebra.
import pickle
from timer import *
from monopoly import *
import numpy


def main():
    total_variables = 38
    main_counter = 1
    not_found = True
    while not_found:
        print(main_counter)
        main_counter += 1
        matrix = []
        money_totals = []
        for i in range(total_variables):
            game = pickle.load(open('results/stalemates/long/game' + str(randint(0, 49999)) + '.pickle', "rb"))
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
                if property.group not in player1.monopolies:
                    coefficients1[prop_id[property.id]-1] += 1  # game.calculate_rent_proportion(property=property, owner=player1)
            for property in player2.inventory:
                if property.group not in player2.monopolies:
                    coefficients1[prop_id[property.id]-1] -= 1  # game.calculate_rent_proportion(property=property, owner=player2)

            coefficients2 = [0 for i in range(10)]

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
            coefficients = []
            coefficients.extend(coefficients1)
            coefficients.extend(coefficients2)

            matrix.append(coefficients)

            money_totals.append((player1.money - player2.money) / (player1.money + player2.money))

        no_solution = False
        try:
            solution =  numpy.linalg.solve(matrix, money_totals)
        except Exception:
            no_solution = True
            print("No solution!")

        if not no_solution:
            not_found = False
            print(solution)



if __name__ == '__main__':
    timer()
    main()
    timer()