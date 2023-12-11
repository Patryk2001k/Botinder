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
    const chatHistory = document.querySelector('.chat-history');

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

    function addMessageToChat(message, className) {
        const messageElement = document.createElement('div');
        messageElement.classList.add(className);
        messageElement.textContent = message;
        chatHistory.appendChild(messageElement);
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }

    textArea.addEventListener('input', () => toggleButton());
    toggleButton(); 

    sendButton.addEventListener('click', function() {
        if (!sendButton.disabled) {
            const message = textArea.value.trim();
            addMessageToChat(message, 'user-message-chat');
            
            const chatroomId = chatHistory.getAttribute('data-chatroom-id');
            fetch('/send_message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message, chatroom_id: chatroomId })
            })
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    addMessageToChat(data.message, 'robot-message-chat');
                }
            })
            .catch(error => console.error('Error:', error));

            textArea.value = '';
            toggleButton();
        }
    });
});


const textarea = document.querySelector("textarea");
textarea.addEventListener("input", function() {
    if (this.value.length > 500) {
        this.value = this.value.slice(0, 500);
    }
});


function disableSockets() {
    // Zakładam, że `socket` jest zmienną globalną lub dostępną w tym zakresie.
    socket.disconnect();
}

async function UnMatch() {
    console.log("UnMatch clicked");
    //disableSockets();
    console.log("Disable sockets");

    const robotNameElement = document.getElementById('robot-name');
    const robotName = robotNameElement.textContent;
    const userInformationDiv = document.querySelector('.user-information');
    const xData = userInformationDiv.getAttribute('x-data');
    const userDisplayDiv = document.getElementById('user-display');
    const robotId = userDisplayDiv.getAttribute('x-data');
    const chatHistory = document.querySelector('.chat-history');
    const chatroomId = chatHistory.getAttribute('data-chatroom-id');

    const data = {
        chatroomId: chatroomId,
        robotName: robotName,
        userName: xData,
        robotId: robotId
    };

    try {
        const response = await fetch('/chatroom_unmatch', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        if (response.ok) {
            console.log("Match Unmatched Successfully");
            window.location.href = '/user_homepage';
            // Możesz dodać tu dodatkowe działania po pomyślnej operacji, np. przekierowanie
        } else {
            console.error('Server responded with non-OK status');
        }
    } catch (error) {
        console.error('Error:', error);
    }
}
