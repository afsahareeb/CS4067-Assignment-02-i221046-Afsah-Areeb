package com.example.bookingservice.dto;

import lombok.Data;

@Data
public class EventAvailabilityDTO {
    private String eventId;
    private int availableTickets;  // Number of tickets available
    private double ticketPrice;    // Price per ticket
}
