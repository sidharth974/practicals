# DC-1 RPC client. Connects to the XML-RPC server and calls factorial(n)
# remotely. The call looks local; under the hood it's an HTTP POST with
# an XML payload describing the method name and arguments.

import xmlrpc.client

# Build a proxy object pointing at the server URL.
# Method calls on this proxy are forwarded over HTTP.
client = xmlrpc.client.ServerProxy("http://localhost:8000/")

while True:
    raw = input("Enter a non-negative integer (or 'q' to quit): ").strip()
    if raw.lower() in ("q", "quit", "exit"):
        break
    try:
        n = int(raw)
    except ValueError:
        print("  Please enter an integer.")
        continue

    # Remote procedure call — server computes and returns the factorial.
    result = client.factorial(n)
    print(f"  {n}! = {result}")
