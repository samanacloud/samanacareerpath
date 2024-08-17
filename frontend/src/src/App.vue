<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

// Define constants for timers (in minutes)
const IDLE_TIMEOUT_MINUTES = 5;
const TOKEN_REFRESH_THRESHOLD_MINUTES = 1;
const TOKEN_EXPIRATION_MINUTES = 60;

const router = useRouter();
const idleTimeout = ref(null);
const lastActivityTime = ref(Date.now());
const tokenExpiryTime = ref(Date.now() + TOKEN_EXPIRATION_MINUTES * 60000);

const activityEvents = ['mousemove', 'keydown', 'click'];

// Convert minutes to milliseconds
const convertMinutesToMilliseconds = (minutes) => minutes * 60000;

// Reset idle timer on user activity
const resetIdleTimer = () => {
    lastActivityTime.value = Date.now();
    clearTimeout(idleTimeout.value);
    idleTimeout.value = setTimeout(logoutUser, convertMinutesToMilliseconds(IDLE_TIMEOUT_MINUTES));
};

// Refresh the token before it expires
const refreshToken = async () => {
    try {
        const response = await axios.post('/path-to-refresh-token-endpoint', {
            refresh_token: sessionStorage.getItem('refreshToken'),
        });

        if (response.data.access_token) {
            sessionStorage.setItem('authToken', response.data.access_token);
            tokenExpiryTime.value = Date.now() + convertMinutesToMilliseconds(TOKEN_EXPIRATION_MINUTES);
        } else {
            logoutUser();
        }
    } catch (error) {
        console.error('Error refreshing token:', error);
        logoutUser();
    }
};

// Check token expiration and refresh if necessary
const checkTokenAndRefresh = () => {
    if (Date.now() > tokenExpiryTime.value - convertMinutesToMilliseconds(TOKEN_REFRESH_THRESHOLD_MINUTES)) {
        refreshToken();
    }
};

// Logout user and clear session
const logoutUser = () => {
    const candidateToken = document.cookie.split('; ').find(row => row.startsWith('candidateToken='));
    const userEmail = document.cookie.split('; ').find(row => row.startsWith('UserEmail='));
    const candidateEmail = document.cookie.split('; ').find(row => row.startsWith('CandidateEmail='));

    sessionStorage.clear();

    const userEmailValue = userEmail ? userEmail.split('=')[1] : '';
    const candidateEmailValue = candidateEmail ? candidateEmail.split('=')[1] : '';

    if (userEmailValue.includes('@gmail.com') || candidateEmailValue.includes('@gmail.com')) {
        router.push('/auth/logoutcandidate');
    } else {
        router.push('/auth/logout');
    }
};


// Set up activity tracking and token refresh logic
onMounted(() => {

    activityEvents.forEach(event => window.addEventListener(event, resetIdleTimer));
    idleTimeout.value = setTimeout(logoutUser, convertMinutesToMilliseconds(IDLE_TIMEOUT_MINUTES));
    setInterval(checkTokenAndRefresh, convertMinutesToMilliseconds(TOKEN_REFRESH_THRESHOLD_MINUTES));


});

// Clean up listeners and timers when component is unmounted
onUnmounted(() => {
    activityEvents.forEach(event => window.removeEventListener(event, resetIdleTimer));
    clearTimeout(idleTimeout.value);
});
</script>

<template>
    <router-view />
</template>

<style scoped></style>