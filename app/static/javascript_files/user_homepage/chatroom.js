const textareas = document.querySelectorAll('.message-sender');

textareas.forEach(textarea => {
const initialHeight = "30px"; // Możesz tu ustawić początkową wysokość

textarea.style.height = initialHeight; // Ustawiamy początkową wysokość

textarea.addEventListener('input', function() {
    this.style.height = initialHeight; // Resetujemy do początkowej wysokości
    const scrollHeight = this.scrollHeight;
    
    if (scrollHeight <= 150) {
    this.style.height = scrollHeight + 'px'; // Powiększ w górę do 300px
    } else {
    this.style.height = '150px'; // Zatrzymaj na 300px i włącz pasek przewijania
    }
});

textarea.addEventListener('focusout', function() {
    if (this.value === '') {
    this.style.height = 30+"px"; // Resetujemy do początkowej wysokości tylko jeśli jest pusty
    }
});
});

document.addEventListener("DOMContentLoaded", function() {
const textArea = document.querySelector('.message-sender');
const sendButton = document.querySelector('.send-message-button');

function toggleButton() {
    if (textArea.value.trim() === '') {
        sendButton.classList.remove('enabled');
        sendButton.classList.add('disabled');
    } else {
        sendButton.classList.remove('disabled');
        sendButton.classList.add('enabled');
    }
}

textArea.addEventListener('input', toggleButton);

sendButton.addEventListener('click', function() {
    if (textArea.value.trim() !== '') {
        async function sendMessage(message) {
            const chatroomId = document.querySelector(".chat-history").getAttribute("data-chatroom-id");
            const payload = {
                message: message,
                chatroom_id: chatroomId
            }
            
            const response = await fetch('/send_message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });
        
            const data = await response.json();
        
        }
        sendMessage(textArea.value.trim())
        console.log(`Wiadomość wysłana: ${textArea.value.trim()}`);
        textArea.value = '';
    }
});

// Sprawdź na początek
toggleButton();
});

const textarea = document.querySelector("textarea");
textarea.addEventListener("input", function() {
    if (this.value.length > 500) {
        this.value = this.value.slice(0, 500);
    }
});