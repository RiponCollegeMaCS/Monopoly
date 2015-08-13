import math
import scipy.stats
import numpy
import random


def percentage(z_score):
    return .5 * (math.erf(z_score / 2 ** .5) + 1)




mean1 = 19.787819193651494
var1 = 29680.186598120901
std1 = math.sqrt(var1)

mean2 = 18.505704910048621
var2 = 29082.653864213582
std2 = math.sqrt(var2)

def z_score(percent):
    return scipy.stats.norm.ppf(percent)

# mean1 = 3.2851584846564279
# var1 = 6026.101720881039
# mean2 = 47.226987906711642
# var2 = 3806.5056004096614

'''
old = 1
for i in range(1, 10000):
    z1 = (-1500 - (i * mean1)) / math.sqrt(pow(i, 2) * var1)
    percent1 = 1 - percentage(z1)  # Prob. that player is still in

    z2 = (-1500 - (i * mean2)) / math.sqrt(pow(i, 2) * var2)
    percent2 = 1 - percentage(z2)  # Prob. that player is still in

    new = old * percent1 * percent2
    print(percent1, percent2, "*", new)
    old = new


'''

'''
still_going = 0
for i in range(1, 10000):
    z1 = (-1500 - (i * mean1)) / math.sqrt(pow(i, 2) * var1)
    percent1 = percentage(z1)

    z2 = (-1500 - (i * mean2)) / math.sqrt(pow(i, 2) * var2)
    percent2 = percentage(z2)

    p1_wins = (1 - percent1) * percent2 * still_going
    p2_wins = percent1 * (1 - percent2) * still_going

    still_going = percent1 * (1 - still_going) * (1 - percent2)

    print(i, percent1, still_going)

'''


def reverse_attempt():
    print("*******************")
    for i in [10000]:
        print(i, (mean1 * i) + (z_score(0.3767) * (math.sqrt(var1)) * i))


def simulation():
    sample = 5000
    winners = [0, 0, 0]
    for i in range(sample):
        p1_money = 2000
        p2_money = 2000
        counter = 0

        while (p2_money > 0 and p1_money > 0) and counter < 1000:
            p1_money += random.gauss(mean1, std1)
            p2_money += random.gauss(mean2, std2)
            counter += 1

        if counter >= 1000:
            winners[0] += 1
        elif p1_money < 0:
            winners[2] += 1
        else:
            winners[1] += 1

    print(winners[0] / sample, winners[1] / sample, winners[2] / sample)


simulation()
