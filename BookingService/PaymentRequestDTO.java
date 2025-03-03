package com.example.bookingservice.dto;

import lombok.Data;

@Data
public class PaymentRequestDTO {
    private String userId;
    private double amount;  // Total amount to be paid for the booking
}
