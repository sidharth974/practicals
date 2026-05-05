# DC-4: Load Balancing simulation across multiple servers.
# Three algorithms are demonstrated: Round Robin, Least Connections, Random.
# Models real load balancers like Nginx/HAProxy in miniature.

import random


# ---------- domain classes ----------

class Server:
    """A backend server with a unique id and a current load counter."""

    def __init__(self, server_id):
        self.server_id = server_id
        self.load = 0          # number of currently-active requests on this server

    def process_request(self):
        """Accept one request -> bump the load."""
        self.load += 1

    def finish_request(self):
        """Mark one request as completed -> drop the load."""
        self.load -= 1

    def __str__(self):
        return f"Server {self.server_id} - Load: {self.load}"


class Request:
    """A single client request."""

    def __init__(self, request_id):
        self.request_id = request_id

    def __str__(self):
        return f"Request {self.request_id}"


class LoadBalancer:
    """The dispatcher. Each algorithm is one method that picks a server."""

    def __init__(self, servers):
        self.servers = servers
        self.round_robin_index = 0          # cursor for round-robin

    def round_robin(self, request):
        """Cycle through servers in order: 0, 1, 2, ..., 0, 1, 2, ..."""
        server = self.servers[self.round_robin_index]
        print(f"Routing {request} to {server}")
        server.process_request()
        self.round_robin_index = (self.round_robin_index + 1) % len(self.servers)

    def least_connections(self, request):
        """Pick the server with the smallest current load."""
        server = min(self.servers, key=lambda s: s.load)
        print(f"Routing {request} to {server}")
        server.process_request()

    def random_assign(self, request):
        """Pick a server uniformly at random."""
        server = random.choice(self.servers)
        print(f"Routing {request} to {server}")
        server.process_request()


# ---------- driver ----------

def reset(servers):
    """Reset all server loads to 0 between experiments."""
    for s in servers:
        s.load = 0


def simulate():
    # 3 backend servers, 10 incoming requests.
    servers = [Server(i) for i in range(1, 4)]
    requests = [Request(i) for i in range(1, 11)]
    lb = LoadBalancer(servers)

    print("\n-- Round Robin --")
    reset(servers)
    for r in requests:
        lb.round_robin(r)

    print("\n-- Least Connections --")
    reset(servers)
    for r in requests:
        lb.least_connections(r)

    print("\n-- Random --")
    reset(servers)
    for r in requests:
        lb.random_assign(r)

    # Final load summary across the random run
    print("\nFinal loads after Random:")
    for s in servers:
        print(f"  {s}")


if __name__ == "__main__":
    simulate()
