import java.rmi.Remote;
import java.rmi.RemoteException;

public interface Math extends Remote {
    int add(int[] numbers) throws RemoteException;
    int multiply(int[] numbers) throws RemoteException;
}
