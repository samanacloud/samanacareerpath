<template>
  <div class="p-4">
    <div v-if="loading" class="text-center p-8">
      <ProgressSpinner style="width: 50px; height: 50px" />
      <p class="mt-2 text-gray-600">Loading candidate profile...</p>
    </div>
    
    <div v-else class="grid grid-cols-12 gap-4">
      <!-- Candidate Basic Info Card -->
      <div class="col-span-12 md:col-span-4">
        <div class="card p-4">
          <div class="flex flex-col items-center">
            <Avatar :label="candidateInitials" shape="circle" size="xlarge" class="mb-4" />
            <h2 class="text-xl font-bold mb-2">{{ formattedName }}</h2>
            
            <!-- Add counters -->
            <div class="flex space-x-6 mb-4">
              <div class="flex items-center">
                <i class="pi pi-star-fill text-yellow-500 mr-1"></i>
                <span>{{ allSkillsAverage }}</span>
              </div>
              <div class="flex items-center">
                <i class="pi pi-comment text-blue-500 mr-1"></i>
                <span>{{ interviewsData.length }}</span>
              </div>
              <div class="flex items-center">
                <i class="pi pi-thumbs-up text-green-500 mr-1"></i>
                <span>{{ approvedCounts.yes }}</span>
              </div>
              <div class="flex items-center">
                <i class="pi pi-clock text-yellow-500 mr-1"></i>
                <span>{{ approvedCounts.pending }}</span>
              </div>
              <div class="flex items-center">
                <i class="pi pi-thumbs-down text-red-500 mr-1"></i>
                <span>{{ approvedCounts.no }}</span>
              </div>
            </div>
            
            <p class="text-sm text-gray-600">Position Applied For: {{ candidateData.recruitmentProcessName }}</p>
            
            <!-- Add additional candidate information -->
            <div class="w-full mt-4 space-y-2 text-sm">
              <div class="flex items-center">
                <i class="pi pi-envelope mr-2"></i>
                <span>{{ candidateData.email }}</span>
              </div>
              <div class="flex items-center">
                <i class="pi pi-globe mr-2"></i>
                <span>{{ candidateData.country }}</span>
              </div>
              <div class="flex items-center">
                <i class="pi pi-phone mr-2"></i>
                <span>{{ candidateData.phone }}</span>
              </div>
              <div class="flex items-center">
                <i class="pi pi-money-bill mr-2"></i>
                <span>Salary Expectation: {{ formattedSalary }}</span>
              </div>
              <div class="flex items-center">
                <i class="pi pi-file mr-2"></i>
                <a v-if="candidateData.candidateCV" 
                   :href="candidateData.candidateCV" 
                   target="_blank" 
                   class="text-blue-500 hover:underline">
                  View CV
                </a>
                <span v-else class="text-gray-500">No CV uploaded</span>
              </div>
              <div class="flex items-center">
                <i class="pi pi-calendar mr-2"></i>
                <span>Applied on: {{ formattedDate }}</span>
              </div>
              
            </div>
            

   
   
            <!-- Update action buttons -->
            <div class="w-full mt-6 flex gap-2">
              <Button class="flex-1" severity="info" @click="reviewCandidate" size="small">
                <i class="pi pi-eye"></i>
              </Button>
              <Button class="flex-1" severity="success" @click="scheduleInterview" size="small">
                <i class="pi pi-calendar-plus"></i>
              </Button>
              <Button class="flex-1" severity="warning" @click="contactCandidate" size="small">
                <i class="pi pi-envelope"></i>
              </Button>
            </div>
          </div>
        </div>
        <div class="col-span-12">
        <div class="card p-4">
          
          <div class="grid grid-cols-1">
            <div class="card p-4">
              <Chart 
                type="radar" 
                :data="categoryRadarData" 
                :options="radarChartOptions" 
               
              />
            </div>
          </div>
        </div>
      </div>
      </div>
      
      
      <!-- Skillset Widget Card -->
      <div class="col-span-12 md:col-span-8">
        
        <div class="card p-4">
          <h5 class="mb-4">Skillsets</h5>
          <div v-if="skillsetData.length === 0" class="text-gray-500 italic">
            No skillset assessments available
          </div>
          <div v-else class="flex flex-wrap gap-2 md:gap-4">
            
            <!-- Dynamic Categories -->
            <div v-for="(skills, category) in groupedSkills" :key="category" class="w-full md:w-[calc(33.333%-1rem)] min-w-[300px]">
              <fieldset class="border p-2 rounded h-full flex flex-col">
                <legend class="cursor-pointer" @click="toggleCategory(category)">
                  <div class="flex items-center gap-2">
                    <h6 class="font-semibold">{{ category }}</h6>
                    <div class="flex items-center gap-1">
                      <span class="text-sm font-medium">{{ calculateAverage(skills) }}</span>
                      <i class="pi pi-star-fill text-yellow-500"></i>
                      <i :class="`pi pi-chevron-${isCategoryOpen(category) ? 'up' : 'down'} text-sm ml-1`"></i>
                    </div>
                  </div>
                </legend>
                <transition name="fade">
                  <ul v-if="isCategoryOpen(category)" class="flex-1 overflow-y-auto">
                    <li v-for="skill in skills" :key="skill.skillsetName" class="grid grid-cols-[1fr_150px_26px] items-center gap-2 mb-1">
                      <span class="text-sm">{{ skill.skillsetName }}</span>
                      <div class="flex justify-end">
                        <Rating v-model="skill.skillsetRating" readonly :stars="5" 
                                v-tooltip="`Reviewed by: ${skill.reviewers.map(r => `${r.name} (${r.email})`).join('\n')}`" />
                      </div>
                      <div class="text-[10px] bg-gray-100 px-1.5 py-0.5 rounded-full border border-gray-200 text-center w-[26px]"
                           v-tooltip="`${skill.reviewCount} reviews`">
                        {{ skill.reviewCount }}
                      </div>
                    </li>
                  </ul>
                </transition>
              </fieldset>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Charts Section -->
      <transition name="fade">
        <div v-if="isAnyCategoryOpen" class="col-span-12">
          <div class="card p-4">
            <h5 class="mb-4">Candidate Analitics - {{ selectedCategory }}</h5>
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
              <!-- Radar Chart Widget -->
              <div class="card p-4">
                <h6 class="mb-2 font-semibold">Skillset Knowledge Distribution</h6>
                <Chart type="radar" :data="radarChartData" :options="radarChartOptions" />
              </div>
            </div>
          </div>
        </div>
      </transition>
      
      <!-- Updated Certifications Section -->
      <div class="col-span-12">
        <fieldset class="border p-2 rounded">
          <legend class="cursor-pointer" @click="isCertificationsExpanded = !isCertificationsExpanded">
            <div class="flex items-center gap-2 px-2">
              <h5 class="font-semibold">Certifications ({{ certificationsData.length }})</h5>
              <i :class="`pi pi-chevron-${isCertificationsExpanded ? 'up' : 'down'} text-sm`"></i>
            </div>
          </legend>
          <transition name="fade">
            <div v-if="isCertificationsExpanded" class="p-4">
              <div v-if="certificationsData.length === 0" class="text-gray-500 italic">
                No certifications recorded
              </div>
              <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                <div 
                  v-for="(certification, index) in certificationsData" 
                  :key="index" 
                  class="card p-4"
                  v-tooltip="`Expires: ${formatDate(certification.certificationExpiration)}`"
                >
                  <div class="flex justify-between items-center gap-2">
                    <div class="font-medium whitespace-normal break-words pr-2">
                      {{ certification.certificationName }}
                    </div>
                    <Tag 
                      :value="isCertificationActive(certification) ? 'active' : 'expired'"
                      :severity="isCertificationActive(certification) ? 'success' : 'danger'"
                      class="text-xs lowercase scale-90 origin-right shrink-0"
                    />
                  </div>
                  <div class="mt-2 text-sm text-gray-600">
                    <div>Issued by: {{ certification.companyName }}</div>
                    <div>Expires: {{ formatDate(certification.certificationExpiration) }}</div>
                  </div>
                </div>
              </div>
            </div>
          </transition>
        </fieldset>
      </div>
      
      <!-- Updated Candidate Reviews Section -->
      <div class="col-span-12">
        <fieldset class="border p-2 rounded">
          <legend class="cursor-pointer" @click="isReviewsExpanded = !isReviewsExpanded">
            <div class="flex items-center gap-2 px-2">
              <h5 class="font-semibold">Candidate Reviews ({{ interviewsData.length }})</h5>
              <i :class="`pi pi-chevron-${isReviewsExpanded ? 'up' : 'down'} text-sm`"></i>
            </div>
          </legend>
          <transition name="fade">
            <div v-if="isReviewsExpanded" class="p-4">
              <div v-if="interviewsData.length === 0" class="text-gray-500 italic">
                No reviews available
              </div>
              <div v-else class="grid grid-cols-1 gap-4">
                <div v-for="(reviews, field) in groupedReviews" :key="field" class="card p-4">
                  <h6 class="font-semibold mb-4">{{ field }}</h6>
                  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    <div v-for="(review, index) in reviews" :key="index" class="card p-4">
                      <div class="grid grid-cols-2 gap-2 text-sm">
                        <div class="font-medium">Rating:</div>
                        <div>
                          <Rating :modelValue="review.rating" readonly :stars="5" />
                        </div>
                        
                        <div class="font-medium">Interviewed By:</div>
                        <div>{{ review.interviewedBy }}</div>
                        
                        <div class="font-medium">Approval Status:</div>
                        <div :class="{
                          'text-green-500': review.approved === 'Yes',
                          'text-yellow-500': review.approved === 'Pending',
                          'text-red-500': review.approved === 'No'
                        }">
                          {{ review.approved }}
                        </div>
                        
                        <div class="font-medium">Date:</div>
                        <div>{{ formatDate(review.createdAt) }}</div>
                      </div>
                      
                      <div class="mt-4 text-sm">
                        <div class="font-medium mb-1">Observations:</div>
                        <p class="text-gray-600">{{ review.observations }}</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </transition>
        </fieldset>
      </div>

      <!-- Metadata Section -->
      <div class="col-span-12">
        <fieldset class="border p-2 rounded">
          <legend class="px-2">
            <h5 class="font-semibold">System Information</h5>
          </legend>
          <div class="p-4 grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
            <div class="flex items-center gap-2 text-gray-600">
              <i class="pi pi-id-card"></i>
              <span>Profile ID: <span class="font-mono text-primary-500">{{ candidateData.id }}</span></span>
            </div>
            <div class="flex items-center gap-2 text-gray-600">
              <i class="pi pi-database"></i>
              <span>Company ID: <span class="font-mono text-primary-500">{{ candidateData.companyId }}</span></span>
            </div>
          </div>
        </fieldset>
      </div>

      <!-- In the Charts Section -->
 </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import Chart from 'primevue/chart';
import Rating from 'primevue/rating';
import Avatar from 'primevue/avatar';
import Button from 'primevue/button';
import Tag from 'primevue/tag';

const route = useRoute();
const router = useRouter();
const loading = ref(true);

// Updated candidateData
const candidateData = ref({
    id: "",
    candidateName: "",  // Changed from 'name' to 'candidateName'
    companyId: "",
    companyName: "",
    email: "",
    country: "",
    role: "",
    phone: "",
    status: "active",
    createdAt: "",
    updatedAt: "",
    salaryExpectation: "",
    candidateCV: "",
    recruitmentProcessId: "",
    recruitmentProcessName: ""
});

// Update the computed properties with null checks
const candidateInitials = computed(() => {
  const name = candidateData.value.candidateName || '';
  const names = name.trim().split(' ');
  
  if (names.length >= 2) {
    return (names[0][0] + names[names.length-1][0]).toUpperCase();
  } else if (names[0]?.length > 0) {
    return names[0][0].toUpperCase();
  }
  return ''; // Return empty string if no name
});

const formattedName = computed(() => {
  const name = candidateData.value.candidateName || '';
  return name
    .split(' ')
    .map(word => word.charAt(0).toUpperCase() + (word.slice(1) || '').toLowerCase())
    .join(' ');
});

// Function to generate a random integer from 0 to 5
const randomRating = () => Math.floor(Math.random() * 6);

// Random ratings for each category
const windowsRatings = {
  'Windows Server': randomRating(),
  'Active Directory': randomRating(),
  'PowerShell': randomRating(),
  'Azure': randomRating(),
  'Office 365': randomRating()
};

const linuxRatings = {
  'Ubuntu': randomRating(),
  'CentOS': randomRating(),
  'RedHat': randomRating(),
  'Debian': randomRating(),
  'Fedora': randomRating()
};

const networkingRatings = {
  'TCP/IP': randomRating(),
  'DNS': randomRating(),
  'DHCP': randomRating(),
  'Routing': randomRating(),
  'Switching': randomRating()
};

// Updated aggregateRating to return a number instead of a string
const aggregateRating = (ratingsObj) => {
  const values = Object.values(ratingsObj);
  const sum = values.reduce((a, b) => a + b, 0);
  return parseFloat((sum / values.length).toFixed(1));
};

// Aggregated ratings for charts
const aggregatedWindowsRating = aggregateRating(windowsRatings);
const aggregatedLinuxRating = aggregateRating(linuxRatings);
const aggregatedNetworkingRating = aggregateRating(networkingRatings);

// Add reactive selected category
const selectedCategory = ref('Windows');

// Update the toggleCategory function to set the selected category
const toggleCategory = (category) => {
  selectedCategory.value = category;
  if (openCategories.value.has(category)) {
    openCategories.value.delete(category);
  } else {
    openCategories.value.add(category);
  }
};

// Update chart data computations to use selected category
const basicChartData = computed(() => {
  const skills = groupedSkills.value[selectedCategory.value] || [];
  return {
    labels: [selectedCategory.value],
    datasets: [{
      label: 'Average Skill Level',
      backgroundColor: ['rgba(249, 115, 22, 0.2)'],
      borderColor: ['rgb(249, 115, 22)'],
      borderWidth: 1,
      data: [calculateAverage(skills)]
    }]
  };
});

const pieChartData = computed(() => {
  const skills = groupedSkills.value[selectedCategory.value] || [];
  return {
    labels: skills.map(skill => skill.skillsetName),
    datasets: [{
      data: skills.map(skill => skill.skillsetRating),
      backgroundColor: [
        'rgba(66, 165, 245, 0.2)',    // #42A5F5 with 0.2 alpha
        'rgba(102, 187, 106, 0.2)',   // #66BB6A with 0.2 alpha
        'rgba(255, 167, 38, 0.2)',    // #FFA726 with 0.2 alpha
        'rgba(255, 99, 132, 0.2)',    // #FF6384 with 0.2 alpha
        'rgba(54, 162, 235, 0.2)',   // #36A2EB with 0.2 alpha
        'rgba(255, 206, 86, 0.2)'     // #FFCE56 with 0.2 alpha
      ],
      borderColor: [
        'rgb(66, 165, 245)',
        'rgb(102, 187, 106)',
        'rgb(255, 167, 38)',
        'rgb(255, 99, 132)',
        'rgb(54, 162, 235)',
        'rgb(255, 206, 86)'
      ],
      borderWidth: 1
    }]
  };
});

const verticalBarChartData = computed(() => {
  const skills = groupedSkills.value[selectedCategory.value] || [];
  return {
    labels: skills.map(skill => skill.skillsetName),
    datasets: [{
      label: 'Skill Ratings',
      backgroundColor: 'rgba(66, 165, 245, 0.2)',
      borderColor: 'rgb(66, 165, 245)',
      borderWidth: 1,
      data: skills.map(skill => skill.skillsetRating)
    }]
  };
});

const radarChartData = computed(() => {
  const skills = groupedSkills.value[selectedCategory.value] || [];
  return {
    labels: skills.map(skill => skill.skillsetName),
    datasets: [{
      label: 'Skill Ratings',
      data: skills.map(skill => skill.skillsetRating),
      backgroundColor: 'rgba(179,181,198,0.2)',
      borderColor: 'rgba(179,181,198,1)',
      borderWidth: 1
    }]
  };
});

// Added new radarChartOptions with a fixed max of 5
const radarChartOptions = ref({
  scales: {
    r: {
      min: 0,
      max: 5,
      ticks: {
        stepSize: 1,
        color: '#646464'
      }
    }
  },
  plugins: {
    legend: {
      labels: {
        color: '#646464'
      }
    }
  }
});

// Add date formatting function
const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
};

// Add formattedDate computed property
const formattedDate = computed(() => {
  return formatDate(candidateData.value.createdAt);
});

// Update formattedSalary
const formattedSalary = computed(() => {
  return candidateData.value.salaryExpectation 
    ? new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
      }).format(candidateData.value.salaryExpectation)
    : 'Not specified';
});

// Add approvedCounts computed property
const approvedCounts = computed(() => {
  return interviewsData.value.reduce((acc, review) => {
    const status = review.approved?.toLowerCase() || 'pending';
    acc[status] += 1;
    return acc;
  }, { yes: 0, pending: 0, no: 0 });
});

// Add reviewCandidate function
const reviewCandidate = () => {
  // Implement review logic
  console.log('Reviewing candidate...');
};

// Add scheduleInterview function
const scheduleInterview = () => {
  // Implement interview scheduling logic
  console.log('Scheduling interview...');
};

// Add contactCandidate function
const contactCandidate = () => {
  // Implement contact logic
  console.log('Contacting candidate...');
};

// Update skillsetData - remove candidateId from all entries
const skillsetData = ref([]);

// In script setup section, add the query and fetch logic
const GET_SKILLSETS_BY_EMAIL = `
  query GetSkillsetsByEmail($email: String!) {
    getSkillsetsByEmail(email: $email) {
      skillsetCategory
      skillsetName
      skillsetRating
      reviewedBy
      reviewerEmail
      companyId
      companyName
      email
      createdAt
    }
  }
`;

async function fetchSkillsets() {
  try {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/graphql`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query: GET_SKILLSETS_BY_EMAIL,
        variables: { email: candidateData.value.email }
      })
    });

    const result = await response.json();
    if (result.errors) {
      throw new Error(result.errors[0]?.message || 'Failed to load skillsets');
    }
    
    skillsetData.value = result.data.getSkillsetsByEmail || [];
  } catch (error) {
    console.error('Error fetching skillsets:', error);
    // You might want to add a toast notification here
  }
}

// Update the groupedSkills computed property to average duplicate skills
const groupedSkills = computed(() => {
  const skillsMap = new Map();
  
  // First pass to aggregate skills and calculate averages
  skillsetData.value.forEach(skill => {
    const key = `${skill.skillsetCategory}-${skill.skillsetName}`;
    if (!skillsMap.has(key)) {
      skillsMap.set(key, {
        ...skill,
        totalRating: skill.skillsetRating,
        reviewCount: 1,
        reviewers: [{
          name: skill.reviewedBy,
          email: skill.reviewerEmail
        }]
      });
    } else {
      const existing = skillsMap.get(key);
      existing.totalRating += skill.skillsetRating;
      existing.reviewCount++;
      existing.reviewers.push({
        name: skill.reviewedBy,
        email: skill.reviewerEmail
      });
    }
  });

  // Create averaged skills array
  const averagedSkills = Array.from(skillsMap.values()).map(skill => ({
    ...skill,
    skillsetRating: Math.round((skill.totalRating / skill.reviewCount) * 2) / 2, // Rounds to nearest 0.5
    reviewedBy: skill.reviewers.map(r => r.name).join(', '),
    reviewerEmail: skill.reviewers.map(r => r.email).join(', ')
  }));

  // Group averaged skills by category
  const groups = {};
  averagedSkills.forEach(skill => {
    if (!groups[skill.skillsetCategory]) {
      groups[skill.skillsetCategory] = [];
    }
    groups[skill.skillsetCategory].push(skill);
  });
  return groups;
});

// Calculate average rating for a category
const calculateAverage = (skills) => {
  const ratings = skills.map(skill => skill.skillsetRating);
  const sum = ratings.reduce((a, b) => a + b, 0);
  return (sum / ratings.length).toFixed(1);
};

// Function to get initials from a full name
const getInitials = (fullName) => {
  const names = fullName.split(' ');
  if (names.length >= 2) {
    return (names[0][0] + names[names.length - 1][0]).toUpperCase();
  }
  return names[0][0].toUpperCase();
};

// Add state for open/closed categories
const openCategories = ref(new Set());

// Check if category is open
const isCategoryOpen = (category) => openCategories.value.has(category);

// Add computed property to check if any category is open
const isAnyCategoryOpen = computed(() => openCategories.value.size > 0);

// Update chartOptions with dynamic colors
const chartOptions = computed(() => {
  const documentStyle = getComputedStyle(document.documentElement);
  const textColor = documentStyle.getPropertyValue('--p-text-color');
  const textColorSecondary = documentStyle.getPropertyValue('--p-text-muted-color');
  const surfaceBorder = documentStyle.getPropertyValue('--p-content-border-color');

  return {
    plugins: {
      legend: {
        labels: {
          color: textColor
        }
      }
    },
    scales: {
      x: {
        ticks: {
          color: textColorSecondary
        },
        grid: {
          color: surfaceBorder
        }
      },
      y: {
        beginAtZero: true,
        max: 5,
        ticks: {
          stepSize: 1,
          color: textColorSecondary
        },
        grid: {
          color: surfaceBorder
        }
      }
    }
  };
});

// Add interview query
const GET_INTERVIEWS = `
  query GetInterviewsByEmail($email: String!) {
    getInterviewsByEmail(email: $email) {
      id
      evaluationField
      rating
      interviewedBy
      interviewerEmail
      approved
      observations
      createdAt
    }
  }
`;

// Replace reviewsData with interviewsData
const interviewsData = ref([]);

// Add fetchInterviews function
async function fetchInterviews() {
  try {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/graphql`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query: GET_INTERVIEWS,
        variables: { email: candidateData.value.email }
      })
    });

    const result = await response.json();
    if (result.errors) {
      throw new Error(result.errors[0]?.message || 'Failed to load interviews');
    }
    
    interviewsData.value = result.data.getInterviewsByEmail || [];
  } catch (error) {
    console.error('Error fetching interviews:', error);
  }
}

// Update onMounted hook
onMounted(async () => {
  if (route.params.id) {
    await fetchCandidate();
    await Promise.all([
      fetchSkillsets(),
      fetchCertifications(),
      fetchInterviews()
    ]);
  }
});

// Update groupedReviews to use interviewsData
const groupedReviews = computed(() => {
  const groups = {};
  interviewsData.value.forEach(review => {
    const field = review.evaluationField;
    if (!groups[field]) {
      groups[field] = [];
    }
    groups[field].push(review);
  });
  return groups;
});

// Update allSkillsAverage to handle empty skillset
const allSkillsAverage = computed(() => {
  if(skillsetData.value.length === 0) return 'N/A';
  const total = skillsetData.value.reduce((acc, skill) => acc + skill.skillsetRating, 0);
  return (total / skillsetData.value.length).toFixed(1);
});

// Add to the script section
const isReviewsExpanded = ref(false);

// Add to the script section
const certificationsData = ref([]);

// Update the GET_CERTIFICATIONS query to match the schema
const GET_CERTIFICATIONS = `
  query GetAssignedCertificationsByEmail($email: String!) {
    getAssignedCertificationsByEmail(email: $email) {
      companyId
      companyName
      email
      certificationName
      certificationExpiration
      createdAt
      updatedAt
    }
  }
`;

// Add fetchCertifications function
async function fetchCertifications() {
  try {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/graphql`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query: GET_CERTIFICATIONS,
        variables: { email: candidateData.value.email }
      })
    });

    const result = await response.json();
    if (result.errors) {
      throw new Error(result.errors[0]?.message || 'Failed to load certifications');
    }
    
    certificationsData.value = result.data.getAssignedCertificationsByEmail || [];
  } catch (error) {
    console.error('Error fetching certifications:', error);
    // Add error handling/toast notification if needed
  }
}

// Update isCertificationActive to use the new data structure
const isCertificationActive = (certification) => {
  const expirationDate = new Date(certification.certificationExpiration);
  return expirationDate > new Date();
};

// Update the GET_CANDIDATE query with all requested fields
const GET_CANDIDATE = `
  query GetCandidate($id: String!) {
    candidate(id: $id) {
      id
      candidateCV
      salaryExpectation
      recruitmentProcessId
      phone
      candidateName
      companyId
      companyName
      country
      createdAt
      email
      recruitmentProcessName
      updatedAt
      status
    }
  }
`;

// Simplified fetch candidate function
async function fetchCandidate() {
  try {
    loading.value = true;
    const response = await fetch(`${import.meta.env.VITE_API_URL}/graphql`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query: GET_CANDIDATE,
        variables: { id: route.params.id } // Directly use route param
      })
    });

    const result = await response.json();
    if (result.errors) {
      throw new Error(result.errors[0]?.message || 'Failed to load candidate');
    }

    candidateData.value = {
      ...candidateData.value, // Keep existing dummy data as fallback
      ...result.data.candidate // Override with actual data
    };
  } catch (error) {
    console.error('Error fetching candidate:', error);
  } finally {
    loading.value = false;
  }
}

// Watch for route changes - simplified version
watch(() => route.params.id, async (newId) => {
  if (newId) {
    await fetchCandidate();
  }
});

// Add new computed property for category averages
const categoryAverages = computed(() => {
  return Object.entries(groupedSkills.value).map(([category, skills]) => ({
    category,
    average: calculateAverage(skills)
  }));
});

// Add new radar chart data for category averages
const categoryRadarData = computed(() => {
  return {
    labels: categoryAverages.value.map(item => item.category),
    datasets: [{
      label: 'Skillser Radar',
      data: categoryAverages.value.map(item => item.average),
      backgroundColor: 'rgba(54, 162, 235, 0.2)',
      borderColor: 'rgba(54, 162, 235, 1)',
      borderWidth: 1
    }]
  };
});

// Add to the script section
const isCertificationsExpanded = ref(false);
</script>

<style scoped>
.card {
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  background-color: #fff;
  border-radius: 4px;
}

/* Add transition for smooth collapse/expand */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease, max-height 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  max-height: 0;
}

fieldset {
  border: 1px solid #e5e7eb;
  border-radius: 0.375rem;
  min-height: 100%;
  display: flex;
  flex-direction: column;
}

legend {
  padding: 0 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
}

legend:hover {
  background-color: #f3f4f6;
}

ul {
  max-height: 300px; /* Adjust this value based on your needs */
  overflow-y: auto;
}

:deep(.p-tooltip) {
  z-index: 50;
  background: var(--p-surface-overlay);
  color: var(--p-text-color);
  padding: 0.5rem 1rem;
  border-radius: 6px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  border: 1px solid var(--p-surface-border);
}

:deep(.p-tooltip-text) {
  font-size: 0.875rem;
  line-height: 1.25rem;
}
</style> 