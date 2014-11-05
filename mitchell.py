from timer import *
from success import *
from monopoly import *
import cProfile


def main():
    timer()
    # print(simple_success_indicator(player1))
    games = 1000
    thresh = 100
    results = []
    for i in range(games):
        player1 = Player(1, buying_threshold=thresh, building_threshold=5, jail_time=0, smart_jail_strategy=False,
                         complete_monopoly=0, group_preferences=(), development_threshold=0)
        player2 = Player(2, buying_threshold=100, building_threshold=5, jail_time=0, smart_jail_strategy=False,
                         complete_monopoly=0, group_preferences=(), development_threshold=0)
        game0 = Game([player1, player2], cutoff=1000)
        results.append(game0.play()[0])

    print("thresh=", thresh, "ties", results.count(0) / games)
    print("thresh=", thresh, "p1", results.count(1) / games)
    print("thresh=", thresh, "p2", results.count(2) / games)
    timer()


# cProfile.run('main()',sort="tottime")

def main2():
    grandma = Player(1, buying_threshold=1000, building_threshold=5, jail_time=3, smart_jail_strategy=False,
                     complete_monopoly=0, group_preferences=(), development_threshold=0)
    aggressive = Player(1, buying_threshold=1, building_threshold=5, jail_time=0, smart_jail_strategy=False,
                        complete_monopoly=2, group_preferences=(), development_threshold=2)
    competitor = Player(1, buying_threshold=150, building_threshold=5, jail_time=0, smart_jail_strategy=True,
                        complete_monopoly=1, group_preferences=(), development_threshold=1)
    newbie = Player(1, buying_threshold=500, building_threshold=5, jail_time=3, smart_jail_strategy=False,
                    complete_monopoly=0, group_preferences=(), development_threshold=0)
    print(success_indicator(grandma, procs=4, number_of_games=1000))



'''for j in range(20):
    results = []
    infinite_games=0
    for i in range(1000):
        grandma = Player(1, buying_threshold=1000, building_threshold=5, jail_time=3, smart_jail_strategy=False,
                         complete_monopoly=0, group_preferences=(), development_threshold=0)
        player1 = generate_random_player(1)
        player2 = generate_random_player(2)
        game = Game(list_of_players=[player1, player2],free_parking_pool=True)
        length = game.play()[1]
        if length == 1000:
            infinite_games +=1
        else:
            results.append(game.play()[1])
    print([infinite_games,sum(results) / len(results)])'''

if __name__ == '__main__':
    timer()
    main2()
    timer()