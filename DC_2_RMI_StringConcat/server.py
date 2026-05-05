# DC-2: Distributed application using Pyro5 (Python Remote Objects) for
# string concatenation. Uses the Pyro name server so the client can locate
# the service by NAME (no need to copy any URI).

import Pyro5.api
import Pyro5.server


# Pyro5.api.expose marks every public method as remotely callable.
@Pyro5.api.expose
class StringService:
    def concat(self, a, b):
        # The actual remote method body.
        return a + b


def main():
    # The Daemon listens on a TCP socket and dispatches incoming RPC calls.
    daemon = Pyro5.server.Daemon()

    # Locate the running Pyro name server (started separately with `pyro5-ns`).
    ns = Pyro5.api.locate_ns()

    # Register the service object with the daemon (returns a URI).
    uri = daemon.register(StringService)

    # Register the URI under a friendly name so clients can look it up by name.
    ns.register("string.concat", uri)

    print("Server ready. Registered as 'string.concat' in the name server.")
    print("Press Ctrl+C to stop.")

    # Block forever, dispatching incoming RPC calls.
    daemon.requestLoop()


if __name__ == "__main__":
    main()
