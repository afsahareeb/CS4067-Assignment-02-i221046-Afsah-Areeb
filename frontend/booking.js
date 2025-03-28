document.addEventListener("DOMContentLoaded", async function() {
    const urlParams = new URLSearchParams(window.location.search);
    const bookingStatus = urlParams.get("status");
    const bookingId = urlParams.get("bookingId");

    const statusMessage = document.getElementById("status-message");

    if (bookingStatus === "confirmed" && bookingId && bookingId.trim() !== "")
        {
        try {
            let response = await fetch(`/api/booking-service/booking/${bookingId}`);
            if (!response.ok) throw new Error("Failed to fetch booking details.");

            let bookingData = await response.json();
            console.log("Booking Data:", bookingData);
            statusMessage.textContent = `Booking Confirmed! Booking ID: ${bookingData._id}`;
            statusMessage.style.color = "green";
        } catch (error) {
            console.error("Error fetching booking details:", error);
            statusMessage.textContent = "Booking Confirmation Failed!";
            statusMessage.style.color = "red";
        }
    } else {
        statusMessage.textContent = "Booking Failed!";
        statusMessage.style.color = "red";
    }
});
