document.addEventListener("DOMContentLoaded", function() {
    loadEvents();
});

async function loadEvents() {
    let response = await fetch("/api/user-service/user/events");
    console.log("Checking sessionStorage...");
    console.log("Stored userEmail:", sessionStorage.getItem("userEmail"));
    console.log("Stored userId:", sessionStorage.getItem("userId"));

    console.log("API Response Status:", response.status);
    let events = await response.json();
    console.log("Fetched Events:", events);

    let tableBody = document.querySelector("#eventsTable tbody");
    tableBody.innerHTML = "";  

    if (!Array.isArray(events) || events.length === 0) {
        console.log("No events found.");
        tableBody.innerHTML = "<tr><td colspan='7'>No events available</td></tr>";
        return;
    }

    let userEmail = sessionStorage.getItem("userEmail");
    if (!userEmail) {
        console.error("User email not found. Please log in.");
        return;
    }

    events.forEach(event => {
        let row = document.createElement("tr");

        row.innerHTML = `
            <td>${event.title}</td>
            <td>${event.description}</td>
            <td>${event.location}</td>
            <td>${new Date(event.date).toLocaleString()}</td>
            <td>${event.num_tickets !== undefined ? event.num_tickets : "N/A"}</td>
            <td>${event.ticket_price !== undefined ? `$${event.ticket_price.toFixed(2)}` : "N/A"}</td>
            <td>
                <input type="number" id="tickets-${event.id}" min="1" max="${event.num_tickets}" value="1">
            </td>
            <td>
                <button class="book-btn" onclick="bookEvent(${event.id}, ${event.num_tickets}, ${event.ticket_price}, '${userEmail}')">
                    Book Now
                </button>
            </td>
        `;

        tableBody.appendChild(row);
    });
}

async function getUserId(userEmail) {
    try {
        let response = await fetch(`/api/user-service/users/${userEmail}`);
        if (!response.ok) {
            throw new Error("User not found");
        }
        let userData = await response.json();
        return userData.user_id;
    } catch (error) {
        console.error("Error fetching user ID:", error);
        return null;
    }
}


async function bookEvent(eventId, availableTickets, ticketPrice, userEmail) {
    let ticketInput = document.getElementById(`tickets-${eventId}`);
    let numTickets = parseInt(ticketInput.value);

    if (numTickets < 1 || numTickets > availableTickets) {
        alert("Please enter a valid number of tickets.");
        return;
    }

    let userId = await getUserId(userEmail);
    if (!userId) {
        alert("Failed to fetch user ID. Please log in.");
        return;
    }

    let totalPrice = numTickets * ticketPrice;

    let bookingData = {
        user_id: userId,
        event_id: eventId,
        tickets: numTickets,
        total_price: totalPrice
    };

    try {
        let response = await fetch("/api/user-service/user/book_event", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(bookingData)
        });

        let result = await response.json();
        console.log("Booking Response:", result);

        if (response.ok) {
            window.location.href = `booking_status.html?status=confirmed&bookingId=${result.booking_id}&total=${totalPrice}`;
        } else {
            window.location.href = `booking_status.html?status=failed`;
        }
    } catch (error) {
        console.error("Error booking event:", error);
        window.location.href = `booking_status.html?status=failed`;
    }
}


