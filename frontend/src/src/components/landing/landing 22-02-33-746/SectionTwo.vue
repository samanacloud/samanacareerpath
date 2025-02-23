<script setup>
import LazyImage from '@/components/landing/LazyImage.vue';
import { useLayout } from '@/layout/composables/layout';
const { isDarkTheme } = useLayout();
</script>

<template>
    <section class="max-w-[77rem] landing-container mx-auto relative py-12 lg:py-24">
        <div class="flex lg:flex-row-reverse flex-col items-center gap-14 lg:gap-4 xl:gap-9">
            <div class="relative lg:flex-1 h-[26.2rem] lg:h-[42rem] w-full max-w-[25rem] lg:max-w-[42rem]">
                <LazyImage
                    class="lg:block hidden rounded-xl absolute h-full w-auto top-0 right-0"
                    :src="'/demo/images/landing/' + (isDarkTheme ? 'landing-section-pattern-dark.png' : 'landing-section-pattern.png')"
                    alt="Project Finance Pattern"
                />
                <LazyImage
                    class="rounded-xl absolute rotate-[22.6deg] lg:rotate-0 right-[3.28rem] lg:right-10 top-[2.5rem] lg:top-56 w-[15.8rem] lg:w-[16.7rem] shadow-[0px_200.426px_55.957px_0px_rgba(0,0,0,0.00),0px_128.191px_50.87px_0px_rgba(0,0,0,0.00),0px_72.235px_42.73px_0px_rgba(0,0,0,0.01),0px_31.539px_31.539px_0px_rgba(0,0,0,0.02),0px_8.139px_17.296px_0px_rgba(0,0,0,0.02)]"
                    :src="'/demo/images/landing/boxes/' + (isDarkTheme ? 'revenue-dark.png' : 'revenue.png')"
                    alt="Budget Tracking Dashboard"
                />
                <LazyImage
                    class="rounded-xl absolute left-0 lg:left-auto lg:right-[21rem] bottom-0 lg:bottom-auto lg:top-72 w-[17.3rem] lg:w-[14.6rem] shadow-[0px_200.426px_55.957px_0px_rgba(0,0,0,0.00),0px_128.191px_50.87px_0px_rgba(0,0,0,0.00),0px_72.235px_42.73px_0px_rgba(0,0,0,0.01),0px_31.539px_31.539px_0px_rgba(0,0,0,0.02),0px_8.139px_17.296px_0px_rgba(0,0,0,0.02)]"
                    :src="'/demo/images/landing/boxes/' + (isDarkTheme ? 'expenses-dark.png' : 'expenses.png')"
                    alt="Burn Rate Analytics"
                />
                <LazyImage
                    class="lg:block hidden rounded-xl absolute right-24 top-3.5 w-[15rem] shadow-[0px_200.426px_55.957px_0px_rgba(0,0,0,0.00),0px_128.191px_50.87px_0px_rgba(0,0,0,0.00),0px_72.235px_42.73px_0px_rgba(0,0,0,0.01),0px_31.539px_31.539px_0px_rgba(0,0,0,0.02),0px_8.139px_17.296px_0px_rgba(0,0,0,0.02)]"
                    :src="'/demo/images/landing/boxes/' + (isDarkTheme ? 'profit-dark.png' : 'profit.png')"
                    alt="Resource Utilization Charts"
                />
                <LazyImage
                    class="lg:block hidden rounded-xl absolute right-96 top-24 w-[14rem] shadow-[0px_179.87px_50.217px_0px_rgba(0,0,0,0.00),0px_115.043px_45.652px_0px_rgba(0,0,0,0.00),0px_64.826px_38.348px_0px_rgba(0,0,0,0.01),0px_28.304px_28.304px_0px_rgba(0,0,0,0.02),0px_7.304px_15.522px_0px_rgba(0,0,0,0.02)]"
                    :src="'/demo/images/landing/boxes/' + (isDarkTheme ? 'balance-dark.png' : 'balance.png')"
                    alt="Multi-Currency Reports"
                />
            </div>
            <div class="max-w-[31.5rem] lg:max-w-md mx-auto w-full flex flex-col items-center lg:items-start">
                <div class="badge mx-0">Financial Intelligence</div>
                <h4 class="title-h5 md:title-h4 text-center lg:text-left mt-4 max-w-xs md:max-w-lg">
                    Smart Project Budget Management
                </h4>
                <p class="body-small md:body-medium text-center lg:text-left mt-6">
                    Take control of your project finances with powerful tools for budget tracking, 
                    burn rate analysis, and resource optimization. Handle multiple currencies, 
                    monitor resource utilization, and make data-driven decisions with real-time insights.
                </p>
                <div class="mt-8 flex flex-col gap-4 w-full">
                    <div class="flex items-start gap-3">
                        <i class="pi pi-chart-line text-primary-500 text-xl mt-1"></i>
                        <div>
                            <h6 class="font-semibold mb-2">Real-time Burn Rate Tracking</h6>
                            <p class="text-700">Monitor project spending and forecast completion costs accurately</p>
                        </div>
                    </div>
                    <div class="flex items-start gap-3">
                        <i class="pi pi-money-bill text-primary-500 text-xl mt-1"></i>
                        <div>
                            <h6 class="font-semibold mb-2">Multi-Currency Support</h6>
                            <p class="text-700">Handle global projects with automatic currency conversion and reporting</p>
                        </div>
                    </div>
                    <div class="flex items-start gap-3">
                        <i class="pi pi-users text-primary-500 text-xl mt-1"></i>
                        <div>
                            <h6 class="font-semibold mb-2">Resource Utilization Analytics</h6>
                            <p class="text-700">Optimize team allocation and track resource efficiency in real-time</p>
                        </div>
                    </div>
                </div>
                <router-link to="/auth/company" class="body-button mt-8">Explore Features</router-link>
            </div>
        </div>
    </section>
</template>
