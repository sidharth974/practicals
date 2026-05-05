# Interactive Fuzzy Set Operations
# Lets the user define two fuzzy sets A and B (membership values in [0,1])
# and then apply union / intersection / complement / difference on demand.

# ---------- core operations (one-line each, applied element-wise) ----------

def fuzzy_union(a, b):
    # Union µ(A∪B)(x) = max(µA(x), µB(x))
    return [max(x, y) for x, y in zip(a, b)]

def fuzzy_intersection(a, b):
    # Intersection µ(A∩B)(x) = min(µA(x), µB(x))
    return [min(x, y) for x, y in zip(a, b)]

def fuzzy_complement(a):
    # Complement µA'(x) = 1 - µA(x)
    return [round(1 - x, 4) for x in a]

def fuzzy_difference(a, b):
    # Difference  A - B = min(µA(x), 1 - µB(x))
    return [round(min(x, 1 - y), 4) for x, y in zip(a, b)]


# ---------- input helpers ----------

def read_set(name, n):
    """Read n membership values for a named fuzzy set with validation."""
    while True:
        raw = input(f"  Enter {n} membership values for set {name} "
                    f"(space-separated, each in [0,1]): ").strip().split()
        if len(raw) != n:
            print(f"  ERROR: expected {n} values, got {len(raw)}.")
            continue
        try:
            vals = [float(x) for x in raw]
        except ValueError:
            print("  ERROR: values must be numeric.")
            continue
        if any(v < 0 or v > 1 for v in vals):
            print("  ERROR: every value must be between 0 and 1 inclusive.")
            continue
        return vals


def read_int(prompt, lo, hi):
    """Read an integer in [lo, hi] with re-prompting on bad input."""
    while True:
        try:
            v = int(input(prompt))
            if lo <= v <= hi:
                return v
            print(f"  ERROR: must be between {lo} and {hi}.")
        except ValueError:
            print("  ERROR: please enter an integer.")


def show(name, values):
    """Pretty-print a fuzzy set."""
    print(f"  {name:18s} = {values}")


# ---------- menu ----------

def main():
    print("=" * 60)
    print(" Interactive Fuzzy Set Operations")
    print("=" * 60)

    n = read_int("How many elements in each set? (1-10): ", 1, 10)
    A = read_set("A", n)
    B = read_set("B", n)

    while True:
        print()
        show("Set A", A)
        show("Set B", B)
        print("\nMenu:")
        print("  1) Union  (A ∪ B)")
        print("  2) Intersection  (A ∩ B)")
        print("  3) Complement of A")
        print("  4) Complement of B")
        print("  5) Difference  (A − B)")
        print("  6) Difference  (B − A)")
        print("  7) Show ALL operations at once")
        print("  8) Re-enter sets")
        print("  9) Exit")
        choice = input("Choose [1-9]: ").strip()

        if choice == "1":
            show("A ∪ B", fuzzy_union(A, B))
        elif choice == "2":
            show("A ∩ B", fuzzy_intersection(A, B))
        elif choice == "3":
            show("A'", fuzzy_complement(A))
        elif choice == "4":
            show("B'", fuzzy_complement(B))
        elif choice == "5":
            show("A − B", fuzzy_difference(A, B))
        elif choice == "6":
            show("B − A", fuzzy_difference(B, A))
        elif choice == "7":
            show("A ∪ B", fuzzy_union(A, B))
            show("A ∩ B", fuzzy_intersection(A, B))
            show("A'",    fuzzy_complement(A))
            show("B'",    fuzzy_complement(B))
            show("A − B", fuzzy_difference(A, B))
            show("B − A", fuzzy_difference(B, A))
        elif choice == "8":
            n = read_int("How many elements in each set? (1-10): ", 1, 10)
            A = read_set("A", n)
            B = read_set("B", n)
        elif choice == "9":
            print("Goodbye.")
            return
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
