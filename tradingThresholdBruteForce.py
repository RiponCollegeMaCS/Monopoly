from m import *
from timer import *
import csv


def random_ordering():
    all_groups = ["Brown", "Light Blue", "Pink", "Orange",
                  "Red", "Yellow", "Green", "Dark Blue",
                  "Utility", "Railroad"]
    shuffle(all_groups)
    return tuple(all_groups)


def random_player():
    return Player(2, buying_threshold=100, trading_threshold=randint(-200, 200))


def main(games_in_a_set=1000):
    with open('results/blah.csv', 'w', newline='') as csvfile:
        output_file = csv.writer(csvfile, quotechar=',')

        game0 = Game(cutoff=1000, trading_enabled=True)

        for trading_threshold in range(-200, 201, 25):
            winner_matrix = [0, 0, 0]
            for i in range(games_in_a_set):
                player1 = Player(1, buying_threshold=100, trading_threshold=trading_threshold)

                player2 = random_player()
                game0.new_players([player1, player2])
                results = game0.play()

                winner_matrix[results['winner']] += 1

            results = [trading_threshold, winner_matrix[1] / games_in_a_set]
            print(results)
            output_file.writerow(results)


if __name__ == '__main__':
    timer()
    main()
    timer()
