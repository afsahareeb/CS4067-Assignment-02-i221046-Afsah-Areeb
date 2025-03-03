document.addEventListener("DOMContentLoaded", function() {
    loadEvents();
});

async function loadEvents() {
    let response = await fetch("http://127.0.0.1:8001/user/events");

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
            <td><button class="book-btn" onclick="bookEvent(${event.id}, ${event.num_tickets})">Book Now</button></td>
        `;

        tableBody.appendChild(row);
    });
}

