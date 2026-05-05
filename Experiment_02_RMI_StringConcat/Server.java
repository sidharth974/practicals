// RMI Server: implements StringConcat and registers it so remote clients can call concat().
// Uses LocateRegistry.createRegistry() to embed the registry in this JVM, which removes
// the need to start the external `rmiregistry` tool separately.
import java.rmi.*;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.rmi.server.*;

// UnicastRemoteObject sets up the socket-based RMI plumbing automatically.
public class Server extends UnicastRemoteObject implements StringConcat {

    Server() throws RemoteException {}

    // Remote method body: concatenates the two strings.
    @Override
    public String concat(String a, String b) {
        return a + b;
    }

    public static void main(String args[]) {
        try {
            // Start an embedded RMI registry on the default port 1099.
            // (Avoids "Connection refused" errors when rmiregistry is not running.)
            Registry registry = LocateRegistry.createRegistry(1099);

            // Create the remote service object.
            Server obj = new Server();

            // Bind it under a logical name so clients can look it up.
            registry.rebind("concat", obj);

            System.out.println("Server ready on rmi://localhost:1099/concat");
        } catch (RemoteException e) {
            // Print the full error so setup problems are visible (don't swallow exceptions).
            e.printStackTrace();
        }
    }
}
