<script setup>
import { useLayout } from '@/layout/composables/layout';
import { ref, computed, onMounted, onBeforeMount } from 'vue';
import { CountryService } from '@/service/CountryService';
import { useRouter } from 'vue-router';
import Toolbar from 'primevue/toolbar';
import Card from 'primevue/card';
import Button from 'primevue/button';
import Dropdown from 'primevue/dropdown';
import InputText from 'primevue/inputtext';
import axios from 'axios';
const { layoutConfig } = useLayout();
const router = useRouter(); 
const isLoggedIn = ref(false);

const countryService = new CountryService();
const countries = ref([





]);










const selectedCountry = ref(null);
const jobs = ref([]); // Add this line
const apiResponse = ref(''); // Add this line
const logoUrl = 'samana-logo-white.png';

// Initialize form fields with cookies
const newCandidate = ref({
    name: document.cookie.replace(/(?:(?:^|.*;\s*)CandidateName\s*\=\s*([^;]*).*$)|^.*$/, "$1"),
    email: document.cookie.replace(/(?:(?:^|.*;\s*)CandidateEmail\s*\=\s*([^;]*).*$)|^.*$/, "$1"),
    profile_photo: document.cookie.replace(/(?:(?:^|.*;\s*)ProfileImage\s*\=\s*([^;]*).*$)|^.*$/, "$1"),
    phone_number: '',
    location: '',
    english_level: '',
    candidate_cv: ''
});

const submitProfile = async () => {
    try {
        const response = await axios.post(`/api/apireg`, {
            action: 'addCandidate',
            ...newCandidate.value
        });

        if (response.data && !response.data.error) {
            candidate.value = response.data; // Update candidate with the new data
        } else {
            console.error('Error saving profile:', response.data.error);
        }
    } catch (error) {
        console.error('Error saving profile:', error);
    }
};

const checkLoginStatus = () => {
    const authToken = document.cookie.split('; ').find(row => row.startsWith('CandidateToken='));
    isLoggedIn.value = !!authToken;
};


const logout = () => {
    // Clear cookies or perform logout logic here
    router.push('/auth/logoutcandidate');
};

// Fetch Job Postings
const listJobPostings = async () => {
  try {
    const response = await axios.post(`/api/apireg`, {
      action: 'listAvailableJobs'
    });
    jobs.value = Array.isArray(response.data) ? response.data : [response.data];
    apiResponse.value = 'Jobs listed successfully';
  } catch (error) {
    apiResponse.value = 'Error: ' + error.message;
  }
};

const candidate = ref(null);

const getCandidate = async (email) => {
    try {
        const response = await axios.post(`/api/apireg`, {
            action: 'getCandidate',
            email: email
        });

        if (response.data && !response.data.error) {
            candidate.value = response.data;
        } else {
            candidate.value = null;
        }
    } catch (error) {
        candidate.value = null;
        console.error('Error fetching candidate:', error);
    }
};

onMounted(() => {
    countryService.getCountries().then(data => countries.value = data);

    checkLoginStatus();
    const candidateEmail = document.cookie.split('; ').find(row => row.startsWith('CandidateEmail=')).split('=')[1];
    if (candidateEmail) {
        getCandidate(candidateEmail);
    }

});
// Lifecycle Hook
onBeforeMount(listJobPostings);
</script>

<template>
    <div class="toolbar-wrapper">
        <Toolbar style="background-color: #133563;">
            <template #start>
                <img alt="logo" :src="logoUrl" height="40" />
            </template>
            <template #center>
                <div class="center-content">
                    <h4>Samana CareerPath</h4>
                </div>
            </template>
            <template #end>
                <Button 
                    v-if="isLoggedIn" 
                    label="Log out" 
                    severity="danger" 
                    class="mb-2 mr-2"
                    @click="logout"
                ></Button>
                <Button 
                    v-else 
                    label="Sign In" 
                    class="w-full" 
                    @click="router.push('/auth/register')"
                ></Button>
            </template>
        </Toolbar>
    </div>
   <div class="grid ">
    <div class="col-12">
      <div class="card"> 


        <div class="intro-section ">
            <br><br>
            <h3>Welcome to the Samana CareerPath Jobs Portal</h3>
            <p>
                Discover the best job opportunities that match your skills and career aspirations. Our portal connects you with top employers looking for your talent.
            </p>
        </div>
        <div class="grid">
            <div class="col-12 lg:col-12">
                 <div class="card candidate-details">
  
                    <h5>Candidate Profile</h5>
                    <div v-if="candidate">
                        <p><strong>Name:</strong> {{ candidate.name }}</p>
                        <p><strong>Email:</strong> {{ candidate.email }}</p>
                        <p><strong>Phone Number:</strong> {{ candidate.phone_number }}</p>
                        <p><strong>Location:</strong> {{ candidate.location }}</p>
                        <p><strong>English Level:</strong> {{ candidate.english_level }}</p>
                        <p><strong>Profile Photo:</strong> <img :src="candidate.profile_photo" alt="Profile Photo" height="100" /></p>
                        <p><strong>Candidate CV:</strong> <a :href="candidate.candidate_cv" target="_blank">View CV</a></p>
                    </div>
                    <div v-else class="card p-fluid col-12 md:col-6 lg:col-4">
                        <form @submit.prevent="submitProfile">
                    <div class="formgrid grid">
                        <div class="field col-12 md:col-6">
                            <label for="name">Name</label>
                            <InputText v-model="newCandidate.name" id="name" type="text" />
                        </div>
                        <div class="field col-12 md:col-6">
                            <label for="email">Email</label>
                            <InputText v-model="newCandidate.email" id="email" type="email" disabled />
                        </div>
                        <div class="field col-12 md:col-6">
                            <label for="phone_number">Phone Number</label>
                            <InputText v-model="newCandidate.phone_number" id="phone_number" type="text" placeholder="+(Country Code) Number"/>
                        </div>
                        <div class="field col-12 md:col-6">
                            <label for="location">Location</label>
                            <Dropdown 
                                    id="location" 
                                    v-model="newCandidate.location" 
                                    :options="countries" 
                                    optionLabel="name" 
                                    filter 
                                    placeholder="Select Country" 
                                />
                        </div>
                        <div class="field col-12 md:col-4">
                            <label for="english_level">English Level</label>
                            <Dropdown id="english_level" v-model="newCandidate.english_level" :options="['A1', 'B1', 'B2', 'C1', 'C2']" placeholder="Select English Level"/>
                        </div>
                        <div class="field col-12 md:col-6">
                            <label for="profile_photo">Profile Photo URL</label>
                            <InputText v-model="newCandidate.profile_photo" id="profile_photo" type="text" />
                        </div>
                        <div class="field col-12 md:col-6">
                            <label for="candidate_cv">Candidate CV URL</label>
                            <InputText v-model="newCandidate.candidate_cv" id="candidate_cv" type="text" />
                        </div>
                    </div>
                    <Button label="Save Profile" type="submit" class="mt-2" />
                </form>                    </div>
                </div>
            </div>
        </div>

        <div class="grid">
            <div class="col-12 lg:col-12 ">
             
  
                    <h5>Available job opportunities</h5>
                    <div class="layout-content flex-container">
               
                        <div v-for="job in jobs" :key="job.id" class="col-12 lg:col-4 ">
                            <Card>
                                <template #header>
                                    <img alt="header image" :src="logoUrl" />
                                </template>
                                <template #title>{{ job.job_title }}</template>
                                <template #subtitle>{{ job.job_category }}</template>
                                <template #content>
                                    <p class="m-0">{{ job.job_details }}</p>
                                </template>
                                <template #footer>
                                    <div class="flex gap-4 mt-1">
                                        <Button label="Details" severity="secondary" outlined class="w-full" />
                                        <Button label="Apply Now" class="w-full" :href="job.linkedin_url" target="_blank" />
                                    </div>
                                </template>
                            </Card>
                        </div>
                    </div>
                
            </div>
        </div>



</div></div></div>
<div class="layout-footer">
            <img :src="logoUrl" alt="Logo" height="20" class="mr-2" />
            by
            <span class="font-medium ml-2">Samana Group LLC</span>
            , All Rights Reserved
        </div>
</template>

<style lang="scss" scoped>



.layout-content {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    gap: 0.1rem;
}

.toolbar-wrapper {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 1000; /* Make sure it stays above other content */
    background-color:  #133563; /* Ensure it has a solid background */
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); /* Optional: Adds a shadow for depth */
    padding: 0; /* Remove any extra padding/margin if necessary */
}

/* Add top padding to the content to avoid being covered by the toolbar */
body {
    padding-top: 80px; /* Adjust according to the height of your Toolbar */
}

.layout-footer {
    background-color: #e0f2ff;
    text-align: center;
    width: 100%;
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 1rem; /* Increase padding to make the footer higher */
    box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.1); /* Optional: Adds a shadow to give it some depth */
}

.intro-section {
    padding: 2rem 1rem;
    text-align: center;
}


.center-content h4 {
    margin: 0; /* Remove default margins */
    color: white;
}


</style>