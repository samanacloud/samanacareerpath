<template>
  <div class="card p-4">
    <h6 class="mb-2 font-semibold">Knowledge Distribution by Skillset</h6>
    <Chart type="pie" :data="pieChartData" :options="chartOptions" />
  </div>
</template>

<script setup>
import { defineProps } from 'vue';
import Chart from 'primevue/chart';

const props = defineProps({
  pieChartData: { type: Object, required: true },
  chartOptions: { type: Object, required: true }
});
</script>

<style scoped>
/* Add component-specific styling if needed */
</style> 