<template>
  <div class="card p-4">
    <h6 class="mb-2 font-semibold">Skillset Knowledge Distribution</h6>
    <Chart type="bar" :data="verticalBarChartData" :options="chartOptions" />
  </div>
</template>

<script setup>
import { defineProps } from 'vue';
import Chart from 'primevue/chart';

const props = defineProps({
  verticalBarChartData: { type: Object, required: true },
  chartOptions: { type: Object, required: true }
});
</script>

<style scoped>
/* Add component-specific styling if needed */
</style> 