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
    const socket = io(); // Upewnij się, że Socket.IO jest poprawnie skonfigurowany i podłączony.

    function toggleButton() {
        if (textArea.value.trim() === '') {
            sendButton.disabled = true;
            sendButton.classList.remove('enabled');
            sendButton.classList.add('disabled');
        } else {
            sendButton.disabled = false;
            sendButton.classList.remove('disabled');
            sendButton.classList.add('enabled');
        }
    }

    textArea.addEventListener('input', toggleButton);
    toggleButton(); // Inicjalizacja stanu przycisku na podstawie zawartości pola tekstowego

    // Dodanie obsługi zdarzenia 'click' na przycisku.
    sendButton.addEventListener('click', function() {
        if (!sendButton.disabled) {
            const chatHistory = document.querySelector('.chat-history');
            const messageElement = document.createElement('div');
            messageElement.classList.add('user-message-chat');
            const message = textArea.value.trim();
            messageElement.textContent = message; // Zakładam, że serwer wysyła obiekt z kluczem 'message'

            chatHistory.appendChild(messageElement);

            
            const chatroomId = chatHistory.getAttribute('data-chatroom-id');
            socket.emit('message_from_client', { message: message, chatroom_id: chatroomId });
            textArea.value = '';
            toggleButton();
        }
    });

    socket.on('message_from_server', function(data) {
        console.log('Wiadomość od serwera:', data);

        // Dodanie wiadomości do historii czatu
        const chatHistory = document.querySelector('.chat-history');
        const messageElement = document.createElement('div');
        messageElement.classList.add('robot-message-chat');
        messageElement.textContent = data.message; // Zakładam, że serwer wysyła obiekt z kluczem 'message'

        chatHistory.appendChild(messageElement);

        // Przewinięcie historii czatu do najnowszej wiadomości
        chatHistory.scrollTop = chatHistory.scrollHeight;
    });

});


const textarea = document.querySelector("textarea");
textarea.addEventListener("input", function() {
    if (this.value.length > 500) {
        this.value = this.value.slice(0, 500);
    }
});