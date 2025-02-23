<script setup>
import { ref } from 'vue';

const isYearly = ref(false);
const pricingData = ref([
    {
        type: 'starter',
        price: {
            yearly: '$144',
            monthly: '$15'
        },
        description: 'Perfect for small teams and startups looking to streamline their project time tracking and resource management.',
        ingredients: [
            'Up to 10 team members',
            'Basic time tracking',
            'Project dashboard',
            'Simple reporting',
            'Email support'
        ]
    },
    {
        type: 'professional',
        price: {
            yearly: '$480',
            monthly: '$49'
        },
        description: 'Ideal for growing teams that need advanced features and detailed resource management capabilities.',
        ingredients: [
            'Up to 50 team members',
            'Advanced time tracking',
            'Resource utilization analytics',
            'Multi-currency support',
            'Priority support',
            'API access'
        ]
    },
    {
        type: 'enterprise',
        price: {
            yearly: '$990',
            monthly: '$99'
        },
        description: 'Complete solution for large organizations requiring maximum security and customization options.',
        ingredients: [
            'Unlimited team members',
            'Custom deployment options',
            'Advanced security features',
            'Dedicated account manager',
            'Custom integrations',
            '24/7 premium support'
        ]
    }
]);
</script>

<template>
    <section class="animate-fadein animate-duration-300 animate-ease-in landing-container mx-auto relative lg:pb-14 lg:pt-52 pt-36 pb-10">
        <h1 class="title-h4 lg:title-h1">
            Simple, Transparent<br />
            <span class="text-primary-600">Project Management Pricing</span>
        </h1>
        <p class="body-small lg:body-medium mt-4 lg:mt-6 max-w-xs sm:max-w-lg lg:max-w-xl mx-auto">
            Choose the perfect plan for your team. All plans include our core time tracking features. 
            Save 20% with annual billing.
        </p>
        <div class="mb-14 mt-12 lg:mt-14 flex items-center gap-6 justify-center">
            <div @click="isYearly = false" class="cursor-pointer text-surface-900 dark:text-surface-0 text-xl">Monthly</div>
            <button @click="isYearly = !isYearly" class="w-[4.5rem] h-9 rounded-full relative bg-surface-100 hover:bg-surface-50 dark:bg-surface-900 dark:hover:bg-surface-800 border border-surface-200 dark:border-surface-800 transition-all">
                <span class="w-7 h-7 rounded-full bg-primary-500 absolute top-[0.2rem] transition-all ease-in-out duration-200" :class="isYearly ? 'left-[calc(100%-2rem)]' : ' left-1'" />
            </button>
            <div @click="isYearly = true" class="cursor-pointer text-surface-900 dark:text-surface-0 text-xl">Yearly</div>
        </div>
        <div class="flex flex-wrap gap-7 mx-auto max-w-lg md:max-w-4xl xl:max-w-full">
            <div v-for="(data, index) of pricingData" :key="index" class="w-full min-w-full sm:min-w-[25rem] flex-1 p-6 border border-surface-200 dark:border-surface-800 rounded-3xl shadow-[0px_1px_2px_0px_rgba(18,18,23,0.05)]">
                <div class="w-fit py-1 px-4 rounded-full bg-surface-200 dark:bg-surface-800 font-medium uppercase text-surface-950 dark:text-surface-0">
                    {{ data.type }}
                </div>
                <div class="mt-9">
                    <span class="title-h2 mr-3">{{ data.price[isYearly ? 'yearly' : 'monthly'] }}</span>
                    <span class="title-h7">/ {{ isYearly ? 'Yearly' : 'Monthly' }}</span>
                </div>
                <p class="mt-7 body-medium text-left">
                    {{ data.description }}
                </p>
                <button class="mt-8 w-full py-3 rounded-xl bg-primary-500 hover:bg-primary-400 text-surface-0 transition-all">Get Started</button>
                <div class="w-full h-[1px] bg-surface-200 dark:bg-surface-800 my-8" />
                <div class="flex flex-col gap-3">
                    <div v-for="(content, j) of data.ingredients" :key="j" class="flex items-center gap-3">
                        <i class="pi pi-check text-surface-950 dark:text-surface-0 leading-none" />
                        <span class="flex-1 body-medium text-left text-surface-950 dark:text-surface-0">{{ content }}</span>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>
