from itertools import product
from math import factorial


def composition(n, k):
    lists = []
    for moo in range(k):
        lists.append(range(1, n + 1))

    counter = 0
    all_counter = 0
    for item in product(*lists):
        all_counter += 1
        if sum(item) == n:
            counter += 1

    return counter


def n_choose_k(n, k):
    return (factorial(n)) / (factorial(k) * factorial((n - k)))


n = 9
for k in range(1, n + 1):
    print([(n, k), composition(n, k), n_choose_k(n - 1, k - 1)])
