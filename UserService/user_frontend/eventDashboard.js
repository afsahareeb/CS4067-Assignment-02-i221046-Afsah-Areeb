document.addEventListener("DOMContentLoaded", function() {
    loadEvents();
});

async function loadEvents() {
    let response = await fetch("http://127.0.0.1:8001/user/events");  // ✅ Fetch via User Service

    console.log("API Response Status:", response.status);
    let events = await response.json();
    console.log("Fetched Events:", events);

    let tableBody = document.querySelector("#eventsTable tbody");
    tableBody.innerHTML = "";  

    if (!Array.isArray(events) || events.length === 0) {
        console.log("No events found.");
        tableBody.innerHTML = "<tr><td colspan='5'>No events available</td></tr>";
        return;
    }

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

