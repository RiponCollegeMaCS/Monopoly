from monopoly import *
from random import *

t = 20  # Tournament size
p = 0.95  # Nonzero probability
C = 10  # Number of candidates

def find_candidate(strategies=None):
    # Create strategies
    if strategies == None:
        strategies = []

    for i in range(t):
        strategies.append({'values': random_property_values(), 'fitness': 0})

    # Compute fitness
    game_set(strategies)

    # Sort strategies by fitness.
    sorted_strategies = sorted(strategies, key=lambda k: k['fitness'], reverse=True)

    # Return candidate.
    element = element_chosen()
    if element > t - 1:
        return sorted_strategies[-1]
    else:
        return sorted_strategies[element]


def game_set(strategies, games=1000):
    for strategy in strategies:
        counter = 0
        strat = strategy['values']

        # Game loop.
        for i in range(games):

            # Choose a random strategy.
            other_strat = strat
            while other_strat == strat:
                other_strat = choice(strategies)['values']


            # Play game.
            player1 = Player(1, buying_threshold=100, property_values=strat)
            player2 = Player(2, buying_threshold=100, property_values=other_strat)
            game0 = Game([player1, player2], cutoff=1000, property_trading=True)
            results = game0.play()

            # Store winner.
            if results['winner'] == 1:
                counter += 1

        strategy['fitness'] = counter / games


def element_chosen():
    rand = uniform(0, 1)
    index = 0
    climbing_p = p

    while True:
        if rand < climbing_p:
            return index
        else:
            index += 1
            climbing_p += p * pow(1 - p, index)


def random_property_values():
    return [randint(200, 500) for i in range(40)]


def find_parents(strategies=None):
    candidates = []

    for i in range(C):
        candidate = find_candidate(strategies)
        candidates.append(candidate)
        print(candidate)

    return candidates


def crossover(parents):
    new_parents = []
    while len(new_parents) < t:
        # Find parents.
        parent1 = choice(parents)
        parent2 = parent1
        while parent1 == parent2:
            parent2 = choice(parents)

        split = randint(0, 39)
        property_values = []
        property_values.extend(parent1['values'][0:split + 1])
        property_values.extend(parent2['values'][split - 1:40])
        new_parents.append({'values':  property_values, 'fitness': 0})

        property_values = []
        property_values.extend(parent2['values'][0:split + 1])
        property_values.extend(parent1['values'][split - 1:40])
        new_parents.append({'values':  property_values, 'fitness': 0})

    return new_parents

def main():
    initial_parents = find_parents()
    new_generation = crossover(initial_parents)




main()