<script setup>
import LazyImage from '@/components/landing/LazyImage.vue';
import { useLayout } from '@/layout/composables/layout';
const { isDarkTheme } = useLayout();
</script>

<template>
    <section class="landing-container relative py-12 lg:py-24">
        <div class="max-w-[68rem] mx-auto flex items-center flex-col lg:flex-row-reverse gap-14 xl:gap-20">
            <div class="relative lg:flex-1 w-full h-[28rem] lg:h-[40rem] max-w-[25rem] lg:max-w-[36rem]">
                <LazyImage
                    class="w-[17.5rem] lg:w-[25rem] z-0 rounded-2xl delay-300 h-auto absolute rotate-[20deg] bottom-10 lg:bottom-16 left-[4.5rem] lg:left-24 shadow-[0px_20px_52px_0px_rgba(0,0,0,0.04)]"
                    :src="'/demo/images/landing/boxes/' + (isDarkTheme ? 'social-media-users-dark.png' : 'social-media-users.png')"
                    alt="Time Tracking Interface"
                />
                <LazyImage
                    class="w-[17.5rem] lg:w-[25rem] rounded-2xl z-10 h-auto absolute bottom-0 left-0 shadow-[0px_20px_52px_0px_rgba(0,0,0,0.04)]"
                    :src="'/demo/images/landing/boxes/' + (isDarkTheme ? 'social-media-revenue-dark.png' : 'social-media-revenue.png')"
                    alt="Project Analytics Dashboard"
                />
            </div>
            <div class="max-w-[25rem] mx-auto lg:max-w-md w-full flex flex-col items-center lg:items-start">
                <div class="badge mx-0">Time Tracking</div>
                <h4 class="title-h5 lg:title-h4 text-center lg:text-left mt-4">
                    Seamless Time & Project Tracking
                </h4>
                <p class="body-medium text-center lg:text-left mt-6">
                    Empower your team with intuitive time tracking tools that integrate seamlessly 
                    with project management. Generate detailed timesheets automatically, track 
                    project progress in real-time, and ensure accurate billing across multiple currencies.
                </p>
                <ul class="list-disc mt-8 body-medium text-center lg:text-left list-inside space-y-3.5">
                    <li>Automated Time Tracking</li>
                    <li>Multi-Currency Support</li>
                    <li>Customizable Reports</li>
                </ul>
            </div>
        </div>
    </section>
</template>
