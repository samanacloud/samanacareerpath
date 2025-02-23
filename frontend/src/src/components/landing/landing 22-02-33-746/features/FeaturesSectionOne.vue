<script setup>
import LazyImage from '@/components/landing/LazyImage.vue';
import { useLayout } from '@/layout/composables/layout';
const { isDarkTheme } = useLayout();
</script>

<template>
    <section class="landing-container relative py-12 lg:py-24">
        <div class="max-w-[68rem] mx-auto flex lg:flex-row flex-col items-center gap-14 xl:gap-20">
            <div class="relative lg:flex-1 h-[27rem] lg:h-[34.6rem] w-full max-w-[25rem] lg:max-w-[32rem]">
                <LazyImage
                    class="w-[19rem] lg:w-[24rem] z-0 rounded-2xl delay-300 h-auto absolute rotate-[-22deg] bottom-10 lg:bottom-12 left-12 lg:left-16 shadow-[0px_20px_52px_0px_rgba(0,0,0,0.04)]"
                    :src="'/demo/images/landing/boxes/' + (isDarkTheme ? 'spending-limit-dark.png' : 'spending-limit.png')"
                    alt="Project Budget Tracking"
                />
                <LazyImage
                    class="w-[18rem] lg:w-[23rem] rounded-2xl z-10 h-auto absolute top-0 right-0 shadow-[0px_20px_52px_0px_rgba(0,0,0,0.04)]"
                    :src="'/demo/images/landing/boxes/' + (isDarkTheme ? 'credit-score-dark.png' : 'credit-score.png')"
                    alt="Resource Allocation Dashboard"
                />
            </div>
            <div class="max-w-[25rem] lg:max-w-md mx-auto w-full flex flex-col items-center lg:items-start">
                <div class="badge mx-0">Resource Management</div>
                <h4 class="title-h5 lg:title-h4 text-center lg:text-left mt-4">
                    Intelligent Resource Planning & Tracking
                </h4>
                <p class="body-medium text-center lg:text-left mt-6">
                    Optimize your team's performance with advanced resource management tools. 
                    Track utilization, monitor burn rates, and ensure efficient allocation across 
                    projects with real-time analytics and predictive insights.
                </p>
                <ul class="list-disc mt-8 body-medium text-center lg:text-left list-inside space-y-3.5">
                    <li>Real-time Resource Utilization</li>
                    <li>Capacity Planning</li>
                    <li>Workload Balancing</li>
                </ul>
            </div>
        </div>
    </section>
</template>
