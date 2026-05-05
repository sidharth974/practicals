# Load Balancing - Round Robin Simulation
# A load balancer distributes incoming requests across a pool of servers
# so that no single server is overloaded. Round Robin cycles through the
# server list in order, giving each server an equal share of requests.

# Pool of available backend servers.
servers = ["Server1", "Server2", "Server3"]

# Total number of incoming client requests to simulate.
requests = 10

for i in range(requests):
    # Round Robin selection: the i-th request goes to server at index (i mod N).
    # This wraps around the list so requests cycle through servers evenly.
    server = servers[i % len(servers)]

    # Print which server handled which request -- this is the "routing decision".
    print("Request", i + 1, "handled by", server)
