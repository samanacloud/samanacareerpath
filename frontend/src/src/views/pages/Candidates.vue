<script setup>
import { ref, onBeforeMount, computed } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

// Function to get the base URL
const baseURL = import.meta.env.VITE_SITE_URL 
    ? `https://${import.meta.env.VITE_SITE_URL}` // Use https if VITE_SITE_URL is defined
    : 'http://localhost:8080'; // Use localhost for development

//redirects to unauthorized if the user role is lower than the pagerole
import { getPageAuthorization } from '@/utils/utils';
const pageRole = 2; // Set the required role for this page
getPageAuthorization(pageRole);

    

const candidatesList = ref([]);
const apiResponse = ref('');
const searchName = ref(''); // reactive variable to store search input

const selectedCandidate = ref(null);
const candidateSkillsets = ref([]);
const candidateReviews = ref([]);
const detailedViewActive = ref(false);
const idFrozen = ref(false); // Add this line for dynamic toggling

const router = useRouter();

const filteredCandidatesList = computed(() => {
  if (!searchName.value) return candidatesList.value;
  const searchTerm = searchName.value.toLowerCase();
  return candidatesList.value.filter(candidate =>
    candidate.name.toLowerCase().includes(searchTerm)
  );
});

const listCandidateProfiles = async () => {
    try {
        const response = await axios.post(`${baseURL}/api/apitest.php`, {
            action: 'listCandidateProfiles'
        });
        candidatesList.value = response.data;
        apiResponse.value = 'Candidates listed successfully';
    } catch (error) {
        apiResponse.value = 'Error: ' + error.message;
    }
};

const viewProfileDetails = (email) => {
    sessionStorage.setItem('candidateEmail', email);
    router.push('/candidatesreviews');
};

const viewProfileDetailstest = (email) => {
    sessionStorage.setItem('candidateEmail', email);
    router.push('tcandidatesreviews');
};

// Placeholder for the default image path
const defaultProfileImage = ref(null);

// Load the default profile image path (e.g., from environmental variables)
onBeforeMount(async () => {
    try {
        const response = await axios.post(`${baseURL}/api/apitest.php`, {
            action: 'getDefaultProfileImage'
        });
        defaultProfileImage.value = response.data; 
        // Ensure defaultProfileImage is set correctly
        if (!defaultProfileImage.value) { 
            defaultProfileImage.value = 'path/to/your/default/user-icon.png'; // Set a fallback
        }
    } catch (error) {
        console.error('Error fetching default profile image:', error.message);
        // Set a fallback if fetching fails
        defaultProfileImage.value = 'path/to/your/default/user-icon.png';
    }
});

onBeforeMount(() => {
    listCandidateProfiles();
});
</script>

<template>
    <div class="grid">
        <div class="col-12">
            <div class="card">
                <h5>Candidates Dashboard</h5>
                <div class="flex justify-content-between flex-column sm:flex-row">
                    <h6>Search by Name</h6>
                    <InputText type="text" v-model="searchName" placeholder="Search by name" class="p-inputtext-sm" />
                </div>
                <DataTable :value="filteredCandidatesList" paginator :rows="10" dataKey="id" rowHover :scrollable="true" scrollHeight="70vh" scrollDirection="vertical">
                    <Column field="profile_photo" header="Profile Photo" bodyStyle="text-align: center" frozen alignFrozen="left">
                        <template #body="{ data }">
                            <i v-if="!data.profile_photo || data.profile_photo === '0'" class="pi pi-user profile-photo"></i>
                            <img v-else :src="data.profile_photo" alt="Profile Photo" class="profile-photo" />
                        </template>
                    </Column>
                    <Column field="name" header="Name & Email" sortable frozen alignFrozen="left">
                        <template #body="{ data }">
                            <div>
                                <strong class="name">{{ data.name }}</strong>
                                <div class="email">{{ data.email }}</div>
                            </div>
                        </template>
                    </Column>
                    <Column field="location" header="Location" sortable></Column>
                    <Column field="created_at" header="Application Date" sortable>
                        <template #body="{ data }">{{ new Date(data.created_at).toLocaleDateString() }}</template>
                    </Column>
                    <Column header="Profile Details" bodyStyle="text-align: center" frozen alignFrozen="right">
                        <template #body="{ data }">
                            <Button icon="pi pi-search" text raised outlined severity="success" @click="viewProfileDetails(data.email)" />

                        </template>
                    </Column>
                </DataTable>
            </div>
        </div>
    </div>


</template>

<style scoped lang="scss">
.profile-photo {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    object-fit: cover;
}

.name {
    font-weight: bold;
}

.email {
    font-size: 0.9rem;
    color: #6c757d;
}

// Media query for smaller screens (adjust breakpoint as needed)
@media (max-width: 768px) { 
    .email {
        font-size: 0.8rem;  // Reduce font size for mobile
    }
}
</style>