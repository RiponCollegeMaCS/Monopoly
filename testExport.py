from monopoly import *


def random_ordering():
    all_groups = ["Brown", "Light Blue", "Pink", "Orange",
                  "Red", "Yellow", "Green", "Dark Blue",
                  "Utility", "Railroad"]
    shuffle(all_groups)
    return tuple(all_groups)

for i in range(1):
    order1 = random_ordering()
    order2 = random_ordering()
    print(order1)
    print(order2)
    player1 = Player(1, buying_threshold=randint(1, 500), group_ordering=order1)
    player2 = Player(2, buying_threshold=randint(1, 500), group_ordering=order2)
    game0 = Game([player1, player2], cutoff=1000, image_exporting=1, trading_enabled=True)
    results = game0.play()

