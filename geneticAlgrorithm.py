from monopoly import *
from random import *
from timer import timer

# Constants
k = 30  # Size of population.
t = 10  # Tournament size in selection
p = 0.95  # Probability for taking an individual that is not the best in tournament
C = 10  # Number of candidates for a new generation of k
mu = 0.05  # The probability of a mutation.
generations = 10  # The number of generations to work through.
detail = 100

# Create a random set of property values
def random_property_values():
    return [random_property_value() for i in range(40)]


# Calculate a suitable random property value
def random_property_value():
    return randint(1, 800)


# Find top candidate of individuals provided
def find_candidate(strategies):
    shuffle(strategies)
    t_random_individuals = strategies[0:k]

    # Compute fitness for each strategy.
    relative_fitness(t_random_individuals)

    # Sort strategies by fitness.
    sorted_individuals = sorted(t_random_individuals, key=lambda k: k['fitness'], reverse=True)

    # Return top candidate.
    index = element_chosen(max_index=t - 1)
    return sorted_individuals[index]


# Play candidates against each other to compute fitness.
def relative_fitness(strategies, games=detail):
    for strategy in strategies:
        counter = 0
        strat = strategy['values']

        # Game loop.
        for i in range(games):

            # Choose a random strategy to play against.
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
        if strategy['fitness'] > 0.70:
            print(strategy)


# Choose the index of the individual based on p.
def element_chosen(max_index):
    rand = uniform(0, 1)
    index = 0
    climbing_p = p

    while index < max_index:
        if rand < climbing_p:
            return index
        else:
            index += 1
            climbing_p += p * pow(1 - p, index)

    return max_index


# Find C candidates.
def selection(strategies):
    # A place to store C candidates.
    candidates = []

    # Find candidates.
    for i in range(C):
        candidate = find_candidate(strategies)
        candidates.append(candidate)
        print(candidate)

    return candidates


# Apply a single crossover.
def crossover(parents):
    # A place to store the next generation
    new_generation = []
    counter = 0

    # Loop until we have k individuals.
    while counter < k:
        # Find two random parents in generation to breed.
        parent1 = choice(parents)
        parent2 = parent1

        while parent1 == parent2:
            parent2 = choice(parents)

        # Choose a random place to splice the property values.
        split = randint(0, 39)

        # Create an individual with parent1 and then parent2
        property_values = []
        property_values.extend(parent1['values'][0:split + 1])
        property_values.extend(parent2['values'][split - 1:40])
        new_generation.append({'values': property_values, 'fitness': 0})

        # Create an individual with parent2 and then parent1
        property_values = []
        property_values.extend(parent2['values'][0:split + 1])
        property_values.extend(parent1['values'][split - 1:40])
        new_generation.append({'values': property_values, 'fitness': 0})

        counter += 2

    return new_generation


# Allow mutations to occur in a population.
def mutation(population):
    # Look at all individuals.
    for individual in population:

        # Calculate a random number on [0,1]
        rand = uniform(0, 1)

        # See if the number is less than the mutation threshold.
        if rand <= mu:
            # Find a random gene.
            random_gene = randint(0, 39)

            # Replace the random gene with a random value
            individual['values'][random_gene] = random_property_value()

    return population


def main():
    # Create an initial population of k random individuals.
    p_new = []
    for i in range(k):
        p_new.append({'values': random_property_values(), 'fitness': 0})

    print("generation 1 done")

    current_generation = 1
    while current_generation < generations:
        p_old = p_new
        # Find the candidates for the next generation.
        candidates = selection(p_old)
        p_new = crossover(candidates)
        p_new = mutation(p_new)

        # Increment generation counter
        current_generation += 1

        print("generation", current_generation, "done")


timer()
main()
timer()