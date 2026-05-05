# Interactive Clonal Selection Algorithm (CSA)
# CSA imitates the immune response: select the best antibodies, clone them,
# mutate each clone, then keep competing across generations.
# Here we use it to find an integer x that minimises |x - target|.

import random


def affinity(antibody, target):
    """Lower distance = higher affinity. We minimise |antibody - target|."""
    return abs(antibody - target)


def csa(target, pop_size, generations, n_select, mutation_range, verbose=True):
    """Run the Clonal Selection Algorithm and return the best antibody found."""

    # 1. Initialise random antibody population in [target-50, target+50] for variety.
    population = [random.randint(target - 50, target + 50) for _ in range(pop_size)]

    if verbose:
        print(f"\n Initial population: {population}")

    for gen in range(1, generations + 1):
        # 2. Sort by affinity to the target (best first).
        population.sort(key=lambda x: affinity(x, target))

        # 3. Select the top n_select antibodies.
        best = population[:n_select]

        # 4. Clone & mutate: one mutated clone per selected antibody.
        clones = [b + random.randint(-mutation_range, mutation_range) for b in best]

        # 5. Form the next generation: elites + clones; trim back to pop_size.
        population = (best + clones)
        population.sort(key=lambda x: affinity(x, target))
        population = population[:pop_size]

        if verbose:
            top = population[0]
            print(f"  Gen {gen:>2}: best = {top:>4}  (distance to target: {affinity(top, target)})")

    return population[0]


def read_int(prompt, lo, hi, default=None):
    while True:
        raw = input(prompt).strip()
        if raw == "" and default is not None:
            return default
        try:
            v = int(raw)
            if lo <= v <= hi:
                return v
            print(f"  ERROR: must be in [{lo}, {hi}].")
        except ValueError:
            print("  ERROR: enter an integer.")


def main():
    print("=" * 60)
    print(" Clonal Selection Algorithm (interactive)")
    print(" Goal: evolve a population of integers toward a target value.")
    print("=" * 60)

    while True:
        target          = read_int("Target value to converge toward [-1000..1000] (default 42): ", -1000, 1000, 42)
        pop_size        = read_int("Population size (5-50, default 10): ", 5, 50, 10)
        generations     = read_int("Number of generations (1-100, default 10): ", 1, 100, 10)
        n_select        = read_int(f"Antibodies selected per gen (1-{pop_size}, default 3): ", 1, pop_size, min(3, pop_size))
        mutation_range  = read_int("Mutation range ±N (1-20, default 5): ", 1, 20, 5)

        verbose = input("Show every-generation progress? [y/N]: ").strip().lower() == "y"

        best = csa(target, pop_size, generations, n_select, mutation_range, verbose=verbose)

        print()
        print("=" * 60)
        print(f" RESULT: best antibody = {best}  (target was {target})")
        print(f"         distance to target = {affinity(best, target)}")
        print("=" * 60)

        if input("\nRun another experiment? [y/N]: ").strip().lower() != "y":
            print("Goodbye.")
            return


if __name__ == "__main__":
    main()
