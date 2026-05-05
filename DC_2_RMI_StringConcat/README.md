# DC-2: RMI String Concatenation (Pyro5 + Name Server)

**Aim:** Distributed application using Python remote objects where the client passes two strings and the server returns their concatenation. Lookup is by **name** through the Pyro name server.

**Tech:** Pyro5 (`pip install Pyro5`).

## Run
**Terminal 1 — start the name server:**
```bash
pyro5-ns
```
**Terminal 2 — start the service:**
```bash
python server.py
```
**Terminal 3 — client:**
```bash
python client.py
```

## Expected
```
Enter first string : hello
Enter second string: world
Concatenated string: helloworld
```
