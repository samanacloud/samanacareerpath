<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const loading = ref(true);
const error = ref(null);
const upcomingInterviews = ref([]);
const activeProcesses = ref([]);
const topCandidates = ref([]);

// GraphQL query for active recruitment processes
const ACTIVE_PROCESSES_QUERY = `
  query getRecruitmentProcessByCompanyId($companyId: String!) {
    getRecruitmentProcessByCompanyId(companyId: $companyId) {
      id
      jobName
      jobCategory
      status
    }
  }
`;

// GraphQL query for candidates by recruitment process
const CANDIDATES_BY_PROCESS_QUERY = `
  query CandidatesByRecruitmentProcessId($recruitmentProcessId: String!) {
    candidatesByRecruitmentProcessId(recruitmentProcessId: $recruitmentProcessId) {
      id
      candidateName
      email
      status
      recruitmentProcessId
      recruitmentProcessName
    }
  }
`;

// GraphQL query for candidate analytics
const CANDIDATE_ANALYTICS_QUERY = `
  query CandidateAnalytics($email: String!) {
    candidateAnalytics(email: $email) {
      skillsetAvg
      interviewYes
      interviewMaybe
      interviewNo
      interviewRating
      certificationCount
      nextInterviewDate
    }
  }
`;

// Fetch data for upcoming interviews with top-rated candidates
const fetchTopRatedCandidates = async () => {
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
    
    // Step 1: Fetch active recruitment processes
    const processesResponse = await fetch(`${import.meta.env.VITE_API_URL}/graphql`, {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json'
      },
      credentials: 'include',
      body: JSON.stringify({
        query: ACTIVE_PROCESSES_QUERY,
        variables: {
          companyId: companyId
        }
      })
    });
    
    const processesResult = await processesResponse.json();
    
    if (processesResult.errors) {
      throw new Error(processesResult.errors[0]?.message || 'Failed to fetch recruitment processes');
    }
    
    // Filter active processes
    const processes = processesResult.data?.getRecruitmentProcessByCompanyId || [];
    activeProcesses.value = processes.filter(process => process.status === 'active');
    
    if (activeProcesses.value.length === 0) {
      // No active processes, use mock data
      createMockData();
      return;
    }
    
    // Step 2: For each active process, fetch candidates
    const candidatesPromises = activeProcesses.value.map(async (process) => {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/graphql`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json'
        },
        credentials: 'include',
        body: JSON.stringify({
          query: CANDIDATES_BY_PROCESS_QUERY,
          variables: {
            recruitmentProcessId: process.id
          }
        })
      });
      
      const result = await response.json();
      if (result.errors) {
        console.error(`Error fetching candidates for process ${process.id}:`, result.errors);
        return [];
      }
      
      return result.data?.candidatesByRecruitmentProcessId.map(candidate => ({
        ...candidate,
        processName: process.jobName,
        jobCategory: process.jobCategory
      })) || [];
    });
    
    const allCandidates = (await Promise.all(candidatesPromises)).flat();
    
    if (allCandidates.length === 0) {
      // No candidates found, use mock data
      createMockData();
      return;
    }
    
    // Step 3: For each candidate, fetch analytics to get ratings and next interview date
    const candidateAnalyticsPromises = allCandidates.map(async (candidate) => {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/graphql`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json'
        },
        credentials: 'include',
        body: JSON.stringify({
          query: CANDIDATE_ANALYTICS_QUERY,
          variables: {
            email: candidate.email
          }
        })
      });
      
      const result = await response.json();
      if (result.errors) {
        console.error(`Error fetching analytics for candidate ${candidate.email}:`, result.errors);
        return {
          ...candidate,
          skillsetAvg: 0,
          interviewRating: 0,
          certificationCount: 0,
          nextInterviewDate: null
        };
      }
      
      const analytics = result.data?.candidateAnalytics || {
        skillsetAvg: 0,
        interviewRating: 0,
        certificationCount: 0,
        nextInterviewDate: null
      };
      
      return {
        ...candidate,
        ...analytics
      };
    });
    
    const candidatesWithAnalytics = await Promise.all(candidateAnalyticsPromises);
    
    // Filter candidates with upcoming interviews
    const candidatesWithInterviews = candidatesWithAnalytics.filter(
      candidate => candidate.nextInterviewDate
    );
    
    if (candidatesWithInterviews.length === 0) {
      // No upcoming interviews, use mock data
      createMockData();
      return;
    }
    
    // Sort by interview date (soonest first) and then by rating (highest first)
    topCandidates.value = candidatesWithInterviews
      .sort((a, b) => {
        // First sort by date
        const dateA = new Date(a.nextInterviewDate);
        const dateB = new Date(b.nextInterviewDate);
        if (dateA < dateB) return -1;
        if (dateA > dateB) return 1;
        
        // If dates are equal, sort by rating
        const ratingA = a.skillsetAvg || 0;
        const ratingB = b.skillsetAvg || 0;
        return ratingB - ratingA;
      })
      .slice(0, 5); // Take top 5
    
    // Format for display
    upcomingInterviews.value = topCandidates.value.map(candidate => ({
      id: candidate.id,
      candidateName: candidate.candidateName,
      candidateId: candidate.id,
      processName: candidate.processName,
      processId: candidate.recruitmentProcessId,
      scheduledDate: candidate.nextInterviewDate,
      interviewType: determineInterviewType(candidate),
      rating: candidate.skillsetAvg || 0,
      certCount: candidate.certificationCount || 0
    }));
    
  } catch (err) {
    console.error('Error fetching top-rated candidates:', err);
    error.value = err.message;
    
    // Use mock data on error
    createMockData();
  } finally {
    loading.value = false;
  }
};

// Create mock data for testing
const createMockData = () => {
  const today = new Date();
  upcomingInterviews.value = [
    { 
      id: '1', 
      candidateName: 'Alex Johnson', 
      candidateId: '101', 
      processName: 'Senior Developer', 
      processId: '201', 
      scheduledDate: new Date(today.getTime() + 1000 * 60 * 60 * 24).toISOString(), // tomorrow
      interviewType: 'Technical',
      rating: 4.8,
      certCount: 5
    },
    { 
      id: '2', 
      candidateName: 'Emma Wilson', 
      candidateId: '102', 
      processName: 'DevOps Engineer', 
      processId: '202', 
      scheduledDate: new Date(today.getTime() + 1000 * 60 * 60 * 24 * 2).toISOString(), // day after tomorrow
      interviewType: 'HR',
      rating: 4.7,
      certCount: 4
    },
    { 
      id: '3', 
      candidateName: 'James Miller', 
      candidateId: '103', 
      processName: 'Cloud Architect', 
      processId: '203', 
      scheduledDate: new Date(today.getTime() + 1000 * 60 * 60 * 24 * 3).toISOString(), // 3 days from now
      interviewType: 'Technical',
      rating: 4.6,
      certCount: 6
    },
    { 
      id: '4', 
      candidateName: 'Sophia Davis', 
      candidateId: '104', 
      processName: 'Security Specialist', 
      processId: '204', 
      scheduledDate: new Date(today.getTime() + 1000 * 60 * 60 * 24 * 4).toISOString(), // 4 days from now
      interviewType: 'Final',
      rating: 4.5,
      certCount: 3
    }
  ];
};

// Determine interview type based on candidate data
const determineInterviewType = (candidate) => {
  if (!candidate) return 'Initial';
  
  const interviewYes = candidate.interviewYes || 0;
  const interviewNo = candidate.interviewNo || 0;
  const interviewMaybe = candidate.interviewMaybe || 0;
  
  if (interviewYes >= 2) return 'Final';
  if (interviewYes >= 1) return 'Technical';
  if (interviewMaybe >= 1) return 'Follow-up';
  return 'Initial';
};

// Format date to relative time (today, tomorrow, or date)
const formatRelativeDate = (dateString) => {
  const date = new Date(dateString);
  const today = new Date();
  const tomorrow = new Date(today);
  tomorrow.setDate(tomorrow.getDate() + 1);
  
  if (date.toDateString() === today.toDateString()) {
    return 'Today';
  } else if (date.toDateString() === tomorrow.toDateString()) {
    return 'Tomorrow';
  } else {
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  }
};

// Format time from date
const formatTime = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
};

// Navigate to candidate profile
const viewCandidateProfile = (candidateId) => {
  router.push(`/candidates?id=${candidateId}`);
};

// Get interview type badge color
const getInterviewTypeColor = (type) => {
  switch (type) {
    case 'Technical':
      return 'bg-blue-100 text-blue-800';
    case 'HR':
      return 'bg-green-100 text-green-800';
    case 'Final':
      return 'bg-purple-100 text-purple-800';
    case 'Initial':
      return 'bg-orange-100 text-orange-800';
    case 'Follow-up':
      return 'bg-cyan-100 text-cyan-800';
    default:
      return 'bg-gray-100 text-gray-800';
  }
};

// Get rating color based on value
const getRatingColor = (rating) => {
  if (rating >= 4.5) return 'text-green-600';
  if (rating >= 4.0) return 'text-blue-600';
  if (rating >= 3.5) return 'text-yellow-600';
  return 'text-gray-600';
};

onMounted(() => {
  fetchTopRatedCandidates();
});
</script>

<template>
  <div class="card">
    <div class="flex justify-between items-center mb-4">
      <div class="font-semibold text-xl">Top Candidates Interviews</div>
      <Button 
        icon="pi pi-calendar" 
        text 
        rounded 
        @click="router.push('/recruitment-leads')"
        v-tooltip.top="'View All Interviews'"
      />
    </div>
    
    <div v-if="loading" class="flex justify-center items-center h-60">
      <i class="pi pi-spin pi-spinner text-2xl text-primary"></i>
    </div>
    
    <div v-else-if="error" class="flex flex-col justify-center items-center h-60 text-center">
      <i class="pi pi-exclamation-triangle text-2xl text-yellow-500 mb-3"></i>
      <p class="text-gray-500">{{ error }}</p>
      <Button label="Retry" icon="pi pi-refresh" outlined class="mt-3" @click="fetchTopRatedCandidates" />
    </div>
    
    <div v-else-if="upcomingInterviews.length === 0" class="flex flex-col justify-center items-center h-60 text-center">
      <i class="pi pi-calendar text-2xl text-gray-400 mb-3"></i>
      <p class="text-gray-500">No upcoming interviews scheduled</p>
    </div>
    
    <div v-else>
      <ul class="list-none p-0 m-0">
        <li 
          v-for="interview in upcomingInterviews" 
          :key="interview.id"
          class="p-3 border-b border-surface-200 cursor-pointer hover:bg-surface-100 transition-colors"
          @click="viewCandidateProfile(interview.candidateId)"
        >
          <div class="flex items-center justify-between mb-2">
            <div class="flex items-center gap-2">
              <span class="font-medium text-surface-900">{{ interview.candidateName }}</span>
              <span :class="['text-xs px-2 py-0.5 rounded-full', getInterviewTypeColor(interview.interviewType)]">
                {{ interview.interviewType }}
              </span>
            </div>
            <div class="flex items-center gap-1">
              <i class="pi pi-star-fill text-yellow-500 text-xs"></i>
              <span :class="['text-sm font-medium', getRatingColor(interview.rating)]">{{ interview.rating.toFixed(1) }}</span>
            </div>
          </div>
          
          <div class="flex justify-between items-center">
            <div class="text-sm text-surface-600">{{ interview.processName }}</div>
            <div class="flex items-center gap-2">
              <span class="text-xs bg-gray-100 text-gray-700 px-1.5 py-0.5 rounded">
                <i class="pi pi-id-card text-xs mr-1"></i>{{ interview.certCount }}
              </span>
              <div class="flex flex-col items-end">
                <div class="text-xs font-medium text-primary-600">{{ formatRelativeDate(interview.scheduledDate) }}</div>
                <div class="text-xs text-surface-500">{{ formatTime(interview.scheduledDate) }}</div>
              </div>
            </div>
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
</style> 