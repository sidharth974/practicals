# CI-1: AIS Pattern Recognition for Structural Damage

**Aim:** Apply Artificial Immune System (AIS) pattern recognition for damage classification.

**Tech:** Python + NumPy + scikit-learn.

## Run
```bash
pip install -r requirements.txt
python ais_damage.py
```

## Method
Detectors are drawn from the NORMAL class and mutated; at test time each sample is classified by comparing distance to the nearest detector against the mean detector distance.
