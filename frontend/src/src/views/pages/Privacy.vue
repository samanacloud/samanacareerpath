<script>
import { ref, onMounted } from 'vue';

export default {
  name: 'PrivacyPolicy',
  setup() {
    const title = ref('Privacy Policy');
    const content = ref('');

    onMounted(() => {
      // Fetch or initialize the content of the Privacy Policy here
      content.value = `
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