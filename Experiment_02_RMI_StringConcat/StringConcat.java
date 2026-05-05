// Remote interface: defines all string-manipulation services exposed by the server.
import java.rmi.Remote;
import java.rmi.RemoteException;
import java.util.List;

public interface StringConcat extends Remote {

    // Concatenate two strings.
    String concat(String a, String b) throws RemoteException;

    // Concatenate a list of strings using a chosen separator.
    String concatAll(List<String> parts, String separator) throws RemoteException;

    // Reverse a single string.
    String reverse(String s) throws RemoteException;

    // Convert a string to upper-case.
    String upper(String s) throws RemoteException;

    // Return how many requests this server has handled in total.
    int requestCount() throws RemoteException;
}
