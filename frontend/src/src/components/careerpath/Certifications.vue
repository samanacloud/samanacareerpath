<template>
  <div class="card p-4">
    <div class="flex items-center justify-between mb-4 cursor-pointer" @click="toggleCertifications">
      <div class="flex items-center gap-2">
        <i class="pi pi-certificate text-blue-500"></i>
        <h5 class="font-semibold m-0">Certifications</h5>
        <div class="bg-blue-100 text-blue-800 text-xs font-medium px-2 py-0.5 rounded-full">
          {{ certificationsData.length }}
        </div>
      </div>
      <i :class="`pi ${isCertificationsCollapsed ? 'pi-chevron-down' : 'pi-chevron-up'} text-gray-500`"></i>
    </div>
    
    <transition name="fade">
      <div v-if="!isCertificationsCollapsed">
        <div v-if="certificationsData.length === 0" class="text-gray-500 italic py-4 text-center">
          No certifications recorded
        </div>
        <div v-else class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div 
            v-for="(certification, index) in certificationsData" 
            :key="index" 
            class="bg-gray-50 rounded-lg p-4 border-l-4"
            :class="isCertificationActive(certification) ? 'border-green-500' : 'border-red-500'"
          >
            <div class="flex justify-between items-start">
              <div class="flex-1">
                <h6 class="font-medium text-gray-900 mb-1 line-clamp-2">{{ certification.certificationName }}</h6>
                
                <div class="flex items-center text-xs text-gray-500 mt-2">
                  <i class="pi pi-calendar mr-1"></i>
                  <span>Expires: {{ formatDate(certification.certificationExpiration) }}</span>
                </div>
              </div>
              <Tag 
                :value="isCertificationActive(certification) ? 'active' : 'expired'"
                :severity="isCertificationActive(certification) ? 'success' : 'danger'"
                class="text-xs ml-2 shrink-0"
              />
            </div>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';
import Tag from 'primevue/tag';

const props = defineProps({
  certificationsData: {
    type: Array,
    required: true
  },
  isCertificationsCollapsed: {
    type: Boolean,
    required: true
  },
  toggleCertifications: {
    type: Function,
    required: true
  },
  formatDate: {
    type: Function,
    required: true
  },
  isCertificationActive: {
    type: Function,
    required: true
  }
});
</script>

<style scoped>
/* You can add component-specific styling here if needed */
</style> 