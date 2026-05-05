# Interactive Evolutionary Algorithm (DEAP-style)
# Optimises a function f(x) over an integer domain using selection,
# crossover and mutation across multiple generations.
# The user picks the goal (minimise / maximise) and tunes all parameters.

import random


# ---------- objective functions the user can pick from ----------

def f_square(x):           # minimum at x = 0
    return x * x

def f_neg_square(x):       # maximum at x = 0  (we'll negate when minimising)
    return -(x * x)

def f_quadratic(x):        # parabola with min at x = 7
    return (x - 7) ** 2 + 3

def f_abs(x):              # V-shape, min at x = 0
    return abs(x)


OBJECTIVES = {
    "1": ("f(x) = x^2          (min @ x=0)",        f_square,     "min"),
    "2": ("f(x) = (x-7)^2 + 3  (min @ x=7)",        f_quadratic,  "min"),
    "3": ("f(x) = |x|          (min @ x=0)",        f_abs,        "min"),
    "4": ("f(x) = -x^2         (max @ x=0)",        f_neg_square, "max"),
}


# ---------- evolutionary algorithm ----------

def evolve(domain, pop_size, generations, mutation_rate, mutation_range,
           elite_size, fitness_fn, mode="min", verbose=True):
    """
    domain          : (lo, hi) integer range for individuals
    pop_size        : population size
    generations     : how many rounds to evolve
    mutation_rate   : probability each new offspring is mutated
    mutation_range  : ± range used when mutating
    elite_size      : top individuals carried over unchanged each generation
    fitness_fn      : callable, individual -> score
    mode            : "min" or "max"
    """
    lo, hi = domain
    population = [random.randint(lo, hi) for _ in range(pop_size)]

    # Sort population such that the best individual is always at index 0.
    def sort_pop(p):
        return sorted(p, key=fitness_fn, reverse=(mode == "max"))

    population = sort_pop(population)

    for gen in range(1, generations + 1):
        # 1. ELITISM — keep the best individuals unchanged.
        new_pop = population[:elite_size]

        # 2. Reproduce until we refill the population.
        while len(new_pop) < pop_size:
            # Tournament selection: pick 3 random, take the best.
            parents = random.sample(population, 3)
            parent  = sort_pop(parents)[0]

            # Crossover: average with a second parent (simple integer crossover).
            other  = random.choice(population)
            child  = (parent + other) // 2

            # Mutation
            if random.random() < mutation_rate:
                child += random.randint(-mutation_range, mutation_range)
                # Clamp to domain
                child = max(lo, min(hi, child))

            new_pop.append(child)

        population = sort_pop(new_pop)

        if verbose:
            best = population[0]
            print(f"  Gen {gen:>3}: best x = {best:>5}, f(x) = {fitness_fn(best)}")

    return population[0]


# ---------- input helpers ----------

def read_int(prompt, lo, hi, default=None):
    while True:
        raw = input(prompt).strip()
        if raw == "" and default is not None:
            return default
        try:
            v = int(raw)
            if lo <= v <= hi:
                return v
            print(f"  ERROR: must be in [{lo},{hi}].")
        except ValueError:
            print("  ERROR: enter an integer.")


def read_float(prompt, lo, hi, default=None):
    while True:
        raw = input(prompt).strip()
        if raw == "" and default is not None:
            return default
        try:
            v = float(raw)
            if lo <= v <= hi:
                return v
            print(f"  ERROR: must be in [{lo},{hi}].")
        except ValueError:
            print("  ERROR: enter a number.")


# ---------- main ----------

def main():
    print("=" * 60)
    print(" Evolutionary Algorithm (interactive)")
    print("=" * 60)

    while True:
        print("\nObjective functions:")
        for k, (label, _, _) in OBJECTIVES.items():
            print(f"  {k}) {label}")
        choice = input("Choose [1-4] (default 1): ").strip() or "1"
        if choice not in OBJECTIVES:
            print("Invalid option."); continue
        label, fn, mode = OBJECTIVES[choice]
        print(f"  Selected: {label}  (we will {'maximise' if mode == 'max' else 'minimise'})")

        lo = read_int("Domain lower bound (default -100): ", -10000, 10000, -100)
        hi = read_int("Domain upper bound (default  100): ", lo, 10000, 100)

        pop_size       = read_int("Population size (5-100, default 20): ", 5, 100, 20)
        generations    = read_int("Generations (1-200, default 30): ",     1, 200, 30)
        mutation_rate  = read_float("Mutation rate (0..1, default 0.3): ", 0.0, 1.0, 0.3)
        mutation_range = read_int("Mutation ±range (1-50, default 5): ",   1, 50, 5)
        elite_size     = read_int(f"Elite carry-over (0-{pop_size//2}, default 2): ", 0, pop_size // 2, 2)

        verbose = input("Show every-generation progress? [y/N]: ").strip().lower() == "y"

        best = evolve((lo, hi), pop_size, generations, mutation_rate,
                      mutation_range, elite_size, fn, mode, verbose=verbose)

        print()
        print("=" * 60)
        print(f" RESULT: best x = {best},  f(x) = {fn(best)}")
        print("=" * 60)

        if input("\nRun another? [y/N]: ").strip().lower() != "y":
            print("Goodbye.")
            return


if __name__ == "__main__":
    main()
