import java.io.Serializable;
import java.time.LocalDateTime;

public class Reservation implements Serializable {
    public final int id;
    public final LocalDateTime time;
    public final int diners;
    public final String name;
    public final String phone;

    public Reservation(int id, LocalDateTime time, int diners, String name, String phone) {
        this.id = id;
        this.time = time;
        this.diners = diners;
        this.name = name;
        this.phone = phone;
    }

    public String toString() {
        return "#" + id + " " + time + " " + diners + " comensales, " + name + " (" + phone + ")";
    }
}
