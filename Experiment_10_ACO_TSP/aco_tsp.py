# Interactive Ant Colony Optimization (ACO) for the Traveling Salesman Problem
# The user picks the city setup, ant count, iterations, and ACO parameters.
# Each iteration prints the best tour found so far.

import random
import math


# ---------- distance matrix construction ----------

def random_cities(n, max_coord=100):
    """Generate n random 2-D city coordinates."""
    return [(random.randint(0, max_coord), random.randint(0, max_coord)) for _ in range(n)]


def distance_matrix(cities):
    """Euclidean-distance matrix from a list of (x,y) coordinates."""
    n = len(cities)
    dist = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                dx = cities[i][0] - cities[j][0]
                dy = cities[i][1] - cities[j][1]
                dist[i][j] = math.hypot(dx, dy)
    return dist


def manual_distance_matrix(n):
    """Read an n x n distance matrix from the user."""
    print(f"  Enter {n} rows of {n} numbers (space-separated). 0 on the diagonal.")
    matrix = []
    for i in range(n):
        while True:
            row = input(f"  row {i+1}: ").split()
            if len(row) != n:
                print(f"  ERROR: need {n} values."); continue
            try:
                matrix.append([float(x) for x in row])
                break
            except ValueError:
                print("  ERROR: values must be numeric.")
    return matrix


# ---------- ACO core ----------

def tour_length(tour, dist):
    total = sum(dist[tour[i]][tour[i+1]] for i in range(len(tour) - 1))
    total += dist[tour[-1]][tour[0]]   # return to start
    return total


def choose_next_city(current, unvisited, pheromone, dist, alpha, beta):
    """Probabilistically pick the next city using pheromone^alpha * (1/dist)^beta."""
    weights = []
    for j in unvisited:
        tau = pheromone[current][j] ** alpha
        eta = (1.0 / dist[current][j]) ** beta if dist[current][j] > 0 else 0
        weights.append(tau * eta)

    total = sum(weights)
    if total == 0:
        return random.choice(unvisited)

    r = random.random() * total
    acc = 0
    for j, w in zip(unvisited, weights):
        acc += w
        if acc >= r:
            return j
    return unvisited[-1]


def aco(dist, n_ants, iterations, alpha, beta, evap, q, verbose=True):
    n = len(dist)
    pheromone = [[1.0] * n for _ in range(n)]

    best_tour, best_len = None, float("inf")

    for it in range(1, iterations + 1):
        all_tours = []

        # Each ant constructs a complete tour.
        for _ in range(n_ants):
            start = random.randrange(n)
            tour = [start]
            unvisited = list(range(n))
            unvisited.remove(start)
            while unvisited:
                nxt = choose_next_city(tour[-1], unvisited, pheromone, dist, alpha, beta)
                tour.append(nxt)
                unvisited.remove(nxt)
            length = tour_length(tour, dist)
            all_tours.append((tour, length))

            if length < best_len:
                best_len, best_tour = length, tour

        # Pheromone evaporation
        for i in range(n):
            for j in range(n):
                pheromone[i][j] *= (1 - evap)

        # Pheromone deposit (each ant lays Q/length on its tour edges)
        for tour, length in all_tours:
            deposit = q / length
            for i in range(len(tour) - 1):
                a, b = tour[i], tour[i+1]
                pheromone[a][b] += deposit
                pheromone[b][a] += deposit
            pheromone[tour[-1]][tour[0]] += deposit
            pheromone[tour[0]][tour[-1]] += deposit

        if verbose:
            print(f"  Iter {it:>3}: best length so far = {best_len:.2f}")

    return best_tour, best_len


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
    print(" Ant Colony Optimization — Travelling Salesman Problem")
    print("=" * 60)

    while True:
        print("\nCity setup:")
        print("  1) Use the bundled 5-city sample matrix")
        print("  2) Generate N random 2-D cities")
        print("  3) Enter your own distance matrix manually")
        sub = input("Choose [1-3] (default 2): ").strip() or "2"

        if sub == "1":
            dist = [[0, 2, 9, 10, 7],
                    [2, 0, 6,  4, 3],
                    [9, 6, 0,  8, 5],
                    [10,4, 8,  0, 6],
                    [7, 3, 5,  6, 0]]
            n = 5
            print("  Loaded 5x5 sample matrix.")
        elif sub == "2":
            n = read_int("  Number of cities (3-20, default 8): ", 3, 20, 8)
            cities = random_cities(n)
            print(f"  Cities (x,y): {cities}")
            dist = distance_matrix(cities)
        elif sub == "3":
            n = read_int("  Number of cities (3-15): ", 3, 15)
            dist = manual_distance_matrix(n)
        else:
            print("Invalid option."); continue

        n_ants     = read_int(f"  Number of ants (1-{4*n}, default {n}): ", 1, 4*n, n)
        iters      = read_int("  Iterations (1-200, default 30): ", 1, 200, 30)
        alpha      = read_float("  Alpha (pheromone weight, default 1.0): ", 0.1, 5.0, 1.0)
        beta       = read_float("  Beta  (heuristic weight, default 2.0): ", 0.1, 5.0, 2.0)
        evap       = read_float("  Evaporation rate 0..1 (default 0.5): ", 0.0, 1.0, 0.5)
        q          = read_float("  Pheromone deposit Q (default 100): ", 1.0, 1000.0, 100.0)
        verbose    = input("  Show per-iteration progress? [y/N]: ").strip().lower() == "y"

        best_tour, best_len = aco(dist, n_ants, iters, alpha, beta, evap, q, verbose=verbose)

        print()
        print("=" * 60)
        print(" RESULT")
        print("=" * 60)
        print(f"  Best tour      : {' -> '.join(str(c) for c in best_tour)} -> {best_tour[0]}")
        print(f"  Tour length    : {best_len:.2f}")
        print("=" * 60)

        if input("\nRun another? [y/N]: ").strip().lower() != "y":
            print("Goodbye.")
            return


if __name__ == "__main__":
    main()
