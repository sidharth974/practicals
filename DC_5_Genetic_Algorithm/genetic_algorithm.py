# DC-5: Genetic Algorithm using DEAP.
# Pure-Python version (no PyTorch / no scikit-learn).
# We use DEAP to evolve a real-valued vector x of length 5 to minimise
# the classic Sphere function:  f(x) = sum(xi^2).
# Optimum is at x = [0, 0, 0, 0, 0] with f(x) = 0.
# The same GA building blocks (selection, crossover, mutation, elitism,
# generations) demonstrate everything needed for the viva.

import random
import numpy as np
from deap import base, creator, tools, algorithms

CHROMOSOME_LEN = 5          # length of each individual
LOWER, UPPER   = -5.0, 5.0  # gene range


# ----------------- Fitness function -----------------

def sphere(individual):
    """Sum of squares — global minimum at the origin."""
    return (sum(x * x for x in individual),)


# ----------------- DEAP setup -----------------

# Minimisation problem: weights = (-1.0,)
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
# Each gene is a uniform random float in [LOWER, UPPER]
toolbox.register("attr_float", random.uniform, LOWER, UPPER)
# Individual = list of CHROMOSOME_LEN floats
toolbox.register("individual", tools.initRepeat,
                 creator.Individual, toolbox.attr_float, n=CHROMOSOME_LEN)
# Population = list of individuals
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Operators
toolbox.register("evaluate", sphere)
toolbox.register("mate",   tools.cxBlend, alpha=0.3)                              # blend crossover
toolbox.register("mutate", tools.mutGaussian, mu=0.0, sigma=0.5, indpb=0.2)      # Gaussian mutation
toolbox.register("select", tools.selTournament, tournsize=3)                      # tournament selection


# ----------------- Driver -----------------

def main():
    pop = toolbox.population(n=50)              # 50 individuals
    hof = tools.HallOfFame(1)                   # remember best ever

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("min", np.min)

    # Run a 30-generation GA: crossover prob 0.7, mutation prob 0.2.
    algorithms.eaSimple(
        pop, toolbox,
        cxpb=0.7, mutpb=0.2, ngen=30,
        stats=stats, halloffame=hof, verbose=True,
    )

    best = hof[0]
    print("\nBest individual found:")
    print(f"  x       = {[round(v, 4) for v in best]}")
    print(f"  f(x)    = {best.fitness.values[0]:.6f}")
    print(f"  optimum = 0.0  at  x = [0,0,0,0,0]")


if __name__ == "__main__":
    main()
