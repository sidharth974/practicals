# Fuzzy Set Operations
# A fuzzy set assigns each element a membership degree in [0, 1] (not just 0/1 like classical sets).
# Operations are applied element-wise on two equally-sized membership lists A and B.

# Two fuzzy sets represented as parallel lists of membership values for the same universe.
A = [0.2, 0.5, 0.7, 0.9]
B = [0.3, 0.6, 0.4, 0.8]

# Result containers, one entry per element of the universe.
union = []
intersection = []
complement = []
difference = []

for i in range(len(A)):
    # Union  µ(A∪B)(x) = max(µA(x), µB(x))  -> "either" membership.
    union.append(max(A[i], B[i]))

    # Intersection  µ(A∩B)(x) = min(µA(x), µB(x))  -> "both" membership.
    intersection.append(min(A[i], B[i]))

    # Complement  µA'(x) = 1 - µA(x)  -> "not in A".
    complement.append(1 - A[i])

    # Difference  A - B = min(µA(x), 1 - µB(x))  -> "in A but not in B".
    difference.append(min(A[i], 1 - B[i]))

# Display results.
print("Set A      :", A)
print("Set B      :", B)
print("Union      :", union)
print("Intersection:", intersection)
print("Complement of A:", complement)
print("Difference (A-B):", difference)
