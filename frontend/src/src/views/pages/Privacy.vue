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

        <h2>Privacy Policy</h2>

        <h5>1. Introduction</h5>
        <p>Your privacy is critically important to us. At Samana CareerPath, we have a few fundamental principles:</p>
        <ul>
          <li>We don’t ask you for personal information unless we truly need it.</li>
          <li>We don’t share your personal information except to comply with the law, develop our products, or protect our rights.</li>
          <li>We don’t store personal information on our servers unless required for the ongoing operation of one of our services.</li>
        </ul>

        <h5>2. Information We Collect</h5>
        <p>We only collect information about you if we have a reason to do so – for example, to provide our services, to communicate with you, or to make our services better.</p>
        <ul>
          <li><strong>Information You Provide to Us:</strong> We collect information that you provide to us directly. For example, we collect information when you create an account, fill out a form, or communicate with us.</li>
          <li><strong>Information We Collect Automatically:</strong> We also collect some information automatically. For example, when you interact with our services, we may collect your IP address, browser type, and other technical information.</li>
        </ul>

        <h5>3. How We Use Information</h5>
        <p>We use the information we collect in various ways, including to:</p>
        <ul>
          <li>Provide, operate, and maintain our services.</li>
          <li>Improve, personalize, and expand our services.</li>
          <li>Understand and analyze how you use our services.</li>
          <li>Communicate with you, either directly or through one of our partners, including for customer service, to provide you with updates and other information relating to the service, and for marketing and promotional purposes.</li>
          <li>Process your transactions and manage your orders.</li>
        </ul>

        <h5>4. Sharing of Information</h5>
        <p>We do not share your personal information with companies, organizations, or individuals outside of Samana CareerPath except in the following cases:</p>
        <ul>
          <li><strong>With your consent:</strong> We will share personal information with companies, organizations, or individuals outside of Samana CareerPath when we have your consent to do so.</li>
          <li><strong>For legal reasons:</strong> We will share personal information with companies, organizations, or individuals outside of Samana CareerPath if we believe that access, use, preservation, or disclosure of the information is reasonably necessary to:</li>
          <ul>
            <li>Meet any applicable law, regulation, legal process, or enforceable governmental request.</li>
            <li>Enforce applicable Terms of Service, including investigation of potential violations.</li>
            <li>Detect, prevent, or otherwise address fraud, security, or technical issues.</li>
            <li>Protect against harm to the rights, property, or safety of Samana CareerPath, our users, or the public as required or permitted by law.</li>
          </ul>
        </ul>

        <h5>5. Security</h5>
        <p>The security of your personal information is important to us. We implement a variety of security measures to maintain the safety of your personal information when you enter, submit, or access your personal information.</p>

        <h5>6. Changes to This Privacy Policy</h5>
        <p>We may update our Privacy Policy from time to time. We will notify you of any changes by posting the new Privacy Policy on this page. You are advised to review this Privacy Policy periodically for any changes.</p>

        <h5>7. Contact Us</h5>
        <p>If you have any questions about this Privacy Policy, please contact us at support@samanagroup.com</p>


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