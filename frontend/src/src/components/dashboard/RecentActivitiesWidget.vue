<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const loading = ref(true);
const error = ref(null);
const latestInterviews = ref([]);

// GraphQL query for latest interviews
const LATEST_INTERVIEWS_QUERY = `
  query GetInterviewsByCompanyId($companyId: String!) {
    getInterviewsByCompanyId(companyId: $companyId) {
      id
      approved
      rating
      recruitmentProcessName
      email
      interviewedBy
      interviewerEmail
      createdAt
    }
  }
`;

// Fetch latest interviews data
const fetchLatestInterviews = async () => {
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
    
    // Now fetch latest interviews
    const response = await fetch(`${import.meta.env.VITE_API_URL}/graphql`, {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json'
      },
      credentials: 'include',
      body: JSON.stringify({
        query: LATEST_INTERVIEWS_QUERY,
        variables: {
          companyId: companyId
        }
      })
    });
    
    const result = await response.json();
    
    if (result.errors) {
      throw new Error(result.errors[0]?.message || 'Failed to fetch latest interviews');
    }
    
    // If we have real data, use it
    if (result.data?.getInterviewsByCompanyId) {
      // Sort by createdAt date (newest first)
      latestInterviews.value = result.data.getInterviewsByCompanyId
        .sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt))
        .slice(0, 10); // Limit to 10 most recent
    } else {
      // Otherwise use mock data
      createMockData();
    }
    
  } catch (err) {
    console.error('Error fetching latest interviews:', err);
    error.value = err.message;
    
    // Use mock data on error
    createMockData();
  } finally {
    loading.value = false;
  }
};

// Create mock data for testing
const createMockData = () => {
  const now = new Date();
  latestInterviews.value = [
    { 
      id: '1', 
      email: 'john.doe@example.com',
      recruitmentProcessName: 'Senior Developer',
      rating: 5,
      approved: 'Yes',
      interviewedBy: 'Maria Garcia',
      interviewerEmail: 'maria@example.com',
      createdAt: new Date(now.getTime() - 1000 * 60 * 30).toISOString() // 30 minutes ago
    },
    { 
      id: '2', 
      email: 'jane.smith@example.com',
      recruitmentProcessName: 'DevOps Engineer',
      rating: 4,
      approved: 'Yes',
      interviewedBy: 'David Lee',
      interviewerEmail: 'david@example.com',
      createdAt: new Date(now.getTime() - 1000 * 60 * 60 * 2).toISOString() // 2 hours ago
    },
    { 
      id: '3', 
      email: 'michael.brown@example.com',
      recruitmentProcessName: 'Cloud Architect',
      rating: 3,
      approved: 'Maybe',
      interviewedBy: 'Sarah Johnson',
      interviewerEmail: 'sarah@example.com',
      createdAt: new Date(now.getTime() - 1000 * 60 * 60 * 5).toISOString() // 5 hours ago
    },
    { 
      id: '4', 
      email: 'emily.davis@example.com',
      recruitmentProcessName: 'Security Specialist',
      rating: 2,
      approved: 'No',
      interviewedBy: 'James Wilson',
      interviewerEmail: 'james@example.com',
      createdAt: new Date(now.getTime() - 1000 * 60 * 60 * 8).toISOString() // 8 hours ago
    },
    { 
      id: '5', 
      email: 'alex.johnson@example.com',
      recruitmentProcessName: 'Frontend Developer',
      rating: 5,
      approved: 'Yes',
      interviewedBy: 'Emma Miller',
      interviewerEmail: 'emma@example.com',
      createdAt: new Date(now.getTime() - 1000 * 60 * 60 * 24).toISOString() // 1 day ago
    }
  ];
};

// Format relative time (e.g., "2 hours ago")
const formatRelativeTime = (timestamp) => {
  const now = new Date();
  const date = new Date(timestamp);
  const diffMs = now - date;
  const diffSec = Math.floor(diffMs / 1000);
  const diffMin = Math.floor(diffSec / 60);
  const diffHour = Math.floor(diffMin / 60);
  const diffDay = Math.floor(diffHour / 24);
  
  if (diffSec < 60) {
    return 'just now';
  } else if (diffMin < 60) {
    return `${diffMin} ${diffMin === 1 ? 'minute' : 'minutes'} ago`;
  } else if (diffHour < 24) {
    return `${diffHour} ${diffHour === 1 ? 'hour' : 'hours'} ago`;
  } else if (diffDay < 7) {
    return `${diffDay} ${diffDay === 1 ? 'day' : 'days'} ago`;
  } else {
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  }
};

// Get rating stars display
const getRatingStars = (rating) => {
  return '★'.repeat(rating) + '☆'.repeat(5 - rating);
};

// Get approval status badge color
const getApprovalStatusColor = (status) => {
  if (!status) return 'bg-gray-100 text-gray-800';
  
  const normalizedStatus = status.toLowerCase();
  if (normalizedStatus === 'yes' || normalizedStatus === 'approved') {
    return 'bg-green-100 text-green-800';
  } else if (normalizedStatus === 'no' || normalizedStatus === 'rejected') {
    return 'bg-red-100 text-red-800';
  } else {
    return 'bg-yellow-100 text-yellow-800';
  }
};

// Navigate to candidate profile
const navigateToCandidate = (email) => {
  router.push(`/candidates?email=${email}`);
};

onMounted(() => {
  fetchLatestInterviews();
});
</script>

<template>
  <div class="card">
    <div class="flex justify-between items-center mb-4">
      <div class="font-semibold text-xl">Latest Interviews</div>
      <Button 
        icon="pi pi-refresh" 
        text 
        rounded 
        @click="fetchLatestInterviews"
        v-tooltip.top="'Refresh'"
      />
    </div>
    
    <div v-if="loading" class="flex justify-center items-center h-60">
      <i class="pi pi-spin pi-spinner text-2xl text-primary"></i>
    </div>
    
    <div v-else-if="error" class="flex flex-col justify-center items-center h-60 text-center">
      <i class="pi pi-exclamation-triangle text-2xl text-yellow-500 mb-3"></i>
      <p class="text-gray-500">{{ error }}</p>
      <Button label="Retry" icon="pi pi-refresh" outlined class="mt-3" @click="fetchLatestInterviews" />
    </div>
    
    <div v-else-if="latestInterviews.length === 0" class="flex flex-col justify-center items-center h-60 text-center">
      <i class="pi pi-calendar text-2xl text-gray-400 mb-3"></i>
      <p class="text-gray-500">No interviews found</p>
    </div>
    
    <div v-else class="interview-timeline">
      <ul class="list-none p-0 m-0">
        <li 
          v-for="interview in latestInterviews" 
          :key="interview.id"
          class="p-3 border-b border-surface-200 cursor-pointer hover:bg-surface-100 transition-colors"
          @click="navigateToCandidate(interview.email)"
        >
          <div class="flex items-center justify-between mb-2">
            <div class="flex items-center gap-2">
              <i class="pi pi-user text-lg bg-blue-100 text-blue-600 p-2 rounded-full"></i>
              <span class="font-medium text-surface-900">{{ interview.email.split('@')[0] }}</span>
            </div>
            <span :class="['text-xs px-2 py-0.5 rounded-full', getApprovalStatusColor(interview.approved)]">
              {{ interview.approved || 'Pending' }}
            </span>
          </div>
          
          <div class="flex justify-between items-center">
            <div class="text-sm text-surface-600">{{ interview.recruitmentProcessName }}</div>
            <div class="flex items-center gap-2">
              <span class="text-xs text-yellow-500">{{ getRatingStars(interview.rating) }}</span>
              <div class="text-xs text-surface-500">{{ formatRelativeTime(interview.createdAt) }}</div>
            </div>
          </div>
          
          <div class="text-xs text-surface-500 mt-1">
            Interviewed by {{ interview.interviewedBy }}
          </div>
        </li>
      </ul>
      
      <div class="flex justify-center mt-4">
        <Button 
          label="View All Interviews" 
          icon="pi pi-calendar" 
          text
          @click="router.push('/recruitment-leads')"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.card {
  padding: 1.25rem;
  border-radius: 0.75rem;
  background-color: var(--surface-card);
  border: 1px solid var(--surface-border);
  height: 100%;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.interview-timeline {
  max-height: 400px;
  overflow-y: auto;
  scrollbar-width: thin;
}

.interview-timeline::-webkit-scrollbar {
  width: 6px;
}

.interview-timeline::-webkit-scrollbar-track {
  background: var(--surface-ground);
  border-radius: 3px;
}

.interview-timeline::-webkit-scrollbar-thumb {
  background: var(--surface-border);
  border-radius: 3px;
}

.interview-timeline::-webkit-scrollbar-thumb:hover {
  background: var(--surface-400);
}
</style> 