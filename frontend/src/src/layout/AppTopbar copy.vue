<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import { useLayout } from '@/layout/composables/layout';
import { useRouter } from 'vue-router';
import { usePrimeVue } from 'primevue/config';
import InputText from 'primevue/inputtext';
import Textarea from 'primevue/textarea';
import Button from 'primevue/button';
import Dropdown from 'primevue/dropdown';
import OverlayPanel from 'primevue/overlaypanel';
import html2canvas from 'html2canvas';
import axios from 'axios';
import ProgressSpinner from 'primevue/progressspinner';
import Badge from 'primevue/badge';
import Tooltip from 'primevue/tooltip';
import Toast from 'primevue/toast';

const { layoutConfig, onMenuToggle } = useLayout();
const $primevue = usePrimeVue();

const outsideClickListener = ref(null);
const topbarMenuActive = ref(false);
const dropdownActive = ref(false);
const router = useRouter();
const toast = ref(null);

const userName = ref('');
const userProfileImage = ref('');
const feedbackType = ref(null);
const feedbackOptions = [
    { label: 'Application Error', value: 'Application Error' },
    { label: 'Functionality', value: 'Functionality' },
    { label: 'Observation', value: 'Observation' },
    { label: 'Other', value: 'Other' }
];
const description = ref('');
const email = ref('');
const uploadUrl = ref('');
const loading = ref(false);
const errorMessage = ref('');
const feedbackSubmitted = ref(false);
const accessToken = ref('');

const logoUrl = computed(() => `${layoutConfig.darkTheme.value ? 'samana-logo-white' : 'samana-logo-dark'}.png`);
const darkModeIcon = computed(() => layoutConfig.darkTheme.value ? 'pi pi-sun' : 'pi pi-moon');

const bindOutsideClickListener = () => {
    if (!outsideClickListener.value) {
        outsideClickListener.value = (event) => {
            if (isOutsideClicked(event)) {
                topbarMenuActive.value = false;
                dropdownActive.value = false;
            }
        };
        document.addEventListener('click', outsideClickListener.value);
    }
};

const unbindOutsideClickListener = () => {
    if (outsideClickListener.value) {
        document.removeEventListener('click', outsideClickListener.value);
        outsideClickListener.value = null;
    }
};

const isOutsideClicked = (event) => {
    if (!topbarMenuActive.value && !dropdownActive.value) return;

    const sidebarEl = document.querySelector('.layout-topbar-menu');
    const topbarEl = document.querySelector('.layout-topbar-button');
    const dropdownEl = document.querySelector('.profile-dropdown');

    return !(sidebarEl.isSameNode(event.target) || sidebarEl.contains(event.target) || topbarEl.isSameNode(event.target) || topbarEl.contains(event.target) || dropdownEl.isSameNode(event.target) || dropdownEl.contains(event.target));
};

const toggleDarkMode = () => {
    layoutConfig.darkTheme.value = !layoutConfig.darkTheme.value;
    const newThemeName = layoutConfig.darkTheme.value ? layoutConfig.theme.value.replace('light', 'dark') : layoutConfig.theme.value.replace('dark', 'light');
    $primevue.changeTheme(layoutConfig.theme.value, newThemeName, 'theme-css', () => {
        layoutConfig.theme.value = newThemeName;
        layoutConfig.darkTheme.value = layoutConfig.darkTheme.value;
    });
};

const onTopBarMenuButton = () => {
    topbarMenuActive.value = !topbarMenuActive.value;
};

const toggleDropdown = () => {
    dropdownActive.value = !dropdownActive.value;
};

const getUserEmailFromCookie = () => {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; userEmail=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
};

const fetchUserInfo = async () => {
    const token = getAuthToken();
    if (token) {
        try {
            const response = await fetch('https://www.googleapis.com/oauth2/v1/userinfo?alt=json&access_token=' + token);
            const userInfo = await response.json();
            userName.value = userInfo.name;
            userProfileImage.value = userInfo.picture;
        } catch (error) {
            console.error('Error fetching user info:', error);
        }
    }
};

const getAuthToken = () => {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; authToken=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
};

const navigateTo = (path) => {
    if (path === '/auth/account') {
        const email = getUserEmailFromCookie();
        if (email) {
            sessionStorage.setItem('employeeEmail', email);
        }
        path = '/employeeprofile';
    }
    router.push(path);
    dropdownActive.value = false;
};

const handleFeedbackSubmit = async () => {
    loading.value = true;
    uploadUrl.value = '';
    errorMessage.value = '';

    try {
        const canvas = await html2canvas(document.body);
        const blob = await new Promise(resolve => canvas.toBlob(resolve, 'image/png'));

        if (blob) {
            uploadUrl.value = await uploadToGoogleDrive(blob, getAuthToken());
            await submitFeedback(uploadUrl.value);
        }
    } catch (error) {
        console.error('Error capturing and uploading screenshot:', error);
        errorMessage.value = 'Failed to upload screenshot. Please try again.';
    } finally {
        loading.value = false;
    }
};

const uploadToGoogleDrive = async (blob, accessToken) => {
    const sessionEmail = getUserEmailFromCookie();
    const currentDateTime = new Date().toISOString().replace(/T/, '_').replace(/:/g, '-').split('.')[0];
    const fileName = `screenshot_${sessionEmail}_${currentDateTime}.png`;

    const fileMetadata = {
        'name': fileName,
        'parents': [import.meta.env.VITE_FEEDBACK_FOLDER]
    };

    const form = new FormData();
    form.append('metadata', new Blob([JSON.stringify(fileMetadata)], { type: 'application/json' }));
    form.append('file', blob);

    try {
        const response = await fetch('https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${accessToken}`,
                'Accept': 'application/json'
            },
            body: form
        });

        if (!response.ok) {
            throw new Error(await response.text());
        }

        const data = await response.json();
        return `https://drive.google.com/file/d/${data.id}/view`;
    } catch (error) {
        console.error('Error uploading to Google Drive:', error);
        throw new Error('Upload failed: ' + error.message);
    }
};

const submitFeedback = async (screenshotUrl) => {
    try {
        const response = await axios.post(`https://${import.meta.env.VITE_SITE_URL}/api/apitest.php`, {
            action: 'addFeedback',
            type: feedbackType.value,
            description: description.value,
            email: email.value,
            screenshotUrl
        });

        if (response.data.success) {
            toast.value.add({ severity: 'success', summary: 'Success', detail: 'Feedback submitted successfully!', life: 3000 }); 
            feedbackSubmitted.value = true;
           

        } else {
            errorMessage.value = 'Failed to submit feedback.';
        }
    } catch (error) {
        console.error('Error submitting feedback:', error);
        errorMessage.value = 'Failed to submit feedback. Please try again.';
    }
};

onMounted(() => {
    bindOutsideClickListener();
    fetchUserInfo();
    email.value = getUserEmailFromCookie();
});

onBeforeUnmount(() => {
    unbindOutsideClickListener();
});

const resetFeedbackForm = () => {
  feedbackType.value = null;
  description.value = '';
  email.value = getUserEmailFromCookie();
  errorMessage.value = ''; // Clear any previous error messages
  feedbackSubmitted.value = false; // Allow resubmission
};
const toggleFeedbackOverlay = (event) => {
    resetFeedbackForm();
  feedbackOverlay.value.toggle(event);
};
</script>

<template>
    <div class="layout-topbar">
        <router-link to="/" class="layout-topbar-logo">
            <img :src="logoUrl" alt="logo" class="logo-image" />
            <div class="app-title">
                <span class="app-title">Samana CareerPath <small class="version-text">0.65 B</small></span>
            </div>
        </router-link>

        <div class="layout-topbar-icons">
            <div class="user-greeting">
                Hello, <span>{{ userName }}</span>
            </div>
            <div class="darkmode-option">
                <button class="p-link layout-topbar-button" @click="toggleDarkMode()">
                    <i :class="darkModeIcon"></i>
                </button>
            </div>

            <div class="profile-dropdown-wrapper">
                <button class="p-link layout-topbar-button" @click="toggleDropdown()">
                    <img :src="userProfileImage" alt="User Profile Image" class="user-profile-image" />
                </button>
                <div v-if="dropdownActive" class="profile-dropdown">
                    <button @click="navigateTo('/auth/account')" class="p-link layout-topbar-button">Account</button>
                    <button @click="navigateTo('/auth/logout')" class="p-link layout-topbar-button">Log out</button>
                </div>
            </div>




            <button class="p-link layout-topbar-button" @click="$refs.feedbackOverlay.toggle($event)"  v-tooltip="'Platform Feedback'">
                <i class="pi pi-exclamation-circle"></i>
            </button>

            <OverlayPanel ref="feedbackOverlay" :breakpoints="{ '960px': '55vw' }" style="width: 250px" class="grid p-fluid">
                <h6>Application Feedback</h6>
                <div class="grid formgrid">
                <form @submit.prevent="handleFeedbackSubmit">
                    <div class="col-12 ">
                    <Dropdown v-model="feedbackType" :options="feedbackOptions" optionLabel="label" placeholder="Select Feedback Type" />
                    </div>
                    <div class="col-12 ">
                    <Textarea v-model="description" rows="4" required placeholder="Description" />
                    </div>
                    <div class="col-12 ">
                    <InputText v-model="email" type="email" disabled hidden />
                    <Button label="Submit" icon="pi pi-upload" type="submit" :disabled="loading" />
                    </div>
                </form>
                <p v-if="loading" class="col-12 ">
                    <ProgressSpinner style="width: 50px; height: 50px;" strokeWidth="5" animationDuration=".5s" />
                </p>
 
                <p v-if="errorMessage && !feedbackSubmitted" class="error-message">{{ errorMessage }}</p>
                </div>
            </OverlayPanel>
            <button class="p-link layout-menu-button layout-topbar-button" @click="onMenuToggle()">
                        <i class="pi pi-bars"></i>
            </button>
        </div>
    </div>
    <Toast ref="toast" />
</template>

<style lang="scss" scoped>
.layout-topbar-logo {
    order: 1;
    width: 30px; /* Adjust the width as needed for mobile */
    height: auto; /* Maintain aspect ratio */
}

.layout-topbar-icons {
    order: 2;
    display: flex;
    align-items: center;
    margin-left: auto;
    gap: 0.5rem; /* Adjust the gap value as needed for symmetry */
}

.user-greeting {
    font-weight: bold;
}

.user-profile-image {
    width: 30px;
    height: 30px;
    border-radius: 50%;
}

.profile-dropdown-wrapper {
    position: relative;
}

.profile-dropdown {
    position: absolute;
    right: 0;
    background-color: var(--surface-card);
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
    border-radius: 0px; /* Change to square corners */
    overflow: hidden;
    z-index: 10;
    opacity: 0;
    transform: translateY(-10px);
    transition: opacity 0.3s ease, transform 0.3s ease;
}

.profile-dropdown-wrapper:hover .profile-dropdown,
.profile-dropdown-wrapper:focus-within .profile-dropdown {
    opacity: 1;
    transform: translateY(0);
}

.profile-dropdown button {
    display: block;
    width: 100%;
    padding: 0.5rem 1rem;
    text-align: left;
    border-radius: 0px; /* Ensure button corners are also square */
}

.profile-dropdown button:hover {
    background-color: var(--surface-hover);
    border-radius: 0px; /* Ensure hover state has square corners */
}

.feedback-form {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.success-message {
    color: green;
    font-weight: bold;
}

.error-message {
    color: red;
}

@media (max-width: 768px) {
    .layout-topbar-logo {
        order: 1;
        width: 30px; /* Adjust the width as needed for mobile */
        height: auto;  /* Maintain aspect ratio */
    }
    .layout-topbar-icons {
        order: 2;
        gap: 0.25rem; /* Reduce the gap on mobile */
    }
    .profile-dropdown-wrapper {

    }
    .app-title {
        font-size: 14px; /* Adjust as needed */
        line-height: 30px; /* Matches the desired height */
        height: 30px;
        overflow: hidden; /* Prevents text from overflowing the container */
        white-space: nowrap; /* Prevents text from wrapping to the next line */
        text-overflow: ellipsis; /* Adds an ellipsis if the text is too long */
    }
    .darkmode-option {

    }
    .layout-topbar-button span { 
        display: none; /* Hide button text labels on mobile */
    }
    /* Target the menu button */
    .layout-menu-button {
        /* Place the menu button last */

    }
    .user-greeting {
        display: none;
    }
}

.app-title .version-text {
    font-size: 10px;
}
</style>