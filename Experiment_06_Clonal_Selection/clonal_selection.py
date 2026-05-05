# Clonal Selection Algorithm (CSA)
# Inspired by the biological immune response: when an antibody recognises an antigen
# it is selected, cloned (multiplied), and mutated to produce slightly varied copies.
# The best of these are kept across generations, driving the population toward better
# solutions. Here we minimise an integer (lower = better).

import random

# Initial random "antibody" population: 10 candidates in the range [1, 100].
population = [random.randint(1, 100) for i in range(10)]

# Run 5 generations of selection -> cloning -> mutation.
for i in range(5):
    # Sort ascending so the smallest (best) values come first.
    population.sort()

    # Selection: pick the top 3 fittest antibodies.
    best = population[:3]

    # Cloning + mutation: create one mutated clone per selected antibody.
    # The mutation is a small random perturbation in [-5, +5].
    clones = []
    for b in best:
        clones.append(b + random.randint(-5, 5))

    # Add clones back to the population so they compete in the next generation.
    population = population + clones

# After all generations, the smallest value is the optimised solution.
print("Best Solution:", min(population))
