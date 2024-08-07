<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import { useLayout } from '@/layout/composables/layout';
import { useRouter } from 'vue-router';
import { usePrimeVue } from 'primevue/config';

const { layoutConfig, onMenuToggle } = useLayout();
const $primevue = usePrimeVue();

const outsideClickListener = ref(null);
const topbarMenuActive = ref(false);
const dropdownActive = ref(false);
const router = useRouter();





const userName = ref('');
const userProfileImage = ref('');

// Function to get the auth token from cookies
function getAuthToken() {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; authToken=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}



// Fetch user info from the auth token
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

onMounted(() => {
    bindOutsideClickListener();
    fetchUserInfo();
});

onBeforeUnmount(() => {
    unbindOutsideClickListener();
});

const logoUrl = computed(() => {
    return `${layoutConfig.darkTheme.value ? 'samana-logo-white' : 'samana-logo-dark'}.png`;
});

const onTopBarMenuButton = () => {
    topbarMenuActive.value = !topbarMenuActive.value;
};
const onSettingsClick = () => {
    topbarMenuActive.value = false;
    router.push('/documentation');
};
const topbarMenuClasses = computed(() => {
    return {
        'layout-topbar-menu-mobile-active': topbarMenuActive.value
    };
});

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

// Dark mode switch functionality
const toggleDarkMode = () => {
    layoutConfig.darkTheme.value = !layoutConfig.darkTheme.value;
    const newThemeName = layoutConfig.darkTheme.value ? layoutConfig.theme.value.replace('light', 'dark') : layoutConfig.theme.value.replace('dark', 'light');
    onChangeTheme(newThemeName, layoutConfig.darkTheme.value);
};

const onChangeTheme = (theme, mode) => {
    $primevue.changeTheme(layoutConfig.theme.value, theme, 'theme-css', () => {
        layoutConfig.theme.value = theme;
        layoutConfig.darkTheme.value = mode;
    });
};

const darkModeIcon = computed(() => {
    return layoutConfig.darkTheme.value ? 'pi pi-sun' : 'pi pi-moon';
});

const toggleDropdown = () => {
    dropdownActive.value = !dropdownActive.value;
};

const getUserEmailFromCookie = () => {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; userEmail=`);
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
</script>

<template>
    <div class="layout-topbar">
        <router-link to="/" class="layout-topbar-logo">
            <img :src="logoUrl" alt="logo" class="logo-image" />
            <div class="app-title"><span class="app-title">Samana CareerPath <small class="version-text">0.5 Beta</small></span></div>
        </router-link>
            
            <div class="layout-topbar-icons">
                        <div  class="user-greeting">
                            Hello, <span >{{ userName }}</span>
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

                    <button class="p-link layout-menu-button layout-topbar-button" @click="onMenuToggle()">
                        <i class="pi pi-bars"></i>
                    </button>
            </div>
    </div>
</template>

<style lang="scss" scoped>
.layout-topbar-logo {
        order: 1;
        width: 30px; /* Adjust the width as needed for mobile */
        height: auto;  /* Maintain aspect ratio */
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