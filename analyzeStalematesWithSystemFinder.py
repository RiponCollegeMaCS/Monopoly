# Uses linear algebra.
import pickle
from timer import *
from monopoly import *
import numpy
from copy import deepcopy
from sympy.matrices import *

def main():
    convert_group = {"Brown": 0, "Light Blue": 1, "Pink": 2, "Orange": 3,
                     "Red": 4, "Yellow": 5, "Green": 6, "Dark Blue": 7,
                     "Railroad": 8, "Utility": 9}
    properties_in_group = {"Brown": 2, "Light Blue": 3, "Pink": 3, "Orange": 3,
                           "Red": 3, "Yellow": 3, "Green": 3, "Dark Blue": 2,
                           "Railroad": 4, "Utility": 2}
    prop_id = {1: 1, 3: 2, 5: 3, 6: 4, 8: 5, 9: 6, 11: 7, 12: 8, 13: 9, 14: 10, 15: 11, 16: 12, 18: 13, 19: 14,
               21: 15, 23: 16, 24: 17, 25: 18, 26: 19, 27: 20, 28: 21, 29: 22, 31: 23, 32: 24, 34: 25, 35: 26,
               37: 27, 39: 28}
    all_groups = ["Brown", "Light Blue", "Pink", "Orange",
                  "Red", "Yellow", "Green", "Dark Blue",
                  "Railroad", "Utility"]
    no_solution = True
    counter = 0
    while no_solution:
        print(counter)
        # Find games with broken groups.
        games_to_use = []
        all_groups_found = []
        all_groups_found_group_vars = []
        while len(all_groups_found) < 10 and len(all_groups_found_group_vars) < 10:
            game = pickle.load(open('results/stalemates/long/game' + str(randint(0, 49999)) + '.pickle', "rb"))

            players = [game.active_players[0], game.active_players[1]]

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

            all_monopolies = []
            all_monopolies.extend(players[0].monopolies)
            all_monopolies.extend(players[1].monopolies)


            game_found = False
            for group in all_groups:
                if group not in all_monopolies:
                    if group not in all_groups_found:
                        all_groups_found.append(group)
                        game_found = True

            for group in all_monopolies:
                if group not in all_groups_found_group_vars:
                    all_groups_found_group_vars.append(group)
                    game_found = True

            if game_found:
                games_to_use.append(deepcopy(game))

        # Add more games until we hit 38.
        while len(games_to_use) < 38:
            game = pickle.load(open('results/stalemates/long/game' + str(randint(0, 49999)) + '.pickle', "rb"))
            games_to_use.append(deepcopy(game))

        matrix = []
        money_totals = []
        for game in games_to_use:
            players = [game.active_players[0], game.active_players[1]]

            # The first set of coefficients.
            coefficients1 = [0 for i in range(28)]

            for current_player in players:
                for property in current_player.inventory:
                    if property.group not in current_player.monopolies:
                        if current_player.number == 1:
                            coefficients1[prop_id[property.id] - 1] += 1
                        elif current_player.number == 2:
                            coefficients1[prop_id[property.id] - 1] -= 1

            # The second set of coefficients.
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

            coefficients = []
            coefficients.extend(coefficients1)
            coefficients.extend(coefficients2)
            print(coefficients)
            matrix.append(coefficients)

            # Add constant.
            #money_totals.append((players[0].money - players[1].money) / (players[0].money + players[1].money))
            money_totals.append(players[0].money - players[1].money)

        print(money_totals)
        for i in range(len(matrix)):
            matrix[i].append(money_totals[i])

        print("!",Matrix(matrix))

        matrix = Matrix.rref(Matrix(matrix))
        print(matrix)
        counter += 1

        '''solution = []
        try:
            print(money_totals)
            solution = numpy.linalg.solve(matrix, money_totals)
            print(solution)
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            no_solution = False
        except:
            print("No solution!")'''



if __name__ == '__main__':
    timer()
    main()
    timer()