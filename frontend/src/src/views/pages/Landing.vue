<script setup>
import { ref, onMounted } from 'vue';
import AppFooter from '../../layout/AppFooter.vue';
import AppTopbar from '../../layout/AppTopbarCandidate.vue';
import { useToast } from 'primevue/usetoast';
import { useLayout } from '@/layout/composables/layout';
import { computed } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

import axios from 'axios';
const toast = useToast();

const { layoutConfig } = useLayout();

const jobs = ref([]); 
const selectedJob = ref(null); // To store the details of the selected job
const showJobDetails = ref(false); // To toggle between job list and job details view
// Fetch the CandidateEmail cookie at the beginning
const candidateEmail = ref(null);
if (typeof document !== 'undefined') {
    const emailCookie = document.cookie.split('; ').find(row => row.startsWith('CandidateEmail='));
    if (emailCookie) {
        candidateEmail.value = emailCookie.split('=')[1];
    }
}

// Fetch Job Postings
const listJobPostings = async () => {
  try {
    const response = await axios.post(`/api/apireg`, {
       action: 'listJobPostings'
    //   action: 'listAvailableJobs'
    });
    jobs.value = Array.isArray(response.data) ? response.data : [response.data];
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to load job postings', life: 3000 });
  }
};

// Fetch Job Details by ID
const fetchJobDetails = async (id) => {
  try {
    const response = await axios.post(`/api/apireg`, {
      action: 'jobDetails',
      id: id
    });
    if (response.data && !response.data.error) {
      selectedJob.value = response.data;
      showJobDetails.value = true;
    } else {
      toast.add({ severity: 'error', summary: 'Error', detail: response.data.error || 'Failed to load job details', life: 3000 });
    }
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to load job details', life: 3000 });
  }
};

//Get candidate Information
const candidate = ref(null);

const getCandidate = async (email) => {
    try {
        const response = await axios.post(`/api/apireg`, {
            action: 'getCandidate',
            email: candidateEmail.value
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

// Back to job list view
const goBackToJobList = () => {
  showJobDetails.value = false;
};

onMounted(() => {
    if (candidateEmail.value !== null) {
        getCandidate(candidateEmail.value);
    }
    listJobPostings();
});
</script>


<template>
    <app-topbar></app-topbar>
    <br> <br> <br> <br> 
    <div
        id="hero"
        class="flex flex-column pt-4 px-4 lg:px-8 overflow-hidden"
        style="background: linear-gradient(0deg, rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0.2)), radial-gradient(77.36% 256.97% at 77.36% 57.52%, rgb(238, 239, 175) 0%, rgb(195, 227, 250) 100%); clip-path: ellipse(150% 87% at 93% 13%)"
    >
        <div class="mx-4 md:mx-8 mt-0 md:mt-4">
            <h1 class="text-6xl font-bold text-gray-900 line-height-2"><span class="font-light block">Welcome to</span>SamanaGroup Jobs Portal</h1>
            <p class="font-normal text-2xl line-height-3 md:mt-3 text-gray-700">Discover top job opportunities that align with your skills and career goals. Join our team of experts in Cloud Computing and Managed Services technologies.</p>
            <br> <br> <br> <br>   
        </div>
    </div>
    


<div v-if="candidateEmail !== null" class="card grid">
    <div class="col-12 lg:col-6 ">
        <h3>Candidate Profile</h3>
    </div>
    <div class="col-12 lg:col-6 ">
        <h3>Candidate Certifications</h3>
    </div>
</div>




    
    <div class="card grid">
        <div class="col-12 lg:col-12 ">
            <h3 v-if="!showJobDetails">Available job opportunities</h3>
            <div v-if="!showJobDetails" class="layout-content grid">
                <div v-for="job in jobs" :key="job.id" class="col-12 md:col-6 lg:col-4">
                    <Card>
                        <template #title>{{ job.job_title }}</template>
                        <template #subtitle>{{ job.job_category }}</template>
                        <template #content>
                            <p class="m-0">{{ job.job_details }}</p>
                        </template>
                        <template #footer>
                            <div class="flex gap-4 mt-1">
                                <Button label="Details" severity="secondary" outlined class="w-full" @click="fetchJobDetails(job.id)" />
                                <Button
                                    v-if="candidateEmail"
                                    label="Apply Now"
                                    class="w-full"
                                    :href="job.linkedin_url"
                                    target="_blank"
                                />
                                <Button
                                    v-else
                                    label="Sign in to Apply"
                                    class="w-full"
                                    @click="router.push('/auth/register')"
                                />
                            </div>
                        </template>
                    </Card>
                </div>
                
            </div>
            <div v-if="jobs.length === 0 && !showJobDetails">
               <card>
                <template #content>
                <p>No jobs available at the moment. Please keep posted for upcoming opportunities.</p>
                </template>
               </card> 
            </div>
    
      
            <!-- Job Details View -->
            <div v-if="showJobDetails">
                <Card>
                    <template #title>{{ selectedJob.job_title }}</template>
                    <template #subtitle>{{ selectedJob.job_category }}</template>
                    <template #content>
                        <p>{{ selectedJob.job_details }}</p>
                        <p><strong>Job Type:</strong> {{ selectedJob.job_type }}</p>
                        <h5>Role Description</h5>
                        <p class="justified-text" v-html="selectedJob.role_description.replace(/\r\n/g, '<br/>')"></p>
                        
                        <h5>Responsibilities</h5>
                        <p class="justified-text" v-html="selectedJob.responsibilities.replace(/\r\n/g, '<br/>')"></p>
                        
                        <h5>Preferred Certifications</h5>
                        <p class="justified-text" v-html="selectedJob.preferred_certifications.replace(/\r\n/g, '<br/>')"></p>
                        
                        <h5>Qualifications</h5>
                        <p class="justified-text" v-html="selectedJob.qualifications.replace(/\r\n/g, '<br/>')"></p>

                        <p><strong>Salary Range:</strong> {{ selectedJob.salary_range }}</p>
                        <p><strong>Post Date:</strong> {{ selectedJob.post_date }}</p>
                    </template>
                    <template #footer>
                        <Button label="Back to Jobs" severity="danger" outlined @click="goBackToJobList" />
                    </template>
                </Card>
            </div>
        </div>
    </div>
    
    <div class="sticky-footer">
        <app-footer></app-footer>
    </div>
    </template>


<style lang="scss" scoped>

.sticky-footer {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    padding: 10px 0; /* Increase padding to make the footer taller */

    background: white;
 
}

body {
    margin-bottom: 40px; /* Adjust this value according to the footer height to avoid overlap */
}
.intro-section {
    padding: 2rem 1rem;
    text-align: center;
}

.justified-text {
    text-align: justify;
    margin-bottom: 10px;
    white-space: pre-wrap; /* This will ensure \r\n are respected and shown as new lines */
}




</style>