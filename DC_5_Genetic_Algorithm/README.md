# DC-5: Genetic Algorithm for Neural-Network Hyperparameter Tuning

**Aim:** Use a Genetic Algorithm (DEAP framework) to evolve the best
hyperparameters (hidden neurons, learning rate, activation function)
for a small PyTorch neural network on a regression task.

**Tech:** Python + DEAP + PyTorch + scikit-learn.

## Run
```bash
pip install -r requirements.txt
python genetic_algorithm.py
```

## What you'll see
A 10-generation GA evolving 10 individuals. Per generation, DEAP prints
how many evaluations were done and the best fitness so far. At the end
the script prints the best hyperparameters and their test MSE.
