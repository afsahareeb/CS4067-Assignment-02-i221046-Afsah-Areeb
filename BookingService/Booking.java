import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import lombok.Data;

@Data
@Document(collection = "bookings")
public class Booking {
    @Id
    private String id;
    private String userId;
    private String eventId;
    private int numOfTickets;
    private String bookingStatus;  // Pending, Confirmed, Cancelled
    private double totalPrice;
}
