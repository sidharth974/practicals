# DC-2 client. Looks up the StringService in the Pyro name server BY NAME
# (PYRONAME:...) and invokes its concat() method remotely.

import Pyro5.api

# The PYRONAME: scheme tells the proxy to ask the name server for this name.
# The name server returns the actual URI; the proxy connects there.
service = Pyro5.api.Proxy("PYRONAME:string.concat")

a = input("Enter first string : ")
b = input("Enter second string: ")

# Remote call.
result = service.concat(a, b)

print("Concatenated string:", result)
