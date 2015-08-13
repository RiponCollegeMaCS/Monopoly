import malt as monopoly
import itertools
from random import shuffle


def generate_dice_rolls():
    dice_rolls = []
    for i in range(1, 7):
        for j in range(1, 7):
            if (j, i) not in dice_rolls:
                dice_rolls.append((i, j))

    return dice_rolls


def is_subseq(x, y):
    it = iter(y)
    return all(any(c == ch for c in it) for ch in x)


def generate_dice_roll_series(desired_rolls):
    return itertools.combinations_with_replacement(generate_dice_rolls(), desired_rolls)
    '''dice_roll_series = []

    triples = [[(i, i), (i, i), (i, i)] for i in range(1, 7)]

    for series in itertools.combinations_with_replacement(generate_dice_rolls(), desired_rolls):
        for roll in triples:
            if not is_subseq(roll, series):
                dice_roll_series.append(series)

    return dice_roll_series'''


def generate_buying_decisions(desired_rolls):
    return itertools.combinations_with_replacement([True, False], desired_rolls-4)


def generate_cards(desired_cards):
    card_configurations = []
    for cards in itertools.combinations(desired_cards, 2):
        other_cards = [i for i in range(1, 17) if i not in cards]
        card_configurations.append(list(cards) + other_cards)

    return card_configurations


def main():
    game0 = monopoly.Game(cutoff=4, trading_enabled=False, shuffle=False)
    counter = 0
    found_counter = 0
    desired_rolls = 12

    for dice_rolls in generate_dice_roll_series(desired_rolls):
        for buying_decisions in generate_buying_decisions(desired_rolls):
            for c_cards in generate_cards([4, 5, 11, 6, 7, 9, 10, 13, 14]):
                for cc_cards in generate_cards([8, 10]):
                    counter += 1

                    # Add players and reset game.
                    player1 = monopoly.Player(1, buying_threshold=1, jail_time=0)
                    player2 = monopoly.Player(2, buying_threshold=1, jail_time=0)
                    game0.new_players([player1, player2])

                    # Add new actions.
                    actions = {'dice_rolls': list(dice_rolls),
                               'buying_decisions': list(buying_decisions),
                               'c_cards': list(c_cards),
                               'cc_cards': list(cc_cards)
                    }

                    orig_actions = {'dice_rolls': list(dice_rolls),
                               'buying_decisions': list(buying_decisions),
                               'c_cards': list(c_cards),
                               'cc_cards': list(cc_cards)
                    }

                    game0.add_actions(actions)

                    # Play game.
                    results = game0.play()

                    if results['winner'] != 0:
                        print(orig_actions)
                        found_counter += 1

                    if counter % 100000 == 0:
                        print(counter, found_counter, orig_actions)
                        print(actions)


main()