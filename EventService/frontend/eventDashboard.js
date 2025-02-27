document.addEventListener("DOMContentLoaded", function() {
    loadEvents();
});

async function loadEvents() {
    let response = await fetch("http://127.0.0.1:8000/events/");
    let events = await response.json();

    let tableBody = document.querySelector("#eventsTable tbody");
    tableBody.innerHTML = "";  // Clear previous data

    events.forEach(event => {
        let row = document.createElement("tr");

        row.innerHTML = `
            <td>${event.title}</td>
            <td>${event.description}</td>
            <td>${event.location}</td>
            <td>${new Date(event.date).toLocaleString()}</td>
            <td><button class="book-btn" onclick="bookEvent(${event.id})">Book Now</button></td>
        `;

        tableBody.appendChild(row);
    });
}

async function bookEvent(eventId) {
    let response = await fetch(`http://127.0.0.1:8000/events/${eventId}/book`, {
        method: "POST",
        headers: { "Content-Type": "application/json" }
    });

    if (response.ok) {
        alert("Event booked successfully!");
    } else {
        alert("Failed to book event!");
    }
}
