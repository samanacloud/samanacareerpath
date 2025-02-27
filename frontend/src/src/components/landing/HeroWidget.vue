<template>
    <div id="home" class="bg-surface-0 dark:bg-surface-950 px-6 py-20 md:px-12 lg:px-20">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 xl:gap-0">
            <div class="flex flex-col justify-center">
                <div class="inline-flex items-center px-4 py-2 rounded-full bg-primary-50 dark:bg-primary-900/30 text-primary-600 dark:text-primary-400 text-sm font-medium mb-6">
                    <span class="mr-2">✨</span>
                    <span>SMART TALENT MANAGEMENT</span>
                </div>
                
                <div class="text-surface-900 dark:text-surface-0 font-bold text-5xl mb-4">CareerPath<br><span class="text-primary text-4xl"> by Samana Group</span></div>
                
                <div class="text-surface-700 dark:text-surface-100 text-xl mb-8 line-height-3">
                    Transform your hiring process with our intuitive platform. Track employee growth, evaluate candidates with AI-powered insights, and build winning teams - all in one place. Make recruitment simpler, smarter, and more human.
                </div>
                
                <div class="flex flex-wrap gap-3">
                    <Button label="Access Now" icon="pi pi-user" severity="primary" raised class="font-bold px-5 py-3" @click="goToLogin" />
                </div>
                
                <div class="mt-8 flex items-center gap-4">
                    <div class="flex -space-x-2">
                        <div class="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center text-white text-xs">JD</div>
                        <div class="w-8 h-8 rounded-full bg-green-500 flex items-center justify-center text-white text-xs">MR</div>
                        <div class="w-8 h-8 rounded-full bg-purple-500 flex items-center justify-center text-white text-xs">KL</div>
                        <div class="w-8 h-8 rounded-full bg-orange-500 flex items-center justify-center text-white text-xs">+</div>
                    </div>
                    <span class="text-surface-600 dark:text-surface-300 text-sm">Trusted by HR professionals</span>
                </div>
            </div>
            
            <div class="flex justify-center items-center">
                <div class="relative">
                    <!-- Browser Frame -->
                    <div class="border border-surface-200 dark:border-surface-700 rounded-xl shadow-2xl transform transition-transform hover:scale-[1.02] hover:shadow-3xl">
                        <!-- Browser Header -->
                        <div class="bg-surface-0 dark:bg-surface-800 border-b border-surface-200 dark:border-surface-700 p-3 flex gap-2 rounded-t-xl">
                            <div class="w-3 h-3 bg-red-500 rounded-full"></div>
                            <div class="w-3 h-3 bg-yellow-500 rounded-full"></div>
                            <div class="w-3 h-3 bg-green-500 rounded-full"></div>
                        </div>
                        <!-- Browser Content -->
                        <div class="bg-surface-0 dark:bg-surface-800 p-4 rounded-b-xl">
                            <img src="/demo/images/landing/landing-1.png" alt="Career Path Platform" class="w-full max-w-[800px] rounded-md" />
                        </div>
                    </div>
                    
                    <!-- Decorative Elements -->
                    <div class="absolute -top-8 -right-8 w-32 h-32 bg-primary-50 dark:bg-primary-900/50 rounded-full blur-2xl"></div>
                    <div class="absolute -bottom-8 -left-8 w-32 h-32 bg-primary-50 dark:bg-primary-900/50 rounded-full blur-2xl"></div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import Button from 'primevue/button';
import { useRouter } from 'vue-router';

const router = useRouter();

function goToLogin() {
    router.push('/auth/login');
}
</script>

<style scoped>
.line-height-3 {
    line-height: 1.75;
}
</style>
