<script setup>
import { ref, onMounted, computed } from 'vue';
import { useLayout } from '@/layout/composables/layout';
import { useRouter } from 'vue-router';

const router = useRouter();
const { getPrimary, getSurface, isDarkTheme } = useLayout();
const loading = ref(true);
const error = ref(null);
const skillsetCategories = ref([]);
const skillsetCounts = ref([]);
const totalSkillsets = ref(0);

// GraphQL query for skillset distribution
const SKILLSET_DISTRIBUTION_QUERY = `
  query ListSkillsetsCategories($companyId: String!) {
    listSkillsetsCategories(companyId: $companyId)
  }
`;

const SKILLSETS_BY_CATEGORY_QUERY = `
  query ListSkillsetsByCategory($companyId: String!, $category: String!) {
    listSkillsetsByCategory(companyId: $companyId, category: $category) {
      id
      skillsetName
      skillsetDescription
      skillsetCategory
    }
  }
`;

// Fetch skillset distribution data
const fetchSkillsetDistribution = async () => {
  try {
    loading.value = true;
    
    // First get the session info to get companyId
    const sessionResponse = await fetch('/core/auth/verify/session', {
      method: 'GET',
      credentials: 'include',
      headers: {
        'Accept': 'application/json',
      }
    });
    
    if (!sessionResponse.ok) {
      throw new Error('Failed to fetch session info');
    }
    
    const sessionData = await sessionResponse.json();
    const companyId = sessionData.user.companyId;
    
    if (!companyId) {
      throw new Error('No company selected');
    }
    
    // First fetch all categories
    const categoriesResponse = await fetch(`${import.meta.env.VITE_API_URL}/graphql`, {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json'
      },
      credentials: 'include',
      body: JSON.stringify({
        query: SKILLSET_DISTRIBUTION_QUERY,
        variables: {
          companyId: companyId
        }
      })
    });
    
    const categoriesResult = await categoriesResponse.json();
    
    if (categoriesResult.errors) {
      throw new Error(categoriesResult.errors[0]?.message || 'Failed to fetch skillset categories');
    }
    
    // If we have real categories data
    if (categoriesResult.data?.listSkillsetsCategories && categoriesResult.data.listSkillsetsCategories.length > 0) {
      const categories = categoriesResult.data.listSkillsetsCategories;
      skillsetCategories.value = categories;
      
      // Now fetch count for each category
      const countPromises = categories.map(async (category) => {
        const response = await fetch(`${import.meta.env.VITE_API_URL}/graphql`, {
          method: 'POST',
          headers: { 
            'Content-Type': 'application/json'
          },
          credentials: 'include',
          body: JSON.stringify({
            query: SKILLSETS_BY_CATEGORY_QUERY,
            variables: {
              companyId: companyId,
              category: category
            }
          })
        });
        
        const result = await response.json();
        if (result.errors) {
          console.error(`Error fetching skillsets for category ${category}:`, result.errors);
          return 0;
        }
        
        return result.data?.listSkillsetsByCategory?.length || 0;
      });
      
      // Wait for all counts to be fetched
      skillsetCounts.value = await Promise.all(countPromises);
      totalSkillsets.value = skillsetCounts.value.reduce((sum, count) => sum + count, 0);
    } else {
      // Otherwise use mock data
      skillsetCategories.value = ['Cloud', 'DevOps', 'Security', 'Development', 'AI/ML', 'Networking'];
      skillsetCounts.value = [42, 35, 28, 45, 22, 30];
      totalSkillsets.value = skillsetCounts.value.reduce((sum, count) => sum + count, 0);
    }
    
  } catch (err) {
    console.error('Error fetching skillset distribution:', err);
    error.value = err.message;
    
    // Use mock data on error
    skillsetCategories.value = ['Cloud', 'DevOps', 'Security', 'Development', 'AI/ML', 'Networking'];
    skillsetCounts.value = [42, 35, 28, 45, 22, 30];
    totalSkillsets.value = skillsetCounts.value.reduce((sum, count) => sum + count, 0);
  } finally {
    loading.value = false;
  }
};

// Chart data and options
const chartData = computed(() => {
  const documentStyle = getComputedStyle(document.documentElement);
  
  return {
    labels: skillsetCategories.value,
    datasets: [
      {
        label: 'Skillset Distribution',
        data: skillsetCounts.value,
        backgroundColor: [
          documentStyle.getPropertyValue('--blue-500'),
          documentStyle.getPropertyValue('--green-500'),
          documentStyle.getPropertyValue('--yellow-500'),
          documentStyle.getPropertyValue('--purple-500'),
          documentStyle.getPropertyValue('--cyan-500'),
          documentStyle.getPropertyValue('--pink-500'),
          documentStyle.getPropertyValue('--indigo-500'),
          documentStyle.getPropertyValue('--teal-500')
        ],
        hoverBackgroundColor: [
          documentStyle.getPropertyValue('--blue-400'),
          documentStyle.getPropertyValue('--green-400'),
          documentStyle.getPropertyValue('--yellow-400'),
          documentStyle.getPropertyValue('--purple-400'),
          documentStyle.getPropertyValue('--cyan-400'),
          documentStyle.getPropertyValue('--pink-400'),
          documentStyle.getPropertyValue('--indigo-400'),
          documentStyle.getPropertyValue('--teal-400')
        ],
        borderWidth: 0
      }
    ]
  };
});

const chartOptions = computed(() => {
  const documentStyle = getComputedStyle(document.documentElement);
  const textColor = documentStyle.getPropertyValue('--text-color');
  
  return {
    plugins: {
      legend: {
        position: 'right',
        labels: {
          color: textColor,
          usePointStyle: true,
          font: {
            weight: 500
          }
        }
      },
      tooltip: {
        callbacks: {
          label: (context) => {
            const label = context.label || '';
            const value = context.raw || 0;
            const percentage = Math.round((value / totalSkillsets.value) * 100);
            return `${label}: ${value} (${percentage}%)`;
          }
        }
      }
    },
    responsive: true,
    maintainAspectRatio: false
  };
});

// Calculate percentage for each category
const getPercentage = (count) => {
  if (totalSkillsets.value === 0) return 0;
  return Math.round((count / totalSkillsets.value) * 100);
};

// Get color for category
const getCategoryColor = (index) => {
  const colors = [
    'bg-blue-500',
    'bg-green-500',
    'bg-yellow-500',
    'bg-purple-500',
    'bg-cyan-500',
    'bg-pink-500',
    'bg-indigo-500',
    'bg-teal-500'
  ];
  return colors[index % colors.length];
};

const navigateToSkillsets = () => {
  router.push('/admin-skillsets');
};

onMounted(() => {
  fetchSkillsetDistribution();
});
</script>

<template>
  <div class="card">
    <div class="flex justify-between items-center mb-4">
      <div class="font-semibold text-xl">Skillset Distribution</div>
      <Button 
        icon="pi pi-cog" 
        text 
        rounded 
        @click="navigateToSkillsets"
        v-tooltip.top="'Manage Skillsets'"
      />
    </div>
    
    <div v-if="loading" class="flex justify-center items-center h-80">
      <i class="pi pi-spin pi-spinner text-2xl text-primary"></i>
    </div>
    
    <div v-else-if="error" class="flex flex-col justify-center items-center h-80 text-center">
      <i class="pi pi-exclamation-triangle text-2xl text-yellow-500 mb-3"></i>
      <p class="text-gray-500">{{ error }}</p>
      <Button label="Retry" icon="pi pi-refresh" outlined class="mt-3" @click="fetchSkillsetDistribution" />
    </div>
    
    <div v-else-if="skillsetCategories.length === 0" class="flex flex-col justify-center items-center h-80 text-center">
      <i class="pi pi-chart-pie text-2xl text-gray-400 mb-3"></i>
      <p class="text-gray-500">No skillset categories found</p>
      <Button label="Add Skillsets" icon="pi pi-plus" outlined class="mt-3" @click="navigateToSkillsets" />
    </div>
    
    <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <!-- Chart -->
      <div class="md:col-span-2 h-80">
        <Chart type="doughnut" :data="chartData" :options="chartOptions" />
      </div>
      
      <!-- Legend with counts -->
      <div class="md:col-span-1 overflow-auto" style="max-height: 320px;">
        <div class="text-sm font-medium mb-2">Categories</div>
        <ul class="list-none p-0 m-0">
          <li v-for="(category, index) in skillsetCategories" :key="category" class="mb-2 flex items-center">
            <div :class="['w-3 h-3 rounded-full mr-2', getCategoryColor(index)]"></div>
            <div class="flex-1 flex justify-between items-center">
              <span class="text-sm">{{ category }}</span>
              <div class="flex items-center gap-2">
                <span class="text-xs font-medium">{{ skillsetCounts[index] }}</span>
                <span class="text-xs text-gray-500">({{ getPercentage(skillsetCounts[index]) }}%)</span>
              </div>
            </div>
          </li>
        </ul>
        <div class="mt-4 pt-3 border-t border-gray-200">
          <div class="flex justify-between items-center">
            <span class="text-sm font-medium">Total</span>
            <span class="text-sm font-medium">{{ totalSkillsets }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.card {
  height: 100%;
}
</style> 