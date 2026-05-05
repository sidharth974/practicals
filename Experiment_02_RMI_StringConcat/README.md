# Experiment 2: RMI String Concatenation

**Aim:** Distributed application using Java RMI where the client sends two strings and the server returns the concatenation.

**Tech:** Java RMI (`java.rmi`).

## Requirements
- JDK 8 or higher (`javac`, `java` on PATH)
- No third-party libraries

## Files
- `StringConcat.java` — remote interface
- `Server.java` — server implementation (embeds the RMI registry, no separate `rmiregistry` needed)
- `Client.java` — client that looks up and calls the remote method

## How to run
Open a terminal in this folder.

```bash
# 1. Compile all files
javac StringConcat.java Server.java Client.java

# 2. Start the server (it spawns the registry on port 1099 itself)
java Server
```

In another terminal in the same folder:
```bash
java Client
```

## Expected Output
**Server terminal:**
```
Server ready on rmi://localhost:1099/concat
```
**Client terminal:**
```
HelloWorld
```

## Common Errors & Fixes
| Error | Cause | Fix |
|-------|-------|-----|
| `Connection refused to host: 127.0.0.1` | Server not running | Start `java Server` first |
| `ClassNotFoundException: StringConcat` | Wrong working directory | Run `java` from the folder containing the `.class` files |
| `Port 1099 already in use` | Another RMI process holds the port | `lsof -i:1099` then kill the PID, or change the port in both files |
