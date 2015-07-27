import mb as monopoly
from timer import *
import cProfile
from random import shuffle, randint, uniform


def random_ordering():
    all_groups = ["Brown", "Light Blue", "Pink", "Orange",
                  "Red", "Yellow", "Green", "Dark Blue",
                  "Utility", "Railroad"]
    shuffle(all_groups)
    return tuple(all_groups)


def random_value():
    return randint(1, 600)


def random_values():
    return {"Brown": random_value(),
            "Light Blue": random_value(),
            "Pink": random_value(),
            "Orange": random_value(),
            "Red": random_value(),
            "Yellow": random_value(),
            "Green": random_value(),
            "Dark Blue": random_value(),
            "Utility": random_value(),
            "Railroad": random_value()}


def main(games_in_a_set=5000):
    game0 = monopoly.Game(cutoff=1000, trading_enabled=True)
    for j in range(40):
        thresh = j / 200
        winners = [0, 0, 0]
        for i in range(games_in_a_set):
            # Play game.
            player1 = monopoly.Player(1, buying_threshold=thresh, group_ordering=random_ordering())
            player2 = monopoly.Player(2, buying_threshold=uniform(0, 1), group_ordering=random_ordering())

            game0.new_players([player1, player2])
            results = game0.play()

            # Store length.
            winners[results['winner']] += 1

        print(winners, thresh)


def main2(games_in_a_set=100):
    game0 = monopoly.Game(cutoff=1000, trading_enabled=True)

    winners = [0, 0, 0]
    for i in range(games_in_a_set):
        # Play game.
        player1 = monopoly.Player(1, buying_threshold=500, group_ordering=random_ordering(), static_threshold=True)
        # player2 = monopoly.Player(2, buying_threshold=randint(1, 500), group_ordering=random_ordering(),static_threshold=True)
        player2 = monopoly.Player(2, buying_threshold=500, group_ordering=random_ordering(), static_threshold=True)

        game0.new_players([player1, player2])
        results = game0.play()

        # Store length.
        winners[results['winner']] += 1

    print(winners)


def go_record(games_in_a_set=1000):
    game0 = monopoly.Game(cutoff=1000, trading_enabled=False)
    go_record = []

    for i in range(games_in_a_set):
        # Play game.
        player1 = monopoly.Player(1, buying_threshold=100)
        player2 = monopoly.Player(2, buying_threshold=100)
        game0.new_players([player1, player2])
        results = game0.play()

        # Store length.
        go_record.extend(player1.go_record)

    print(sum(go_record) / len(go_record))


def main3(games_in_a_set=1000):
    for m1 in range(1, 21):
        for m2 in range(1, 21):
            game0 = monopoly.Game(cutoff=1000, trading_enabled=True, image_exporting=0, matrix1=m1, matrix2=m2)
            trade_count = []
            winners = [0, 0, 0]
            for i in range(games_in_a_set):
                # Play game.
                player1 = monopoly.Player(1, buying_threshold=100,
                                          # group_ordering=random_ordering(),
                                          dynamic_ordering=True,
                                          static_threshold=False
                )
                player2 = monopoly.Player(2, buying_threshold=100,
                                          group_ordering=["Railroad", "Light Blue", "Orange", "Pink", "Red", "Yellow",
                                                          "Green", "Dark Blue", "Utility", "Brown"],
                                          # group_ordering=random_ordering(),
                                          static_threshold=True)

                game0.new_players([player1, player2])
                results = game0.play()

                # Store length.
                winners[results['winner']] += 1
                trade_count.append(results['trade count'])

            print(winners, m1, m2)

        '''print("**")
        print("trades:",results['trade count'])
        for trade_pair in game0.trades:
            print(trade_pair[0].name, "--", trade_pair[1].name)'''

        '''print("avg. trades", sum(trade_count) / games_in_a_set)
        print("max trades", max(trade_count))
        print("min trades", min(trade_count))'''


def best_ordering():
    return tuple(["Railroad", "Light Blue", "Orange", "Pink", "Red",
                  "Yellow", "Green", "Dark Blue", "Utility", "Brown"])


def optimize(games_in_a_set=10000):
    game0 = monopoly.Game(cutoff=1000, trading_enabled=True, image_exporting=0)
    for c in range(-1000, 1, 100):
        trade_count = []
        winners = [0, 0, 0]
        for i in range(games_in_a_set):
            # Play game.
            player1 = monopoly.Player(1,
                                      dynamic_ordering=True,
                                      # group_ordering=random_ordering(),
                                      c=c,
                                      n=6,
            )
            player2 = monopoly.Player(2,
                                      group_ordering=best_ordering(),
                                      step_threshold=True,
                                      buying_threshold=1000
            )

            game0.new_players([player1, player2])
            results = game0.play()

            # Store length.
            winners[results['winner']] += 1
            trade_count.append(results['trade count'])

        print(winners, c, sum(trade_count) / games_in_a_set)
        # print("avg. trades", sum(trade_count) / games_in_a_set)
        # print("max trades", max(trade_count))
        #print("min trades", min(trade_count))


if __name__ == '__main__':
    timer()
    optimize()
    # cProfile.run('main2()', sort=1)
    timer()