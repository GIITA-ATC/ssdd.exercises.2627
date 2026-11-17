import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;

public class Client {
    private Client() {}

    public static void main(String[] args) {
        String host = (args.length < 1) ? null : args[0];
        try {
            Registry registry = LocateRegistry.getRegistry(host);
            Math stub = (Math) registry.lookup("Math");

            int[] numbers = {2,3};
            int s = stub.add(numbers);
            int m = stub.multiply(numbers);
            System.out.println("add: " + Integer.toString(s));
            System.out.println("prod: " + Integer.toString(m));

        } catch (Exception e) {
            System.err.println("Client exception: " + e.toString());
            e.printStackTrace();
        }
    }
}
