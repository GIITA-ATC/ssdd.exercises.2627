import java.rmi.Remote;
import java.rmi.RemoteException;
import java.time.LocalDateTime;
import java.util.List;

public interface Restaurant extends Remote {
    Reservation request(LocalDateTime time, int diners, String name, String phone)
            throws RemoteException, ReservationException;
    Reservation check(int id) throws RemoteException, ReservationException;
    void cancel(int id) throws RemoteException, ReservationException;
    List<Reservation> list() throws RemoteException;
}
