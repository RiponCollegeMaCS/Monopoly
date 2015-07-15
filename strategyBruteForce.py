from monopoly import *
from timer import *
import csv


def random_ordering():
    all_groups = ["Brown", "Light Blue", "Pink", "Orange",
                  "Red", "Yellow", "Green", "Dark Blue",
                  "Utility", "Railroad"]
    shuffle(all_groups)
    return tuple(all_groups)


def random_player():
    return Player(2, buying_threshold=randint(1, 1000),
                  development_threshold=randint(0, 2),
                  complete_monopoly=randint(0, 2),
                  group_ordering=random_ordering()
    )


def main(games_in_a_set=1000):
    with open('results/bruteForceStrategiesHigherThresh.csv', 'w', newline='') as csvfile:
        output_file = csv.writer(csvfile, quotechar=',')

        game0 = Game(cutoff=1000, trading_enabled=True)

        for buying_threshold in [1, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]:
            for development_threshold in [0, 1, 2]:
                for complete_monopoly in [0, 1, 2]:

                    winner_matrix = [0, 0, 0]
                    for i in range(games_in_a_set):
                        player1 = Player(1, buying_threshold=buying_threshold,
                                         development_threshold=development_threshold,
                                         complete_monopoly=complete_monopoly,
                                         group_ordering=random_ordering()#('Railroad','Light Blue','Orange','Utility','Dark Blue','Red','Brown','Yellow','Pink','Green')

                        )

                        player2 = random_player()
                        game0.new_players([player1, player2])
                        results = game0.play()

                        winner_matrix[results['winner']] += 1

                    results = [buying_threshold, development_threshold, complete_monopoly,
                               winner_matrix[1] / games_in_a_set]
                    print(results)
                    output_file.writerow(results)


if __name__ == '__main__':
    timer()
    main()
    timer()
