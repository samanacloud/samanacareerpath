<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import { useLayout } from '@/layout/composables/layout';
import { useRouter } from 'vue-router';



const logoUrl = 'samana-logo-dark.png';



</script>

<template>
    <div class="layout-topbar">
        <router-link to="/landing" class="layout-topbar-logo">
            <img :src="logoUrl" alt="logo" />
            <span>Samana CareerPath</span>
        </router-link>

        <button  class="p-link layout-menu-button layout-topbar-button" />           
    
       
        <button class="p-link layout-topbar-menu-button layout-topbar-button" />
          


    </div>
</template>

<style lang="scss" scoped></style>
