# RPC Client: connects to the Factorial server and invokes fact(n) remotely.
# To the client the call looks local, but it actually crosses the network.

import Pyro4

# Ask the user for the URI printed by the server (e.g. PYRO:obj_xxxx@host:port).
uri = input("Enter server uri:")

# Pyro4.Proxy creates a local stub bound to the remote object at this URI.
# Method calls on this proxy are transparently forwarded to the server.
obj = Pyro4.Proxy(uri)

# Take the integer input from the user.
n = int(input("Enter number:"))

# Remote call: server computes the factorial and returns the result.
print("Factorial =", obj.fact(n))
