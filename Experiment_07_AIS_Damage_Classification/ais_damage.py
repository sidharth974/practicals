# Artificial Immune System (AIS) - Structural Damage Pattern Recognition
# Antigens  -> incoming structural data points (0 = normal, 1 = damaged)
# Antibodies -> randomly initialised detectors that try to match antigens
# Affinity   -> similarity measure (here, 1 - |antigen - antibody|; we use distance directly)
# For each antigen we pick the antibody with the highest affinity (smallest distance).

import random

# Sample structural sensor readings: 0 = normal, 1 = damage detected.
data = [0, 0, 1, 0, 1, 1, 0]

# Random initial population of antibody detectors with values in [0, 1].
antibodies = [random.random() for i in range(5)]

# For each antigen find the antibody with the smallest absolute distance
# (equivalent to highest affinity). This is the "recognition" step.
for antigen in data:
    best = min(antibodies, key=lambda x: abs(x - antigen))

    # Print the antigen and the antibody that best matches it -- this is the classification.
    print("Antigen:", antigen, "Matched Antibody:", best)

print("Classification Completed")
