import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.time.LocalDateTime;

public class Client {
    private Client() {}

    public static void main(String[] args) {
        if (args.length < 2) {
            System.out.println("Uso: Client <host> request <yyyy-MM-ddTHH:mm> <comensales> <nombre> <telefono>");
            System.out.println("     Client <host> check|cancel <id>");
            System.out.println("     Client <host> list");
            return;
        }
        try {
            Registry registry = LocateRegistry.getRegistry(args[0]);
            Restaurant stub = (Restaurant) registry.lookup("Restaurant");

            switch (args[1]) {
                case "request":
                    Reservation r = stub.request(
                        LocalDateTime.parse(args[2]),
                        Integer.parseInt(args[3]),
                        args[4],
                        args[5]
                    );
                    System.out.println("Reserva creada: " + r);
                    break;
                case "check":
                    System.out.println("Reserva: " + stub.check(Integer.parseInt(args[2])));
                    break;
                case "cancel":
                    stub.cancel(Integer.parseInt(args[2]));
                    System.out.println("Reserva " + args[2] + " cancelada");
                    break;
                case "list":
                    System.out.println("Reservas: " + stub.list().size());
                    for (Reservation res : stub.list()) System.out.println("  " + res);
                    break;
                default:
                    System.out.println("Operación desconocida: " + args[1]);
            }
        } catch (ReservationException e) {
            System.out.println("Error: " + e.getMessage());
        } catch (Exception e) {
            System.err.println("Client exception: " + e.toString());
            e.printStackTrace();
        }
    }
}
