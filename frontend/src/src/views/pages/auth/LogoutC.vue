<script setup>
import { useLayout } from '@/layout/composables/layout';
import { ref, computed, onMounted } from 'vue';
import AppConfig from '@/layout/AppConfig.vue';
import { useRouter } from 'vue-router';

const { layoutConfig } = useLayout();
const router = useRouter();
const logoutMessage = ref('');

const logoUrl = computed(() => {
    return `/${layoutConfig.darkTheme.value ? 'samana-logo-white' : 'samana-logo-dark'}.png`;
});

const handleLogout = () => {
    // Get all cookies and split them into individual name=value pairs
    const cookies = document.cookie.split(';');

    // Loop through all cookies and delete each one
    cookies.forEach((cookie) => {
        const eqPos = cookie.indexOf('=');
        const name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;
        document.cookie = name + '=; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC; SameSite=Lax; Secure';
    });


    logoutMessage.value = 'You have successfully logged out';
};

onMounted(() => {
    handleLogout();
});
</script>

<template>
    <div class="surface-ground flex align-items-center justify-content-center min-h-screen min-w-screen overflow-hidden">
        <div class="flex flex-column align-items-center justify-content-center">
            <div style="border-radius: 56px; padding: 0.3rem; background: linear-gradient(180deg, var(--primary-color) 10%, rgba(33, 150, 243, 0) 30%)">
                <div class="w-full surface-card py-8 px-5 sm:px-8" style="border-radius: 53px">
                    <div class="text-center mb-5">
                        <img :src="logoUrl" alt="Samana logo" class="mb-2 w-6rem flex-shrink-0" />
                        <div class="text-900 text-3xl font-medium mb-3">{{ logoutMessage }}</div>
                        <Button label="Login Again" class="w-full p-3 text-xl mt-3" @click="router.push('/auth/register')"></Button>
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
</style>