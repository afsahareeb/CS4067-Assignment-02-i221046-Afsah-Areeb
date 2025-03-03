document.getElementById("signupForm").addEventListener("submit", async function(event) {
    event.preventDefault();

    let firstName = document.getElementById("firstName").value;
    let lastName = document.getElementById("lastName").value;
    let email = document.getElementById("email").value;
    let password = document.getElementById("password").value;
    let balance = parseFloat(document.getElementById("balance").value);

    let response = await fetch("http://127.0.0.1:8001/signup", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            first_name: firstName,
            last_name: lastName,
            email: email,
            password: password,
            balance: balance 
        })
    });

    let data = await response.json();

    if (response.ok) {
        document.getElementById("signupMessage").style.color = "green";
        document.getElementById("signupMessage").innerText = "Account created successfully!";
        
        setTimeout(() => {
            window.location.href = "../user_frontend/eventDashboard.html";
        }, 2000);
    } else {
        document.getElementById("signupMessage").style.color = "red";
        document.getElementById("signupMessage").innerText = data.detail || "Signup failed!";
    }
});

async function signupUser(firstName, lastName, email, password, balance) {
    let response = await fetch("http://127.0.0.1:8001/signup", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            first_name: firstName,
            last_name: lastName,
            email: email,
            password: password,
            balance: balance
        })
    });

    let result = await response.json();

    if (response.ok) {
        sessionStorage.setItem("userEmail", result.user_email);
        sessionStorage.setItem("userId", result.user_id);
        alert("Signup successful!");
        window.location.href = "events.html"; // Redirect to events page
    } else {
        alert("Signup failed: " + result.detail);
    }
}
