<template>
  <div class="card p-4">
    <div class="flex items-center gap-2 mb-4">
      <i class="pi pi-cog text-gray-500"></i>
      <h5 class="font-semibold m-0">System Information</h5>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
      <div class="flex items-center gap-2 p-3 bg-gray-50 rounded-lg">
        <i class="pi pi-id-card text-gray-500"></i>
        <div>
          <div class="text-gray-500">Profile ID</div>
          <div class="font-mono text-primary-500">{{ candidateData.id }}</div>
        </div>
      </div>
      <div class="flex items-center gap-2 p-3 bg-gray-50 rounded-lg">
        <i class="pi pi-database text-gray-500"></i>
        <div>
          <div class="text-gray-500">Company ID</div>
          <div class="font-mono text-primary-500">{{ candidateData.companyId }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  candidateData: { type: Object, required: true }
});
</script>

<style scoped>
/* Add any component-specific styling if needed */
</style> 