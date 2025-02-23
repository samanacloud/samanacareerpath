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

const employeeRanges = ref([
    { label: '0-10 employees', value: '0-10' },
    { label: '20-50 employees', value: '20-50' },
    { label: '50-100 employees', value: '50-100' },
    { label: '100-500 employees', value: '100-500' },
    { label: '500-5000 employees', value: '500-5000' },
    { label: '5000-10000 employees', value: '5000-10000' }
]);

const countries = ref([
    { 
        name: 'United States', 
        code: 'US',
        phoneCode: '+1',
        pattern: /^(\+?1)?[-. ]?\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$/
    },
    { 
        name: 'United Kingdom', 
        code: 'UK',
        phoneCode: '+44',
        pattern: /^(?:(?:\+44)|0)?(?:[1-9]\d{8,9})$/
    },
    { 
        name: 'United Arab Emirates', 
        code: 'UAE',
        phoneCode: '+971',
        pattern: /^(?:\+971|0)?(?:50|51|52|53|54|55|56|58|2|3|4|6|7|9)\d{7}$/
    },
    {
        name: 'Qatar',
        code: 'QA',
        phoneCode: '+974',
        pattern: /^(?:\+974|0)?(?:3|4|5|6|7)\d{7}$/
    },
    {
        name: 'Saudi Arabia',
        code: 'SA',
        phoneCode: '+966',
        pattern: /^(?:\+966|0)?(?:5)\d{8}$/
    },
    {
        name: 'Oman',
        code: 'OM',
        phoneCode: '+968',
        pattern: /^(?:\+968|0)?(?:7|9)\d{7}$/
    }
]);

const selectedEmployeeRange = ref('');
const selectedCountry = ref(countries.value[0]);

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

const isValidPhone = computed(() => {
    if (!phonenumber.value) return true;
    
    // Allow + and numbers only
    const cleanNumber = phonenumber.value.replace(/[^\d+]/g, '');
    
    switch (selectedCountry.value.name) {
        case 'United Arab Emirates':
            return /^\+971\d{9}$/.test(cleanNumber) || // Format: +971501234567
                   /^(0|5)\d{8}$/.test(cleanNumber);   // Format: 0501234567 or 501234567
        case 'United States':
            return /^\+1\d{10}$/.test(cleanNumber) ||  // Format: +11234567890
                   /^\d{10}$/.test(cleanNumber);       // Format: 1234567890
        case 'United Kingdom':
            return /^\+44\d{10}$/.test(cleanNumber) || // Format: +441234567890
                   /^\d{10,11}$/.test(cleanNumber);    // Format: 01234567890
        case 'Qatar':
            return /^\+974\d{8}$/.test(cleanNumber) || // Format: +97412345678
                   /^\d{8}$/.test(cleanNumber);        // Format: 12345678
        case 'Saudi Arabia':
            return /^\+9665\d{8}$/.test(cleanNumber) || // Format: +966512345678
                   /^5\d{8}$/.test(cleanNumber);        // Format: 512345678
        case 'Oman':
            return /^\+968[79]\d{7}$/.test(cleanNumber) || // Format: +96879123456
                   /^[79]\d{7}$/.test(cleanNumber);        // Format: 79123456
        default:
            return true;
    }
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

async function navigateToVerification() {
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
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('azure_token')}`
            },
            body: JSON.stringify(registrationData)
        });

        const data = await response.json();

        if (response.ok) {
            // Navigate to verification with email from response
            router.push({
                path: '/auth/verification',
                query: { email: data.email }
            });
        } else {
            // Handle specific error cases
            if (data.detail?.type === 'company_exists') {
                // Clear the form
                resetForm();
                
                toast.add({
                    severity: 'warn',
                    summary: 'Company Already Registered',
                    detail: data.detail.message,
                    life: 5000,
                    closable: true,
                    styleClass: 'company-exists-toast'
                });

                showContactAdmin.value = true;
                contactMessage.value = data.detail.message;
            } else {
                throw new Error(data.detail?.message || 'Failed to send verification');
            }
        }
    } catch (error) {
        console.error('Registration error:', error);
        toast.add({
            severity: 'error',
            summary: 'Error',
            detail: error.message || 'Failed to send verification. Please try again.',
            life: 3000
        });
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

onMounted(async () => {
    ipAddress.value = await getIpAddress();
});
</script>

<template>
    <section
        class="min-h-screen flex items-center lg:items-start lg:py-20 justify-center animate-fadein animate-duration-300 animate-ease-in max-w-[100rem] mx-auto"
    >
        <div class="flex w-full h-full justify-center gap-12">
            <div class="flex flex-col py-20 lg:min-w-[30rem]">
                <router-link to="/" class="flex items-center justify-center lg:justify-start mb-8">
                    <Logo />
                </router-link>
                <div class="flex flex-col justify-center flex-grow">
                    <div class="max-w-md mx-auto w-full">
                        <h5 class="title-h5 text-center lg:text-left">Welcome to TimeBandit!</h5>
                        <p class="body-small mt-3.5 text-center lg:text-left">
                            Ready to streamline your time management? Register your company today and unlock powerful tools to track, manage, and optimize your team's time. Join countless businesses already benefiting from
                            TimeBandit's intuitive platform.
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
                            <Select
                                v-model="selectedCountry"
                                :options="countries"
                                optionLabel="name"
                                placeholder="Select country"
                                class="w-full"
                            />
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

                        <div class="w-full mt-4">
                            <InputText 
                                type="text" 
                                v-model="phonenumber" 
                                class="w-full" 
                                :placeholder="'Enter phone number for ' + selectedCountry.name"
                                :class="{ 'p-invalid': phoneError }"
                                @input="formatPhoneNumber"
                            />
                            <small class="text-red-500" v-if="phoneError">{{ getPhoneErrorMessage }}</small>
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
                        <Button @click="validateForm" type="button" class="body-button w-full" :disabled="!canRegister">Register</Button>
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
                            <!-- Add contact information or support link -->
                            <a 
                                href="mailto:support@timebandit.com" 
                                class="inline-block mt-2 text-sm text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300"
                            >
                                Contact Support
                            </a>
                        </div>
                    </div>
                </div>
                <div class="mt-8 text-center lg:text-start block relative text-surface-400 dark:text-surface-500 text-sm">©{{ new Date().getFullYear() }} EEC Services</div>
            </div>
            <div class="hidden lg:flex h-full py-20">
                <div
                    class="h-full w-full lg:max-w-[32.5rem] xl:max-w-[60.5rem] mx-auto flex items-center justify-center shadow-[0px_1px_2px_0px_rgba(18,18,23,0.05)] rounded-3xl border border-surface overflow-hidden"
                >
                    <LazyImage class="w-auto h-full object-contain object-left" src="/demo/images/landing/auth-image.svg" alt="Auth Image" />
                </div>
            </div>
        </div>
        <Toast />
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
</style>