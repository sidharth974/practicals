// RMI Client: looks up the remote object in the registry and calls its concat() method.
// The call looks local but is actually executed on the server JVM.
import java.rmi.*;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;

public class Client {
    public static void main(String args[]) {
        try {
            // Connect to the registry the server created on localhost:1099.
            Registry registry = LocateRegistry.getRegistry("localhost", 1099);

            // Look up the remote object by the name the server bound it under.
            StringConcat obj = (StringConcat) registry.lookup("concat");

            // Remote call -- "Hello" + "World" is computed on the server, returned to us.
            System.out.println(obj.concat("Hello", "World"));
        } catch (RemoteException | NotBoundException e) {
            // Common causes: server not running, registry down, name not bound.
            e.printStackTrace();
        }
    }
}
