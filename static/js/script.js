document.querySelector(".send").addEventListener("click", function () {
    let message = document.getElementById("msg").value.trim(); // Get user input and remove extra spaces

    if (message === "") return; // Prevent sending empty messages

    fetch("/send-message", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("response").innerText = "Bot Response: " + data.message;
        document.getElementById("msg").value = ""; // Clear textarea after sending
    })
    .catch(error => console.error("Error:", error));
});

// Allow pressing "Enter" to send the message
document.getElementById("msg").addEventListener("keypress", function(event) {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        document.querySelector(".send").click();
    }
});