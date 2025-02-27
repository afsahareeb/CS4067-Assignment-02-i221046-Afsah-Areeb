document.getElementById("loginForm").addEventListener("submit", async function(event) {
    event.preventDefault();
    
    let email = document.getElementById("email").value;
    let password = document.getElementById("password").value;

    let response = await fetch("http://127.0.0.1:8000/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ email: email, password: password })
    });

    let data = await response.json();
    
    if (response.status === 200) {
        document.getElementById("message").style.color = "green";
        document.getElementById("message").innerText = "Login successful! 🎉";
    } else {
        document.getElementById("message").innerText = data.detail || "Login failed!";
    }
});
