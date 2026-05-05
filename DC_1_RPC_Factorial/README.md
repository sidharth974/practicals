# DC-1: RPC Factorial

**Aim:** Implement a distributed application using RPC where the client sends an integer and the server returns its factorial.

**Tech:** Python's built-in `xmlrpc.server` / `xmlrpc.client` — no third-party libraries.

## Run
**Terminal 1 (server):**
```bash
python server.py
```
**Terminal 2 (client):**
```bash
python client.py
```
Enter numbers; type `q` to quit.

## Expected
```
Enter a non-negative integer: 5
  5! = 120
```
