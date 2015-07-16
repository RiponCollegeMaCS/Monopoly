import m as monopoly
import numpy
import itertools
import csv


def diff(a, b):
    b = set(b)
    return tuple(aa for aa in a if aa not in b)

# Game object
game0 = monopoly.Game()
board = game0.board

# Probability matrix
matrix = numpy.loadtxt(open("data/longtime.csv", "rb"), delimiter=",")
odds = matrix[0]

prop_odds = []
rents = []
for i in range(40):
    prop = board[i]
    if prop.is_property:
        prop_odds.append(odds[i])
        if prop.group in ["Utility", "Railroad"]:
            rents.append(0)
        else:
            rents.append(prop.rents[0])

# Indices for the 28 properties
subsets = itertools.combinations(range(28), 14)

money_changes = [0] * 41

# Community Chest
money_changes[2] = (465 / 14)
money_changes[17] = (465 / 14)
money_changes[33] = (465 / 14)

# Chance
money_changes[7] = (185 / 6)
money_changes[22] = (185 / 6)
money_changes[36] = (185 / 6)

# Fixed spaces.
money_changes[4] = -75  # Luxury Tax
money_changes[38] = -200  # Income Tax
money_changes[40] = -50  # For the last entry, "In Jail"

######
expected_value = numpy.dot(odds, money_changes)
expected_value += (1 / 6.09) * 200

print(expected_value)

# money_changes_sq = [pow(i, 2) for i in money_changes]
# variance = numpy.dot(odds, money_changes_sq) + ((200 ^ 2) * (1 / 6.09)) - pow(expected_value, 2)
# stdev = math.sqrt(variance)

with open('propertyConfigurations.csv', 'w', newline='') as csvfile:
    output_file = csv.writer(csvfile, quotechar=',')

    for props1 in subsets:
        # Create two inventory lists.
        inv1 = [1 if i in props1 else 0 for i in range(28)]
        inv2 = [1 if i not in props1 else 0 for i in range(28)]
        inv1_set = set(props1)
        inv2_set = set()

        for element in range(28):
            if element not in inv1_set:
                inv2_set.add(element)

        quit = False
        groups = [{0, 1}, {3, 4, 5}, {6, 8, 9}, {11, 12, 13}, {14, 15, 16}, {18, 19, 21}, {22, 23, 24}, {26, 27}]
        for group in groups:
            if group.issubset(inv1_set) or group.issubset(inv2_set):
                quit = True
                break

        if quit:
            continue

        # Count RRs
        railroads = [2, 10, 17, 25]
        inv1_railroads = 0
        for i in railroads:
            if inv1[i]:
                inv1_railroads += 1

        inv2_railroads = 4 - inv1_railroads

        inv1_rents = list(rents)
        inv2_rents = list(rents)

        inv1_rr_rent = pow(2, inv1_railroads - 1) * 25
        inv2_rr_rent = pow(2, inv2_railroads - 1) * 25
        for i in railroads:
            inv1_rents[i] = inv1_rr_rent
            inv2_rents[i] = inv2_rr_rent

        utilities = [7, 20]
        inv1_utilities = 0
        for i in utilities:
            if inv1[i]:
                inv1_utilities += 1

        if inv1_utilities == 0:
            inv1_ut_rent = 0
            inv2_ut_rent = 70
        elif inv1_utilities == 1:
            inv1_ut_rent = 28
            inv2_ut_rent = 28
        else:
            inv1_ut_rent = 70
            inv2_ut_rent = 0

        for i in utilities:
            inv1_rents[i] = inv1_ut_rent
            inv2_rents[i] = inv2_ut_rent

        # print(inv1, inv2)
        p1_power = 0
        p2_power = 0
        for i in range(28):
            p1_power += inv1[i] * prop_odds[1] * inv1_rents[i]
            p2_power += inv2[i] * prop_odds[1] * inv2_rents[i]

        p1_change = p1_power - p2_power + expected_value
        p2_change = p2_power - p1_power + expected_value

        output_file.writerow([p1_change, p2_change])



