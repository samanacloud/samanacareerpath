<script setup>
import { ref } from 'vue';

const plans = ref(['starter', 'professional', 'enterprise']);
const planDetails = ref([
    {
        plan: 'Monthly Price',
        ingredients: ['$15', '$49', '$99']
    },
    {
        plan: 'Team Members',
        ingredients: ['Up to 10', 'Up to 50', 'Unlimited']
    },
    {
        plan: 'Projects',
        ingredients: ['5', 'Unlimited', 'Unlimited']
    },
    {
        plan: 'Time Tracking',
        ingredients: ['_yes', '_yes', '_yes']
    },
    {
        plan: 'Project Dashboard',
        ingredients: ['_yes', '_yes', '_yes']
    },
    {
        plan: 'Basic Reports',
        ingredients: ['_yes', '_yes', '_yes']
    },
    {
        plan: 'Resource Management',
        ingredients: ['Basic', 'Advanced', 'Enterprise']
    },
    {
        plan: 'Multi-Currency Support',
        ingredients: ['_no', '_yes', '_yes']
    },
    {
        plan: 'API Access',
        ingredients: ['_no', '_yes', '_yes']
    },
    {
        plan: 'Custom Integrations',
        ingredients: ['_no', '_no', '_yes']
    },
    {
        plan: 'Expense Tracking',
        ingredients: ['_no', '_yes', '_yes']
    },
    {
        plan: 'Advanced Analytics',
        ingredients: ['_no', '_yes', '_yes']
    },
    {
        plan: 'Custom Deployment',
        ingredients: ['_no', '_no', '_yes']
    },
    {
        plan: 'Priority Support',
        ingredients: ['Email Only', '24/7 Chat', 'Dedicated Manager']
    },
    {
        plan: 'Data Export',
        ingredients: ['CSV', 'All Formats', 'All Formats + API']
    }
]);
</script>

<template>
    <section class="landing-container mx-auto py-10 lg:py-20">
        <div class="max-w-lg md:max-w-4xl xl:max-w-full mx-auto p-7 border border-surface-200 dark:border-surface-800 rounded-3xl">
            <div
                class="sticky top-24 text-surface-950 dark:text-surface-0 label-medium leading-normal hidden md:flex rounded-xl bg-surface-100 dark:bg-surface-900 border border-surface-200 dark:border-surface-800 shadow-[0px_1px_2px_0px_rgba(18,18,23,0.05)]"
            >
                <span class="flex-[1.15] px-6 py-3 text-left">Features</span>
                <div class="flex flex-[3]">
                    <span v-for="(data, index) of plans" :key="index" class="flex-1 px-6 py-3 text-center capitalize">{{ data }}</span>
                </div>
            </div>
            <div class="md:mt-7">
                <div v-for="(data, index) of planDetails" :key="index">
                    <div class="flex md:flex-row flex-col">
                        <div
                            class="md:!bg-transparent bg-surface-100 dark:bg-surface-900 border md:border-0 rounded-xl border-surface-200 dark:border-surface-800 flex-[1.15] px-6 py-4 text-left body-medium leading-normal text-surface-950 dark:text-surface-0"
                        >
                            {{ data.plan }}
                        </div>
                        <div class="flex md:flex-[3]">
                            <div v-for="(ingredient, j) of data.ingredients" :key="j" class="flex-1 md:px-6 md:py-4 text-surface-950 dark:text-surface-0 text-center">
                                <span class="md:hidden block flex-1 py-4 text-center capitalize body-medium leading-normal text-surface-950 dark:text-surface-0">{{ plans[j] }}</span>
                                <div class="w-full h-[1px] bg-surface-200 dark:bg-surface-800 md:hidden block" />
                                <div class="py-4 md:py-0">
                                    <i v-if="ingredient.includes('_yes')" class="pi pi-check text-center !text-sm text-surface-950 font-bold dark:text-surface-0" />
                                    <i v-else-if="ingredient.includes('_no')" class="pi pi-minus text-center !text-sm text-surface-500" />
                                    <span v-else class="text-surface-950 dark:text-surface-0 body-medium leading-normal">{{ ingredient }}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div v-if="index !== planDetails.length - 1" class="w-full md:block hidden h-[1px] bg-surface-200 dark:bg-surface-800" />
                </div>
            </div>
        </div>
    </section>
</template>
