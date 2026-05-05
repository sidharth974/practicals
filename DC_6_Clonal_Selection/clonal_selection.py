# DC-6: Clonal Selection Algorithm (CSA / CLONALG).
# Goal: evolve a binary string of N bits to maximise the number of 1s.
# Optimum is therefore the all-ones string [1,1,1,1,...,1].

import random


def fitness(antibody):
    """Number of 1s in the binary string -> bigger is better."""
    return sum(antibody)


def generate_antibody(size):
    """Return a random binary string of given length."""
    return [random.randint(0, 1) for _ in range(size)]


def initialize_population(pop_size, size):
    """Build the initial random population."""
    return [generate_antibody(size) for _ in range(pop_size)]


def select_best(population, num_selected):
    """Return the top `num_selected` antibodies, sorted by fitness desc."""
    population.sort(key=fitness, reverse=True)
    return population[:num_selected]


def clone_antibodies(selected, clone_factor):
    """Make several copies of each selected antibody (the cloning step)."""
    clones = []
    for antibody in selected:
        num_clones = int(clone_factor * len(selected))
        clones.extend([antibody.copy() for _ in range(num_clones)])
    return clones


def hypermutation(clones, mutation_rate):
    """Flip each bit with probability `mutation_rate` (somatic hypermutation)."""
    mutated = []
    for clone in clones:
        new_clone = clone[:]
        for i in range(len(clone)):
            if random.random() < mutation_rate:
                new_clone[i] = 1 - new_clone[i]      # bit flip
        mutated.append(new_clone)
    return mutated


def replace_worst(population, keep_size):
    """Keep top `keep_size` antibodies; refill rest with random new ones."""
    return population[:keep_size] + [
        generate_antibody(len(population[0]))
        for _ in range(len(population) - keep_size)
    ]


def clonal_selection(pop_size=10, size=8, generations=10,
                     clone_factor=2, mutation_rate=0.2):
    """Main CSA loop."""
    population = initialize_population(pop_size, size)

    for gen in range(generations):
        # Pick top 50% as breeders
        selected = select_best(population, num_selected=int(pop_size * 0.5))
        # Clone them
        clones = clone_antibodies(selected, clone_factor)
        # Hypermutate clones to explore neighbouring solutions
        mutated = hypermutation(clones, mutation_rate)
        # Compete: keep top pop_size from old + new
        population.extend(mutated)
        population = select_best(population, pop_size)
        # Refresh diversity by replacing worst 20% with random antibodies
        population = replace_worst(population, keep_size=int(pop_size * 0.8))

        best = max(population, key=fitness)
        print(f"Gen {gen+1:>2}: best fitness = {fitness(best)}, antibody = {best}")

    return max(population, key=fitness)


if __name__ == "__main__":
    best = clonal_selection()
    print(f"\nFinal best antibody: {best}  (fitness = {fitness(best)})")
