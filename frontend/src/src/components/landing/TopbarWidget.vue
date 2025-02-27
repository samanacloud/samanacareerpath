<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import Button from 'primevue/button';

const router = useRouter();
const mobileMenuOpen = ref(false);

function smoothScroll(id) {
    document.body.click();
    mobileMenuOpen.value = false;
    const element = document.getElementById(id);
    if (element) {
        element.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

function goToLogin() {
    router.push('/auth/login');
}

function goToContact() {
    router.push('/contact-us');
}
</script>

<template>
    <div class="w-full flex items-center justify-between">
        <!-- Logo -->
        <a class="flex items-center gap-3" href="#">
            <img src="/demo/images/samana-logo.png" alt="CareerPath" class="h-10 w-auto" />
            <span class="text-surface-900 dark:text-surface-0 font-semibold text-xl md:text-2xl">CareerPath</span>
        </a>
        
        <!-- Mobile Menu Button -->
        <button 
            @click="mobileMenuOpen = !mobileMenuOpen"
            class="lg:hidden flex items-center justify-center w-10 h-10 rounded-full hover:bg-surface-100 dark:hover:bg-surface-800 transition-colors"
        >
            <i class="pi" :class="mobileMenuOpen ? 'pi-times' : 'pi-bars'"></i>
        </button>
        
        <!-- Desktop Navigation -->
        <div class="hidden lg:flex items-center gap-8">
            <ul class="list-none p-0 m-0 flex items-center gap-6">
                <li>
                    <a @click="smoothScroll('home')" class="cursor-pointer text-surface-700 dark:text-surface-300 hover:text-primary dark:hover:text-primary-400 font-medium transition-colors">
                        Home
                    </a>
                </li>
                <li>
                    <a @click="smoothScroll('features')" class="cursor-pointer text-surface-700 dark:text-surface-300 hover:text-primary dark:hover:text-primary-400 font-medium transition-colors">
                        Features
                    </a>
                </li>
                <li>
                    <a @click="smoothScroll('highlights')" class="cursor-pointer text-surface-700 dark:text-surface-300 hover:text-primary dark:hover:text-primary-400 font-medium transition-colors">
                        Highlights
                    </a>
                </li>
                <li>
                    <a @click="smoothScroll('pricing')" class="cursor-pointer text-surface-700 dark:text-surface-300 hover:text-primary dark:hover:text-primary-400 font-medium transition-colors">
                        Pricing
                    </a>
                </li>
                <li>
                    <a @click="goToContact" class="cursor-pointer text-surface-700 dark:text-surface-300 hover:text-primary dark:hover:text-primary-400 font-medium transition-colors">
                        Contact Us
                    </a>
                </li>
            </ul>
            
            <div class="flex items-center gap-3">
                <Button label="Login" text class="font-medium" @click="goToLogin" />
                <Button label="Access Now" severity="primary" raised class="font-medium px-4" @click="goToLogin" />
            </div>
        </div>
        
        <!-- Mobile Navigation -->
        <div 
            v-show="mobileMenuOpen" 
            class="lg:hidden absolute top-full left-0 right-0 bg-surface-0 dark:bg-surface-900 shadow-md z-50 py-4 px-6 border-t border-surface-200 dark:border-surface-700"
        >
            <ul class="list-none p-0 m-0 flex flex-col gap-4 mb-4">
                <li>
                    <a @click="smoothScroll('home')" class="block py-2 text-surface-700 dark:text-surface-300 hover:text-primary dark:hover:text-primary-400 font-medium">
                        Home
                    </a>
                </li>
                <li>
                    <a @click="smoothScroll('features')" class="block py-2 text-surface-700 dark:text-surface-300 hover:text-primary dark:hover:text-primary-400 font-medium">
                        Features
                    </a>
                </li>
                <li>
                    <a @click="smoothScroll('highlights')" class="block py-2 text-surface-700 dark:text-surface-300 hover:text-primary dark:hover:text-primary-400 font-medium">
                        Highlights
                    </a>
                </li>
                <li>
                    <a @click="smoothScroll('pricing')" class="block py-2 text-surface-700 dark:text-surface-300 hover:text-primary dark:hover:text-primary-400 font-medium">
                        Pricing
                    </a>
                </li>
                <li>
                    <a @click="goToContact" class="block py-2 text-surface-700 dark:text-surface-300 hover:text-primary dark:hover:text-primary-400 font-medium">
                        Contact Us
                    </a>
                </li>
            </ul>
            
            <div class="flex flex-col gap-2">
                <Button label="Login" text class="w-full justify-center" @click="goToLogin" />
                <Button label="Access Now" severity="primary" raised class="w-full justify-center" @click="goToLogin" />
            </div>
        </div>
    </div>
</template>

<style scoped>
.pi {
    font-size: 1.25rem;
}
</style>
