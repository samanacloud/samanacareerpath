<script setup>
import { useLayout } from '@/layout/composables/layout';
import { ref, computed, onMounted } from 'vue';
import AppConfig from '@/layout/AppConfig.vue';
import { useRouter } from 'vue-router';
import { useToast } from 'primevue/usetoast';
import axios from 'axios';

const { layoutConfig } = useLayout();
const router = useRouter();
const toast = useToast();

const logoUrl = computed(() => {
    return `/${layoutConfig.darkTheme.value ? 'samana-logo-white' : 'samana-logo-dark'}.png`;
});

const convertCookieValue = (name) => {
    const value = document.cookie
        .split('; ')
        .find(row => row.startsWith(name))
        ?.split('=')[1];
    return value ? decodeURIComponent(value.replace(/\+/g, ' ')) : null;
};

const loginWithGoogle = async () => {
    window.location.href = `/api/oauthRedirect`;
};

onMounted(async () => {
    const urlParams = new URLSearchParams(window.location.search);
    const status = urlParams.get('status');
    const message = urlParams.get('message');
    const userData = urlParams.get('userData');

    if (userData) {
        const userInfo = JSON.parse(decodeURIComponent(userData));
        const email = userInfo.email;

        // Delete existing cookies
        document.cookie = 'userName=; Max-Age=-99999999;';
        document.cookie = 'userEmail=; Max-Age=-99999999;';
        document.cookie = 'userProfileImage=; Max-Age=-99999999;';
        document.cookie = 'CandidateName=; Max-Age=-99999999;';
        document.cookie = 'CandidateEmail=; Max-Age=-99999999;';
        document.cookie = 'ProfileImage=; Max-Age=-99999999;';
        document.cookie = 'admin=; Max-Age=-99999999;';

        if (email.includes('@samanagroup.co')) {
            try {
                const userDetailsResponse = await axios.post(`/api/apireg`, {
                    action: 'getUserDetails',
                    email
                });

                const adminValue = userDetailsResponse.data.admin;

                // Set new cookies
                document.cookie = `authToken=${userInfo.accessToken}; path=/; SameSite=Lax; Secure`;
                document.cookie = `userName=${userInfo.name}; path=/; SameSite=Lax; Secure`;
                document.cookie = `userProfileImage=${userInfo.picture}; path=/; SameSite=Lax; Secure`;
                document.cookie = `userEmail=${userInfo.email}; path=/; SameSite=Lax; Secure`;
                document.cookie = `idToken=${userInfo.idToken}; path=/; SameSite=Lax; Secure`;
                document.cookie = `admin=${adminValue}; path=/; SameSite=Lax; Secure`;

                router.push('/');
            } catch (error) {
                toast.add({
                    severity: 'error',
                    summary: 'Error',
                    detail: 'Failed to retrieve user details. Please try again.',
                    life: 5000
                });
            }
        } else if (email.includes('@gmail.com')) {
            document.cookie = `CandidateToken=${userInfo.accessToken}; path=/; SameSite=Lax; Secure`;
            document.cookie = `CandidateName=${userInfo.name}; path=/; SameSite=Lax; Secure`;
            document.cookie = `ProfileImage=${userInfo.picture}; path=/; SameSite=Lax; Secure`;
            document.cookie = `CandidateEmail=${userInfo.email}; path=/; SameSite=Lax; Secure`;
            document.cookie = `CandidateidToken=${userInfo.idToken}; path=/; SameSite=Lax; Secure`;
            router.push('/landing');
        }
    }

    if (status === 'success') {
        toast.add({
            severity: 'success',
            summary: 'Login Successful',
            detail: message,
            life: 5000
        });
    } else if (status === 'error') {
        toast.add({
            severity: 'error',
            summary: 'Login Error',
            detail: message,
            life: 5000
        });
    }
});
</script>

<template>
    <div class="surface-ground flex align-items-center justify-content-center min-h-screen min-w-screen overflow-hidden ">
        <div class="flex flex-column align-items-center justify-content-center">
            <div style="border-radius: 56px; padding: 0.3rem; background: linear-gradient(180deg, var(--primary-color) 10%, rgba(33, 150, 243, 0) 30%)">
                <div class="w-full surface-card py-8 px-5 sm:px-8" style="border-radius: 53px">
                    <div class="text-center mb-5">
                        <img :src="logoUrl" alt="Samana Group Logo" class="mb-2 w-6rem flex-shrink-0" />
                        <div class="text-900 text-3xl font-medium mb-3">Welcome to CareerPath</div>
                        <span class="text-600 font-medium">Sign in to continue</span>
                    </div>
                    <div>
                        <Button label="Login with Google" icon="pi pi-google" class="w-full p-3 text-xl mt-3" @click="loginWithGoogle"></Button>
                    </div>
                    <div class="layout-footer">
                        <img :src="logoUrl" alt="Logo" height="20" class="mr-2" />
                        by
                        <span class="font-medium ml-2">Samana Group LLC</span>, All Rights Reserved
                        <div class="ml-4">
                            <a href="/termsofservice" class="text-primary">Terms of Use</a> | 
                            <a href="/privacypolicy" class="text-primary">Privacy Policy</a>
                        </div>
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
.layout-footer {
    background-color: #e0f2ff;
    text-align: center;
    width: 100%;
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 1rem; /* Increase padding to make the footer higher */
    box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.1); /* Optional: Adds a shadow to give it some depth */
}
</style>