// JavaScript to handle voice input and chat messages
let recognition;

if ("webkitSpeechRecognition" in window) {
    recognition = new webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = "en-US";

    recognition.onstart = () => {
        console.log("Voice recognition started.");
    };

    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        document.getElementById("userInput").value = transcript;
        sendMessage();  // Automatically send the message after voice input
    };

    recognition.onerror = (event) => {
        console.error("Error occurred in recognition: " + event.error);
    };

    recognition.onend = () => {
        console.log("Voice recognition ended.");
    };
}

// Function to start voice input on button click
document.getElementById("voiceInputBtn").onclick = () => {
    recognition.start();
};

// Function to send the message
async function sendMessage() {
    const userInput = document.getElementById("userInput").value;
    if (userInput === "") return;

    // Display user's message
    const chatbox = document.getElementById("chatbox");
    chatbox.innerHTML += `<div class="user-message">${userInput}</div>`;

    // Send message to Flask backend
    const response = await fetch("/get_response", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: userInput })
    });
    const data = await response.json();

    // Display chatbot's response
    chatbox.innerHTML += `<div class="bot-message">${data.response}</div>`;
    chatbox.scrollTop = chatbox.scrollHeight;
    document.getElementById("userInput").value = "";
}
