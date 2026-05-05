// Remote interface: defines the contract for the RMI service.
// Both the server (which implements it) and the client (which uses it) reference this interface.
import java.rmi.*;

// Any RMI-callable interface must extend java.rmi.Remote.
public interface StringConcat extends Remote {
    // Every remote method must declare RemoteException to handle network/RMI failures.
    String concat(String a, String b) throws RemoteException;
}
