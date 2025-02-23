<script setup>
import { ref, onMounted } from 'vue';
import LazyImage from '@/components/landing/LazyImage.vue';
import { useToast } from 'primevue/usetoast';
import { useRouter } from 'vue-router';

const email = ref('');
const password = ref('');
const checked = ref(false);
const ipAddress = ref('');
const showEmailForm = ref(false);
const showVerificationForm = ref(false);
const verificationCode = ref('');
const isLoading = ref(false);
const toast = useToast();
const router = useRouter();

// Get IP address on mount
onMounted(async () => {
    try {
        const response = await fetch('https://api.ipify.org?format=json');
        const data = await response.json();
        ipAddress.value = data.ip;

        // Handle logout message
        const urlParams = new URLSearchParams(window.location.search);
        if (urlParams.get('success') === 'true') {
            showToast('success', 'Success', urlParams.get('message'));
        } else if (urlParams.get('error') === 'true') {
            showToast('error', 'Error', urlParams.get('message'));
        }
        
        // Clean up URL after showing toast
        if (urlParams.has('success') || urlParams.has('error')) {
            window.history.replaceState({}, '', '/auth/login');
        }
    } catch (error) {
        console.error('Error fetching IP:', error);
        ipAddress.value = 'Unable to detect IP';
    }
});

const showToast = (type, title, message) => {
    toast.add({
        severity: type,
        summary: title,
        detail: message,
        life: 5000,
        closable: true
    });
};

const handleEmailSubmit = async () => {
    if (!email.value || isLoading.value || !ipAddress.value) return;
    
    isLoading.value = true;
    try {
        const response = await fetch(`${import.meta.env.VITE_API_URL}/auth/email/send`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                email: email.value,
                ipAddress: ipAddress.value
            })
        });

        const data = await response.json();

        if (response.ok) {
            // Show server's success message
            showToast(
                'success',
                'Verification Code Sent',
                data.message || 'Please check your email for the verification code'
            );
            
            // Reset verification code and show form
            verificationCode.value = '';
            showVerificationForm.value = true;
        } else {
            showToast('error', 'Error', data.detail?.message || 'Failed to send verification code');
        }
    } catch (error) {
        console.error('Email verification error:', error);
        showToast('error', 'Error', 'Failed to send verification code');
    } finally {
        isLoading.value = false;
    }
};

const verifyCode = async () => {
    if (!verificationCode.value || isLoading.value || !ipAddress.value) return;
    
    isLoading.value = true;
    try {
        const response = await fetch(`${import.meta.env.VITE_API_URL}/auth/email/code`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: email.value,
                code: verificationCode.value.trim(),
                ipAddress: ipAddress.value
            })
        });

        const data = await response.json();

        if (response.ok) {
            // Store session token
            localStorage.setItem('session_token', data.session_token);
            
            // Decode token to get user info
            const tokenParts = data.session_token.split('.');
            const tokenPayload = JSON.parse(atob(tokenParts[1]));
            
            // Show success toast with user's name and company
            showToast(
                'success',
                'Login Successful',
                `Welcome back ${tokenPayload.userName}! You've been logged in to ${tokenPayload.companyName}`
            );
            
            // Reset forms
            showVerificationForm.value = false;
            verificationCode.value = '';
            
            // Add delay before redirect to show success message
            setTimeout(() => {
                // Redirect to dashboard or home page
                router.push('/');
            }, 2000); // Increased delay to 2 seconds to ensure toast is visible
        } else {
            showToast('error', 'Error', data.detail?.message || 'Invalid verification code');
        }
    } catch (error) {
        console.error('Code verification error:', error);
        showToast('error', 'Error', 'Failed to verify code');
    } finally {
        isLoading.value = false;
    }
};

// Handle social login
const handleGoogleLogin = async () => {
    if (isLoading.value) return;
    
    isLoading.value = true;
    try {
        // First, get the Google OAuth URL from our backend
        const response = await fetch(`${import.meta.env.VITE_API_URL}/auth/google/url`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                ipAddress: ipAddress.value,
                redirectUri: `${window.location.origin}/auth/callback`
            })
        });

        const data = await response.json();

        if (response.ok && data.url) {
            // Redirect to Google's OAuth page
            window.location.href = data.url;
        } else {
            showToast('error', 'Error', data.detail?.message || 'Failed to initialize Google login');
        }
    } catch (error) {
        console.error('Google login error:', error);
        showToast('error', 'Error', 'Failed to initialize Google login');
    } finally {
        isLoading.value = false;
    }
};

const handleMicrosoftLogin = () => {
    // Implement Microsoft login (disabled for now)
    console.log('Microsoft login clicked');
};

const switchToEmailLogin = () => {
    showEmailForm.value = true;
};
</script>

<template>
    <div class="bg-surface-50 dark:bg-surface-950 flex items-center justify-center min-h-screen min-w-[100vw] overflow-hidden">
        <Toast />
        
        <div class="flex flex-col items-center justify-center">
            <div style="border-radius: 56px; padding: 0.3rem; background: linear-gradient(180deg, var(--primary-color) 10%, rgba(33, 150, 243, 0) 30%)">
                <div class="w-full bg-surface-0 dark:bg-surface-900 py-20 px-8 sm:px-20" style="border-radius: 53px">
                    <div class="text-center mb-8">
                        <LazyImage src="/demo/images/samana-logo.png" alt="CareerPath" isLogo className="dark:brightness-200 mx-auto block" />
                        <div class="text-surface-900 dark:text-surface-0 text-3xl font-medium mb-4">Welcome to Careerpath!</div>
                        <span class="text-muted-color font-medium">Sign in to continue</span>
                    </div>

                    <!-- Social Login Buttons -->
                    <div class="flex flex-col gap-3 mb-8 login-form-container" v-if="!showEmailForm">
                        <Button 
                            class="p-button-google p-button-raised w-full" 
                            @click="handleGoogleLogin"
                            :loading="isLoading"
                        >
                            <i class="pi pi-google mr-2"></i>
                            Continue with Google
                        </Button>
                        
                        <Button 
                            class="p-button-microsoft w-full" 
                            disabled
                            @click="handleMicrosoftLogin"
                        >
                            <i class="pi pi-microsoft p-button-raised mr-2"></i>
                            Continue with Microsoft
                        </Button>

                        <div class="relative text-center my-4">
                            <span class="bg-surface-0 dark:bg-surface-900 px-4 text-muted-color">or</span>
                            <div class="absolute top-1/2 left-0 right-0 h-px bg-surface-200 dark:bg-surface-700 -z-1"></div>
                        </div>

                        <Button 
                            class="p-button-secondary w-full"
                            @click="switchToEmailLogin"
                        >
                            <i class="pi pi-envelope mr-2"></i>
                            Use Email Instead
                        </Button>
                    </div>

                    <!-- Email Login Form -->
                    <div v-if="showEmailForm" class="login-form-container">
                        <div class="flex flex-col gap-3">
                            <Button 
                                icon="pi pi-arrow-left" 
                                class="p-button-text p-button-rounded self-start" 
                                @click="showEmailForm = false"
                                aria-label="Go back"
                                :disabled="showVerificationForm"
                            />

                            <div class="flex flex-col gap-2">
                                <label for="email1" class="block text-surface-900 dark:text-surface-0 text-xl font-medium">
                                    Email
                                </label>
                                <InputText 
                                    id="email1" 
                                    type="text" 
                                    placeholder="Email address" 
                                    class="w-full" 
                                    v-model="email"
                                    @keyup.enter="handleEmailSubmit"
                                    :disabled="showVerificationForm"
                                    :class="{ 'p-disabled': showVerificationForm }"
                                />
                            </div>

                            <Button 
                                v-if="!showVerificationForm"
                                label="Continue" 
                                class="w-full mt-2" 
                                @click="handleEmailSubmit"
                                :loading="isLoading"
                            />

                            <div v-if="showVerificationForm" class="verification-section">
                                <label class="block text-surface-900 dark:text-surface-0 text-xl font-medium mb-2">
                                    Verification Code
                                </label>
                                <InputText 
                                    v-model="verificationCode"
                                    type="text"
                                    placeholder="Enter 6-digit code"
                                    class="w-full text-center text-2xl tracking-widest mb-4"
                                    maxlength="6"
                                    @keyup.enter="verifyCode"
                                />
                                <Button 
                                    label="Verify Code" 
                                    class="w-full" 
                                    @click="verifyCode"
                                    :loading="isLoading"
                                />
                            </div>
                        </div>
                    </div>

                    <!-- IP Address and Copyright -->
                    <div class="mt-8 text-center text-surface-400 dark:text-surface-500 text-sm">
                        <div class="mb-2">
                            {{ ipAddress ? `Your IP address: ${ipAddress}` : 'Unable to detect IP address' }}
                        </div>
                        <div>
                            ©{{ new Date().getFullYear() }} CareerPath by Samana Group
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
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

/* Social Login Button Styles */
.p-button-google {
    background-color: #4285f4;
    border-color: #4285f4;
    color: white;
}

.p-button-google:hover {
    background-color: #357abd;
    border-color: #357abd;
}

.p-button-microsoft {
    background-color: #2f2f2f;
    border-color: #2f2f2f;
    color: white;
}

.p-button-microsoft:not(:disabled):hover {
    background-color: #1f1f1f;
    border-color: #1f1f1f;
}

.p-button-microsoft:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.-z-1 {
    z-index: -1;
}

.verification-section {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    margin-top: 0.5rem;
}

.verification-section input {
    letter-spacing: 0.5em;
}

/* Add success toast styling */
:deep(.p-toast-message-success) {
    background-color: #d4edda;
    border: solid #c3e6cb;
    border-width: 0 0 0 6px;
    color: #155724;
}

:deep(.dark .p-toast-message-success) {
    background-color: #1e4c2c;
    border-color: #155724;
    color: #d4edda;
}

:deep(.p-toast-message-success .p-toast-message-icon) {
    color: #28a745;
}

:deep(.dark .p-toast-message-success .p-toast-message-icon) {
    color: #2fd365;
}

/* Add this new style for consistent form container size */
.login-form-container {
    width: 100%;
    max-width: 320px; /* Adjust this value to match your social buttons width */
    margin: 0 auto;
    min-height: 200px; /* Adjust this value to match your social buttons height */
    display: flex;
    flex-direction: column;
}

/* Ensure consistent button heights */
.p-button {
    height: 2.5rem; /* Adjust this value to match your existing buttons */
}

/* Ensure consistent input heights */
.p-inputtext {
    height: 2.5rem; /* Adjust this value to match your existing inputs */
}

/* Add styles for disabled state */
.p-disabled {
    opacity: 0.6;
    cursor: not-allowed;
    background-color: var(--surface-200);
}
</style>
