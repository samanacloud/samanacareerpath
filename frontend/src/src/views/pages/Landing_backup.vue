<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import Toolbar from 'primevue/toolbar';
import Card from 'primevue/card';
import Button from 'primevue/button';
import Dropdown from 'primevue/dropdown';
import InputText from 'primevue/inputtext';
import { useToast } from 'primevue/usetoast';
import { CountryService } from '@/service/CountryService';
import axios from 'axios';


</script>
<template>
  
            <div class="layout-footer">
                <img :src="logoUrl" alt="Logo" height="20" class="mr-2" />
                by
                <span class="font-medium ml-2">Samana Group LLC</span>, All Rights Reserved
                <div class="ml-4">
                    <a href="/termsofservice" class="text-primary">Terms of Use</a> | 
                    <a href="/privacypolicy" class="text-primary">Privacy Policy</a>
                </div>
            </div>
</template>
<style lang="scss" scoped>

.layout-footer {
    background-color: #e0f2ff;
    text-align: center;
    width: 100%;
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 1rem; /* Increase padding to make the footer higher */
    box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.1); /* Optional: Adds a shadow to give it some depth */
}

</style>
