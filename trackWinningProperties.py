from timer import *
from monopoly import *


def main():
    property_success = [0 for i in range(28)]
    prop_id = {1: 1, 3: 2, 5: 3, 6: 4, 8: 5, 9: 6, 11: 7, 12: 8, 13: 9, 14: 10, 15: 11, 16: 12, 18: 13, 19: 14,
               21: 15, 23: 16, 24: 17, 25: 18, 26: 19, 27: 20, 28: 21, 29: 22, 31: 23, 32: 24, 34: 25, 35: 26,
               37: 27, 39: 28}

    for i in range(100000):
        # Play game.
        player1 = Player(1)
        player2 = Player(2)
        game0 = Game([player1, player2], cutoff=1000, trading_enabled=False, hotel_upgrade=False)
        results = game0.play()

        if results['winner']:
            for property in results['players'][0].inventory:
                property_success[prop_id[property.id] - 1] += 1

    for element in property_success:
        print(element)


if __name__ == '__main__':
    timer()
    main()
    timer()