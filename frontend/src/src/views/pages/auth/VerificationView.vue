<template>
    <section class="min-h-screen flex items-center lg:items-start lg:py-20 justify-center animate-fadein animate-duration-300 animate-ease-in max-w-[100rem] mx-auto">
        <div class="flex w-full h-full justify-center gap-12">
            <div class="flex flex-col py-20 lg:min-w-[30rem]">
                <router-link to="/" class="flex items-center justify-center lg:justify-start mb-8">
                    <Logo />
                </router-link>
                <div class="flex flex-col justify-center flex-grow">
                    <div class="max-w-md mx-auto w-full">
                        <!-- Verification Form -->
                        <div v-if="!isVerified">
                            <h5 class="title-h5 text-center lg:text-left">Verification</h5>
                            <p class="body-small mt-3.5 text-center lg:text-left">
                                We have sent a code to your email: 
                                <span class="text-primary">{{ email }}</span>
                            </p>
                            <form class="mt-8" @submit.prevent="verifyCode">
                                <InputOtp 
                                    v-model="code" 
                                    :length="6" 
                                    class="!w-full" 
                                    pt:pcInput:root:class="!flex-1 xl:!w-9 !w-full"
                                    :disabled="loading"
                                />
                                <small v-if="errorMessage" class="block text-red-500 mt-2">{{ errorMessage }}</small>
                                
                                <div class="flex align-items-center justify-content-between my-4">
                                    <span class="text-600">Code expires in: {{ timeLeft }}</span>
                                    <a 
                                        class="font-medium no-underline text-blue-500 cursor-pointer" 
                                        @click="resendCode"
                                        :class="{ 'opacity-50 cursor-not-allowed': resendDisabled }"
                                    >
                                        {{ resendDisabled ? 'Wait 1 minute to resend' : 'Resend Code' }}
                                    </a>
                                </div>

                                <div class="flex items-center gap-4 mt-8">
                                    <button 
                                        @click="$router.push('/auth/company')" 
                                        type="button" 
                                        class="body-button border border-surface-200 dark:border-surface-800 bg-transparent hover:bg-surface-100 dark:hover:bg-surface-800 text-surface-950 dark:text-surface-0 flex-1"
                                    >
                                        Cancel
                                    </button>
                                    <button 
                                        type="submit" 
                                        class="body-button flex-1"
                                        :disabled="loading || code.length !== 6"
                                    >
                                        Verify
                                    </button>
                                </div>
                            </form>
                        </div>

                        <!-- Success Message -->
                        <div v-else class="text-center animate-fadein">
                            <i class="pi pi-check-circle text-6xl text-green-500 mb-4"></i>
                            <h5 class="title-h5 mb-4">Verification Successful!</h5>
                            <p class="body-small mb-8">
                                Welcome to TimeBandit! Your company <span class="font-semibold">{{ companyName }}</span> has been successfully verified.
                                You can now proceed to login and start managing your time efficiently.
                            </p>
                            <button 
                                @click="goToLogin" 
                                class="body-button w-full"
                            >
                                Proceed to Login
                            </button>
                        </div>
                    </div>
                </div>
                <div class="mt-8 text-center lg:text-start block relative text-surface-400 dark:text-surface-500 text-sm">
                    ©{{ new Date().getFullYear() }} EEC Services
                </div>
            </div>
            <div class="hidden lg:flex h-full py-20">
                <div class="h-full w-full lg:max-w-[32.5rem] xl:max-w-[60.5rem] mx-auto flex items-center justify-center shadow-[0px_1px_2px_0px_rgba(18,18,23,0.05)] rounded-3xl border border-surface overflow-hidden">
                    <LazyImage class="w-auto h-full object-contain object-left" src="/demo/images/landing/auth-image.svg" alt="Auth Image" />
                </div>
            </div>
        </div>
        <Toast />
    </section>
</template>

<script setup>
import LazyImage from '@/components/landing/LazyImage.vue';
import Logo from '@/components/landing/Logo.vue';
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import axios from 'axios';
import InputOtp from 'primevue/inputotp';
import Toast from 'primevue/toast';
import { useToast } from 'primevue/usetoast';

const router = useRouter();
const route = useRoute();
const toast = useToast();

// Form data
const code = ref('');
const email = ref('');
const companyName = ref('');
const phoneNumber = ref('');
const adminName = ref('');
const website = ref('');
const employeeRange = ref('');
const country = ref('');

// UI states
const loading = ref(false);
const errorMessage = ref('');
const timeLeft = ref('15:00');
const resendDisabled = ref(false);
const isVerified = ref(false);
let timer;

onMounted(() => {
    // Get email from route query params first (from API response)
    const emailFromQuery = route.query.email;
    
    if (emailFromQuery) {
        email.value = emailFromQuery;
        // Start timer for code expiration
        startTimer();
        return;
    }

    // Fallback to registration data if no query param
    const registrationData = JSON.parse(localStorage.getItem('registrationData') || '{}');
    
    if (!registrationData.email || !registrationData.company_name) {
        toast.add({
            severity: 'error',
            summary: 'Error',
            detail: 'Please complete the registration form first',
            life: 3000
        });
        router.push('/auth/company');
        return;
    }

    // Set values from registration data
    email.value = registrationData.email;
    companyName.value = registrationData.company_name;
    phoneNumber.value = registrationData.phone_number;
    adminName.value = registrationData.admin_name;
    website.value = registrationData.website;
    employeeRange.value = registrationData.employee_range;
    country.value = registrationData.country;

    // Start timer
    startTimer();
});

onBeforeUnmount(() => {
    if (timer) clearInterval(timer);
});

const startTimer = () => {
    let timeInSeconds = 15 * 60; // 15 minutes
    if (timer) {
        clearInterval(timer);
    }
    
    timeLeft.value = '15:00'; // Reset display immediately
    
    timer = setInterval(() => {
        timeInSeconds--;
        if (timeInSeconds <= 0) {
            clearInterval(timer);
            timeLeft.value = 'Expired';
            // Enable resend when timer expires
            resendDisabled.value = false;
        } else {
            const minutes = Math.floor(timeInSeconds / 60);
            const seconds = timeInSeconds % 60;
            timeLeft.value = `${minutes}:${seconds.toString().padStart(2, '0')}`;
        }
    }, 1000);
};

const sendVerificationCode = async (retries = 3) => {
    try {
        loading.value = true;
        resendDisabled.value = true;

        // Get data from localStorage
        const registrationData = JSON.parse(localStorage.getItem('registrationData') || '{}');
        
        // Validate data before sending
        if (!registrationData.email || !registrationData.companyName || 
            !registrationData.phoneNumber || !registrationData.adminName) {
            throw new Error('Missing registration data');
        }

        const response = await axios.post('https://timebandit.eecservices.com/core/auth/verify/send', {
            email: registrationData.email,
            company_name: registrationData.companyName,
            phone_number: registrationData.phoneNumber,
            admin_name: registrationData.adminName
        });

        // Update local state with registration data
        email.value = registrationData.email;
        companyName.value = registrationData.companyName;
        phoneNumber.value = registrationData.phoneNumber;
        adminName.value = registrationData.adminName;

        toast.add({
            severity: 'success',
            summary: 'Code Sent',
            detail: 'Verification code has been sent to your email',
            life: 3000
        });

        startTimer();
        setTimeout(() => {
            resendDisabled.value = false;
        }, 60000);

    } catch (error) {
        console.error('Verification error:', error);
        
        if (error.message === 'Missing registration data') {
            toast.add({
                severity: 'error',
                summary: 'Error',
                detail: 'Please complete the registration form first',
                life: 3000
            });
            router.push('/auth/company');
            return;
        }
        
        // Handle validation errors
        if (error.response?.data?.[0]?.msg) {
            errorMessage.value = error.response.data[0].msg;
        } else if (error.response?.status === 502 && retries > 0) {
            await new Promise(resolve => setTimeout(resolve, 1000));
            return sendVerificationCode(retries - 1);
        } else {
            errorMessage.value = error.response?.data?.detail?.message || 
                               error.response?.data?.detail || 
                               'Failed to send verification code';
        }

        toast.add({
            severity: 'error',
            summary: 'Error',
            detail: errorMessage.value,
            life: 5000
        });
    } finally {
        loading.value = false;
    }
};

const verifyCode = async () => {
    if (!code.value || code.value.length !== 6) return;
    
    try {
        loading.value = true;
        errorMessage.value = '';
        
        await axios.post('https://timebandit.eecservices.com/core/auth/verify/code', {
            email: email.value,
            code: code.value
        });

        // Show success state
        isVerified.value = true;
        toast.add({
            severity: 'success',
            summary: 'Verification Successful',
            detail: 'Your email has been verified successfully!',
            life: 3000
        });

    } catch (error) {
        errorMessage.value = error.response?.data?.detail || 'Invalid verification code';
        toast.add({
            severity: 'error',
            summary: 'Verification Failed',
            detail: errorMessage.value,
            life: 3000
        });
    } finally {
        loading.value = false;
    }
};

const resendCode = async () => {
    if (!resendDisabled.value) {
        try {
            loading.value = true;
            resendDisabled.value = true;

            const response = await axios.post('https://timebandit.eecservices.com/core/auth/verify/send', {
                email: email.value,
                company_name: companyName.value,
                phone_number: phoneNumber.value,
                admin_name: adminName.value
            });

            toast.add({
                severity: 'success',
                summary: 'Code Sent',
                detail: 'A new verification code has been sent to your email',
                life: 3000
            });

            // Reset timer
            startTimer();

            // Enable resend after 1 minute
            setTimeout(() => {
                resendDisabled.value = false;
            }, 60000);

        } catch (error) {
            console.error('Resend error:', error);
            
            const errorMessage = error.response?.data?.detail?.message || 
                               error.response?.data?.detail || 
                               'Failed to resend verification code';
            
            toast.add({
                severity: 'error',
                summary: 'Error',
                detail: errorMessage,
                life: 5000
            });
        } finally {
            loading.value = false;
        }
    }
};

const goToLogin = () => {
    router.push({
        path: '/auth/login',
        query: { verified: 'true', email: email.value }
    });
};
</script>
