<script setup>
import { onMounted, ref } from 'vue';
import { useToast } from 'primevue/usetoast';
import { useRouter } from 'vue-router';

// Import dashboard widgets
import EmployeeStatsWidget from '@/components/dashboard/EmployeeStatsWidget.vue';
import CandidateStatsWidget from '@/components/dashboard/CandidateStatsWidget.vue';
import RecruitmentProcessWidget from '@/components/dashboard/RecruitmentProcessWidget.vue';
import CertificationStatsWidget from '@/components/dashboard/CertificationStatsWidget.vue';
import RecentActivitiesWidget from '@/components/dashboard/RecentActivitiesWidget.vue';
import WelcomeGuideWidget from '@/components/dashboard/WelcomeGuideWidget.vue';

const toast = useToast();
const loading = ref(true);
const sessionInfo = ref(null);
const companyName = ref('');
const router = useRouter();

// Function to fetch session info
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
            companyName.value = data.user.companyName || 'Your Company';
            
            // Show personalized welcome toast if coming from login
            const urlParams = new URLSearchParams(window.location.search);
            if (urlParams.get('success') === 'true') {
                const userName = data.user.userName;
                
                toast.add({
                    severity: 'success',
                    summary: userName === 'Juan Pablo' ? 'Welcome back Juan!' : `Welcome back ${userName}!`,
                    detail: 'You have successfully logged in',
                    life: 3000
                });
                
                // Clean up URL parameters
                window.history.replaceState({}, '', '/');
            }
        }
    } catch (error) {
        console.error('Error fetching session info:', error);
        // Fallback to generic welcome message if URL has success param
        const urlParams = new URLSearchParams(window.location.search);
        if (urlParams.get('success') === 'true') {
            toast.add({
                severity: 'success',
                summary: 'Welcome Back!',
                detail: 'You have successfully logged in',
                life: 3000
            });
            
            // Clean up URL parameters
            window.history.replaceState({}, '', '/');
        }
    } finally {
        loading.value = false;
    }
};

onMounted(async () => {
    await fetchSessionInfo();
});
</script>

<template>
    <div>
        <!-- Loading State -->
        <div v-if="loading" class="flex justify-center items-center h-96">
            <i class="pi pi-spin pi-spinner text-4xl text-primary"></i>
        </div>
        
        <!-- Dashboard Content -->
        <div v-else class="grid grid-cols-12 gap-4 md:gap-6 lg:gap-8">
            <!-- Dashboard Header -->
            <div class="col-span-12 mb-2">
                <h1 class="text-2xl font-medium text-900">{{ companyName }} Dashboard</h1>
                <p class="text-sm font-medium text-500 mt-1">Welcome to your company dashboard. Here's an overview of your organization.</p>
                
                <!-- Quick Navigation Links -->
                <div class="flex flex-wrap gap-2 mt-3">
                    <Button 
                        label="Employees" 
                        icon="pi pi-users" 
                        class="p-button-sm p-button-outlined"
                        @click="router.push('/employees')"
                    />
                    <Button 
                        label="Candidates" 
                        icon="pi pi-user-plus" 
                        class="p-button-sm p-button-outlined"
                        @click="router.push('/candidates')"
                    />
                    <Button 
                        label="Recruitment" 
                        icon="pi pi-briefcase" 
                        class="p-button-sm p-button-outlined"
                        @click="router.push('/recruitment-leads')"
                    />
                    <Button 
                        label="Skillsets" 
                        icon="pi pi-star" 
                        class="p-button-sm p-button-outlined"
                        @click="router.push('/admin-skillsets')"
                    />
                    <Button 
                        label="Certifications" 
                        icon="pi pi-check-circle" 
                        class="p-button-sm p-button-outlined"
                        @click="router.push('/admin-certifications')"
                    />
                </div>
            </div>
            
            <!-- Stats Row -->
            <div class="col-span-12 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <EmployeeStatsWidget />
                <CandidateStatsWidget />
                <RecruitmentProcessWidget />
                <CertificationStatsWidget />
            </div>
            
            <!-- Welcome Guide Widget (Replaces Skillset Distribution and Top Performers) -->
            <div class="col-span-12 xl:col-span-8">
                <WelcomeGuideWidget />
            </div>
            
            <!-- Sidebar Widgets -->
            <div class="col-span-12 xl:col-span-4">
                <div class="grid grid-cols-1 gap-4 md:gap-6 lg:gap-8">
                    <!-- Recent Activities -->
                    <div class="col-span-1">
                        <RecentActivitiesWidget />
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
