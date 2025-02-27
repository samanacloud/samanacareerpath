<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const loading = ref(true);
const error = ref(null);
const topPerformers = ref([]);

// GraphQL query for top performers
const TOP_PERFORMERS_QUERY = `
  query TopPerformers($companyId: String!, $limit: Int!) {
    topPerformers(companyId: $companyId, limit: $limit) {
      id
      name
      email
      role
      skillsetCount
      certificationCount
      skillsetRating
    }
  }
`;

// Fetch top performers data
const fetchTopPerformers = async () => {
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
    
    // Now fetch top performers
    const response = await fetch(`${import.meta.env.VITE_API_URL}/graphql`, {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json'
      },
      credentials: 'include',
      body: JSON.stringify({
        query: TOP_PERFORMERS_QUERY,
        variables: {
          companyId: companyId,
          limit: 5
        }
      })
    });
    
    const result = await response.json();
    
    if (result.errors) {
      throw new Error(result.errors[0]?.message || 'Failed to fetch top performers');
    }
    
    // If we have real data, use it
    if (result.data?.topPerformers) {
      topPerformers.value = result.data.topPerformers;
    } else {
      // Otherwise use mock data
      topPerformers.value = [
        { id: '1', name: 'John Smith', email: 'john.smith@example.com', role: 'Senior Developer', skillsetCount: 12, certificationCount: 5, skillsetRating: 4.8 },
        { id: '2', name: 'Maria Garcia', email: 'maria.garcia@example.com', role: 'DevOps Engineer', skillsetCount: 10, certificationCount: 4, skillsetRating: 4.7 },
        { id: '3', name: 'David Lee', email: 'david.lee@example.com', role: 'Security Specialist', skillsetCount: 8, certificationCount: 6, skillsetRating: 4.6 },
        { id: '4', name: 'Sarah Johnson', email: 'sarah.johnson@example.com', role: 'Cloud Architect', skillsetCount: 9, certificationCount: 7, skillsetRating: 4.5 },
        { id: '5', name: 'Michael Brown', email: 'michael.brown@example.com', role: 'Data Scientist', skillsetCount: 7, certificationCount: 3, skillsetRating: 4.4 }
      ];
    }
    
  } catch (err) {
    console.error('Error fetching top performers:', err);
    error.value = err.message;
    
    // Use mock data on error
    topPerformers.value = [
      { id: '1', name: 'John Smith', email: 'john.smith@example.com', role: 'Senior Developer', skillsetCount: 12, certificationCount: 5, skillsetRating: 4.8 },
      { id: '2', name: 'Maria Garcia', email: 'maria.garcia@example.com', role: 'DevOps Engineer', skillsetCount: 10, certificationCount: 4, skillsetRating: 4.7 },
      { id: '3', name: 'David Lee', email: 'david.lee@example.com', role: 'Security Specialist', skillsetCount: 8, certificationCount: 6, skillsetRating: 4.6 },
      { id: '4', name: 'Sarah Johnson', email: 'sarah.johnson@example.com', role: 'Cloud Architect', skillsetCount: 9, certificationCount: 7, skillsetRating: 4.5 },
      { id: '5', name: 'Michael Brown', email: 'michael.brown@example.com', role: 'Data Scientist', skillsetCount: 7, certificationCount: 3, skillsetRating: 4.4 }
    ];
  } finally {
    loading.value = false;
  }
};

// Navigate to employee profile
const viewEmployeeProfile = (employeeId) => {
  router.push(`/employees?id=${employeeId}`);
};

// Get initials from name
const getInitials = (name) => {
  if (!name) return '??';
  const names = name.split(' ');
  let initials = names[0].substring(0, 1).toUpperCase();
  if (names.length > 1) {
    initials += names[names.length - 1].substring(0, 1).toUpperCase();
  }
  return initials;
};

onMounted(() => {
  fetchTopPerformers();
});
</script>

<template>
  <div class="card">
    <div class="flex justify-between items-center mb-4">
      <div class="font-semibold text-xl">Top Performers</div>
      <Button 
        icon="pi pi-users" 
        text 
        rounded 
        @click="router.push('/employees')"
        v-tooltip.top="'View All Employees'"
      />
    </div>
    
    <div v-if="loading" class="flex justify-center items-center h-80">
      <i class="pi pi-spin pi-spinner text-2xl text-primary"></i>
    </div>
    
    <div v-else-if="error" class="flex flex-col justify-center items-center h-80 text-center">
      <i class="pi pi-exclamation-triangle text-2xl text-yellow-500 mb-3"></i>
      <p class="text-gray-500">{{ error }}</p>
      <Button label="Retry" icon="pi pi-refresh" outlined class="mt-3" @click="fetchTopPerformers" />
    </div>
    
    <div v-else>
      <ul class="list-none p-0 m-0">
        <li 
          v-for="(performer, index) in topPerformers" 
          :key="performer.id"
          class="flex items-center p-3 border-b border-surface-200 cursor-pointer hover:bg-surface-100 transition-colors"
          @click="viewEmployeeProfile(performer.id)"
        >
          <div class="flex items-center gap-3 flex-1">
            <div class="w-10 h-10 rounded-full bg-primary-100 flex items-center justify-center text-primary-700 font-medium">
              {{ getInitials(performer.name) }}
            </div>
            <div class="flex flex-col">
              <span class="font-medium text-surface-900">{{ performer.name }}</span>
              <span class="text-sm text-surface-600">{{ performer.role }}</span>
            </div>
          </div>
          
          <div class="flex items-center gap-4">
            <div class="flex flex-col items-center">
              <div class="text-sm font-semibold">{{ performer.skillsetCount }}</div>
              <div class="text-xs text-surface-600">Skills</div>
            </div>
            
            <div class="flex flex-col items-center">
              <div class="text-sm font-semibold">{{ performer.certificationCount }}</div>
              <div class="text-xs text-surface-600">Certs</div>
            </div>
            
            <div class="flex items-center gap-1 bg-primary-50 text-primary-700 px-2 py-1 rounded">
              <i class="pi pi-star-fill text-yellow-500 text-xs"></i>
              <span class="text-sm font-medium">{{ performer.skillsetRating.toFixed(1) }}</span>
            </div>
          </div>
        </li>
      </ul>
      
      <div class="flex justify-center mt-4">
        <Button 
          label="View All Employees" 
          icon="pi pi-users" 
          text
          @click="router.push('/employees')"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.card {
  height: 100%;
}
</style> 