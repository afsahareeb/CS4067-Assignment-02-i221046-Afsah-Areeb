package com.example.bookingservice.dto;

import lombok.Data;

@Data
public class BookingRequestDTO {
    private String userId;   // ID of the user making the booking
    private String eventId;  // ID of the event being booked
    private int numOfTickets; // Number of tickets requested
}
