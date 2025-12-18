// chat.js - Chat functionality
document.addEventListener('DOMContentLoaded', async function() {
    // Wait for API to initialize
    await window.HealthComAPI.initializeAPI().then(service => {
        window.APIService = service;
    });

    const chatMessages = document.getElementById('chatMessages');
    const messageInput = document.getElementById('messageInput');
    const sendMessageBtn = document.getElementById('sendMessageBtn');
    const loadingIndicator = document.getElementById('loadingIndicator');

    // Check if user is authenticated
    window.SessionManager.redirectIfNotAuthenticated();

    if (!chatMessages) return;

    // Auto-scroll to bottom of chat
    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Add message to chat
    function addMessage(content, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user-message' : 'doctor-message'}`;

        const icon = document.createElement('i');
        icon.className = isUser ? 'fas fa-user' : 'fas fa-user-md';

        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        messageContent.innerHTML = `<p>${content}</p>`;

        messageDiv.appendChild(icon);
        messageDiv.appendChild(messageContent);
        chatMessages.appendChild(messageDiv);

        scrollToBottom();
    }

    // Send message to API
    async function sendMessage() {
        const message = messageInput.value.trim();
        if (!message) return;

        // Add user message to chat
        addMessage(message, true);
        messageInput.value = '';

        // Show loading indicator
        loadingIndicator.classList.remove('hidden');

        try {
            const user = window.SessionManager.getUser();
            const response = await window.APIService.sendMessage(message, user.id);

            // Add doctor response to chat
            addMessage(response.response, false);
        } catch (error) {
            addMessage(`Error: ${error.message}`, false);
        } finally {
            // Hide loading indicator
            loadingIndicator.classList.add('hidden');
        }
    }

    // Event listeners
    if (sendMessageBtn) {
        sendMessageBtn.addEventListener('click', sendMessage);
    }

    if (messageInput) {
        messageInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    }

    // Initial scroll to bottom
    scrollToBottom();
});