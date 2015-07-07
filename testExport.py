from m import *


def random_values():
    return {"Brown": randint(1, 600),
            "Light Blue": randint(1, 600),
            "Pink": randint(1, 600),
            "Orange": randint(1, 600),
            "Red": randint(1, 600),
            "Yellow": randint(1, 600),
            "Green": randint(1, 600),
            "Dark Blue": randint(1, 600),
            "Utility": randint(1, 600),
            "Railroad": randint(1, 600)}


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
    player1 = Player(1, buying_threshold=randint(1, 500), group_values=random_values())
    player2 = Player(2, buying_threshold=randint(1, 500), group_values=random_values())
    game0 = Game([player1, player2], cutoff=1000, image_exporting=1, trading_enabled=True)
    results = game0.play()

