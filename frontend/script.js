
// ======================================
// 1. IDENTIFY CURRENT USER
// ======================================

const currentUser = document.body.dataset.user;
const receiver = document.body.dataset.receiver;

console.log("Current User:", currentUser);
console.log("Receiver:", receiver);


// ======================================
// 2. GET HTML ELEMENTS
// ======================================

const messagesContainer = document.getElementById("messages");
const messageInput = document.getElementById("message-input");
const sendButton = document.getElementById("send-button");
const connectionStatus = document.getElementById("connection-status");


// Check required HTML elements
if (
    !currentUser ||
    !receiver ||
    !messagesContainer ||
    !messageInput ||
    !sendButton ||
    !connectionStatus
) {
    throw new Error("Required dashboard elements or user details are missing.");
}


// ======================================
// 3. CONNECT TO SOCKET.IO SERVER
// ======================================

const socket = io("http://127.0.0.1:5000", {
    auth: {
        username: currentUser
    }
});


// ======================================
// 4. CONNECTION EVENTS
// ======================================

socket.on("connect", () => {

    console.log("Connected to server:", socket.id);

    connectionStatus.textContent = "Connected";
    connectionStatus.style.color = "#25d366";

});


socket.on("connect_error", (error) => {

    console.error("Connection error:", error.message);

    connectionStatus.textContent = "Connection failed";
    connectionStatus.style.color = "red";

});


socket.on("connection_status", (data) => {

    console.log(data.message);

});


// ======================================
// 5. DISPLAY MESSAGE
// ======================================

function displayMessage(messageText, messageType, timestamp) {

    const welcomeMessage = messagesContainer.querySelector(
        ".welcome-message"
    );

    if (welcomeMessage) {
        welcomeMessage.remove();
    }

    const messageDiv = document.createElement("div");

    messageDiv.classList.add("message", messageType);

    const textElement = document.createElement("span");

    // textContent prevents HTML injection
    textElement.textContent = messageText;

    const timeElement = document.createElement("span");

    timeElement.classList.add("message-time");

    timeElement.textContent = timestamp
        ? new Date(timestamp).toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit"
        })
        : new Date().toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit"
        });

    messageDiv.appendChild(textElement);
    messageDiv.appendChild(timeElement);

    messagesContainer.appendChild(messageDiv);

    messagesContainer.scrollTop = messagesContainer.scrollHeight;

}


// ======================================
// 6. SEND MESSAGE
// ======================================

function sendMessage() {

    const messageText = messageInput.value.trim();

    if (messageText === "") {
        return;
    }

    if (!socket.connected) {
        alert("Server is not connected!");
        return;
    }

    // Send plaintext to Python backend.
    // RSA encryption is performed by the backend.

    socket.emit("send_message", {

        receiver: receiver,

        message: messageText

    });

    // Display outgoing message
    displayMessage(messageText, "sent");

    messageInput.value = "";

}


// ======================================
// 7. SEND BUTTON EVENT
// ======================================

sendButton.addEventListener("click", sendMessage);


// ======================================
// 8. SEND MESSAGE USING ENTER KEY
// ======================================

messageInput.addEventListener("keydown", (event) => {

    if (event.key === "Enter" && !event.shiftKey) {

        event.preventDefault();

        sendMessage();

    }

});


// ======================================
// 9. RECEIVE MESSAGE
// ======================================


socket.on("receive_message", (message) => {

    console.log("Received RSA message:", message);

    if (typeof message.message !== "string") {
        console.error("Invalid decrypted message received.");
        return;
    }

    // Identify whether this dashboard is the sender or receiver
    const messageType =
        message.sender === currentUser ? "sent" : "received";

    displayMessage(
        message.message,
        messageType,
        message.timestamp
    );

});



// ======================================
// 10. MESSAGE STATUS
// ======================================

socket.on("message_sent", (data) => {

    console.log("RSA message processed successfully:", data);

});


socket.on("message_error", (data) => {

    console.error("Message error:", data.error);

    alert(data.error);

});


// ======================================
// 11. DISCONNECTION
// ======================================

socket.on("disconnect", () => {

    connectionStatus.textContent = "Disconnected";
    connectionStatus.style.color = "red";

    console.log("Disconnected from server.");

});
