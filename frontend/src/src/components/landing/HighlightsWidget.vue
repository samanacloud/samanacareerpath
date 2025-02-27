<template>
    <div id="highlights" class="flex lg:flex-row flex-col gap-4 bg-surface-0 dark:bg-surface-900 px-6 py-20 md:px-12 lg:px-20">
        <Toast />
        <div class="flex-1 flex items-center justify-center">
            <div class="p-6 pt-12 lg:p-12">
                <h1 class="text-3xl lg:text-5xl font-bold text-surface-900 dark:text-surface-0 mb-4 lg:leading-normal text-center lg:text-left">
                    Streamline Your <br /><span class="text-primary">Talent Management</span>
                </h1>
                <p class="text-surface-700 dark:text-surface-200 leading-normal mb-8 text-center lg:text-left text-xl">
                    Leverage AI-powered analytics to make data-driven hiring decisions. Track employee growth, evaluate candidates, and build winning teams with confidence.
                </p>
                <div class="flex items-center justify-center lg:justify-start gap-6">
                    <Button label="View Features" type="button" icon="pi pi-list" @click="showComingSoonToast('features')" />
                    <Button label="Try Demo" type="button" outlined icon="pi pi-play" @click="showComingSoonToast('demo')" />
                </div>
            </div>
        </div>
        <div class="flex-1 overflow-hidden">
            <img src="/demo/images/landing/mockup-desktop.svg" alt="Analytics Dashboard" class="h-full w-full object-cover lg:[clip-path:polygon(12%_0,100%_0%,100%_100%,0_100%)]" />
        </div>
    </div>
</template>

<script setup>
import Button from 'primevue/button';
import Toast from 'primevue/toast';
import { useToast } from 'primevue/usetoast';

const toast = useToast();

const showComingSoonToast = (type) => {
    let title = type === 'features' ? 'Features Coming Soon!' : 'Demo Coming Soon!';
    let detail = 'Please join our waitlist to receive updates when this becomes available.';
    
    toast.add({
        severity: 'info',
        summary: title,
        detail: detail,
        life: 5000
    });
};
</script>

<style scoped>
.line-height-3 {
    line-height: 1.75;
}
</style>
