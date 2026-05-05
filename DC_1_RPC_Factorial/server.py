# DC-1: Distributed application using RPC for factorial.
# Uses Python's built-in xmlrpc.server (NO third-party libraries needed).
# The server listens on a port and exposes the factorial() function for
# remote clients to call.

from xmlrpc.server import SimpleXMLRPCServer

# The function we want to expose remotely.
def factorial(n):
    if n < 0:
        return "Invalid input"
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

# Bind to localhost on a fixed port so the client knows where to connect.
HOST, PORT = "localhost", 8000
server = SimpleXMLRPCServer((HOST, PORT), allow_none=True, logRequests=True)

# Register the function under the name "factorial" — that's what the client calls.
server.register_function(factorial, "factorial")

print(f"RPC Server running on http://{HOST}:{PORT}/")
print("Press Ctrl+C to stop.")
server.serve_forever()
