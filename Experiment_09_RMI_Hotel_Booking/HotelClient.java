// RMI Client: looks up the remote Hotel object from the registry and invokes
// its booking and cancellation methods as if they were local calls.
import java.rmi.*;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;

public class HotelClient {
    public static void main(String args[]) {
        try {
            // Connect to the registry the server created on localhost:1099.
            Registry registry = LocateRegistry.getRegistry("localhost", 1099);

            // Look up the remote object by the name the server bound it under.
            Hotel obj = (Hotel) registry.lookup("hotel");

            // Invoke remote methods. The actual work runs on the server JVM.
            System.out.println(obj.bookRoom("Amit"));
            System.out.println(obj.cancelRoom("Amit"));
        } catch (RemoteException | NotBoundException e) {
            // Surface failures (server down, name not bound, network error, etc.).
            e.printStackTrace();
        }
    }
}
