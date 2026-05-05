# DC-2 all-in-one: name server + service + client, all in this single script.
# Useful when you want a one-command demo. The same architecture as the
# 3-terminal version below, just orchestrated with threads.

import threading
import time
import Pyro5.api
import Pyro5.nameserver
import Pyro5.server


# ----------- Name server (background thread) -----------

def start_name_server():
    """Run the Pyro5 name server forever on localhost:9090."""
    Pyro5.nameserver.start_ns_loop(host="localhost")

threading.Thread(target=start_name_server, daemon=True).start()
time.sleep(2)                                # give the NS time to bind its port


# ----------- Remote object -----------

@Pyro5.api.expose
class StringService:
    def concat(self, a, b):
        return a + b


# ----------- Service daemon (background thread) -----------

def start_service():
    """Register StringService with the name server and serve forever."""
    daemon = Pyro5.server.Daemon()
    ns = Pyro5.api.locate_ns()
    uri = daemon.register(StringService)
    ns.register("string.concat", uri)
    print("Service registered as 'string.concat'.")
    daemon.requestLoop()

threading.Thread(target=start_service, daemon=True).start()
time.sleep(2)                                # give the service time to register


# ----------- Client (foreground) -----------

print("\n" + "=" * 50)
print(" Pyro5 String Concatenation Client")
print("=" * 50)

a = input("Enter first string : ")
b = input("Enter second string: ")

# Look up by name and call remotely.
service = Pyro5.api.Proxy("PYRONAME:string.concat")
result = service.concat(a, b)
print("Concatenated string:", result)
