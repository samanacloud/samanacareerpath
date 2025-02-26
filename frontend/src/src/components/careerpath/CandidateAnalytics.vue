<template>
  <div class="card p-4">
    <h5 class="mb-4">Candidate Analytics - {{ selectedCategory }}</h5>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <!-- Basic Bar Chart Widget -->
      <div class="card p-4">
        <h6 class="mb-2 font-semibold">Skillset Average Rating</h6>
        <Chart type="bar" :data="basicChartData" :options="chartOptions" />
      </div>
      <!-- Pie Chart Widget -->
      <div class="card p-4">
        <h6 class="mb-2 font-semibold">Knowledge Distribution by Skillset</h6>
        <Chart type="pie" :data="pieChartData" :options="chartOptions" />
      </div>
      <!-- Vertical Bar Chart Widget -->
      <div class="card p-4">
        <h6 class="mb-2 font-semibold">Skillset Knowledge Distribution</h6>
        <Chart type="bar" :data="verticalBarChartData" :options="chartOptions" />
      </div>
      <!-- Skillset Radar Component -->
      <div class="card p-4">
        <SkillsetRadar :radarChartData="radarChartData" :radarChartOptions="radarChartOptions" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';
import Chart from 'primevue/chart';
import SkillsetRadar from '@/components/careerpath/SkillsetRadar.vue';

const props = defineProps({
  selectedCategory: { type: String, required: true },
  basicChartData: { type: Object, required: true },
  pieChartData: { type: Object, required: true },
  verticalBarChartData: { type: Object, required: true },
  radarChartData: { type: Object, required: true },
  chartOptions: { type: Object, required: true },
  radarChartOptions: { type: Object, required: true }
});
</script>

<style scoped>
/* Add component-specific styling if needed */
</style> 