# RPC Server: exposes a Factorial service over the network using Pyro4.
# Logs every incoming call (with timestamp) so you can see clients hitting the server live.

import Pyro4
import datetime

@Pyro4.expose
class Factorial:
    """Remote object exposed via Pyro4. Holds a small request counter."""

    def __init__(self):
        self.calls = 0  # how many factorial requests have been served

    # Remote method: compute n!
    def fact(self, n):
        self.calls += 1
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"[{ts}] call #{self.calls}: fact({n})")

        if n < 0:
            # Pyro4 will propagate this exception back to the client
            raise ValueError("factorial undefined for negative numbers")

        f = 1
        for i in range(1, n + 1):
            f *= i
        return f

    # Remote method: how many times has this server been called?
    def stats(self):
        return self.calls


def main():
    daemon = Pyro4.Daemon()                      # network daemon
    uri = daemon.register(Factorial())           # register one Factorial instance
    print("=" * 60)
    print(" Pyro4 Factorial Server is running")
    print("=" * 60)
    print(" Copy this URI and paste it into the client:")
    print(f"   {uri}")
    print("-" * 60)
    print(" Waiting for client requests... (Ctrl+C to stop)")
    print("=" * 60)
    daemon.requestLoop()


if __name__ == "__main__":
    main()
