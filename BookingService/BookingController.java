import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/bookings")
public class BookingController {
    private final BookingService bookingService;

    public BookingController(BookingService bookingService) {
        this.bookingService = bookingService;
    }

    @PostMapping
    public Booking createBooking(@RequestParam String userId, 
                                 @RequestParam String eventId, 
                                 @RequestParam int numOfTickets) {
        return bookingService.createBooking(userId, eventId, numOfTickets);
    }
}
