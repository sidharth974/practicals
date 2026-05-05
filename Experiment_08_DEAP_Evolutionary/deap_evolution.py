# Distributed Evolutionary Algorithm (DEAP-style)
# Evolutionary algorithms imitate natural evolution:
#   1. Initialise a random population of candidate solutions.
#   2. Evaluate fitness (here: smaller value = better).
#   3. Select the fittest individuals.
#   4. Apply mutation (and/or crossover) to produce new offspring.
#   5. Form the next generation and repeat.
# Over many generations the population converges toward optimal values.

import random

# Initial random population of 10 individuals (integers in [0, 100]).
population = [random.randint(0, 100) for i in range(10)]

# Run 5 evolutionary generations.
for generation in range(5):
    # Fitness sort: smaller values are considered fitter for this minimisation task.
    population.sort()

    # Selection: keep the top 5 fittest as parents/survivors (elitism).
    best = population[:5]

    # Start the next generation with the elite survivors preserved.
    new_population = best.copy()

    # Mutation: create 5 new offspring by perturbing each elite by a small random delta.
    for i in range(5):
        child = best[i] + random.randint(-5, 5)
        new_population.append(child)

    # The new generation replaces the old one for the next iteration.
    population = new_population

# Best (smallest) value left in the population is the optimised solution.
print("Best Solution:", min(population))
