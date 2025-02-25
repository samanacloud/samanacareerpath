<script setup>
import { useLayout } from '@/layout/composables/layout';
import { computed, ref, onMounted } from 'vue';
import AppConfigurator from './AppConfigurator.vue';
import Avatar from 'primevue/avatar';
import Button from 'primevue/button';
import Menu from 'primevue/menu';
import { useRouter } from 'vue-router';

const router = useRouter();
const { toggleMenu, toggleDarkMode, isDarkTheme } = useLayout();
const menu = ref();
const items = ref([
    {
        label: 'Profile',
        icon: 'pi pi-user',
        command: () => {
            // Handle profile click
        }
    },
    {
        label: 'Logout',
        icon: 'pi pi-power-off',
        command: () => {
            handleLogout();
        }
    }
]);

// Compute logo URL based on dark mode state
const logoUrl = computed(() => 
    isDarkTheme.value ? '/demo/images/samana-logo-white.png' : '/demo/images/samana-logo-dark.png'
);

// Add state for session info
const sessionInfo = ref(null);

// Function to fetch and update session info
const fetchSessionInfo = async () => {
    try {
        const response = await fetch('/core/auth/verify/session', {
            method: 'GET',
            credentials: 'include',
            headers: {
                'Accept': 'application/json',
            }
        });

        if (response.ok) {
            const data = await response.json();
            sessionInfo.value = data.user;
            // Store the session info in localStorage for use in other components
            if(data.user){
                localStorage.setItem('userName', data.user.userName || '');
                localStorage.setItem('userEmail', data.user.email || '');
            }
        }
    } catch (error) {
        console.error('Error fetching session info:', error);
    }
};

// Fetch session info on component mount
onMounted(() => {
    fetchSessionInfo();
});

// Function to get initials from name
const getInitials = (name) => {
    if (!name) return '';
    return name
        .split(' ')
        .map(word => word[0])
        .join('')
        .toUpperCase()
        .slice(0, 2);
};

// Add logout handler
const handleLogout = async () => {
    try {
        const response = await fetch(`${import.meta.env.VITE_API_URL}/auth/logout`, {
            method: 'POST',
            credentials: 'include'  // Important to include cookies
        });

        if (response.ok) {
            // Clear local storage
            localStorage.removeItem('session_token');
            localStorage.removeItem('userName');
            localStorage.removeItem('userEmail');
            // Redirect to login page with success message
            router.push({
                path: '/auth/login',
                query: { 
                    success: 'true',
                    message: 'You have been successfully logged out'
                }
            });
        }
    } catch (error) {
        console.error('Logout error:', error);
        router.push({
            path: '/auth/login',
            query: { 
                error: 'true',
                message: 'Error during logout'
            }
        });
    }
};
</script>

<template>
    <div class="layout-topbar">
        <div class="layout-topbar-logo-container">
            <button class="layout-menu-button layout-topbar-action" @click="toggleMenu">
                <i class="pi pi-bars"></i>
            </button>
            <router-link to="/" class="layout-topbar-logo">
                <img :src="logoUrl" alt="Samana CareerPath" class="logo" />
                <span>CareerPath</span>
            </router-link>
        </div>

        <div class="layout-topbar-actions">
            <div class="layout-config-menu">
                <button type="button" class="layout-topbar-action" @click="toggleDarkMode">
                    <i :class="['pi', { 'pi-moon': isDarkTheme, 'pi-sun': !isDarkTheme }]"></i>
                </button>
            </div>

            <!-- User info with avatar and menu button -->
            <div v-if="sessionInfo" class="flex items-center mr-4 gap-3 relative">
                <div class="hidden md:flex flex-col items-end">
                    <span class="text-sm font-medium text-gray-900 dark:text-surface-0">{{ sessionInfo.userName }}</span>
                    <span class="text-xs text-gray-600 dark:text-surface-0/80">{{ sessionInfo.companyName }}</span>
                </div>
                <Avatar 
                    :label="getInitials(sessionInfo.userName)"
                    size="medium"
                    class="bg-primary outline outline-1 outline-offset-2 outline-primary"
                />
                <Button
                    icon="pi pi-angle-down"
                    @click="menu.toggle($event)"
                    aria-haspopup="true"
                    aria-controls="overlay_menu"
                    class="p-button-text p-button-rounded"
                />
                <Menu ref="menu" id="overlay_menu" :model="items" :popup="true" />
            </div>
        </div>
    </div>
</template>

<style scoped>
.session-debug-tooltip {
    display: none;
    position: absolute;
    background: #333;
    color: white;
    padding: 10px;
    border-radius: 4px;
    font-size: 12px;
    white-space: pre-wrap;
    z-index: 1000;
    max-width: 400px;
    top: 100%;
    right: 0;
    margin-top: 5px;
}

.layout-topbar-action:hover .session-debug-tooltip {
    display: block;
}

pre {
    margin: 0;
    font-family: monospace;
}
</style>