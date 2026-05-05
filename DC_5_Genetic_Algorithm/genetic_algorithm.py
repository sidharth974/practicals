# DC-5: Genetic Algorithm for hyperparameter tuning of a small neural network.
# We use DEAP to evolve a population where each "individual" encodes:
#   [num_hidden_neurons, learning_rate, activation_function]
# Fitness = test-set MSE loss (lower is better) on a tiny synthetic regression task.

import random
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from deap import base, creator, tools, algorithms


# ----------------- Neural network used for evaluation -----------------

class SimpleNN(nn.Module):
    """One hidden-layer feed-forward network: 3 -> hidden -> 1."""

    def __init__(self, num_neurons, activation):
        super().__init__()
        self.hidden = nn.Linear(3, num_neurons)
        self.output = nn.Linear(num_neurons, 1)
        # Pick activation function based on the gene
        self.activation = {
            "relu":    nn.ReLU(),
            "tanh":    nn.Tanh(),
            "sigmoid": nn.Sigmoid(),
        }[activation]

    def forward(self, x):
        return self.output(self.activation(self.hidden(x)))


# ----------------- Fitness function -----------------

def objective(individual, X_tr, y_tr, X_te, y_te):
    """
    Train the network with the given hyperparameters for a few epochs;
    return its test MSE as the fitness (lower = better; GA minimises).
    """
    num_neurons, lr, activation = individual
    model = SimpleNN(int(num_neurons), activation)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=float(lr))

    X_tr_t = torch.tensor(X_tr, dtype=torch.float32)
    y_tr_t = torch.tensor(y_tr, dtype=torch.float32).view(-1, 1)
    X_te_t = torch.tensor(X_te, dtype=torch.float32)
    y_te_t = torch.tensor(y_te, dtype=torch.float32).view(-1, 1)

    # Short training loop -- enough to differentiate hyperparameters.
    for _ in range(50):
        optimizer.zero_grad()
        loss = criterion(model(X_tr_t), y_tr_t)
        loss.backward()
        optimizer.step()

    # Evaluate on test set
    model.eval()
    with torch.no_grad():
        test_loss = criterion(model(X_te_t), y_te_t).item()

    return (test_loss,)                                  # DEAP needs a tuple


# ----------------- DEAP setup -----------------

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))      # minimisation
creator.create("Individual", list, fitness=creator.FitnessMin)


def make_individual():
    """Random (num_neurons, learning_rate, activation) triple."""
    return [
        random.randint(5, 100),                          # hidden-layer size
        random.uniform(0.0001, 0.01),                    # learning rate
        random.choice(["relu", "tanh", "sigmoid"]),      # activation
    ]


def mutate(individual):
    """Gaussian mutation on numeric genes; small chance to flip activation."""
    individual[0] = max(5, min(100, individual[0] + int(random.gauss(0, 10))))
    individual[1] = max(0.0001, min(0.01, individual[1] + random.gauss(0, 0.005)))
    if random.random() < 0.2:
        individual[2] = random.choice(["relu", "tanh", "sigmoid"])
    return (individual,)


# ----------------- Main GA driver -----------------

def main():
    # Create a tiny synthetic regression dataset.
    X = np.random.rand(100, 3)
    y = np.random.rand(100)
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=0)

    toolbox = base.Toolbox()
    toolbox.register("individual", tools.initIterate, creator.Individual, make_individual)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", objective, X_tr=X_tr, y_tr=y_tr, X_te=X_te, y_te=y_te)
    toolbox.register("mate",   tools.cxTwoPoint)
    toolbox.register("mutate", mutate)
    toolbox.register("select", tools.selTournament, tournsize=3)

    population = toolbox.population(n=10)

    # Run a 10-generation evolutionary loop with crossover prob 0.7, mutation prob 0.2.
    algorithms.eaSimple(
        population, toolbox,
        cxpb=0.7, mutpb=0.2,
        ngen=10, verbose=True,
    )

    best = tools.selBest(population, k=1)[0]
    print("\nBest hyperparameters found:")
    print(f"  hidden neurons     : {best[0]}")
    print(f"  learning rate      : {best[1]:.6f}")
    print(f"  activation function: {best[2]}")
    print(f"  test loss (MSE)    : {best.fitness.values[0]:.6f}")


if __name__ == "__main__":
    main()
