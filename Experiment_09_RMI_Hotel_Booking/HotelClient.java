// Interactive hotel-booking client.
// Presents a menu to view rooms, book, cancel, and check status.
// Each menu choice triggers exactly one RMI call to the server.
import java.rmi.NotBoundException;
import java.rmi.RemoteException;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.util.List;
import java.util.Scanner;

public class HotelClient {

    private static int readInt(Scanner in, String prompt) {
        while (true) {
            System.out.print(prompt);
            String raw = in.nextLine().trim();
            try {
                return Integer.parseInt(raw);
            } catch (NumberFormatException e) {
                System.out.println("  ERROR: please enter a whole number.");
            }
        }
    }

    private static void showAvailable(Hotel h) throws RemoteException {
        List<Integer> rooms = h.listAvailable();
        if (rooms.isEmpty()) {
            System.out.println("  No rooms available — hotel is fully booked.");
        } else {
            System.out.println("  Available rooms: " + rooms);
        }
    }

    private static void showBookings(Hotel h) throws RemoteException {
        List<String> b = h.listBookings();
        if (b.isEmpty()) {
            System.out.println("  No active bookings.");
            return;
        }
        System.out.println();
        System.out.printf("  %-8s %s%n", "ROOM", "GUEST");
        System.out.println("  ------------------------------");
        for (String entry : b) {
            String[] parts = entry.split(":", 2);
            System.out.printf("  %-8s %s%n", parts[0], parts[1]);
        }
        System.out.println("  Total bookings: " + b.size());
    }

    public static void main(String[] args) {
        System.out.println("============================================================");
        System.out.println(" RMI Hotel Booking Client");
        System.out.println("============================================================");

        Scanner in = new Scanner(System.in);
        Hotel hotel;

        try {
            Registry registry = LocateRegistry.getRegistry("localhost", 1099);
            hotel = (Hotel) registry.lookup("hotel");
            System.out.println("Connected to rmi://localhost:1099/hotel  ("
                    + hotel.totalRooms() + " rooms)");
        } catch (RemoteException | NotBoundException e) {
            System.out.println("ERROR: cannot reach the server. Run `java HotelServer` first.");
            return;
        }

        while (true) {
            System.out.println();
            System.out.println("Menu:");
            System.out.println("  1) View available rooms");
            System.out.println("  2) View all current bookings");
            System.out.println("  3) Book a room");
            System.out.println("  4) Cancel a booking");
            System.out.println("  5) Check status of a specific room");
            System.out.println("  6) Exit");
            System.out.print("Choose [1-6]: ");
            String choice = in.nextLine().trim();

            try {
                switch (choice) {
                    case "1":
                        showAvailable(hotel);
                        break;
                    case "2":
                        showBookings(hotel);
                        break;
                    case "3": {
                        showAvailable(hotel);
                        int room = readInt(in, "  Room number to book: ");
                        System.out.print("  Guest name: ");
                        String guest = in.nextLine();
                        System.out.println("  -> " + hotel.bookRoom(room, guest));
                        break;
                    }
                    case "4": {
                        showBookings(hotel);
                        int room = readInt(in, "  Room number to cancel: ");
                        System.out.println("  -> " + hotel.cancelRoom(room));
                        break;
                    }
                    case "5": {
                        int room = readInt(in, "  Room number: ");
                        System.out.println("  -> " + hotel.roomStatus(room));
                        break;
                    }
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
