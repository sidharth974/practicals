// Remote interface for the hotel booking service.
// Defines every operation a client may invoke remotely.
import java.rmi.Remote;
import java.rmi.RemoteException;
import java.util.List;

public interface Hotel extends Remote {

    // List the room numbers that are currently available (not booked).
    List<Integer> listAvailable() throws RemoteException;

    // List "roomNo:guestName" pairs for every active booking.
    List<String> listBookings() throws RemoteException;

    // Book a specific room for a guest. Returns a confirmation/error string.
    String bookRoom(int roomNo, String guest) throws RemoteException;

    // Cancel an existing booking by room number.
    String cancelRoom(int roomNo) throws RemoteException;

    // Look up the current status of one room.
    String roomStatus(int roomNo) throws RemoteException;

    // Total number of rooms in the hotel.
    int totalRooms() throws RemoteException;
}
