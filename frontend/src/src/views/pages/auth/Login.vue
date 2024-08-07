<script setup>
import { useLayout } from '@/layout/composables/layout';
import { ref, computed, onMounted } from 'vue';
import AppConfig from '@/layout/AppConfig.vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { useToast } from 'primevue/usetoast';

const { layoutConfig } = useLayout();
const router = useRouter();
const toast = useToast();

const logoUrl = computed(() => {
    return `/${layoutConfig.darkTheme.value ? 'samana-logo-white' : 'samana-logo-dark'}.png`;
});

// Function to get the base URL
const baseURL = import.meta.env.VITE_SITE_URL 
    ? `https://${import.meta.env.VITE_SITE_URL}` 
    : 'http://localhost:8080'; 

// Use environmental variables
const clientId = import.meta.env.VITE_GOOGLE_CLIENT_ID;
const clientSecret = import.meta.env.VITE_GOOGLE_CLIENT_SECRET;
const redirectUri = `${window.location.origin}/auth/login`;

const loginWithGoogle = async () => {
    const scope = 'https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/drive.file';
    const authUrl = `https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id=${clientId}&redirect_uri=${redirectUri}&scope=${scope}&access_type=online`;

    window.location.href = authUrl;
};

const handleGoogleCallback = async () => {
    const params = new URLSearchParams(window.location.search);
    const code = params.get('code');
    if (code) {
        try {
            const tokenResponse = await axios.post('https://oauth2.googleapis.com/token', {
                code,
                client_id: clientId,
                client_secret: clientSecret,
                redirect_uri: redirectUri,
                grant_type: 'authorization_code'
            });

            const { access_token, id_token } = tokenResponse.data; // Extract id_token as well
            const userInfoResponse = await axios.get(`https://www.googleapis.com/oauth2/v1/userinfo?alt=json&access_token=${access_token}`);
            const userInfo = userInfoResponse.data;

            // Calculate expiration time (20 minutes from now)
            const expirationDate = new Date();
            expirationDate.setTime(expirationDate.getTime() + 20 * 60 * 1000); // 20 minutes * 60 seconds * 1000 milliseconds
            const expires = expirationDate.toUTCString();

            // Set the cookie with proper attributes
            document.cookie = `authToken=${access_token}; path=/; SameSite=Lax; Secure`;
            document.cookie = `userName=${userInfo.name}; path=/; SameSite=Lax; Secure`;
            document.cookie = `userProfileImage=${userInfo.picture}; path=/; SameSite=Lax; Secure`;
            document.cookie = `userEmail=${userInfo.email}; path=/; SameSite=Lax; Secure`;
            document.cookie = `idToken=${id_token}; path=/; SameSite=Lax; Secure`;

            // Check if the user exists
            const email = userInfo.email;
            const userDetailsResponse = await axios.post(`${baseURL}/api/apitest.php`, {
                action: 'getUserDetails',
                email
            });

            if (userDetailsResponse.data.error === 'User not found') {
                // If user does not exist, add the user and set admin=0 in the cookie
                await axios.post(`${baseURL}/api/apitest.php`, {
                    action: 'addSystemUser',
                    google_id: userInfo.id,
                    name: userInfo.name,
                    email: userInfo.email,
                    profile_image: userInfo.picture,
                    admin: 0
                });

                document.cookie = `admin=0; path=/; SameSite=Lax; Secure`;
            } else if (userDetailsResponse.data.error === 'Unauthorized') {
                // Show unauthorized message
                toast.add({
                    severity: 'error',
                    summary: 'Unauthorized',
                    detail: 'You are not authorized to access this platform. Please contact your administrator.',
                    life: 5000
                });
            } else {
                // If user exists, set admin=value in the cookie
                const adminValue = userDetailsResponse.data.admin;
                document.cookie = `admin=${adminValue}; path=/; SameSite=Lax; Secure`;
                router.push('/');
            }

            console.log('User Info:', userInfo);
        } catch (error) {
            console.error('Error during Google login callback:', error);
            toast.add({
                severity: 'error',
                summary: 'Login Error: Unauthorized',
                detail: 'You are not authorized to access this platform. Please contact your administrator.',
                life: 5000
            });
        }
    }
};

onMounted(() => {
    handleGoogleCallback();
});
</script>

<template>
    <div class="surface-ground flex align-items-center justify-content-center min-h-screen min-w-screen overflow-hidden ">
        <div class="flex flex-column align-items-center justify-content-center">
            <div style="border-radius: 56px; padding: 0.3rem; background: linear-gradient(180deg, var(--primary-color) 10%, rgba(33, 150, 243, 0) 30%)">
                <div class="w-full surface-card py-8 px-5 sm:px-8" style="border-radius: 53px">
                    <div class="text-center mb-5">
                        <img :src="logoUrl" alt="Samana Group Logo" class="mb-2 w-6rem flex-shrink-0" />
                        <div class="text-900 text-3xl font-medium mb-3">Welcome to CareerPath!</div>
                        <span class="text-600 font-medium">Sign in to continue</span>
                    </div>
                    <div>
                        <Button label="Login with Google" icon="pi pi-google" class="w-full p-3 text-xl mt-3" @click="loginWithGoogle"></Button>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <Toast />
</template>

<style scoped>
.pi-eye {
    transform: scale(1.6);
    margin-right: 1rem;
}

.pi-eye-slash {
    transform: scale(1.6);
    margin-right: 1rem;
}
</style>