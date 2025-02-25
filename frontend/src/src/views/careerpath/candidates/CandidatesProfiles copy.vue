<template>
  <div class="p-4">
    <div class="grid grid-cols-12 gap-4">
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
                <span>{{ reviewsData.length }}</span>
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
            
            <p class="text-sm text-gray-600">Applied Position: {{ candidateData.role }}</p>
            
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
                        <Rating v-model="skill.skillsetRating" readonly :stars="5" v-tooltip="`Reviewed by: ${skill.reviewedBy} (${skill.reviewerEmail})`" />
                      </div>
                      <div class="text-[10px] bg-gray-100 px-1.5 py-0.5 rounded-full border border-gray-200 text-center w-[26px]">
                        {{ getInitials(skill.reviewedBy) }}
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
            <h5 class="mb-4">Skillset Charts - {{ selectedCategory }}</h5>
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
          <legend class="cursor-pointer">
            <div class="flex items-center gap-2 px-2">
              <h5 class="font-semibold">Certifications</h5>
            </div>
          </legend>
          <div class="p-4">
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
              </div>
            </div>
          </div>
        </fieldset>
      </div>
      
      <!-- Candidate Reviews -->
      <div class="col-span-12">
        <fieldset class="border p-2 rounded">
          <legend class="cursor-pointer" @click="isReviewsExpanded = !isReviewsExpanded">
            <div class="flex items-center gap-2 px-2">
              <h5 class="font-semibold">Candidate Reviews</h5>
              <i :class="`pi pi-chevron-${isReviewsExpanded ? 'up' : 'down'} text-sm`"></i>
            </div>
          </legend>
          <transition name="fade">
            <div v-if="isReviewsExpanded" class="p-4">
              <div v-if="reviewsData.length === 0" class="text-gray-500 italic">
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
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import Chart from 'primevue/chart';
import Rating from 'primevue/rating';
import Avatar from 'primevue/avatar';
import Button from 'primevue/button';
import Tag from 'primevue/tag';

// Updated candidateData
const candidateData = ref({
    "id": "67bb1df37635d2ae25dd8df2",
    "companyId": "6792df37ae32f695bcd13420",
    "companyName": "Samana Group LLC",
    "name": "Juan Jose Romero Porto",
    "email": "josearielromeroarias@gmail.com",
    "country": "Colombia",
    "role": "Service Desk Engineer L2 Q1-2025",
    "phone": "+5703043909770",
    "status": "active",
    "createdAt": "2025-02-22T14:53:04.612Z",
    "updatedAt": "2025-02-22T14:53:04.612Z",
    "salaryExpectation": "1000",
    "candidateCV": "https://drive.google.com/open?id=1EnJ4eNCry1pHTFEobjyOdfq6M5apv47f"
});

// Compute candidate initials for Avatar from candidateName
const candidateInitials = computed(() => {
  const names = candidateData.value.name.trim().split(' ');
  if (names.length >= 2) {
    return (names[0][0] + names[names.length-1][0]).toUpperCase();
  } else {
    return names[0][0].toUpperCase();
  }
});

// Add this new computed property to format the name
const formattedName = computed(() => {
  return candidateData.value.name
    .split(' ')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
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
  return reviewsData.value.reduce((acc, review) => {
    acc[review.approved.toLowerCase()] += 1
    return acc
  }, { yes: 0, pending: 0, no: 0 })
})

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
const skillsetData = ref([
  {
    companyId: "6792df37ae32f695bcd13420",
    companyName: "Samana Group LLC",
    email: "josearielromeroarias@gmail.com",
    skillsetCategory: "Windows",
    skillsetName: "Windows Server",
    skillsetRating: Math.floor(Math.random() * 6),
    reviewedBy: "Juan Pablo Otalvaro",
    reviewerEmail: "juan.otalvaro@test.com"
  },
  {
    companyId: "6792df37ae32f695bcd13420",
    companyName: "Samana Group LLC",
    email: "josearielromeroarias@gmail.com",
    skillsetCategory: "Windows",
    skillsetName: "Active Directory",
    skillsetRating: Math.floor(Math.random() * 6),
    reviewedBy: "Juan Pablo Otalvaro",
    reviewerEmail: "juan.otalvaro@test.com"
  },
  {
    companyId: "6792df37ae32f695bcd13420",
    companyName: "Samana Group LLC",
    email: "josearielromeroarias@gmail.com",
    skillsetCategory: "Windows",
    skillsetName: "PowerShell",
    skillsetRating: Math.floor(Math.random() * 6),
    reviewedBy: "Maria Gonzalez",
    reviewerEmail: "maria.gonzalez@test.com"
  },
  {
    companyId: "6792df37ae32f695bcd13420",
    companyName: "Samana Group LLC",
    email: "josearielromeroarias@gmail.com",
    skillsetCategory: "Windows",
    skillsetName: "Azure",
    skillsetRating: Math.floor(Math.random() * 6),
    reviewedBy: "Carlos Martinez",
    reviewerEmail: "carlos.martinez@test.com"
  },
  {
    companyId: "6792df37ae32f695bcd13420",
    companyName: "Samana Group LLC",
    email: "josearielromeroarias@gmail.com",
    skillsetCategory: "Windows",
    skillsetName: "Office 365",
    skillsetRating: Math.floor(Math.random() * 6),
    reviewedBy: "Ana Rodriguez",
    reviewerEmail: "ana.rodriguez@test.com"
  },
  {
    companyId: "6792df37ae32f695bcd13420",
    companyName: "Samana Group LLC",
    email: "josearielromeroarias@gmail.com",
    skillsetCategory: "Windows",
    skillsetName: "Group Policy",
    skillsetRating: Math.floor(Math.random() * 6),
    reviewedBy: "Luis Fernandez",
    reviewerEmail: "luis.fernandez@test.com"
  },

  // Linux skills
  {
    companyId: "6792df37ae32f695bcd13420",
    companyName: "Samana Group LLC",
    email: "josearielromeroarias@gmail.com",
    skillsetCategory: "Linux",
    skillsetName: "Ubuntu",
    skillsetRating: Math.floor(Math.random() * 6),
    reviewedBy: "Maria Gonzalez",
    reviewerEmail: "maria.gonzalez@test.com"
  },
  {
    companyId: "6792df37ae32f695bcd13420",
    companyName: "Samana Group LLC",
    email: "josearielromeroarias@gmail.com",
    skillsetCategory: "Linux",
    skillsetName: "CentOS",
    skillsetRating: Math.floor(Math.random() * 6),
    reviewedBy: "Carlos Martinez",
    reviewerEmail: "carlos.martinez@test.com"
  },
  {
    companyId: "6792df37ae32f695bcd13420",
    companyName: "Samana Group LLC",
    email: "josearielromeroarias@gmail.com",
    skillsetCategory: "Linux",
    skillsetName: "RedHat",
    skillsetRating: Math.floor(Math.random() * 6),
    reviewedBy: "Ana Rodriguez",
    reviewerEmail: "ana.rodriguez@test.com"
  },
  {
    companyId: "6792df37ae32f695bcd13420",
    companyName: "Samana Group LLC",
    email: "josearielromeroarias@gmail.com",
    skillsetCategory: "Linux",
    skillsetName: "Debian",
    skillsetRating: Math.floor(Math.random() * 6),
    reviewedBy: "Luis Fernandez",
    reviewerEmail: "luis.fernandez@test.com"
  },
  {
    companyId: "6792df37ae32f695bcd13420",
    companyName: "Samana Group LLC",
    email: "josearielromeroarias@gmail.com",
    skillsetCategory: "Linux",
    skillsetName: "Fedora",
    skillsetRating: Math.floor(Math.random() * 6),
    reviewedBy: "Sofia Ramirez",
    reviewerEmail: "sofia.ramirez@test.com"
  },
  {
    companyId: "6792df37ae32f695bcd13420",
    companyName: "Samana Group LLC",
    email: "josearielromeroarias@gmail.com",
    skillsetCategory: "Linux",
    skillsetName: "Bash Scripting",
    skillsetRating: Math.floor(Math.random() * 6),
    reviewedBy: "Diego Morales",
    reviewerEmail: "diego.morales@test.com"
  },

  // Networking skills
  {
    companyId: "6792df37ae32f695bcd13420",
    companyName: "Samana Group LLC",
    email: "josearielromeroarias@gmail.com",
    skillsetCategory: "Networking",
    skillsetName: "TCP/IP",
    skillsetRating: Math.floor(Math.random() * 6),
    reviewedBy: "Carlos Martinez",
    reviewerEmail: "carlos.martinez@test.com"
  },
  {
    companyId: "6792df37ae32f695bcd13420",
    companyName: "Samana Group LLC",
    email: "josearielromeroarias@gmail.com",
    skillsetCategory: "Networking",
    skillsetName: "DNS",
    skillsetRating: Math.floor(Math.random() * 6),
    reviewedBy: "Ana Rodriguez",
    reviewerEmail: "ana.rodriguez@test.com"
  },
  {
    companyId: "6792df37ae32f695bcd13420",
    companyName: "Samana Group LLC",
    email: "josearielromeroarias@gmail.com",
    skillsetCategory: "Networking",
    skillsetName: "DHCP",
    skillsetRating: Math.floor(Math.random() * 6),
    reviewedBy: "Luis Fernandez",
    reviewerEmail: "luis.fernandez@test.com"
  },
  {
    companyId: "6792df37ae32f695bcd13420",
    companyName: "Samana Group LLC",
    email: "josearielromeroarias@gmail.com",
    skillsetCategory: "Networking",
    skillsetName: "Routing",
    skillsetRating: Math.floor(Math.random() * 6),
    reviewedBy: "Sofia Ramirez",
    reviewerEmail: "sofia.ramirez@test.com"
  },
  {
    companyId: "6792df37ae32f695bcd13420",
    companyName: "Samana Group LLC",
    email: "josearielromeroarias@gmail.com",
    skillsetCategory: "Networking",
    skillsetName: "Switching",
    skillsetRating: Math.floor(Math.random() * 6),
    reviewedBy: "Diego Morales",
    reviewerEmail: "diego.morales@test.com"
  },
  {
    companyId: "6792df37ae32f695bcd13420",
    companyName: "Samana Group LLC",
    email: "josearielromeroarias@gmail.com",
    skillsetCategory: "Networking",
    skillsetName: "Firewalls",
    skillsetRating: Math.floor(Math.random() * 6),
    reviewedBy: "Camila Vargas",
    reviewerEmail: "camila.vargas@test.com"
  }
]);

// Group skills by category
const groupedSkills = computed(() => {
  const groups = {};
  skillsetData.value.forEach(skill => {
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

// Update reviewsData - remove candidateId from all entries
const reviewsData = ref([
  {
    companyId: "6792df37ae32f695bcd13420",
    companyName: "Samana Group LLC",
    email: "josearielromeroarias@gmail.com",
    recruitmentProcessId: "67b9f0627635d2ae25dd8ce4",
    availability: "Immediate",
    evaluationfield: "Technical Knowledge",
    rating: 4,
    observations: "Demonstrated strong understanding of Windows Server environments and PowerShell scripting.",
    interviewedBy: "Juan Pablo Otalvaro",
    interviewerEmail: "juan.otalvaro@test.com",
    approved: "Yes",
    createdAt: "2025-03-01T09:00:00.000Z"
  },
  {
    companyId: "6792df37ae32f695bcd13420",
    companyName: "Samana Group LLC",
    email: "josearielromeroarias@gmail.com",
    recruitmentProcessId: "67b9f0627635d2ae25dd8ce4",
    availability: "1 Week Notice",
    evaluationfield: "Cultural Fit",
    rating: 4,
    observations: "Aligned well with company values and team dynamics during group exercise.",
    interviewedBy: "Sofia Ramirez",
    interviewerEmail: "sofia.ramirez@test.com",
    approved: "Pending",
    createdAt: "2025-02-28T15:30:00.000Z"
  },
  {
    companyId: "6792df37ae32f695bcd13420",
    companyName: "Samana Group LLC",
    email: "josearielromeroarias@gmail.com",
    recruitmentProcessId: "67b9f0627635d2ae25dd8ce4",
    availability: "3 Weeks Notice",
    evaluationfield: "Cultural Fit",
    rating: 3,
    observations: "Produced clear documentation for complex technical processes.",
    interviewedBy: "Diego Morales",
    interviewerEmail: "diego.morales@test.com",
    approved: "Yes",
    createdAt: "2025-02-27T16:45:00.000Z"
  },
  {
    companyId: "6792df37ae32f695bcd13420",
    companyName: "Samana Group LLC",
    email: "josearielromeroarias@gmail.com",
    recruitmentProcessId: "67b9f0627635d2ae25dd8ce4",
    availability: "Immediate",
    evaluationfield: "Time Management",
    rating: 2,
    observations: "Struggled with prioritizing tasks during timed exercise.",
    interviewedBy: "Camila Vargas",
    interviewerEmail: "camila.vargas@test.com",
    approved: "No",
    createdAt: "2025-02-26T10:20:00.000Z"
  },
  {
    companyId: "6792df37ae32f695bcd13420",
    companyName: "Samana Group LLC",
    email: "josearielromeroarias@gmail.com",
    recruitmentProcessId: "67b9f0627635d2ae25dd8ce4",
    availability: "2 Weeks Notice",
    evaluationfield: "Problem Solving",
    rating: 3,
    observations: "Showed excellent troubleshooting skills in simulated network outage scenario.",
    interviewedBy: "Maria Gonzalez",
    interviewerEmail: "maria.gonzalez@test.com",
    approved: "Pending",
    createdAt: "2025-02-25T14:15:00.000Z"
  },
  {
    companyId: "6792df37ae32f695bcd13420",
    companyName: "Samana Group LLC",
    email: "josearielromeroarias@gmail.com",
    recruitmentProcessId: "67b9f0627635d2ae25dd8ce4",
    availability: "Immediate",
    evaluationfield: "Cloud Infrastructure",
    rating: 5,
    observations: "Expert-level knowledge in Azure cloud management and deployment.",
    interviewedBy: "Luis Fernandez",
    interviewerEmail: "luis.fernandez@test.com",
    approved: "Yes",
    createdAt: "2025-02-24T11:10:00.000Z"
  },
  {
    companyId: "6792df37ae32f695bcd13420",
    companyName: "Samana Group LLC",
    email: "josearielromeroarias@gmail.com",
    recruitmentProcessId: "67b9f0627635d2ae25dd8ce4",
    availability: "Immediate",
    evaluationfield: "Communication Skills",
    rating: 5,
    observations: "Clear and concise communication during technical explanation exercises.",
    interviewedBy: "Carlos Martinez",
    interviewerEmail: "carlos.martinez@test.com",
    approved: "No",
    createdAt: "2025-02-23T09:30:00.000Z"
  }
]);

// Add the sortedReviews computed property before groupedReviews
const sortedReviews = computed(() => {
  return [...reviewsData.value].sort((a, b) => {
    return new Date(b.createdAt) - new Date(a.createdAt);
  });
});

// Then define groupedReviews
const groupedReviews = computed(() => {
  const groups = {};
  sortedReviews.value.forEach(review => {
    const field = review.evaluationfield;
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
const certificationsData = ref([
  {
    companyId: "6792df37ae32f695bcd13420",
    companyName: "Samana Group LLC",
    email: "josearielromeroarias@gmail.com",
    certificationName: "Microsoft Certified: Azure Administrator Associate",
    certificationExpiration: "2026-03-15T00:00:00.000Z"
  },
  {
    companyId: "6792df37ae32f695bcd13420",
    companyName: "Samana Group LLC",
    email: "josearielromeroarias@gmail.com",
    certificationName: "CompTIA Security+",
    certificationExpiration: "2025-12-31T00:00:00.000Z"
  },
  {
    companyId: "6792df37ae32f695bcd13420",
    companyName: "Samana Group LLC",
    email: "josearielromeroarias@gmail.com",
    certificationName: "Cisco CCNA",
    certificationExpiration: "2024-09-01T00:00:00.000Z"
  }
]);

// Add this computed property to the script section
const isCertificationActive = (certification) => {
  const expirationDate = new Date(certification.certificationExpiration);
  return expirationDate > new Date();
};

onMounted(() => {
  // Dummy data is already set up for demonstration
});
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