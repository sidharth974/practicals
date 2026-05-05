# Experiment 1: RPC Factorial

**Aim:** Distributed application using RPC where the client sends an integer to the server and receives the factorial back.

**Tech:** Python + Pyro4 (Python Remote Objects).

## Requirements
- Python 3.6+
- Pyro4 library (see `requirements.txt`)

## Setup
```bash
pip install -r requirements.txt
```

## How to run
Open **two terminals** in this folder:

**Terminal 1 — Server**
```bash
python server.py
```
Copy the URI it prints, e.g. `PYRO:obj_xxxx@localhost:port`.

**Terminal 2 — Client**
```bash
python client.py
```
Paste the URI when prompted, then enter a number.

## Expected Output
```
Enter server uri: PYRO:obj_xxxx@localhost:39845
Enter number: 5
Factorial = 120
```
