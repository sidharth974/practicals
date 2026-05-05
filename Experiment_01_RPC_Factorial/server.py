# RPC Server: exposes a Factorial service over the network using Pyro4.
# Client calls fact(n) remotely and gets the factorial value back.

import Pyro4

# @Pyro4.expose makes every public method of this class callable remotely.
@Pyro4.expose
class Factorial:
    # Remote method: computes n! using an iterative loop.
    def fact(self, n):
        f = 1
        for i in range(1, n + 1):
            f = f * i
        return f

# Daemon listens for incoming Pyro4 RPC calls.
daemon = Pyro4.Daemon()

# Register the Factorial object with the daemon; returns a unique URI
# the client must use to locate this remote object on the network.
uri = daemon.register(Factorial)

# Print the URI so the client can connect to this exact server instance.
print("Server Ready:", uri)

# Block forever, processing remote method calls as they arrive.
daemon.requestLoop()
