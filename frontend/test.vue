<script setup>
import { ref } from 'vue'
import axios from 'axios'

defineProps({
  msg: {
    type: String,
    required: true
  }
})

// Function to get the auth token from cookies
function getAuthToken() {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; authToken=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

const SITE_URL = import.meta.env.VITE_SITE_URL;
const apiResponse = ref('')
const usersList = ref([])
const userDetails = ref(null)
const defaultProfileImage = '/public/samana-logo.png' // Path to the default user image

const testDbConnection = async () => {
  try {
    const response = await axios.post(`${SITE_URL}/api/apitest.php`, {
      action: 'testDbConnection'
    })
    apiResponse.value = response.data.success ? 'Database connection successful' : 'Database connection failed'
  } catch (error) {
    apiResponse.value = 'Error: ' + error.message
  }
}

const listUsers = async () => {
  try {
    const response = await axios.post(`${SITE_URL}/api/apitest.php`, {
      action: 'listUsers'
    })
    usersList.value = response.data
    apiResponse.value = 'Users listed successfully'
  } catch (error) {
    apiResponse.value = 'Error: ' + error.message
  }
}

const getUser = async (userId) => {
  try {
    const response = await axios.post(`${SITE_URL}/api/apitest.php`, {
      action: 'getUser',
      userId: userId
    })
    userDetails.value = response.data
    apiResponse.value = `User ${userId} details fetched successfully`
  } catch (error) {
    apiResponse.value = 'Error: ' + error.message
  }
}

</script>

<template>
  <div class="greetings">
    <h1 class="green">{{ msg }}</h1>
    <h3>
      Test Page JP Hola
    </h3>
    <p>Site URL: {{ SITE_URL }}</p>
    <button @click="testDbConnection">Test Database Connection</button>
    <button @click="listUsers">List Users</button>
    <p>{{ apiResponse }}</p>
    <ul v-if="usersList.length > 0">
      <li v-for="user in usersList" :key="user.id">
        {{ user.name }} ({{ user.email }})
        <button @click="getUser(user.id)">Get User Info</button>
      </li>
    </ul>
    <div v-if="userDetails">
      <h3>User Details</h3>
      <p>Name: {{ userDetails.name }}</p>
      <p>Email: {{ userDetails.email }}</p>
      <p>Profile Image: <img :src="userDetails.profile_image || defaultProfileImage" alt="Profile Image" /></p>
    </div>
  </div>
</template>

<style scoped>
h1 {
  font-weight: 500;
  font-size: 2.6rem;
  position: relative;
  top: -10px;
}

h3 {
  font-size: 1.2rem;
}

.greetings h1,
.greetings h3 {
  text-align: center;
}

@media (min-width: 1024px) {
  .greetings h1,
  .greetings h3 {
    text-align: left;
  }
}

button {
  margin-left: 10px;
}

img {
  max-width: 100px;
  height: auto;
}
</style>