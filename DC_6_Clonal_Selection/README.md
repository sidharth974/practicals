# DC-6: Clonal Selection Algorithm

**Aim:** Implement the immune-inspired Clonal Selection Algorithm (CSA / CLONALG) to evolve a binary string of N bits toward the all-ones optimum.

**Tech:** Plain Python.

## Run
```bash
python clonal_selection.py
```

## Steps the algorithm performs each generation
1. Sort antibodies by fitness (number of 1s).
2. Select the top 50% (the highest-affinity ones).
3. Clone them — better antibodies get more clones.
4. Hypermutate the clones (random bit flips).
5. Re-rank the combined pool, keep the best `pop_size`.
6. Replace the worst 20% with random new antibodies for diversity.
