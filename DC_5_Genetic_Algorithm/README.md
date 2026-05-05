# DC-5: Genetic Algorithm with DEAP

**Aim:** Use a Genetic Algorithm (DEAP framework) to evolve a population of real-valued vectors toward the minimum of the Sphere function `f(x) = Σ xᵢ²`.

**Tech:** Python + DEAP + NumPy. No PyTorch, no scikit-learn.

## Run
```bash
pip install -r requirements.txt
python genetic_algorithm.py
```

## What you'll see
30 generations of evolution. Each line shows generation number, evaluations, average fitness, and minimum fitness. The best individual at the end should have all genes near zero with fitness near zero (the global optimum of the Sphere function).
