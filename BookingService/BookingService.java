import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import java.util.Optional;

@Service
public class BookingService {
    private final BookingRepository bookingRepository;
    private final RestTemplate restTemplate;

    public BookingService(BookingRepository bookingRepository, RestTemplate restTemplate) {
        this.bookingRepository = bookingRepository;
        this.restTemplate = restTemplate;
    }

    public Booking createBooking(String userId, String eventId, int numOfTickets) {
        // Step 1: Check Event Availability
        String eventUrl = "http://localhost:8081/events/" + eventId + "/availability";
        EventResponse event = restTemplate.getForObject(eventUrl, EventResponse.class);

        if (event == null || event.getNumTickets() < numOfTickets) {
            throw new RuntimeException("Not enough tickets available");
        }

        // Step 2: Calculate total price
        double totalPrice = numOfTickets * event.getTicketPrice();

        // Step 3: Make Payment
        PaymentRequest paymentRequest = new PaymentRequest(userId, totalPrice);
        String paymentUrl = "http://localhost:8083/payments";
        PaymentResponse paymentResponse = restTemplate.postForObject(paymentUrl, paymentRequest, PaymentResponse.class);

        if (!paymentResponse.isSuccess()) {
            throw new RuntimeException("Payment failed");
        }

        // Step 4: Confirm Booking
        Booking booking = new Booking();
        booking.setUserId(userId);
        booking.setEventId(eventId);
        booking.setNumOfTickets(numOfTickets);
        booking.setTotalPrice(totalPrice);
        booking.setBookingStatus("Confirmed");

        return bookingRepository.save(booking);
    }
}
