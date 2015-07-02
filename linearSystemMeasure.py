import mono as monopoly
import numpy
from random import shuffle
import copy


def random_ordering():
    all_groups = ["Brown", "Light Blue", "Pink", "Orange",
                  "Red", "Yellow", "Green", "Dark Blue",
                  "Utility", "Railroad"]
    shuffle(all_groups)
    return tuple(all_groups)


def main():
    while True:
        all_solns = []
        solns_to_find = 5
        for i in range(solns_to_find):
            games_in_a_set = 1000
            main_counter = 0
            equations = 28
            constant_vector = []
            matrix = []

            while main_counter < equations:
                # Play game.
                player1 = monopoly.Player(1, buying_threshold=500, group_ordering=random_ordering())
                player2 = monopoly.Player(2, buying_threshold=500, group_ordering=random_ordering())
                game = monopoly.Game(cutoff=1000, ranking_trading=True)
                game.new_players([player1, player2])
                results = game.play()

                # Check if we actually ended early.
                if results['end behavior'] == "Tie":
                    game.bought_properties = 0  # Reset this flag to continue the game.
                    winner_matrix = [0, 0, 0]  # A place to store who wins in the sample.

                    # Play game forward many times.
                    for i in range(games_in_a_set):
                        new_game = copy.deepcopy(game)  # Create a copy of the game object to play ahead.
                        results = new_game.play()  # Play the game.
                        winner_matrix[results['winner']] += 1  # Store the winner.

                    '''print("-------")
                    if winner_matrix[2] != 0:
                        print(winner_matrix[1] / winner_matrix[2])
                    else:
                        print("inf")

                    print(winner_matrix)'''

                    # Only continue if eac player wins at least 10% of the time.
                    if (winner_matrix[1] / games_in_a_set) > 0.05 and (winner_matrix[2] / games_in_a_set) > 0.05:
                        scalar = winner_matrix[1] / winner_matrix[2]
                        main_counter += 1  # Increment counter to indicate that we found one.
                        matrix_row = []  # The row of the matrix we find from these results.

                        # Fill matrix row with property data.
                        for property in game.board:
                            if property.is_property:
                                # If player 1 owns it, it is just the scalar.
                                if property.owner.number == 1:
                                    matrix_row.append(scalar * game.calculate_rent_proportion(property=property))
                                # Otherwise it is -1.
                                else:
                                    matrix_row.append(-1 * game.calculate_rent_proportion(property=property))

                        # Add constant based upon how much money players had when all props were bought.
                        constant_vector.append((player1.money * scalar) - player2.money)
                        matrix.append(matrix_row)  # Add matrix row.

            soln = numpy.linalg.solve(matrix, constant_vector)
            shifted_soln = []
            soln_min = min(soln)

            for element in soln:
                shifted_soln.append(element - soln_min)

            scaled_soln = []
            soln_max = max(shifted_soln)
            for element in shifted_soln:
                scaled_soln.append(element / soln_max)

            all_solns.append(scaled_soln)

        print("*****************************************************")
        avg_vector = [0] * 28
        for i in range(solns_to_find):
            for j in range(28):
                avg_vector[j] += all_solns[i][j]

        for element in avg_vector:
            print(element)


main()