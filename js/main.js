document.addEventListener('DOMContentLoaded', () => {
  const menuToggle = document.querySelector('.menu-toggle');
  const navLinks = document.querySelector('.nav-links');
  if (menuToggle && navLinks) {
    menuToggle.addEventListener('click', () => navLinks.classList.toggle('open'));
  }

  const chatForm = document.querySelector('#chat-form');
  const chatInput = document.querySelector('#chat-input');
  const chatMessages = document.querySelector('#chat-messages');
  const clearChat = document.querySelector('#clear-chat');

  const addMessage = (text, type) => {
    const item = document.createElement('div');
    item.className = `message ${type === 'user' ? 'user-message' : 'message-ai'}`;
    item.innerHTML = type === 'user'
      ? `<div class="bubble"><p></p><span>Just now</span></div>`
      : `<div class="mini-avatar">✦</div><div class="bubble"><p></p><span>Just now</span></div>`;
    item.querySelector('p').textContent = text;
    chatMessages.appendChild(item);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return item;
  };

  const sendMessage = async (message) => {
    if (!message.trim()) return;
    addMessage(message, 'user');
    chatInput.value = '';
    const pending = addMessage('Thinking...', 'ai');
    try {
      const response = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message })
      });
      if (!response.ok) throw new Error('Unable to reach assistant');
      const data = await response.json();
      pending.querySelector('p').textContent = data.response || 'I could not generate a response right now.';
    } catch (error) {
      pending.querySelector('p').textContent = 'I’m having trouble connecting right now. Please check that the FastAPI server is running and try again.';
    }
  };

  if (chatForm) {
    chatForm.addEventListener('submit', (event) => {
      event.preventDefault();
      sendMessage(chatInput.value);
    });
    document.querySelectorAll('.suggestions button').forEach((button) => {
      button.addEventListener('click', () => sendMessage(button.dataset.message));
    });
    clearChat?.addEventListener('click', () => {
      chatMessages.innerHTML = '<div class="message message-ai"><div class="mini-avatar">✦</div><div class="bubble"><p>Fresh start! What would you like to work on?</p><span>Just now</span></div></div>';
    });
  }
});
