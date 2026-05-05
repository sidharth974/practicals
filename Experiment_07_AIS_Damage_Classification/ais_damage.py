# Interactive Artificial Immune System (AIS) - Structural Damage Classifier
# - Antigens   = sensor readings from a structure (numeric)
# - Antibodies = learned detectors that recognise "damaged" patterns
# - Affinity   = closeness between an antigen and an antibody (smaller = better match)
#
# Workflow:
#   1. The user "trains" the system by labelling some sensor readings as
#      damaged (1) or normal (0). The system grows antibodies for each class.
#   2. The user then enters new readings and the system classifies them.

import random


# ---------- training & classification ----------

def train(samples, n_antibodies_per_class=5, mutation_range=0.05):
    """
    samples: list of (reading, label) where label is 0 (normal) or 1 (damaged).
    Returns two antibody pools: one for normal, one for damaged readings.
    """
    normals  = [r for r, lab in samples if lab == 0]
    damaged  = [r for r, lab in samples if lab == 1]

    def grow(seed_pool):
        # Make antibodies by randomly perturbing real labelled samples.
        if not seed_pool:
            return []
        return [random.choice(seed_pool) + random.uniform(-mutation_range, mutation_range)
                for _ in range(n_antibodies_per_class)]

    return grow(normals), grow(damaged)


def classify(reading, normal_pool, damaged_pool):
    """Return 'NORMAL' or 'DAMAGED' based on which pool has the closest antibody."""
    def best_distance(pool):
        return min(abs(reading - ab) for ab in pool) if pool else float("inf")
    return "NORMAL" if best_distance(normal_pool) < best_distance(damaged_pool) else "DAMAGED"


# ---------- input ----------

def read_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("  ERROR: enter a number.")


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


# ---------- menu ----------

def main():
    print("=" * 60)
    print(" Artificial Immune System — Structural Damage Classifier")
    print("=" * 60)
    print(" Sensor readings:")
    print("   ~0.0 typically means NORMAL structure")
    print("   ~1.0 typically means DAMAGED structure")
    print()

    # Pre-loaded sample dataset to make the demo runnable without manual entry.
    samples = [(0.05, 0), (0.10, 0), (0.08, 0), (0.12, 0),
               (0.92, 1), (0.85, 1), (0.95, 1), (0.88, 1)]
    print(f" Pre-loaded training set ({len(samples)} samples):")
    for r, lab in samples:
        print(f"   reading {r:>5}  ->  {'DAMAGED' if lab else 'NORMAL'}")

    n_anti = read_int("\nAntibodies per class (1-20, default 5): ", 1, 20, 5)
    normal_pool, damaged_pool = train(samples, n_antibodies_per_class=n_anti)
    print(f"\n Trained.  normal antibodies: {len(normal_pool)}, "
          f"damaged antibodies: {len(damaged_pool)}")

    # Main menu loop
    while True:
        print("\nMenu:")
        print("  1) Classify a single sensor reading")
        print("  2) Classify a batch of readings (space-separated)")
        print("  3) Add a new training sample and retrain")
        print("  4) Show current antibody pools")
        print("  5) Exit")
        choice = input("Choose [1-5]: ").strip()

        if choice == "1":
            r = read_float("  Reading [0..1]: ")
            verdict = classify(r, normal_pool, damaged_pool)
            print(f"  -> {r}  classified as  {verdict}")

        elif choice == "2":
            raw = input("  Enter readings: ").strip().split()
            try:
                vals = [float(x) for x in raw]
            except ValueError:
                print("  ERROR: all values must be numbers.")
                continue
            print(f"\n  {'READING':>10}  {'VERDICT':<10}")
            print("  " + "-" * 24)
            for v in vals:
                print(f"  {v:>10.4f}  {classify(v, normal_pool, damaged_pool):<10}")

        elif choice == "3":
            r = read_float("  Reading: ")
            lab = read_int("  Label (0=NORMAL, 1=DAMAGED): ", 0, 1)
            samples.append((r, lab))
            normal_pool, damaged_pool = train(samples, n_antibodies_per_class=n_anti)
            print(f"  Sample added. Now have {len(samples)} training samples.")

        elif choice == "4":
            print(f"\n  Normal antibodies  ({len(normal_pool)}): "
                  f"{[round(a, 3) for a in normal_pool]}")
            print(f"  Damaged antibodies ({len(damaged_pool)}): "
                  f"{[round(a, 3) for a in damaged_pool]}")

        elif choice == "5":
            print("Goodbye.")
            return

        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
