const socket = io();

const chatContainer = document.querySelector('.chat-container');
const messages = document.getElementById('messages');
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');
const themeToggle = document.querySelector('.theme-toggle');

function addMessage(message, className, iconClass) {
  const messageDiv = document.createElement('div');
  messageDiv.className = `chat-message ${className}`;

  const iconDiv = document.createElement('div');
  iconDiv.className = `message-icon ${iconClass}`;
  iconDiv.textContent = className === 'userMessage' ? 'U' : 'AI';

  const textDiv = document.createElement('div');
  textDiv.className = 'chat-message-text';
  textDiv.textContent = message;

  messageDiv.appendChild(iconDiv);
  messageDiv.appendChild(textDiv);
  messages.appendChild(messageDiv);
  messages.scrollTop = messages.scrollHeight;
}

function sendMessage() {
  const message = messageInput.value.trim();
  if (message !== '') {
    addMessage(message, 'userMessage', 'userIcon');
    socket.emit('chat message', message);
    messageInput.value = '';
  }
}

messageInput.addEventListener('keypress', (event) => {
  if (event.key === 'Enter') sendMessage();
});

sendButton.addEventListener('click', sendMessage);

socket.on('chat message', (message) => {
  if (message.startsWith('AI: ')) {
    addMessage(message.replace('AI: ', ''), 'incomingMessage', 'aiIcon');
  }
});

themeToggle.addEventListener('click', () => {
  chatContainer.classList.toggle('light-theme');
});
