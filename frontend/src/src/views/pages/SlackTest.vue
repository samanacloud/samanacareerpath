<template>
    <div>
      <h1>Slack Test</h1>
      <input v-model="message" placeholder="Type your message here" />
      <button @click="sendMessage">Send Message</button>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import axios from 'axios';
  
  const message = ref('');
  
  const sendMessage = async () => {
    try {
      const response = await axios.post('/api/slackProxy.php', {
        channel: '#samana-careerpath',
        message: message.value
      });
  
      console.log('Message sent:', response.data);
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };
  </script>