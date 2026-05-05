# Interactive Load Balancer Simulator
# Lets the user configure servers, request count, and the algorithm,
# then simulates request distribution and prints per-server stats.

import random


# ---------- algorithms ----------

def round_robin(servers, n):
    """Cycle through servers in order: 0, 1, 2, 0, 1, 2, ..."""
    return [servers[i % len(servers)] for i in range(n)]


def random_pick(servers, n):
    """Pick a server uniformly at random for each request."""
    return [random.choice(servers) for _ in range(n)]


def least_connections(servers, n):
    """Send each new request to the server currently handling the fewest."""
    counts = {s: 0 for s in servers}
    assignments = []
    for _ in range(n):
        target = min(counts, key=counts.get)
        counts[target] += 1
        assignments.append(target)
    return assignments


def weighted_round_robin(server_weights, n):
    """
    Round robin where servers with higher weights get more turns.
    server_weights is a list of (name, weight) tuples.
    """
    expanded = []
    for name, w in server_weights:
        expanded.extend([name] * w)
    return [expanded[i % len(expanded)] for i in range(n)]


# ---------- input helpers ----------

def read_int(prompt, lo, hi):
    while True:
        try:
            v = int(input(prompt))
            if lo <= v <= hi:
                return v
            print(f"  ERROR: must be between {lo} and {hi}.")
        except ValueError:
            print("  ERROR: enter an integer.")


def read_servers():
    n = read_int("How many servers? (2-10): ", 2, 10)
    servers = []
    for i in range(n):
        name = input(f"  Name of server {i+1} [default Server{i+1}]: ").strip() or f"Server{i+1}"
        servers.append(name)
    return servers


def read_weights(servers):
    print("Enter a positive integer weight for each server (higher = more requests):")
    weights = []
    for s in servers:
        w = read_int(f"  weight for {s}: ", 1, 100)
        weights.append((s, w))
    return weights


# ---------- presentation ----------

def show_distribution(assignments):
    counts = {}
    for s in assignments:
        counts[s] = counts.get(s, 0) + 1
    total = len(assignments)

    print("\nDistribution:")
    print(f"  {'SERVER':<15} {'REQUESTS':>10} {'%':>8}   BAR")
    print("  " + "-" * 50)
    for s, c in sorted(counts.items(), key=lambda x: -x[1]):
        pct = 100 * c / total
        bar = "█" * int(pct / 2)            # one block ≈ 2%
        print(f"  {s:<15} {c:>10} {pct:>7.1f}%  {bar}")
    print("  " + "-" * 50)
    print(f"  {'TOTAL':<15} {total:>10}\n")


def show_trace(assignments, limit=20):
    """Show the first `limit` request-to-server assignments."""
    print(f"\nFirst {min(limit, len(assignments))} request assignments:")
    for i, s in enumerate(assignments[:limit], 1):
        print(f"  Request {i:>3} -> {s}")
    if len(assignments) > limit:
        print(f"  ... ({len(assignments) - limit} more)")


# ---------- menu ----------

def main():
    print("=" * 60)
    print(" Load Balancer Simulator")
    print("=" * 60)

    servers = read_servers()
    requests = read_int("Number of incoming requests (1-1000): ", 1, 1000)

    while True:
        print("\nAlgorithms:")
        print("  1) Round Robin")
        print("  2) Random")
        print("  3) Least Connections")
        print("  4) Weighted Round Robin")
        print("  5) Compare ALL on the same workload")
        print("  6) Reconfigure (servers / request count)")
        print("  7) Exit")
        choice = input("Choose [1-7]: ").strip()

        if choice == "1":
            a = round_robin(servers, requests)
            show_trace(a); show_distribution(a)
        elif choice == "2":
            a = random_pick(servers, requests)
            show_trace(a); show_distribution(a)
        elif choice == "3":
            a = least_connections(servers, requests)
            show_trace(a); show_distribution(a)
        elif choice == "4":
            weights = read_weights(servers)
            a = weighted_round_robin(weights, requests)
            show_trace(a); show_distribution(a)
        elif choice == "5":
            for name, fn in [("ROUND ROBIN", round_robin),
                             ("RANDOM",       random_pick),
                             ("LEAST CONN",   least_connections)]:
                print(f"\n--- {name} ---")
                show_distribution(fn(servers, requests))
        elif choice == "6":
            servers = read_servers()
            requests = read_int("Number of requests (1-1000): ", 1, 1000)
        elif choice == "7":
            print("Goodbye.")
            return
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
