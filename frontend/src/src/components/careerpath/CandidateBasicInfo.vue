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
        <Button class="flex-1" severity="info" @click="showInterviewForm" size="small" v-tooltip.top="'Interview Candidate'">
          <i class="pi pi-eye"></i>
        </Button>
        <Button class="flex-1" severity="warning" @click="toggleSkillsetAssessment" size="small" v-tooltip.top="'Assess Skillsets'">
          <i class="pi pi-star"></i>
        </Button>
        <Button class="flex-1" severity="success" @click="contactCandidate" size="small" v-tooltip.top="'Contact Candidate'">
          <i class="pi pi-envelope"></i>
        </Button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';
import Avatar from 'primevue/avatar';
import Button from 'primevue/button';

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
  isRefreshingSkillAverage: { type: Boolean, default: false }
});

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
/* Add any component specific styling here if needed */
</style> 