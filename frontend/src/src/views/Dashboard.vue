<script setup>
import { onMounted } from 'vue';
import { useToast } from 'primevue/usetoast';
import BestSellingWidget from '@/components/dashboard/BestSellingWidget.vue';
import NotificationsWidget from '@/components/dashboard/NotificationsWidget.vue';
import RecentSalesWidget from '@/components/dashboard/RecentSalesWidget.vue';
import RevenueStreamWidget from '@/components/dashboard/RevenueStreamWidget.vue';
import StatsWidget from '@/components/dashboard/StatsWidget.vue';

const toast = useToast();

onMounted(async () => {
    // Get URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('success') === 'true') {
        try {
            // Fetch session info to get user data
            const response = await fetch('/core/auth/verify/session', {
                method: 'GET',
                credentials: 'include',
                headers: {
                    'Accept': 'application/json',
                }
            });

            if (response.ok) {
                const data = await response.json();
                const userName = data.user.userName;
                
                // Show personalized welcome toast
                toast.add({
                    severity: 'success',
                    summary: userName === 'Juan Pablo' ? 'Welcome back Juan!' : `Welcome back ${userName}!`,
                    detail: 'You have successfully logged in',
                    life: 3000
                });
            }
        } catch (error) {
            console.error('Error fetching session info:', error);
            // Fallback to generic welcome message
            toast.add({
                severity: 'success',
                summary: 'Welcome Back!',
                detail: 'You have successfully logged in',
                life: 3000
            });
        }

        // Clean up URL parameters
        window.history.replaceState({}, '', '/');
    }
});
</script>

<template>
    <div class="grid grid-cols-12 gap-8">
        <StatsWidget />

        <div class="col-span-12 xl:col-span-6">
            <RecentSalesWidget />
            <BestSellingWidget />
        </div>
        <div class="col-span-12 xl:col-span-6">
            <RevenueStreamWidget />
            <NotificationsWidget />
        </div>
    </div>
</template>
