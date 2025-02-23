<script setup>
import LazyImage from '@/components/landing/LazyImage.vue';
import Logo from '@/components/landing/Logo.vue';
import { ref, computed, watch, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import Select from 'primevue/select';
import InputText from 'primevue/inputtext';
import Checkbox from 'primevue/checkbox';
import Button from 'primevue/button';
import { useToast } from 'primevue/usetoast';
import Toast from 'primevue/toast';
import { CountryService } from '@/service/CountryService';
import AutoComplete from 'primevue/autocomplete';
import ProgressSpinner from 'primevue/progressspinner';
import Dialog from 'primevue/dialog';

const employeeRanges = ref([
    { label: '0-10 employees', value: '0-10' },
    { label: '20-50 employees', value: '20-50' },
    { label: '50-100 employees', value: '50-100' },
    { label: '100-500 employees', value: '100-500' },
    { label: '500-5000 employees', value: '500-5000' },
    { label: '5000-10000 employees', value: '5000-10000' }
]);

// Country handling
const countries = ref([]);
const selectedCountry = ref(null);
const filteredCountries = ref([]);

// Load countries on mount
onMounted(async () => {
    try {
        // Get countries from service
        const data = await CountryService.getCountries();
        countries.value = data;
        
        // Set default to United States if available
        selectedCountry.value = data.find(c => c.code === 'US') || data[0];
    } catch (error) {
        console.error('Error loading countries:', error);
    }

    // Get IP address
    ipAddress.value = await getIpAddress();
});

const companyname = ref('');
const email = ref('');
const phonenumber = ref('');
const remember = ref(false);
const adminName = ref('');

const emailError = ref(false); // Track email error visibility
const phoneError = ref(false); // Track phone error visibility

const website = ref('');

const selectedPhoneCode = ref(countries.value[0]);

const handlePhoneCodeChange = (event) => {
    // Find and set the country based on phone code
    const country = countries.value.find(c => c.phoneCode === event.value.phoneCode);
    if (country) {
        selectedCountry.value = country;
        phonenumber.value = ''; // Reset phone number when country changes
    }
};

const isValidEmail = computed(() => {
    if (!email.value) return true;
    
    // More permissive email regex that allows dots in username part
    const emailRegex = /^[a-zA-Z0-9]+([\._-]?[a-zA-Z0-9]+)*@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*(\.[a-zA-Z]{2,})$/;
    
    // First check basic format
    if (!emailRegex.test(email.value)) {
        return false;
    }
    
    // Check for common invalid patterns
    const invalidPatterns = [
        /\.{2,}/, // Multiple consecutive dots
        /^[.-]/, // Starting with dot or hyphen
        /[.-]@/, // Dot or hyphen before @
        /@.*@/, // Multiple @ symbols
    ];
    
    return !invalidPatterns.some(pattern => pattern.test(email.value));
});

// Phone validation based on international format
const isValidPhone = computed(() => {
    if (!phonenumber.value) return true;
    
    // Basic international phone validation
    const cleanNumber = phonenumber.value.replace(/[^\d+]/g, '');
    
    // Must start with + and have 5-15 digits
    const phoneRegex = /^\+\d{5,15}$/;
    return phoneRegex.test(cleanNumber);
});

const isValidWebsite = computed(() => {
    if (!website.value) return true;
    const websiteRegex = /^(https?:\/\/)?([\da-z.-]+)\.([a-z.]{2,6})(\/.*)*\/?$/;
    return websiteRegex.test(website.value.trim());
});

const websiteError = ref(false);

watch(website, () => {
    websiteError.value = !isValidWebsite.value && website.value;
});

const canRegister = computed(() => {
    return companyname.value &&
        isValidEmail.value &&
        isValidPhone.value &&
        adminName.value &&
        selectedEmployeeRange.value &&
        selectedCountry.value &&
        isValidWebsite.value &&
        remember.value;
});

// Watch for changes to show/hide error messages
watch(email, () => {
    emailError.value = !isValidEmail.value && email.value;
});
watch(phonenumber, () => {
    phoneError.value = !isValidPhone.value && phonenumber.value;
});

function validateForm() {
    // Force error check on submit
    emailError.value = !isValidEmail.value;
    phoneError.value = !isValidPhone.value;
    websiteError.value = !isValidWebsite.value;

    if (canRegister.value) {
        navigateToVerification();
    }
}

const router = useRouter();
const toast = useToast();

// Update formatPhoneNumber to allow + character
const formatPhoneNumber = (event) => {
    // Allow + only at the start and numbers
    phonenumber.value = event.target.value.replace(/[^\d+]|(?!^)\+/g, '');
};

// Update phone error messages
const getPhoneErrorMessage = computed(() => {
    if (!phonenumber.value) return '';
    
    switch (selectedCountry.value.name) {
        case 'United Arab Emirates':
            return 'Enter a valid UAE number (e.g., +971501234567 or 0501234567)';
        case 'United States':
            return 'Enter a valid US number (e.g., +11234567890 or 1234567890)';
        case 'United Kingdom':
            return 'Enter a valid UK number (e.g., +441234567890 or 01234567890)';
        case 'Qatar':
            return 'Enter a valid Qatar number (e.g., +97412345678 or 12345678)';
        case 'Saudi Arabia':
            return 'Enter a valid Saudi number (e.g., +966512345678 or 512345678)';
        case 'Oman':
            return 'Enter a valid Oman number (e.g., +96879123456 or 79123456)';
        default:
            return 'Please enter a valid phone number';
    }
});

const showContactAdmin = ref(false);
const contactMessage = ref('');

// Add loading state
const isLoading = ref(false);

// Add toast configuration
const showToast = (type, title, message) => {
    const toastConfig = {
        severity: type,
        summary: title,
        detail: message,
        life: 5000,
        closable: true
    };

    // Add special styling for company exists warning
    if (type === 'warn' && title === 'Company Already Registered') {
        toastConfig.styleClass = 'company-exists-toast';
    }

    // Add special styling for success messages
    if (type === 'success') {
        toastConfig.styleClass = 'success-toast';
    }

    toast.add(toastConfig);
};

// Add new refs for verification
const showVerificationDialog = ref(false);
const verificationCode = ref('');
const verificationEmail = ref('');
const verificationError = ref('');
const isVerifying = ref(false);

// Update the verifyCode function
async function verifyCode() {
    if (isVerifying.value) return;
    
    isVerifying.value = true;
    try {
        const response = await fetch(`${import.meta.env.VITE_API_URL}/auth/verify/code`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('azure_token')}`
            },
            body: JSON.stringify({
                email: verificationEmail.value,
                code: verificationCode.value.trim()
            })
        });

        const data = await response.json();

        if (response.ok) {
            showToast('success', 'Success', 'Company verified successfully!');
            showVerificationDialog.value = false;
            resetForm();
            
            // Add delay before redirect to show success message
            setTimeout(() => {
                router.push({
                    path: '/auth/login',
                    query: { 
                        email: verificationEmail.value,
                        verified: 'true'
                    }
                });
            }, 1500);
        } else {
            verificationError.value = data.detail?.message || 'Invalid verification code';
            if (data.detail?.type === 'code_expired') {
                showVerificationDialog.value = false;
                showToast('error', 'Code Expired', data.detail.message);
            }
        }
    } catch (error) {
        verificationError.value = 'Failed to verify code. Please try again.';
        showToast('error', 'Verification Failed', 'Failed to verify code. Please try again.');
    } finally {
        isVerifying.value = false;
    }
}

// Update the resendVerification function
async function resendVerification() {
    if (isVerifying.value) return;
    
    isVerifying.value = true;
    try {
        const response = await fetch(`${import.meta.env.VITE_API_URL}/auth/verify/resend/${verificationEmail.value}`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('azure_token')}`
            }
        });

        const data = await response.json();

        if (response.ok) {
            showToast('info', 'Code Resent', 'A new verification code has been sent to your email.');
            verificationCode.value = '';
            verificationError.value = '';
        } else {
            showToast('error', 'Error', data.detail?.message || 'Failed to resend code');
            if (data.detail?.type === 'rate_limit') {
                showVerificationDialog.value = false;
            }
        }
    } catch (error) {
        showToast('error', 'Error', 'Failed to resend verification code');
    } finally {
        isVerifying.value = false;
    }
}

// Update navigateToVerification function
async function navigateToVerification() {
    if (isLoading.value) return;
    
    isLoading.value = true;
    try {
        const registrationData = {
            companyName: companyname.value.trim(),
            email: email.value.trim(),
            phoneNumber: phonenumber.value.replace(/\s/g, ''),
            adminName: adminName.value.trim(),
            website: website.value.trim(),
            employeeRange: selectedEmployeeRange.value,
            country: selectedCountry.value.name,
            ipAddress: ipAddress.value
        };
        
        const response = await fetch(`${import.meta.env.VITE_API_URL}/auth/verify/send`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(registrationData)
        });

        const data = await response.json();

        if (response.ok) {
            verificationEmail.value = data.email;
            showVerificationDialog.value = true;
            showToast(
                'success',
                'Verification Email Sent',
                `Please check your email (${data.email}) for the verification code.`
            );
        } else {
            if (data.detail?.type === 'company_exists') {
                resetForm();
                showToast(
                    'warn',
                    'Company Already Registered',
                    data.detail.message
                );
                showContactAdmin.value = true;
                contactMessage.value = data.detail.message;
            } else {
                throw new Error(data.detail?.message || 'Failed to send verification');
            }
        }
    } catch (error) {
        console.error('Registration error:', error);
        showToast(
            'error',
            'Registration Failed',
            error.message || 'Failed to send verification. Please try again.'
        );
    } finally {
        isLoading.value = false;
    }
}

// Update error message display
const getEmailErrorMessage = computed(() => {
    if (!email.value) return '';
    
    if (email.value.includes('..')) {
        return 'Email cannot contain consecutive dots';
    }
    if (email.value.startsWith('.') || email.value.startsWith('-')) {
        return 'Email cannot start with a dot or hyphen';
    }
    if (email.value.includes('.@') || email.value.includes('-@')) {
        return 'Email cannot have a dot or hyphen just before @';
    }
    if ((email.value.match(/@/g) || []).length > 1) {
        return 'Email cannot contain multiple @ symbols';
    }
    
    return 'Please enter a valid corporate email address';
});

// Add computed for website error message
const getWebsiteErrorMessage = computed(() => {
    if (!website.value) return '';
    return 'Please enter a valid website URL (e.g., www.company.com)';
});

function resetForm() {
    companyname.value = '';
    website.value = '';
    email.value = '';
    phonenumber.value = '';
    adminName.value = '';
    selectedEmployeeRange.value = '';
    selectedCountry.value = countries.value[0];
    remember.value = false;
    showContactAdmin.value = false;
    contactMessage.value = '';
    ipAddress.value = null;  // Reset IP address
}

const ipAddress = ref(null);

async function getIpAddress() {
    try {
        const response = await fetch('https://api.ipify.org?format=json');
        const data = await response.json();
        return data.ip;
    } catch (error) {
        console.error('Error getting IP address:', error);
        return null;
    }
}

const selectedEmployeeRange = ref('');

const searchCountry = async (event) => {
    try {
        if (!countries.value.length) {
            // Load countries if not already loaded
            countries.value = await CountryService.getCountries();
        }
        
        filteredCountries.value = countries.value.filter(country => 
            country.name.toLowerCase().includes(event.query.toLowerCase())
        );
    } catch (error) {
        console.error('Error searching countries:', error);
        filteredCountries.value = [];
    }
};
</script>

<template>
    <section
        class="min-h-screen flex items-center lg:items-start lg:py-20 justify-center animate-fadein animate-duration-300 animate-ease-in max-w-[100rem] mx-auto"
    >
        <div class="flex w-full h-full justify-center gap-12">
            <div class="flex flex-col py-20 lg:min-w-[30rem]">
                <router-link to="/" class="flex items-center justify-center lg:justify-start mb-8 gap-2">
                    <LazyImage 
                        src="/demo/images/samana-logo.png" 
                        alt="CareerPath" 
                        isLogo 
                        className="dark:brightness-200"
                    />
                    <span class="text-4xl font-semibold text-surface-900 dark:text-surface-0">Welcome to CareerPath!</span>
                </router-link>
                <div class="flex flex-col justify-center flex-grow">
                    <div class="max-w-md mx-auto w-full">
                      
                        <p class="body-small mt-3.5 text-center lg:text-left">
                            Streamline your hiring process with AI-powered tools for candidate evaluation and team building. Join leading organizations using CareerPath to make data-driven hiring decisions.
                        </p>

                        <div class="flex items-center gap-3.5 my-7">
                            <span class="flex h-[1px] bg-surface-200 dark:bg-surface-800" />
                            <span class="flex-1 h-[1px] bg-surface-200 dark:bg-surface-800" />
                        </div>

                        <InputText type="text" v-model="companyname" class="w-full" placeholder="Company Name" />

                        <!-- Add Website Input -->
                        <InputText 
                            type="text" 
                            v-model="website" 
                            class="w-full mt-4" 
                            placeholder="Company Website (e.g., www.company.com)" 
                            :class="{ 'p-invalid': websiteError }"
                        />
                        <small class="text-red-500" v-if="websiteError">{{ getWebsiteErrorMessage }}</small>

                        <!-- Add Employee Range Dropdown -->
                        <div class="mt-4">
                            <Select
                                v-model="selectedEmployeeRange"
                                :options="employeeRanges"
                                optionLabel="label"
                                optionValue="value"
                                placeholder="Select number of employees"
                                class="w-full"
                            />
                        </div>

                        <!-- Add Country Dropdown -->
                        <div class="mt-4">
                            <AutoComplete
                                v-model="selectedCountry"
                                :suggestions="filteredCountries"
                                @complete="searchCountry"
                                optionLabel="name"
                                placeholder="Type to search country"
                                class="w-full"
                                :class="{ 'p-invalid': !selectedCountry && canRegister }"
                                :dropdown="true"
                            >
                                <template #option="slotProps">
                                    <div class="flex align-items-center">
                                        <span>{{ slotProps.option.name }}</span>
                                    </div>
                                </template>
                            </AutoComplete>
                            <small class="text-red-500" v-if="!selectedCountry && canRegister">
                                Please select a country
                            </small>
                        </div>

                        <InputText 
                            type="text" 
                            v-model="adminName" 
                            class="w-full mt-4" 
                            placeholder="Root Admin Name" 
                        />

                        <InputText 
                            type="text" 
                            v-model="email" 
                            class="w-full mt-4" 
                            placeholder="Corporate Email" 
                            :class="{ 'p-invalid': emailError }" 
                        />
                        <small class="text-red-500" v-if="emailError">{{ getEmailErrorMessage }}</small>

                        <!-- Phone input with country context -->
                        <div class="w-full mt-4">
                            <InputText 
                                type="text" 
                                v-model="phonenumber" 
                                class="w-full" 
                                :placeholder="`Enter phone number (e.g., +${selectedCountry?.code}...)`"
                                :class="{ 'p-invalid': phoneError }"
                                @input="formatPhoneNumber"
                            />
                            <small class="text-red-500" v-if="phoneError">
                                Please enter a valid international phone number starting with + and country code
                            </small>
                        </div>

                        <div class="my-8 flex items-center justify-between">
                            <div class="flex items-center gap-2">
                                <Checkbox inputId="remember" v-model="remember" :binary="true" />
                                <label for="remember" class="body-small">
                                    <span class="label-small text-surface-950 dark:text-surface-0">I have read the </span>
                                    Terms and Conditions
                                </label>
                            </div>
                        </div>
                        <Button 
                            @click="validateForm" 
                            type="button" 
                            class="body-button w-full relative" 
                            :disabled="!canRegister || isLoading"
                        >
                            <span :class="{ 'opacity-0': isLoading }">Register</span>
                            <div 
                                v-if="isLoading" 
                                class="absolute top-0 left-0 w-full h-full flex items-center justify-center"
                            >
                                <ProgressSpinner 
                                    style="width: 1.5rem; height: 1.5rem" 
                                    strokeWidth="4" 
                                    fill="var(--surface-ground)" 
                                    animationDuration=".5s"
                                />
                            </div>
                        </Button>
                        <div class="mt-4 text-center">
                            <small class="text-surface-400 dark:text-surface-500 text-sm">
                                {{ ipAddress ? `Your IP address: ${ipAddress}` : 'Unable to detect IP address' }}
                            </small>
                        </div>
                    </div>
                </div>
                <div v-if="showContactAdmin" class="mt-4 p-4 bg-yellow-50 dark:bg-yellow-900 rounded-lg">
                    <div class="flex items-start">
                        <i class="pi pi-exclamation-triangle mr-3 text-yellow-500" style="font-size: 1.5rem;"></i>
                        <div>
                            <h6 class="text-sm font-semibold mb-1">Company Already Registered</h6>
                            <p class="text-sm">{{ contactMessage }}</p>
                            <a 
                                href="mailto:support@careerpath.samanagroup.com" 
                                class="inline-block mt-2 text-sm text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300"
                            >
                                Contact Support
                            </a>
                        </div>
                    </div>
                </div>
                <div class="mt-8 text-center lg:text-start block relative text-surface-400 dark:text-surface-500 text-sm">
                    ©{{ new Date().getFullYear() }} CareerPath by Samana Group
                </div>
            </div>
            <div class="hidden lg:flex h-full py-20">
                <div
                    class="h-full w-full lg:max-w-[32.5rem] xl:max-w-[60.5rem] mx-auto flex items-center justify-center shadow-[0px_1px_2px_0px_rgba(18,18,23,0.05)] rounded-3xl border border-surface overflow-hidden"
                >
                    <LazyImage class="w-auto h-full object-contain object-left" src="https://fqjltiegiezfetthbags.supabase.co/storage/v1/render/image/public/block.images/blocks/hero/hero-1.png" alt="Auth Image" />
                </div>
            </div>
        </div>
        <Toast position="top-right" />

        <!-- Add Verification Dialog -->
        <Dialog 
            v-model:visible="showVerificationDialog"
            modal
            :closable="false"
            :style="{ width: '90%', maxWidth: '400px' }"
            class="p-fluid"
        >
            <template #header>
                <h3 class="text-xl font-semibold">Enter Verification Code</h3>
            </template>

            <div class="flex flex-col gap-4">
                <p class="text-sm text-surface-600">
                    Please enter the verification code sent to {{ verificationEmail }}
                </p>

                <div class="field">
                    <InputText
                        v-model="verificationCode"
                        type="text"
                        placeholder="Enter 6-digit code"
                        :class="{ 'p-invalid': verificationError }"
                        maxlength="6"
                        @keyup.enter="verifyCode"
                    />
                    <small class="text-red-500" v-if="verificationError">{{ verificationError }}</small>
                </div>

                <div class="flex flex-col gap-2">
                    <Button
                        type="button"
                        label="Verify"
                        :loading="isVerifying"
                        @click="verifyCode"
                    />
                    <Button
                        type="button"
                        label="Resend Code"
                        severity="secondary"
                        :loading="isVerifying"
                        @click="resendVerification"
                    />
                    <Button
                        type="button"
                        label="Cancel"
                        severity="danger"
                        text
                        @click="showVerificationDialog = false"
                    />
                </div>
            </div>
        </Dialog>
    </section>
</template>

<style>
.company-exists-toast {
    background-color: #fff3cd;
    border-color: #ffeeba;
    color: #856404;
}

.dark .company-exists-toast {
    background-color: #433204;
    border-color: #856404;
    color: #fff3cd;
}

:deep(.p-autocomplete) {
    width: 100%;
}

:deep(.p-autocomplete-input) {
    width: 100%;
    padding: 0.75rem;
}

:deep(.p-autocomplete-panel) {
    max-height: 250px;
    overflow-y: auto;
}

.p-button:disabled {
    opacity: 0.7;
    cursor: wait;
}

:deep(.p-progress-spinner) {
    width: 1.5rem;
    height: 1.5rem;
}

:deep(.p-progress-spinner-circle) {
    stroke: var(--primary-color-text);
    stroke-width: 4;
    animation-duration: 0.5s;
}

/* Add new toast styles */
.success-toast {
    background-color: #d4edda !important;
    border-color: #c3e6cb !important;
    color: #155724 !important;
}

.dark .success-toast {
    background-color: #1e4c2c !important;
    border-color: #155724 !important;
    color: #d4edda !important;
}

.p-toast .p-toast-message {
    margin: 0 0 1rem 0;
    padding: 1rem;
    border-radius: 6px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.p-toast .p-toast-message .p-toast-message-content {
    padding: 0;
    margin: 0;
}

.p-toast .p-toast-message .p-toast-message-content .p-toast-summary {
    font-weight: 600;
    font-size: 1rem;
    margin-bottom: 0.5rem;
}

.p-toast .p-toast-message .p-toast-message-content .p-toast-detail {
    margin: 0;
    line-height: 1.5;
    font-size: 0.875rem;
}

:deep(.p-toast-icon-close) {
    width: 2rem;
    height: 2rem;
    border-radius: 50%;
    background: transparent;
    transition: background-color 0.2s;
}

:deep(.p-toast-icon-close:hover) {
    background: rgba(0,0,0,0.1);
}

:deep(.p-dialog-header) {
    padding: 1.5rem 1.5rem 0.5rem 1.5rem;
}

:deep(.p-dialog-content) {
    padding: 1.5rem;
}

:deep(.p-dialog) {
    border-radius: 1rem;
}

:deep(.p-inputtext) {
    text-align: center;
    letter-spacing: 0.5rem;
    font-size: 1.5rem;
}
</style>