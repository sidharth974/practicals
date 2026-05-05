// RMI Client: presents an interactive menu to the user and forwards each
// chosen operation as a remote method call to the StringConcat server.
import java.rmi.NotBoundException;
import java.rmi.RemoteException;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Scanner;

public class Client {

    private static void banner() {
        System.out.println("============================================================");
        System.out.println(" RMI String Service Client");
        System.out.println("============================================================");
    }

    private static void menu() {
        System.out.println();
        System.out.println("Menu:");
        System.out.println("  1) Concatenate two strings");
        System.out.println("  2) Concatenate a list of strings (custom separator)");
        System.out.println("  3) Reverse a string");
        System.out.println("  4) Convert a string to UPPERCASE");
        System.out.println("  5) Show server request count");
        System.out.println("  6) Exit");
    }

    public static void main(String args[]) {
        banner();
        Scanner in = new Scanner(System.in);

        StringConcat obj;
        try {
            // Connect to the registry the server created on localhost:1099.
            Registry registry = LocateRegistry.getRegistry("localhost", 1099);
            obj = (StringConcat) registry.lookup("concat");
            System.out.println("Connected to rmi://localhost:1099/concat");
        } catch (RemoteException | NotBoundException e) {
            System.out.println("ERROR: cannot connect to server. Is `java Server` running?");
            return;
        }

        // Main interactive loop.
        while (true) {
            menu();
            System.out.print("Choose an option [1-6]: ");
            String choice = in.nextLine().trim();

            try {
                switch (choice) {
                    case "1": {
                        System.out.print("  First string : ");
                        String a = in.nextLine();
                        System.out.print("  Second string: ");
                        String b = in.nextLine();
                        System.out.println("  -> " + obj.concat(a, b));
                        break;
                    }
                    case "2": {
                        System.out.print("  Enter strings separated by commas: ");
                        String csv = in.nextLine();
                        List<String> parts = new ArrayList<>(Arrays.asList(csv.split(",")));
                        // Trim each piece so "a, b ,c" works as expected.
                        parts.replaceAll(String::trim);
                        System.out.print("  Separator (e.g. \" \", \"-\", \"|\"): ");
                        String sep = in.nextLine();
                        System.out.println("  -> " + obj.concatAll(parts, sep));
                        break;
                    }
                    case "3": {
                        System.out.print("  Enter string to reverse: ");
                        String s = in.nextLine();
                        System.out.println("  -> " + obj.reverse(s));
                        break;
                    }
                    case "4": {
                        System.out.print("  Enter string to uppercase: ");
                        String s = in.nextLine();
                        System.out.println("  -> " + obj.upper(s));
                        break;
                    }
                    case "5":
                        System.out.println("  Server has handled " + obj.requestCount() + " requests so far.");
                        break;
                    case "6":
                        System.out.println("Goodbye.");
                        return;
                    default:
                        System.out.println("Invalid option, try again.");
                }
            } catch (RemoteException e) {
                System.out.println("  Remote call failed: " + e.getMessage());
            }
        }
    }
}
