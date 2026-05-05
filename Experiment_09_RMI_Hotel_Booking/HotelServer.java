// RMI Server: hosts the booking logic and registers itself in the RMI registry
// so remote clients can locate and invoke its methods.
// The registry is embedded in this JVM (no separate `rmiregistry` process needed).
import java.rmi.*;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.rmi.server.*;

public class HotelServer extends UnicastRemoteObject implements Hotel {

    HotelServer() throws RemoteException {}

    // Booking implementation -- in a real system this would update a database.
    @Override
    public String bookRoom(String name) {
        return "Room booked for " + name;
    }

    // Cancellation implementation -- mirrors bookRoom for symmetry.
    @Override
    public String cancelRoom(String name) {
        return "Booking cancelled for " + name;
    }

    public static void main(String args[]) {
        try {
            // Start an embedded RMI registry on default port 1099 inside this JVM.
            Registry registry = LocateRegistry.createRegistry(1099);

            // Create the remote service instance.
            HotelServer obj = new HotelServer();

            // Bind it in the registry under the lookup name "hotel".
            registry.rebind("hotel", obj);

            System.out.println("Hotel Server ready on rmi://localhost:1099/hotel");
        } catch (RemoteException e) {
            // Always surface RMI errors instead of swallowing them.
            e.printStackTrace();
        }
    }
}
