<template>
  <div class="card p-4">
    <div class="flex flex-col items-center">
      <Avatar :label="candidateInitials" shape="circle" size="xlarge" class="mb-4" />
      <h2 class="text-xl font-bold mb-2">{{ formattedName }}</h2>
      <!-- Counters Section -->
      <div class="flex space-x-6 mb-4">
        <div class="flex items-center">
          <i class="pi pi-star-fill text-yellow-500 mr-1"></i>
          <span v-if="!isRefreshingSkillAverage">{{ allSkillsAverage }}</span>
          <span v-else class="flex items-center">
            <i class="pi pi-spin pi-spinner text-yellow-500 text-sm mr-1"></i>
          </span>
        </div>
        <div class="flex items-center">
          <i class="pi pi-comment text-blue-500 mr-1"></i>
          <span>{{ interviewsCount }}</span>
        </div>
        <div class="flex items-center">
          <i class="pi pi-thumbs-up text-green-500 mr-1"></i>
          <span>{{ approvedCounts.yes }}</span>
        </div>
        <div class="flex items-center">
          <i class="pi pi-clock text-yellow-500 mr-1"></i>
          <span>{{ approvedCounts.pending }}</span>
        </div>
        <div class="flex items-center">
          <i class="pi pi-thumbs-down text-red-500 mr-1"></i>
          <span>{{ approvedCounts.no }}</span>
        </div>
      </div>
      <p class="text-sm text-gray-600 text-center mb-4"><i class="pi pi-briefcase"></i>{{ candidateData.recruitmentProcessName }}</p>
      
      <!-- Skills Radar Toggle Button -->
      <div class="w-full mb-4">
        <Button 
          :icon="showSkillsRadar ? 'pi pi-eye-slash' : 'pi pi-chart-line'" 
          :label="showSkillsRadar ? 'Hide Skills Radar' : 'Show Skills Radar'" 
          class="p-button-outlined p-button-sm w-full"
          :class="showSkillsRadar ? 'p-button-secondary' : 'p-button-info'"
          @click="toggleSkillsRadar"
        />
      </div>
      
      <!-- Contact Info Section -->
      <div class="w-full mt-4 space-y-2 text-sm">
        <div class="flex items-center">
          <i class="pi pi-envelope mr-2"></i>
          <span>{{ candidateData.email }}</span>
        </div>
        <div class="flex items-center">
          <i class="pi pi-globe mr-2"></i>
          <span>{{ candidateData.country }}</span>
        </div>
        <div class="flex items-center">
          <i class="pi pi-phone mr-2"></i>
          <span>{{ candidateData.phone }}</span>
        </div>
        <div class="flex items-center">
          <i class="pi pi-money-bill mr-2"></i>
          <span>{{ candidateData.salaryExpectation ? candidateData.salaryExpectation : 'Not specified' }}</span>
        </div>
        <div class="flex items-center">
          <i class="pi pi-file mr-2"></i>
          <a v-if="candidateData.candidateCV" :href="candidateData.candidateCV" target="_blank" class="text-blue-500 hover:underline">View CV</a>
          <span v-else class="text-gray-500">No CV uploaded</span>
        </div>
        <div class="flex items-center">
          <i class="pi pi-calendar mr-2"></i>
          <span>{{ formatDate(candidateData.createdAt) }}</span>
        </div>
      </div>
      <!-- Action Buttons -->
      <div class="w-full mt-6 flex gap-2">
        <Button 
          class="flex-1" 
          severity="info" 
          @click="showInterviewForm" 
          size="small"
          raised
          v-tooltip.top="'Interview Candidate'"
          :label="!showSkillsRadar && windowWidth >= 1024 ? 'Interview' : ''"
          :icon="'pi pi-eye'"
        />
        <Button 
          class="flex-1" 
          severity="warn" 
          raised
          @click="toggleSkillsetAssessment" 
          size="small" 
          v-tooltip.top="'Assess Skillsets'"
          :label="!showSkillsRadar && windowWidth >= 1024 ? 'Assess' : ''"
          :icon="'pi pi-star'"
        />
        <SplitButton 
          class="flex-1" 
          severity="success" 
          size="small" 
          raised
          :label="!showSkillsRadar && windowWidth >= 1024 ? 'Contact' : ''" 
          icon="pi pi-envelope" 
          :model="contactOptions" 
          @click="contactViaEmail"
          v-tooltip.top="'Contact Candidate'"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';
import Avatar from 'primevue/avatar';
import Button from 'primevue/button';
import SplitButton from 'primevue/splitbutton';
import { ref, onMounted, onUnmounted } from 'vue';

const props = defineProps({
  candidateData: { type: Object, required: true },
  candidateInitials: { type: String, required: true },
  formattedName: { type: String, required: true },
  allSkillsAverage: { type: [String, Number], required: true },
  interviewsCount: { type: Number, required: true },
  approvedCounts: { type: Object, required: true },
  showInterviewForm: { type: Function, required: true },
  toggleSkillsetAssessment: { type: Function, required: true },
  contactCandidate: { type: Function, required: true },
  isRefreshingSkillAverage: { type: Boolean, default: false },
  showSkillsRadar: { type: Boolean, required: true },
  toggleSkillsRadar: { type: Function, required: true }
});

// Add reactive variable to track window width
const windowWidth = ref(window.innerWidth);

// Add resize event listener
const handleResize = () => {
  windowWidth.value = window.innerWidth;
};

// Setup and cleanup event listeners
onMounted(() => {
  window.addEventListener('resize', handleResize);
});

onUnmounted(() => {
  window.removeEventListener('resize', handleResize);
});

// Contact options for the SplitButton
const contactOptions = [
  {
    label: 'WhatsApp',
    icon: 'pi pi-whatsapp',
    command: () => {
      contactViaWhatsApp();
    }
  },
  {
    label: 'Google Calendar',
    icon: 'pi pi-calendar',
    command: () => {
      contactViaCalendar();
    }
  }
];

// Function to contact via WhatsApp
const contactViaWhatsApp = () => {
  const userName = localStorage.getItem('userName') || 'a recruiter';
  const companyName = localStorage.getItem('companyName') || 'Samana Group';
  
  // Get first name for a more friendly greeting
  const firstName = props.formattedName.split(' ')[0];
  
  // Updated message asking about availability for a quick call
  const message = `Hello ${firstName}, Nice to meet you! My name is ${userName} from ${companyName}. I'm reviewing your application for the ${props.candidateData.recruitmentProcessName} role and I'm impressed with your profile. Are you available for a quick call right now to confirm some information from your CV? If not, please let me know when would be a convenient time for you. Thank you!`;
  
  // Encode the message for URL
  const encodedMessage = encodeURIComponent(message);
  
  // Open WhatsApp Web with the pre-filled message
  window.open(`https://web.whatsapp.com/send?phone=${props.candidateData.phone}&text=${encodedMessage}`, '_blank');
};

// Function to contact via Google Calendar
const contactViaCalendar = () => {
  const userName = localStorage.getItem('userName') || 'a recruiter';
  const userEmail = localStorage.getItem('userEmail') || 'recruiting@samanagroup.com';
  const companyName = localStorage.getItem('companyName') || 'Samana Group';
  const subject = `Interview: ${props.formattedName} - ${props.candidateData.recruitmentProcessName} Position`;
  
  // Get first name for a more friendly greeting
  const firstName = props.formattedName.split(' ')[0];
  
  // Create a more professional description with friendly greeting
  let description = `Dear ${firstName},\n\n`;
  description += `I would like to invite you to an interview for the ${props.candidateData.recruitmentProcessName} position at ${companyName}. `;
  description += `We were impressed with your application and would like to discuss your qualifications and experience in more detail.\n\n`;
  
  // Add CV reference in a cleaner way
  if (props.candidateData.candidateCV) {
    description += `I have reviewed your CV and would like to explore how your skills align with our requirements.\n\n`;
  }
  
  description += `Please confirm if this time works for you. If not, please suggest a few alternative times that would be convenient.\n\n`;
  
  // Add candidate contact information in a more structured way
  description += `Reference Information:\n\n`;
  description += `• Candidate: ${props.formattedName}\n`;
  description += `• Position: ${props.candidateData.recruitmentProcessName}\n`;
  description += `• Email: ${props.candidateData.email}\n`;
  description += `• Phone: ${props.candidateData.phone}\n`;
  description += `• Country: ${props.candidateData.country}\n\n`;
  description += `• CV: ${props.candidateData.candidateCV}\n\n`;
  
  // Add professional signature
  description += `Best Regards,\n\n`;
  description += `${userName}\n`;
  description += `${userEmail}\n`;
  description += `${companyName}`;
  
  // Create Google Calendar event URL
  const startDate = new Date();
  startDate.setDate(startDate.getDate() + 1); // Set to tomorrow
  startDate.setHours(10, 0, 0, 0); // Set to 10:00 AM
  
  const endDate = new Date(startDate);
  endDate.setHours(11, 0, 0, 0); // Set to 11:00 AM (1 hour meeting)
  
  // Format dates for Google Calendar
  const formatDate = (date) => {
    return date.toISOString().replace(/-|:|\.\d+/g, '');
  };
  
  // Add Google Meet video conferencing by including the 'crm' parameter
  const calendarUrl = `https://calendar.google.com/calendar/render?action=TEMPLATE&text=${encodeURIComponent(subject)}&dates=${formatDate(startDate)}/${formatDate(endDate)}&details=${encodeURIComponent(description)}&add=${encodeURIComponent('recruiting@samanagroup.com')}&add=${encodeURIComponent(props.candidateData.email)}&crm=AVAILABLE&sf=true&output=xml`;
  
  window.open(calendarUrl, '_blank');
};

// Function to contact via Email
const contactViaEmail = () => {
  const userName = localStorage.getItem('userName') || 'a recruiter';
  const companyName = localStorage.getItem('companyName') || 'Samana Group';
  const subject = `Regarding your application for ${props.candidateData.recruitmentProcessName}`;
  const body = `Hello, Nice to meet you! My name is ${userName} from ${companyName} and I would like to ask you some questions regarding the application you recently sent us for the role ${props.candidateData.recruitmentProcessName}`;
  
  // Open Gmail with pre-filled message
  window.open(`https://mail.google.com/mail/?view=cm&fs=1&to=${props.candidateData.email}&su=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`, '_blank');
};

// Function to format date to Jan-03-2025 format
const formatDate = (dateString) => {
  if (!dateString) return 'Not available';
  
  const date = new Date(dateString);
  if (isNaN(date.getTime())) return 'Invalid date';
  
  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  const month = months[date.getMonth()];
  const day = String(date.getDate()).padStart(2, '0');
  const year = date.getFullYear();
  
  return `${month}-${day}-${year}`;
};
</script>

<style scoped>
/* Custom styling for SplitButton to match regular buttons */
:deep(.p-splitbutton) {
  display: flex;
  width: 100%;
}

:deep(.p-splitbutton .p-button) {
  flex: 1;
}

:deep(.p-splitbutton .p-splitbutton-menubutton) {
  width: auto;
}

/* Ensure all buttons in the action section have the same width */
.w-full.mt-6.flex.gap-2 > * {
  flex: 1;
  min-width: 0;
}
</style> 