document.getElementById("loginForm").addEventListener("submit", async function(event) {
    event.preventDefault(); // Prevent default form submission
    
    let email = document.getElementById("email").value;
    let password = document.getElementById("password").value;

    // Call the login function that properly stores session data
    await loginUser(email, password);
});

async function loginUser(email, password) {
    let response = await fetch("/api/user-service/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ email, password })
    });

    let result = await response.json();

    if (response.ok) {
        sessionStorage.setItem("userEmail", result.user_email);
        sessionStorage.setItem("userId", result.user_id);

        document.getElementById("message").style.color = "green";
        document.getElementById("message").innerText = "Login successful!";

        setTimeout(() => {
            window.location.href = "eventDashboard.html"; // Redirect after storing data
        }, 2000);
    } else {
        document.getElementById("message").innerText = result.detail || "Login failed!";
    }
}
