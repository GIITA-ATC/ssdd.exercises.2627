import java.rmi.registry.Registry;
import java.rmi.registry.LocateRegistry;
import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;

public class Server implements Math {
    public int add(int[] numbers) {
        int result = 0;
        for(int n : numbers) {
            result += n;
        }
        return result;
    }

    public int multiply(int[] numbers) {
        int result = 1;
        for(int n : numbers) {
            result *= n;
        }
        return result;
    }

    public static void main(String args[]) {
        try {
            Server obj = new Server();
            Math stub = (Math) UnicastRemoteObject.exportObject(obj, 5002);

            Registry registry = LocateRegistry.createRegistry(1099);
            registry.rebind("Math", stub);

            System.out.println("Server ready");

        } catch (Exception e) {
            System.err.println("Server exception: " + e.toString());
            e.printStackTrace();
        }
    }
}
