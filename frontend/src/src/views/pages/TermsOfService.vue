<script>
import { ref, onMounted } from 'vue';


export default {
  name: 'TermsOfService',
  setup() {
    const title = ref('Terms of Service');
    const content = ref('');

    onMounted(() => {
      // Fetch or initialize the content of the Terms of Service here
      content.value = `
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
      `;
    });

    return {
      title,
      content
    };
  }
};
</script>

<template>
  <div class="card">
    <h3>{{ title }}</h3>
    <div v-html="content"></div>
  </div>
</template>

<style scoped>
.card {
  padding: 20px;
  margin: 20px;
}
</style>