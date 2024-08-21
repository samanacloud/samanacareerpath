<template>
  <div class="grid p-fluid">
    <div class="card">
      <h5>Application Feedback</h5>
      <p>Please, use this section to provide feedback about the platform.</p>
      <div class="grid formgrid">
          <form v-if="!feedbackSubmitted" @submit.prevent="handleSubmit">
            <div class="col-12 ">
              
              <Dropdown v-model="feedbackType" :options="feedbackOptions" optionLabel="label" placeholder="Select Feedback Type" />
            </div>
            <div class="col-12 ">
              <Textarea v-model="description" id="description" placeholder="Description of the error" rows="4" required class="p-inputtextarea p-component"></Textarea>
            
            </div>
            <div class="col-12 ">
        
              <InputText v-model="email" id="email" type="email" disabled class="p-inputtext p-component" />
            </div>
            <Button label="Submit Feedback & Upload Screenshot" icon="pi pi-upload" type="submit" :disabled="loading" class="p-button p-component mt-3" />
          </form>

          <p v-if="loading">
            <ProgressSpinner style="width: 50px; height: 50px;" strokeWidth="8" fill="#EEEEEE" animationDuration=".5s"/>
          </p>

          <div v-if="feedbackSubmitted && !loading" class="success-message">
            <Badge value="Success" severity="success" /> Feedback submitted successfully!
          </div>
          <p v-if="errorMessage && !feedbackSubmitted" class="error-message">{{ errorMessage }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import InputText from 'primevue/inputtext';
import Textarea from 'primevue/textarea';
import Button from 'primevue/button';
import Dropdown from 'primevue/dropdown';
import html2canvas from 'html2canvas';
import ProgressSpinner from 'primevue/progressspinner';
import Badge from 'primevue/badge';
import axios from 'axios';


export default {
  components: {
    ProgressSpinner,
    Badge,
    InputText,
    Textarea,
    Button,
    Dropdown
  },
  data() {
    return {
      feedbackType: null,
      feedbackOptions: [
        { label: 'Application Error', value: 'Application Error' },
        { label: 'Functionality', value: 'Functionality' },
        { label: 'Observation', value: 'Observation' },
        { label: 'Other', value: 'Other' }
      ],
      description: '',
      email: '',
      uploadUrl: '',
      loading: false,
      errorMessage: '',
      feedbackSubmitted: false,
      accessToken: ''
    };
  },
  mounted() {
    this.retrieveAuthToken();
    this.email = this.getSessionEmail(); // Set the email during mounted

  },
  methods: {
    async submitFeedback(screenshotUrl) {
    try {
      const response = await axios.post(`/api/api`, {
        action: 'addFeedback',
        type: this.feedbackType,
        description: this.description,
        email: this.email,
        screenshotUrl
      });

      if (response.data.success) {
        this.feedbackSubmitted = true;  // Ensure this is set to true
        this.errorMessage = ''; // Clear error message
      } else {
        this.errorMessage = 'Failed to submit feedback.';
      }
    } catch (error) {
      console.error('Error submitting feedback:', error);
      this.errorMessage = 'Failed to submit feedback. Please try again.';
    }
  
  },
 
    retrieveAuthToken() {
      const authToken = this.getCookie('authToken');
      if (authToken) {
        this.accessToken = authToken;
      } else {
        this.errorMessage = 'Please sign in first.';
      }
    },
    async handleSubmit() {
      this.loading = true;
      this.uploadUrl = '';
      this.errorMessage = '';

      try {
        // Capture the screenshot
        const canvas = await html2canvas(document.body);
        const blob = await new Promise(resolve => canvas.toBlob(resolve, 'image/png'));

        if (blob) {
          // Upload the screenshot to Google Drive
          this.uploadUrl = await this.uploadToGoogleDrive(blob, this.accessToken);
          this.feedbackSubmitted = true; // Mark feedback as submitted


          // Submit the feedback to the server
          await this.submitFeedback(this.uploadUrl);
          // Clear form fields after successful submission
          this.feedbackType = null;
          this.description = '';
        }
      } catch (error) {
        console.error('Error capturing and uploading screenshot:', error);
        this.errorMessage = 'Failed to upload screenshot. Please try again.';
      } finally {
        this.loading = false;
      }
    },
    async uploadToGoogleDrive(blob, accessToken) {
      const sessionEmail = this.getSessionEmail();
      const currentDateTime = this.getCurrentDateTime();
      const fileName = `screenshot_${sessionEmail}_${currentDateTime}.png`;

      const fileMetadata = {
        'name': fileName,
        'parents': [import.meta.env.VITE_FEEDBACK_FOLDER]
      };

      const form = new FormData();
      form.append('metadata', new Blob([JSON.stringify(fileMetadata)], { type: 'application/json' }));
      form.append('file', blob);

      try {
        const response = await fetch('https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${accessToken}`,
            'Accept': 'application/json'
          },
          body: form
        });

        if (!response.ok) {
          throw new Error(await response.text());
        }

        const data = await response.json();
        return `https://drive.google.com/file/d/${data.id}/view`;
      } catch (error) {
        console.error('Error uploading to Google Drive:', error);
        throw new Error('Upload failed: ' + error.message);
      }
    },
    async submitFeedback(screenshotUrl) {
      try {
        const response = await axios.post(`https://${import.meta.env.VITE_SITE_URL}/api/api`, {
          action: 'addFeedback',
          type: this.feedbackType,
          description: this.description,
          email: this.email,
          screenshotUrl
        });

        if (response.data.success) {
          this.errorMessage = 'Feedback submitted successfully!';
        } else {
          this.errorMessage = 'Failed to submit feedback.';
        }
      } catch (error) {
        console.error('Error:', error);
        this.errorMessage = error.message || 'An error occurred.';

      }
    },
    getCookie(name) {
      const value = `; ${document.cookie}`;
      const parts = value.split(`; ${name}=`);
      if (parts.length === 2) return parts.pop().split(';').shift();
    },
    getSessionEmail() {
      return this.getCookie('userEmail') || 'unknown';
    },
    getCurrentDateTime() {
      const date = new Date();
      return date.toISOString().replace(/T/, '_').replace(/:/g, '-').split('.')[0];
    }
  }
};
</script>

<style scoped>
/* Add styles for the success and error messages */
.success-message {
  color: green;
  font-weight: bold;
}

.error-message {
  color: red;
}
</style>