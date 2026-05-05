# CI-2: Distributed Evolutionary Algorithm with DEAP

**Aim:** Use DEAP (Distributed Evolutionary Algorithms in Python) to evolve a 10-bit binary string toward the all-ones optimum (the OneMax problem).

**Tech:** Python + DEAP.

## Run
```bash
pip install -r requirements.txt
python deap_binary.py
```

## What you'll see
20 generations of evolution. Each line shows generation number, evaluations, average fitness, and max fitness. Optimum is reached when `max = 10`.
