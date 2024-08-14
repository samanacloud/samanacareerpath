<script setup>
import { useLayout } from '@/layout/composables/layout';
import { ref, computed, onMounted, onBeforeMount } from 'vue';
import { CountryService } from '@/service/CountryService';
import { useRouter } from 'vue-router';
import Toolbar from 'primevue/toolbar';
import Card from 'primevue/card';
import Button from 'primevue/button';
import Dropdown from 'primevue/dropdown';
import InputText from 'primevue/inputtext';
import axios from 'axios';
const { layoutConfig } = useLayout();
const router = useRouter(); 















const logoUrl = 'samana-logo-white.png';
const logoUrlD = 'samana-logo-dark.png';




</script>

<template>
    <div class="toolbar-wrapper">
        <Toolbar style="background-color: #133563;">
            <template #start>
                <img alt="logo" :src="logoUrl" height="40" />
            </template>
            <template #center>
                <div class="center-content">
                    <h4>Samana CareerPath</h4>
                </div>
            </template>

        </Toolbar>
    </div>
   <div class="grid ">
    <div class="col-12">
      <div class="card"> 
    
        <h2>Terms of Service</h2>
    <h5>1. Introduction</h5>
    <p>Welcome to Samana CareerPath. These terms of service outline the rules and regulations for the use of our platform.</p>
    
    <h5>2. User Obligations</h5>
    <p>By accessing this platform, we assume you accept these terms and conditions. Do not continue to use Samana CareerPath if you do not agree to all of the terms and conditions stated on this page.</p>

    <h5>3. Privacy Policy</h5>
    <p>Your privacy is important to us. Please read our <a href="/privacypolicy">Privacy Policy</a> for details on how we handle your personal information.</p>

    <h5>4. Intellectual Property</h5>
    <p>Unless otherwise stated, Samana CareerPath and/or its licensors own the intellectual property rights for all material on the platform. All intellectual property rights are reserved.</p>

    <h5>5. Limitation of Liability</h5>
    <p>In no event shall Samana CareerPath, nor any of its officers, directors, and employees, be held liable for anything arising out of or in any way connected with your use of this platform.</p>

    <h5>6. Changes to These Terms</h5>
    <p>We reserve the right to amend these terms at any time. Your continued use of the platform will signify your acceptance of any adjustment to these terms.</p>

    <h5>7. Contact Us</h5>
    <p>If you have any questions about these Terms, please contact us at support@samanagroup.com</p>


</div></div></div>
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



.layout-content {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    gap: 0.1rem;
}

.toolbar-wrapper {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 1000; /* Make sure it stays above other content */
    background-color:  #133563; /* Ensure it has a solid background */
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); /* Optional: Adds a shadow for depth */
    padding: 0; /* Remove any extra padding/margin if necessary */
}

/* Add top padding to the content to avoid being covered by the toolbar */
body {
    padding-top: 80px; /* Adjust according to the height of your Toolbar */
}

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

.intro-section {
    padding: 2rem 1rem;
    text-align: center;
}


.center-content h4 {
    margin: 0; /* Remove default margins */
    color: white;
}


</style>