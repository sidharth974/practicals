# DC-3: Fuzzy set operations and fuzzy relation composition.
# Operations: Union, Intersection, Complement, Difference, Cartesian Product,
# and Max-Min Composition of two fuzzy relations.
# Fuzzy sets are represented as dictionaries mapping element -> membership in [0,1].


def fuzzy_union(set_a, set_b):
    """Union: μ(x) = max(μA(x), μB(x)) over all elements in either set."""
    return {k: max(set_a.get(k, 0), set_b.get(k, 0)) for k in set_a.keys() | set_b.keys()}


def fuzzy_intersection(set_a, set_b):
    """Intersection: μ(x) = min(μA(x), μB(x)) over the common elements."""
    return {k: min(set_a.get(k, 0), set_b.get(k, 0)) for k in set_a.keys() & set_b.keys()}


def fuzzy_complement(set_a):
    """Complement: μA'(x) = 1 - μA(x) for every element of A."""
    return {k: round(1 - v, 4) for k, v in set_a.items()}


def fuzzy_difference(set_a, set_b):
    """Bounded difference: max(μA(x) - μB(x), 0)."""
    return {k: round(max(set_a.get(k, 0) - set_b.get(k, 0), 0), 4) for k in set_a.keys()}


def fuzzy_cartesian_product(set_a, set_b):
    """A x B: produces a fuzzy relation. μ(a,b) = min(μA(a), μB(b))."""
    return {(a, b): min(set_a[a], set_b[b]) for a in set_a for b in set_b}


def fuzzy_max_min_composition(relation_r, relation_s):
    """
    Max-Min composition R o S of two fuzzy relations.
    For each pair (a, c): μ(a,c) = max over b of  min(μR(a,b), μS(b,c)).
    """
    result = {}
    for (a, b1), v1 in relation_r.items():
        for (b2, c), v2 in relation_s.items():
            if b1 == b2:                                     # only matching middle elements
                m = min(v1, v2)
                result[(a, c)] = max(result.get((a, c), 0), m)
    return result


# ---------------- Demonstration with sample fuzzy sets ----------------

if __name__ == "__main__":
    # Three fuzzy sets defined as dictionaries (element -> membership in [0,1]).
    set_a = {'a': 0.5, 'b': 0.8, 'c': 0.2}
    set_b = {'b': 0.6, 'c': 0.7, 'd': 0.3}
    set_c = {'c': 0.9, 'd': 0.4}

    print("Set A :", set_a)
    print("Set B :", set_b)
    print("Set C :", set_c)
    print()

    # Operations on A and B
    print("Union (A ∪ B)        :", fuzzy_union(set_a, set_b))
    print("Intersection (A ∩ B) :", fuzzy_intersection(set_a, set_b))
    print("Complement of A      :", fuzzy_complement(set_a))
    print("Difference (A − B)   :", fuzzy_difference(set_a, set_b))
    print()

    # Build two fuzzy relations via Cartesian product, then compose them.
    relation_ab = fuzzy_cartesian_product(set_a, set_b)
    relation_bc = fuzzy_cartesian_product(set_b, set_c)
    print("Fuzzy Relation R = A x B :", relation_ab)
    print("Fuzzy Relation S = B x C :", relation_bc)

    composition = fuzzy_max_min_composition(relation_ab, relation_bc)
    print("\nMax-Min Composition (R o S):", composition)
