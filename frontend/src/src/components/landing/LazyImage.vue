<script setup>
import { onMounted, ref, computed } from 'vue';

const props = defineProps({
    src: {
        type: String,
        required: true
    },
    alt: {
        type: String,
        default: ''
    },
    className: {
        type: String,
        default: ''
    },
    isLogo: {
        type: Boolean,
        default: false
    }
});

const isIntersecting = ref(false);
const isLoaded = ref(false);
const image = ref(null);

const handleLoad = () => {
    isLoaded.value = true;
};

onMounted(() => {
    if (props.isLogo) {
        isIntersecting.value = true;
        isLoaded.value = true;
        return;
    }

    const observer = new IntersectionObserver(
        ([entry]) => {
            if (entry.isIntersecting && entry.intersectionRatio >= 0.1) {
                isIntersecting.value = true;
                observer.unobserve(image.value);
            }
        },
        { threshold: 0.1 }
    );

    observer.observe(image.value);
});

const imageClasses = computed(() => {
    return [
        props.className,
        { 'opacity-0': !isLoaded },
        'transition-opacity duration-700 ease-out delay-75',
        { 'logo-image': props.isLogo }
    ];
});
</script>

<template>
    <img :src="isIntersecting ? src : ''" :alt="alt" :class="imageClasses" @load="handleLoad" ref="image" />
</template>

<style scoped>
.logo-image {
    height: 48px;
    width: auto;
    object-fit: contain;
}

@media (max-width: 768px) {
    .logo-image {
        height: 40px;
    }
}
</style>
