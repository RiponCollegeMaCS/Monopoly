import random


def double_amounts(money_amounts):
    original_amounts = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
    new_amounts = []
    for i in range(len(original_amounts)):
        if money_amounts[i] == 100000:
            new_amounts.append(money_amounts[i])
        elif money_amounts[i] + original_amounts[i] >= 50000:
            new_amounts.append(100000)
        else:
            new_amounts.append(money_amounts[i] + original_amounts[i])

    return new_amounts


def play_game(turns):
    chests_left = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    money_amounts = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
    old_amount = 0
    for i in range(turns):
        chest = random.choice(chests_left)
        chests_left.remove(chest)
        new_amount = money_amounts[chest]

        if new_amount < old_amount:
            return 0
        else:
            old_amount = new_amount

        money_amounts = double_amounts(money_amounts)


    return old_amount

total_winnings = 0
games = 10000
for i in range(games):
    total_winnings += play_game(3)

print("Avg $:",total_winnings/games)