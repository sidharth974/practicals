// RMI Hotel Server: keeps an in-memory map of room -> guest bookings.
// Embeds the RMI registry on port 1099 so no separate process is needed.
// Synchronises every operation so concurrent clients can't corrupt state.
import java.rmi.RemoteException;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.rmi.server.UnicastRemoteObject;
import java.time.LocalTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public class HotelServer extends UnicastRemoteObject implements Hotel {

    private static final int TOTAL_ROOMS = 10;

    // Maintain bookings in insertion order so listings look stable.
    private final Map<Integer, String> bookings = new LinkedHashMap<>();

    HotelServer() throws RemoteException {}

    private void log(String msg) {
        String ts = LocalTime.now().format(DateTimeFormatter.ofPattern("HH:mm:ss"));
        System.out.println("[" + ts + "] " + msg);
    }

    @Override
    public synchronized List<Integer> listAvailable() {
        List<Integer> free = new ArrayList<>();
        for (int i = 1; i <= TOTAL_ROOMS; i++) {
            if (!bookings.containsKey(i)) free.add(i);
        }
        log("listAvailable -> " + free);
        return free;
    }

    @Override
    public synchronized List<String> listBookings() {
        List<String> out = new ArrayList<>();
        for (Map.Entry<Integer, String> e : bookings.entrySet()) {
            out.add(e.getKey() + ":" + e.getValue());
        }
        log("listBookings -> " + out);
        return out;
    }

    @Override
    public synchronized String bookRoom(int roomNo, String guest) {
        // Reject invalid room numbers, double-bookings and empty names.
        if (roomNo < 1 || roomNo > TOTAL_ROOMS) {
            log("bookRoom(" + roomNo + ", " + guest + ") -> invalid room");
            return "FAIL: room " + roomNo + " does not exist (1-" + TOTAL_ROOMS + ").";
        }
        if (guest == null || guest.trim().isEmpty()) {
            return "FAIL: guest name cannot be empty.";
        }
        if (bookings.containsKey(roomNo)) {
            log("bookRoom(" + roomNo + ", " + guest + ") -> already booked by " + bookings.get(roomNo));
            return "FAIL: room " + roomNo + " is already booked by " + bookings.get(roomNo) + ".";
        }
        bookings.put(roomNo, guest.trim());
        log("bookRoom(" + roomNo + ", " + guest + ") -> OK");
        return "OK: room " + roomNo + " booked for " + guest.trim() + ".";
    }

    @Override
    public synchronized String cancelRoom(int roomNo) {
        if (!bookings.containsKey(roomNo)) {
            log("cancelRoom(" + roomNo + ") -> not booked");
            return "FAIL: room " + roomNo + " is not currently booked.";
        }
        String guest = bookings.remove(roomNo);
        log("cancelRoom(" + roomNo + ") -> OK (was " + guest + ")");
        return "OK: booking cancelled for room " + roomNo + " (was " + guest + ").";
    }

    @Override
    public synchronized String roomStatus(int roomNo) {
        if (roomNo < 1 || roomNo > TOTAL_ROOMS) {
            return "Room " + roomNo + " does not exist.";
        }
        if (bookings.containsKey(roomNo)) {
            return "Room " + roomNo + " is BOOKED by " + bookings.get(roomNo) + ".";
        }
        return "Room " + roomNo + " is AVAILABLE.";
    }

    @Override
    public int totalRooms() {
        return TOTAL_ROOMS;
    }

    public static void main(String args[]) {
        try {
            Registry registry = LocateRegistry.createRegistry(1099);
            HotelServer obj = new HotelServer();
            registry.rebind("hotel", obj);

            System.out.println("============================================================");
            System.out.println(" Hotel Booking Server ready on rmi://localhost:1099/hotel");
            System.out.println(" Hotel has " + TOTAL_ROOMS + " rooms (numbered 1.." + TOTAL_ROOMS + ").");
            System.out.println("============================================================");
            System.out.println(" Live request log: (Ctrl+C to stop)");
            System.out.println("============================================================");
        } catch (RemoteException e) {
            e.printStackTrace();
        }
    }
}
