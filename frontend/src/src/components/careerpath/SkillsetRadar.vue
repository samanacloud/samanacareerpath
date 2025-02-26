<template>
  <div class="card p-4">
    <Chart type="radar" :data="radarChartData" :options="radarChartOptions" />
  </div>
</template>

<script setup>
import { defineProps } from 'vue';
import Chart from 'primevue/chart';

const props = defineProps({
  radarChartData: {
    type: Object,
    required: true
  },
  radarChartOptions: {
    type: Object,
    required: true
  }
});
</script>

<style scoped>
/* You can add component-specific styling here if needed */
</style> 