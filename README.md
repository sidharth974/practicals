# Computer Laboratory III (417534) — CL3 Practicals

Implementations for the SPPU 4th-year Computer Engineering subject **417534: Computer Laboratory III**, organised by the two streams it spans:

- **DC** — Distributed Computing (6 practicals)
- **CI** — Computational Intelligence (4 practicals)

Each folder has source code + its own `README.md` with run instructions, plus a `requirements.txt` where third-party libraries are needed.

## Index

### Distributed Computing (DC)
| # | Practical | Tech |
|---|-----------|------|
| 1 | [RPC Factorial](DC_1_RPC_Factorial/) | Python `xmlrpc` |
| 2 | [RMI String Concatenation](DC_2_RMI_StringConcat/) | Pyro5 + Name Server |
| 3 | [Fuzzy Logic](DC_3_Fuzzy_Logic/) | Python (set ops + Cartesian product + Max-Min composition) |
| 4 | [Load Balancing](DC_4_Load_Balancing/) | Python (Round Robin / Least Connections / Random) |
| 5 | [Genetic Algorithm for NN tuning](DC_5_Genetic_Algorithm/) | DEAP + PyTorch |
| 6 | [Clonal Selection Algorithm](DC_6_Clonal_Selection/) | Python |

### Computational Intelligence (CI)
| # | Practical | Tech |
|---|-----------|------|
| 1 | [AIS Damage Classification](CI_1_AIS_Damage/) | NumPy + scikit-learn |
| 2 | [DEAP Binary Optimization](CI_2_DEAP_Binary/) | DEAP |
| 3 | [MapReduce Hottest/Coolest Year](CI_3_MapReduce_Weather/) | Python `concurrent.futures` |
| 4 | [Ant Colony Optimization (TSP)](CI_4_ACO_TSP/) | NumPy |

## Global Setup
- Python 3.8+ is sufficient for everything (no Hadoop / no Java needed).
- Install third-party packages per-folder:
  ```bash
  pip install -r DC_2_RMI_StringConcat/requirements.txt   # Pyro5
  pip install -r DC_5_Genetic_Algorithm/requirements.txt  # DEAP, PyTorch, sklearn
  pip install -r CI_1_AIS_Damage/requirements.txt         # NumPy, scikit-learn
  pip install -r CI_2_DEAP_Binary/requirements.txt        # DEAP, NumPy
  ```

## Theory & Viva Prep
A complete viva-prep document covering theory, real-world examples, code walkthroughs, and Q&A is at [VIVA_THEORY.md](VIVA_THEORY.md) (and PDF [VIVA_THEORY.pdf](VIVA_THEORY.pdf)).
