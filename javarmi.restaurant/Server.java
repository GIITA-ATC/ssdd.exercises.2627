import java.rmi.registry.Registry;
import java.rmi.registry.LocateRegistry;
import java.rmi.server.UnicastRemoteObject;
import java.time.LocalDateTime;
import java.util.*;

public class Server implements Restaurant {
    private static final int CAPACITY = 40;
    private final Map<Integer, Reservation> reservations = new HashMap<>();
    private int nextId = 1;

    // synchronized: forces requests to be handled one at a time, so concurrent
    // clients can't book the same seats or get the same reservation id.
    public synchronized Reservation request(LocalDateTime time, int diners, String name, String phone)
            throws ReservationException {
        if (diners <= 0)
            throw new ReservationException("Número de comensales no válido");
        if (time.getHour() < 20 || time.getHour() >= 23)
            throw new ReservationException("Fuera del horario de cena (20:00-23:00)");

        int occupied = 0;
        for (Reservation r : reservations.values())
            if (r.time.toLocalDate().equals(time.toLocalDate())) occupied += r.diners;
        if (occupied + diners > CAPACITY)
            throw new ReservationException("No hay plazas ese día (quedan " + (CAPACITY - occupied) + ")");

        Reservation r = new Reservation(nextId++, time, diners, name, phone);
        reservations.put(r.id, r);
        return r;
    }

    public synchronized Reservation check(int id) throws ReservationException {
        Reservation r = reservations.get(id);
        if (r == null) throw new ReservationException("La reserva " + id + " no existe");
        return r;
    }

    public synchronized void cancel(int id) throws ReservationException {
        if (reservations.remove(id) == null)
            throw new ReservationException("La reserva " + id + " no existe");
    }

    public synchronized List<Reservation> list() {
        return new ArrayList<>(reservations.values());
    }

    public static void main(String args[]) {
        try {
            Server obj = new Server();
            Restaurant stub = (Restaurant) UnicastRemoteObject.exportObject(obj, 5002);

            Registry registry;
            try {
                registry = LocateRegistry.createRegistry(1099);
            } catch (java.rmi.server.ExportException e) {
                registry = LocateRegistry.getRegistry(1099);
            }
            registry.rebind("Restaurant", stub);

            System.out.println("Server ready");
        } catch (Exception e) {
            System.err.println("Server exception: " + e.toString());
            e.printStackTrace();
        }
    }
}
