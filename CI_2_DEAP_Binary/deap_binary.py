# CI-2: Distributed Evolutionary Algorithm using the DEAP framework.
# Problem: maximise the number of 1s in a 10-bit binary string (toy
# OneMax problem). Optimal solution is [1,1,1,1,1,1,1,1,1,1].

import random
import numpy as np
from deap import base, creator, tools, algorithms

# 1. Tell DEAP this is a maximisation problem.
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

# 2. Genes are random bits (0/1); each individual is a list of 10 genes.
toolbox.register("attr_bool", random.randint, 0, 1)
toolbox.register("individual", tools.initRepeat,
                 creator.Individual, toolbox.attr_bool, n=10)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)


# 3. Fitness: count of 1s.
def eval_function(individual):
    return (sum(individual),)

toolbox.register("evaluate", eval_function)
toolbox.register("mate",   tools.cxTwoPoint)               # two-point crossover
toolbox.register("mutate", tools.mutFlipBit, indpb=0.2)    # flip each bit with prob 0.2
toolbox.register("select", tools.selTournament, tournsize=3)


def main():
    pop = toolbox.population(n=50)                         # 50 individuals
    hof = tools.HallOfFame(1)                              # remember the best

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("max", np.max)

    # Run 20 generations: crossover prob 0.7, mutation prob 0.2.
    algorithms.eaSimple(
        pop, toolbox,
        cxpb=0.7, mutpb=0.2, ngen=20,
        stats=stats, halloffame=hof, verbose=True,
    )

    print(f"\nBest individual: {hof[0]}  fitness = {hof[0].fitness.values[0]}")


if __name__ == "__main__":
    main()
