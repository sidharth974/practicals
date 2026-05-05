# CI-1: Artificial Immune System (AIS) classifier for structural damage detection.
# - "Detectors" are sampled from the NORMAL class, then mutated.
# - At classification time, a sample is labelled DAMAGED if its nearest detector
#   is unusually far away (i.e., further than the average detector distance) --
#   a simple anomaly-detection rule inspired by the Negative-Selection idea.

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


class ArtificialImmuneClassifier:
    """Tiny AIS-style anomaly classifier."""

    def __init__(self, num_detectors=50, mutation_rate=0.05):
        self.num_detectors = num_detectors
        self.mutation_rate = mutation_rate
        self.detectors = None

    def generate_detectors(self, X_train, y_train):
        """Pick `num_detectors` samples from the NORMAL class (label 0)."""
        normal_samples = X_train[y_train == 0]
        idx = np.random.choice(len(normal_samples), self.num_detectors, replace=False)
        self.detectors = normal_samples[idx].astype(float)

    def mutate_detectors(self):
        """Add a small Gaussian perturbation to every detector (hypermutation)."""
        self.detectors += self.mutation_rate * np.random.randn(*self.detectors.shape)

    def classify(self, X):
        """
        For each sample compute distances to all detectors. If the nearest
        detector is FURTHER than the mean detector distance, the sample is
        considered DAMAGED (anomalous); otherwise NORMAL.
        """
        labels = []
        for sample in X:
            distances = np.linalg.norm(self.detectors - sample, axis=1)
            labels.append(1 if distances.min() > distances.mean() else 0)
        return np.array(labels)


def main():
    # Synthetic dataset: 200 samples, 5 features. A simple threshold rule
    # decides damage so we have a reproducible target.
    np.random.seed(42)
    X = np.random.rand(200, 5)
    y = np.where(X[:, 0] + X[:, 1] > 1, 1, 0)        # 1 = damaged, 0 = normal

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    clf = ArtificialImmuneClassifier(num_detectors=50, mutation_rate=0.05)
    clf.generate_detectors(X_train, y_train)
    clf.mutate_detectors()

    y_pred = clf.classify(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print(f"Test samples            : {len(y_test)}")
    print(f"Predicted DAMAGED count : {int((y_pred == 1).sum())}")
    print(f"Actual    DAMAGED count : {int((y_test == 1).sum())}")
    print(f"Accuracy                : {accuracy:.2f}")


if __name__ == "__main__":
    main()
