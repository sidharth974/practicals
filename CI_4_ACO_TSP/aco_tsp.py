# CI-4: Ant Colony Optimization (ACO) for the Travelling Salesman Problem.
# Many "ants" build candidate tours guided by pheromone strength and an
# inverse-distance heuristic. Pheromone evaporates each iteration and ants
# deposit additional pheromone proportional to 1/length on the tour they took.
# Over time the colony converges on a short tour.

import numpy as np


class AntColonyOptimizer:
    def __init__(self, distances, n_ants, n_iterations, decay,
                 alpha=1, beta=2):
        # Distance matrix and ACO parameters.
        self.distances     = distances
        self.n_ants        = n_ants
        self.n_iterations  = n_iterations
        self.decay         = decay              # pheromone evaporation factor (0..1)
        self.alpha         = alpha              # pheromone weight in transition rule
        self.beta          = beta               # heuristic weight (1/distance)
        self.n_cities      = distances.shape[0]
        # Start with equal pheromone on every edge.
        self.pheromones    = np.ones((self.n_cities, self.n_cities))

    def _select_next_city(self, current_city, visited):
        """Pick the next city using probability ∝ τ^α × (1/d)^β."""
        probabilities = np.zeros(self.n_cities)
        for city in range(self.n_cities):
            if city not in visited:
                probabilities[city] = (
                    self.pheromones[current_city, city] ** self.alpha
                    * (1 / self.distances[current_city, city]) ** self.beta
                )
        probabilities /= probabilities.sum()
        return np.random.choice(range(self.n_cities), p=probabilities)

    def _construct_solution(self):
        """Each ant builds a complete tour (returns to its start city)."""
        solutions, lengths = [], []
        for _ in range(self.n_ants):
            tour = [np.random.randint(self.n_cities)]
            while len(tour) < self.n_cities:
                tour.append(self._select_next_city(tour[-1], tour))
            tour.append(tour[0])                # close the loop
            solutions.append(tour)
            length = sum(
                self.distances[tour[i], tour[i + 1]] for i in range(self.n_cities)
            )
            lengths.append(length)
        return solutions, lengths

    def _update_pheromones(self, solutions, lengths):
        """Evaporation, then deposit ∝ 1/length on each tour's edges."""
        self.pheromones *= self.decay
        for tour, length in zip(solutions, lengths):
            for i in range(self.n_cities):
                self.pheromones[tour[i], tour[i + 1]] += 1.0 / length

    def optimize(self):
        """Main loop: repeat construct → update for n_iterations."""
        best_solution, best_length = None, float("inf")
        for it in range(self.n_iterations):
            solutions, lengths = self._construct_solution()
            self._update_pheromones(solutions, lengths)

            min_len = min(lengths)
            if min_len < best_length:
                best_length   = min_len
                best_solution = solutions[lengths.index(min_len)]

            print(f"Iteration {it+1:>3}: best length so far = {best_length}")

        return best_solution, best_length


# -------- demo --------

if __name__ == "__main__":
    # Symmetric 4-city distance matrix.
    distance_matrix = np.array([
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0],
    ])

    aco = AntColonyOptimizer(
        distance_matrix,
        n_ants=10,
        n_iterations=50,
        decay=0.9,        # 10% evaporation per iteration
        alpha=1, beta=2,
    )
    best_path, best_length = aco.optimize()

    print(f"\nBest path found : {best_path}")
    print(f"Best path length: {best_length}")
