<template>
  <div class="chat-container">
    <header class="chat-header">
      <h1>LangChain Agent</h1>
    </header>

    <div class="messages" ref="messagesContainer">
      <div
        v-for="(message, index) in messages"
        :key="index"
        :class="['message', message.role]"
      >
        <div class="message-content">{{ message.content }}</div>
      </div>
      <div v-if="loading" class="message assistant">
        <div class="message-content loading">Thinking...</div>
      </div>
    </div>

    <div class="input-area">
      <form @submit.prevent="sendMessage">
        <input
          v-model="inputMessage"
          type="text"
          placeholder="Type a message..."
          :disabled="loading"
          @keyup.enter="sendMessage"
        />
        <button type="submit" :disabled="loading || !inputMessage.trim()">
          Send
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted } from 'vue'
import axios from 'axios'

const messages = ref([])
const inputMessage = ref('')
const loading = ref(false)
const messagesContainer = ref(null)

const API_URL = '/api/chat'

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

const sendMessage = async () => {
  if (!inputMessage.value.trim() || loading.value) return

  const userMessage = inputMessage.value.trim()
  messages.value.push({ role: 'user', content: userMessage })
  inputMessage.value = ''
  loading.value = true
  scrollToBottom()

  try {
    const response = await axios.post(API_URL, { message: userMessage })
    messages.value.push({ role: 'assistant', content: response.data.response })
  } catch (error) {
    messages.value.push({
      role: 'assistant',
      content: 'Sorry, something went wrong. Please try again.'
    })
    console.error('Error:', error)
  } finally {
    loading.value = false
    scrollToBottom()
  }
}

onMounted(() => {
  messages.value.push({
    role: 'assistant',
    content: 'Hello! I am your AI assistant. I can help you with calculations and tell you the current time. How can I help you today?'
  })
})
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.chat-header {
  background: #4a90e2;
  color: white;
  padding: 1rem;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.chat-header h1 {
  font-size: 1.5rem;
  margin: 0;
}

.messages {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  background: #f9f9f9;
}

.message {
  margin-bottom: 1rem;
  display: flex;
}

.message.user {
  justify-content: flex-end;
}

.message.assistant {
  justify-content: flex-start;
}

.message-content {
  max-width: 70%;
  padding: 0.75rem 1rem;
  border-radius: 12px;
  line-height: 1.5;
  word-wrap: break-word;
}

.message.user .message-content {
  background: #4a90e2;
  color: white;
  border-bottom-right-radius: 4px;
}

.message.assistant .message-content {
  background: white;
  color: #333;
  border-bottom-left-radius: 4px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.message-content.loading {
  color: #999;
  font-style: italic;
}

.input-area {
  padding: 1rem;
  background: white;
  border-top: 1px solid #e0e0e0;
}

.input-area form {
  display: flex;
  gap: 0.5rem;
}

.input-area input {
  flex: 1;
  padding: 0.75rem 1rem;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
  outline: none;
}

.input-area input:focus {
  border-color: #4a90e2;
}

.input-area button {
  padding: 0.75rem 1.5rem;
  background: #4a90e2;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.2s;
}

.input-area button:hover:not(:disabled) {
  background: #357abd;
}

.input-area button:disabled {
  background: #ccc;
  cursor: not-allowed;
}
</style>
