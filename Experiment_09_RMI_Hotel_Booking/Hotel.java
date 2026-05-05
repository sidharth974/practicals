// Remote interface defining the contract of the hotel-booking RMI service.
// Both server (implements) and client (uses) reference this same interface.
import java.rmi.*;

// Must extend Remote so RMI knows the interface defines remotely-callable methods.
public interface Hotel extends Remote {
    // Book a room for a given guest name; returns a confirmation message.
    String bookRoom(String name) throws RemoteException;

    // Cancel an existing booking for a given guest name; returns a status message.
    String cancelRoom(String name) throws RemoteException;
}
