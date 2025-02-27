<template>
  <div class="card p-4">
    <h6 class="mb-2 font-semibold">Skillset Radar</h6>
    <Chart type="radar" :data="radarChartData" :options="radarChartOptions" />
  </div>
</template>

<script setup>
import { defineProps } from 'vue';
import Chart from 'primevue/chart';

const props = defineProps({
  radarChartData: { type: Object, required: true },
  radarChartOptions: { type: Object, required: true }
});
</script>

<style scoped>
/* Add component-specific styling if needed */
</style> 