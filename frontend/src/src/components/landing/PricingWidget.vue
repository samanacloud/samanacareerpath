<template>
    <div id="pricing" class="bg-surface-0 dark:bg-surface-950 px-6 py-20 md:px-12 lg:px-20">
        <div class="text-surface-900 dark:text-surface-0 font-bold text-4xl lg:text-6xl mb-6 text-center">Pricing Plans</div>
        <div class="text-surface-700 dark:text-surface-0/70 text-xl mb-12 text-center leading-normal">Choose the plan that best fits your team</div>
        <div class="flex lg:flex-row flex-col gap-8 lg:gap-4 xl:gap-12 max-w-7xl mx-auto">
            <!-- Starter Plan -->
            <div class="w-full flex-1 py-4 px-4 lg:px-6 flex rounded-lg flex-col bg-surface-0 dark:bg-surface-800 shadow-[0px_2px_6px_0px_rgba(0,0,0,0.12),0px_0px_2px_0px_rgba(0,0,0,0.06),0px_4px_10px_0px_rgba(0,0,0,0.03)]">
                <div class="text-surface-900 dark:text-surface-0 font-medium text-xl mb-2">Starter</div>
                <div class="text-surface-600 dark:text-surface-300">Perfect for small teams</div>
                <div class="my-4 w-full h-px bg-surface-300 dark:bg-surface-700" />
                <div class="flex items-center gap-2">
                    <span class="font-bold text-2xl text-surface-900 dark:text-surface-0">$0</span>
                    <span class="font-medium text-surface-600 dark:text-surface-300">first Admin</span>
                </div>
                <div class="my-4 w-full h-px bg-surface-300 dark:bg-surface-700" />
                <ul class="list-none flex flex-col gap-4 flex-1">
                    <li class="flex items-center gap-2">
                        <i class="pi pi-check-circle text-green-500 text-lg" />
                        <span class="text-surface-800 dark:text-surface-100 leading-6">Up to 50 candidates</span>
                    </li>
                    <li class="flex items-center gap-2">
                        <i class="pi pi-check-circle text-green-500 text-lg" />
                        <span class="text-surface-800 dark:text-surface-100 leading-6">Up to 5 employees</span>
                    </li>
                    <li class="flex items-center gap-2">
                        <i class="pi pi-check-circle text-green-500 text-lg" />
                        <span class="text-surface-800 dark:text-surface-100 leading-6">5 job postings</span>
                    </li>
                </ul>
                <div class="my-4 w-full h-px bg-surface-300 dark:bg-surface-700" />
                <Button label="Get Started" class="px-5 py-3" />
            </div>

            <!-- Professional Plan -->
            <div class="w-full flex-1 py-4 px-4 lg:px-6 flex rounded-lg flex-col bg-surface-0 dark:bg-surface-800 shadow-[0px_2px_6px_0px_rgba(0,0,0,0.12),0px_0px_2px_0px_rgba(0,0,0,0.06),0px_4px_10px_0px_rgba(0,0,0,0.03)]">
                <div class="text-surface-900 dark:text-surface-0 font-medium text-xl mb-2">Professional</div>
                <div class="text-surface-600 dark:text-surface-300">For growing teams</div>
                <div class="my-4 w-full h-px bg-surface-300 dark:bg-surface-700" />
                <div class="flex items-center gap-2">
                    <span class="font-bold text-2xl text-surface-900 dark:text-surface-0">$20</span>
                    <span class="font-medium text-surface-600 dark:text-surface-300">per Admin</span>
                </div>
                <div class="my-4 w-full h-px bg-surface-300 dark:bg-surface-700" />
                <ul class="list-none flex flex-col gap-4 flex-1">
                    <li class="flex items-center gap-2">
                        <i class="pi pi-check-circle text-green-500 text-lg" />
                        <span class="text-surface-800 dark:text-surface-100 leading-6">Up to 50 candidates</span>
                    </li>
                    <li class="flex items-center gap-2">
                        <i class="pi pi-check-circle text-green-500 text-lg" />
                        <span class="text-surface-800 dark:text-surface-100 leading-6">Up to 20 employees</span>
                    </li>
                    <li class="flex items-center gap-2">
                        <i class="pi pi-check-circle text-green-500 text-lg" />
                        <span class="text-surface-800 dark:text-surface-100 leading-6">Candidate reviews</span>
                    </li>
                    <li class="flex items-center gap-2">
                        <i class="pi pi-check-circle text-green-500 text-lg" />
                        <span class="text-surface-800 dark:text-surface-100 leading-6">All Free features</span>
                    </li>
                </ul>
                <div class="my-4 w-full h-px bg-surface-300 dark:bg-surface-700" />
                <Button label="Get Started" class="px-5 py-3" />
            </div>

            <!-- Business Plan -->
            <div class="w-full flex-1 py-4 px-4 lg:px-6 flex rounded-lg flex-col bg-surface-0 dark:bg-surface-800 shadow-[0px_2px_6px_0px_rgba(0,0,0,0.12),0px_0px_2px_0px_rgba(0,0,0,0.06),0px_4px_10px_0px_rgba(0,0,0,0.03)]">
                <div class="text-surface-900 dark:text-surface-0 font-medium text-xl mb-2">Business</div>
                <div class="text-surface-600 dark:text-surface-300">For medium-sized companies</div>
                <div class="my-4 w-full h-px bg-surface-300 dark:bg-surface-700" />
                <div class="flex items-center gap-2">
                    <span class="font-bold text-2xl text-surface-900 dark:text-surface-0">$50</span>
                    <span class="font-medium text-surface-600 dark:text-surface-300">per Admin</span>
                </div>
                <div class="my-4 w-full h-px bg-surface-300 dark:bg-surface-700" />
                <ul class="list-none flex flex-col gap-4 flex-1">
                    <li class="flex items-center gap-2">
                        <i class="pi pi-check-circle text-green-500 text-lg" />
                        <span class="text-surface-800 dark:text-surface-100 leading-6">Unlimited candidates</span>
                    </li>
                    <li class="flex items-center gap-2">
                        <i class="pi pi-check-circle text-green-500 text-lg" />
                        <span class="text-surface-800 dark:text-surface-100 leading-6">Up to 100 employees</span>
                    </li>
                    <li class="flex items-center gap-2">
                        <i class="pi pi-check-circle text-green-500 text-lg" />
                        <span class="text-surface-800 dark:text-surface-100 leading-6">AI-powered reviews</span>
                    </li>
                    <li class="flex items-center gap-2">
                        <i class="pi pi-check-circle text-green-500 text-lg" />
                        <span class="text-surface-800 dark:text-surface-100 leading-6">24/7 Premium support</span>
                    </li>
                    <li class="flex items-center gap-2">
                        <i class="pi pi-check-circle text-green-500 text-lg" />
                        <span class="text-surface-800 dark:text-surface-100 leading-6">All Basic features</span>
                    </li>
                </ul>
                <div class="my-4 w-full h-px bg-surface-300 dark:bg-surface-700" />
                <Button label="Get Started" class="px-5 py-3" />
            </div>
        </div>
    </div>
</template>

<script setup>
import Button from 'primevue/button';
</script>
