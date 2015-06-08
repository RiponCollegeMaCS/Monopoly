from timer import *
from monopoly import *

def main():
    games_in_a_set = 10000

    for evolving_thresh in range(1, 10, 1):
        winner_matrix = [0, 0, 0]
        et = evolving_thresh / 100
        for i in range(games_in_a_set):
            player1 = Player(1, buying_threshold=100,
                             jail_time=3,
                             smart_jail_strategy=False,
                             complete_monopoly=1,
                             development_threshold=0,
                             group_preferences=(),
                             building_threshold=5,
                             evolving_threshold=et,

            )
            player2 = Player(2, buying_threshold=100,
                             jail_time=3,
                             smart_jail_strategy=False,
                             complete_monopoly=1,
                             development_threshold=0,
                             group_preferences=(),
                             building_threshold=5,
                             evolving_threshold=0,
            )
            # Play game.
            game0 = Game([player1, player2],
                         cutoff=1000,
                         auctions_enabled=True,
                         trading_enabled=True,
                         #hotel_upgrade=True,
                         building_sellback=False,
                         free_parking_pool=False,
                         double_on_go=False,
                         no_rent_in_jail=False,
                         trip_to_start=False,
                         snake_eyes_bonus=False,
            )
            results = game0.play()

            # Store winner.
            winner_matrix[results['winner']] += 1

        print(evolving_thresh, winner_matrix)


if __name__ == '__main__':
    timer()
    main()
    timer()