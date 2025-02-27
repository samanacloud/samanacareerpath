<script setup lang="ts">
import FeaturesWidget from '@/components/landing/FeaturesWidget.vue';
import FooterWidget from '@/components/landing/FooterWidget.vue';
import HeroWidget from '@/components/landing/HeroWidget.vue';
import HighlightsWidget from '@/components/landing/HighlightsWidget.vue';
import PricingWidget from '@/components/landing/PricingWidget.vue';
import TopbarWidget from '@/components/landing/TopbarWidget.vue';
</script>

<template>
    <div class="landing-wrapper overflow-hidden">
        <!-- Background with gradient -->
        <div class="bg-gradient-to-b from-surface-50 to-surface-100 dark:from-surface-900 dark:to-surface-800 min-h-screen">
            <!-- Topbar with improved spacing -->
            <div class="sticky top-0 z-50 backdrop-blur-sm bg-white/80 dark:bg-surface-900/80 shadow-sm">
                <div class="py-4 px-6 mx-auto max-w-7xl md:px-8 lg:px-12">
                    <TopbarWidget />
                </div>
            </div>
            
            <!-- Main content -->
            <HeroWidget />
            <FeaturesWidget />
            <HighlightsWidget />
            <PricingWidget />
            <FooterWidget />
        </div>
    </div>
</template>

<style scoped>
.landing-wrapper {
    font-family: var(--font-family);
}
</style>
