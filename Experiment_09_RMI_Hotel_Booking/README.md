# Experiment 9: Distributed Hotel Booking using Java RMI

**Aim:** Build a distributed hotel-booking system where the client invokes `bookRoom` and `cancelRoom` operations on a remote server using Java RMI.

**Tech:** Java RMI (`java.rmi`).

## Requirements
- JDK 8 or higher (`javac`, `java` on PATH)
- No third-party libraries

## Files
- `Hotel.java` — remote interface (`bookRoom`, `cancelRoom`)
- `HotelServer.java` — service implementation; embeds the RMI registry on port 1099
- `HotelClient.java` — client that looks up the service and invokes both methods

## How to run
Open a terminal in this folder.

```bash
# 1. Compile all files
javac Hotel.java HotelServer.java HotelClient.java

# 2. Start the server (the registry is started inside the same JVM)
java HotelServer
```

In another terminal in the same folder:
```bash
java HotelClient
```

## Expected Output
**Server terminal:**
```
Hotel Server ready on rmi://localhost:1099/hotel
```
**Client terminal:**
```
Room booked for Amit
Booking cancelled for Amit
```

## Common Errors & Fixes
| Error | Cause | Fix |
|-------|-------|-----|
| `Connection refused to host: 127.0.0.1` | Server not running | Start `java HotelServer` first |
| `ClassNotFoundException: Hotel` | Wrong working directory | Run `java` from the folder containing the `.class` files |
| `Port 1099 already in use` | Old RMI process still bound to the port | `lsof -i:1099` then kill the PID |
