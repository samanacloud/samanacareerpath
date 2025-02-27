<template>
  <div class="card p-4">
    <h6 class="mb-2 font-semibold">Skillset Average Rating</h6>
    <Chart type="bar" :data="basicChartData" :options="chartOptions" />
  </div>
</template>

<script setup>
import { defineProps } from 'vue';
import Chart from 'primevue/chart';

const props = defineProps({
  basicChartData: { type: Object, required: true },
  chartOptions: { type: Object, required: true }
});
</script>

<style scoped>
/* Add component-specific styling if needed */
</style> 