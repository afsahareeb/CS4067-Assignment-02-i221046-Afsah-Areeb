document.addEventListener("DOMContentLoaded", function() {
    loadEvents();  // Load events when the page loads

    document.getElementById("eventForm").addEventListener("submit", async function(event) {
        event.preventDefault();

        let title = document.getElementById("title").value;
        let description = document.getElementById("description").value;
        let location = document.getElementById("location").value;

        let response = await fetch("http://127.0.0.1:8000/events/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ title: title, description: description, location: location })
        });

        let data = await response.json();
        
        if (response.ok) {
            document.getElementById("eventMessage").style.color = "green";
            document.getElementById("eventMessage").innerText = "Event created successfully! 🎉";
            loadEvents();  // Reload events
        } else {
            document.getElementById("eventMessage").style.color = "red";
            document.getElementById("eventMessage").innerText = data.detail || "Event creation failed!";
        }
    });
});

async function loadEvents() {
    let response = await fetch("http://127.0.0.1:8000/events/");
    let events = await response.json();

    let eventList = document.getElementById("eventList");
    eventList.innerHTML = "";  // Clear previous events

    events.forEach(event => {
        let eventCard = document.createElement("div");
        eventCard.classList.add("event-card");
        eventCard.innerHTML = `
            <h4>${event.title}</h4>
            <p>${event.description}</p>
            <p><strong>Location:</strong> ${event.location}</p>
            <button onclick="registerForEvent(${event.id})">Register</button>
        `;
        eventList.appendChild(eventCard);
    });
}

async function registerForEvent(eventId) {
    let response = await fetch(`http://127.0.0.1:8000/events/${eventId}/register`, {
        method: "POST"
    });

    if (response.ok) {
        alert("You have registered for the event!");
    } else {
        alert("Failed to register!");
    }
}
