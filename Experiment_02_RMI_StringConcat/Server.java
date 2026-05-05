// RMI Server: implements every method of StringConcat and serves them over RMI.
// Embeds the registry on port 1099 so no separate `rmiregistry` is needed.
// Logs every incoming request with a timestamp.
import java.rmi.RemoteException;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.rmi.server.UnicastRemoteObject;
import java.time.LocalTime;
import java.time.format.DateTimeFormatter;
import java.util.List;

public class Server extends UnicastRemoteObject implements StringConcat {

    // Counter shared by every method to track total RPC calls served.
    private int calls = 0;

    Server() throws RemoteException {}

    // Tiny helper that prints "[HH:mm:ss] <message>" to the server console.
    private void log(String msg) {
        calls++;
        String ts = LocalTime.now().format(DateTimeFormatter.ofPattern("HH:mm:ss"));
        System.out.println("[" + ts + "] call #" + calls + ": " + msg);
    }

    @Override
    public String concat(String a, String b) {
        log("concat(\"" + a + "\", \"" + b + "\")");
        return a + b;
    }

    @Override
    public String concatAll(List<String> parts, String separator) {
        log("concatAll(" + parts + ", sep=\"" + separator + "\")");
        return String.join(separator, parts);
    }

    @Override
    public String reverse(String s) {
        log("reverse(\"" + s + "\")");
        return new StringBuilder(s).reverse().toString();
    }

    @Override
    public String upper(String s) {
        log("upper(\"" + s + "\")");
        return s.toUpperCase();
    }

    @Override
    public int requestCount() {
        return calls;
    }

    public static void main(String args[]) {
        try {
            Registry registry = LocateRegistry.createRegistry(1099);
            Server obj = new Server();
            registry.rebind("concat", obj);

            System.out.println("============================================================");
            System.out.println(" RMI String Service ready on rmi://localhost:1099/concat");
            System.out.println(" Methods: concat, concatAll, reverse, upper, requestCount");
            System.out.println("============================================================");
            System.out.println(" Waiting for client requests... (Ctrl+C to stop)");
            System.out.println("============================================================");
        } catch (RemoteException e) {
            e.printStackTrace();
        }
    }
}
