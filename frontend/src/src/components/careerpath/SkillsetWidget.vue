<template>
  <div class="card p-4 mb-4">
    <!-- Header -->
    <div class="flex items-center justify-between mb-4 cursor-pointer">
      <div class="flex items-center gap-2">
        <i class="pi pi-star text-blue-500"></i>
        <h5 class="font-semibold m-0">Skillset Assessment</h5>
        <div class="bg-blue-100 text-blue-800 text-xs font-medium px-2 py-0.5 rounded-full">
          {{ filteredCompanySkillsets.length }}
        </div>
      </div>
      <Button icon="pi pi-times" class="p-button-rounded p-button-text" @click="$emit('close')" />
    </div>

    <!-- Categories Section -->
    <div class="mb-4">
      <h6 class="text-sm font-medium text-gray-700 mb-2">Categories</h6>
      <div class="flex flex-wrap gap-1">
        <Chip 
          v-for="category in skillsetCategories" 
          :key="category"
          :label="category"
          :class="{
            'bg-primary-500 text-primary-500 shadow-lg': selectedSkillsetCategory === category,
            'hover:bg-primary-50 hover:text-primary-500 hover:shadow-lg transition-all duration-200': true
          }"
          @click="setSelectedSkillsetCategory(category)"
          class="cursor-pointer border-1 border-transparent bg-surface-100 shadow-sm text-xs px-2 py-1"
        />
      </div>
    </div>

    <!-- Skillsets List -->
    <div v-if="selectedSkillsetCategory" class="mb-4">
      <h6 class="text-sm font-medium text-gray-700 mb-2">Skillsets in {{ selectedSkillsetCategory }}</h6>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
        <div 
          v-for="skillset in filteredCompanySkillsets" 
          :key="skillset.id" 
          class="p-3 border rounded-lg hover:bg-surface-100 cursor-pointer relative"
          :class="{'border-primary-500 bg-primary-50': selectedSkillset && selectedSkillset.id === skillset.id}"
          @click="selectSkillsetForAssessment(skillset)"
        >
          <div class="flex justify-between items-start">
            <div class="flex-1">
              <div class="font-medium flex items-center gap-1">
                <span v-tooltip.right="skillset.description" class="hidden md:inline">
                  {{ skillset.name }}
                </span>
                <span class="md:hidden">{{ skillset.name }}</span>
                <Button 
                  icon="pi pi-info-circle" 
                  class="p-button-text p-button-rounded p-button-sm text-gray-500 hover:text-primary-500 md:hidden"
                  @click.stop="showMobileDescription(skillset.description)"
                />
              </div>
              <div class="text-xs text-gray-500 md:hidden mt-1">
                {{ truncateDescription(skillset.description) }}
              </div>
            </div>
            <i 
              v-if="selectedSkillset && selectedSkillset.id === skillset.id" 
              class="pi pi-check-circle text-primary-500 ml-2"
            ></i>
          </div>
        </div>
      </div>
    </div>

    <!-- Assessment Form -->
    <div v-if="selectedSkillset" class="border-t pt-4 mt-4">
      <h6 class="font-medium mb-3">Assess: {{ selectedSkillset.name }}</h6>
      <div class="mb-3">
        <label class="block text-sm font-medium text-gray-700 mb-1">Rating</label>
        <Rating v-model="newSkillsetAssessment.rating" :stars="5" />
      </div>
      <div class="mb-3">
        <label class="block text-sm font-medium text-gray-700 mb-1">Notes</label>
        <Textarea v-model="newSkillsetAssessment.notes" rows="2" class="w-full" />
      </div>
      <div class="flex justify-end gap-2">
        <Button label="Cancel" class="p-button-outlined" @click="cancelSkillsetAssessment" />
        <Button label="Submit Assessment" severity="warning" @click="submitSkillsetAssessment" />
      </div>
    </div>

  </div>
</template>

<script setup>
import { defineProps } from 'vue';
import Button from 'primevue/button';
import Chip from 'primevue/chip';
import Rating from 'primevue/rating';
import Textarea from 'primevue/textarea';

const props = defineProps({
  skillsetCategories: { type: Array, required: true },
  filteredCompanySkillsets: { type: Array, required: true },
  selectedSkillsetCategory: { type: String, default: null },
  setSelectedSkillsetCategory: { type: Function, required: true },
  selectedSkillset: { type: Object, default: null },
  selectSkillsetForAssessment: { type: Function, required: true },
  newSkillsetAssessment: { type: Object, required: true },
  cancelSkillsetAssessment: { type: Function, required: true },
  submitSkillsetAssessment: { type: Function, required: true },
  showMobileDescription: { type: Function, required: true },
  truncateDescription: { type: Function, required: true }
});
</script>

<style scoped>
/* Add any component-specific styling if needed */
</style> 