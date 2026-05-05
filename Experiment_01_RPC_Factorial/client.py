# RPC Client: connects to the Factorial server and offers an interactive menu.
# Lets the user issue any number of factorial requests in one session.

import Pyro4
import time


def banner():
    print("=" * 60)
    print(" Pyro4 Factorial Client")
    print("=" * 60)


def menu():
    print("\nMenu:")
    print("  1) Compute factorial of a number")
    print("  2) Compute factorials of a range (e.g. 1..10)")
    print("  3) Show server call statistics")
    print("  4) Exit")
    return input("Choose an option [1-4]: ").strip()


def main():
    banner()
    uri = input("Enter server URI (PYRO:obj_xxx@host:port): ").strip()

    try:
        proxy = Pyro4.Proxy(uri)
        # Quick ping to fail fast if URI is wrong
        proxy._pyroBind()
    except Exception as e:
        print(f"ERROR: cannot connect to server -> {e}")
        return

    print("Connected.")

    while True:
        choice = menu()

        if choice == "1":
            try:
                n = int(input("  Enter a non-negative integer: "))
                t0 = time.perf_counter()
                result = proxy.fact(n)
                ms = (time.perf_counter() - t0) * 1000
                print(f"  -> {n}! = {result}")
                print(f"     (round-trip time: {ms:.2f} ms)")
            except ValueError as e:
                print(f"  ERROR: {e}")
            except Exception as e:
                print(f"  Remote error: {e}")

        elif choice == "2":
            try:
                a = int(input("  Start of range: "))
                b = int(input("  End of range  : "))
                if a > b:
                    a, b = b, a
                print(f"  Computing {a}! through {b}!:")
                for n in range(a, b + 1):
                    print(f"    {n:>3}! = {proxy.fact(n)}")
            except ValueError:
                print("  ERROR: please enter integers.")
            except Exception as e:
                print(f"  Remote error: {e}")

        elif choice == "3":
            print(f"  Total requests served by this server: {proxy.stats()}")

        elif choice == "4":
            print("Goodbye.")
            return

        else:
            print("Invalid option, try again.")


if __name__ == "__main__":
    main()
