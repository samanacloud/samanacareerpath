<script setup>
import { ref, onBeforeMount } from 'vue';
import axios from 'axios';
import { FilterMatchMode } from 'primevue/api';
import Button from 'primevue/button';
import { useToast } from 'primevue/usetoast';
import Rating from 'primevue/rating';
import Tag from 'primevue/tag';
import { useRouter } from 'vue-router'; // Add this line
import Tooltip from 'primevue/tooltip';


const toast = useToast();

// Add Job Process
const showAddDialog = ref(false); // Add this line


const newJob = ref({
  job_category: '',
  job_title: '',
  job_details: '',
  workplace_type: '',
  job_type: '',
  salary_range: '',
  role_description: '',
  responsibilities: '',
  preferred_certifications: '',
  qualifications: '',
  linkedin_url: '',
  post_date: new Date().toISOString().slice(0, 10), // Add this line
  enabled: 1
});

const jobCategories = [
  { label: 'Consulting Services', value: 'Consulting Services' },
  { label: 'VDI Managed Services', value: 'VDI Managed Services' },
  { label: 'Administrative Role', value: 'Administrative Role' },
  { label: 'Other', value: 'Other' }
];

const jobTypes = [
  { label: 'Full-Time', value: 'Full-Time' },
  { label: 'Partial Time', value: 'Partial Time' },
  { label: 'Half Time', value: 'Half Time' },
  { label: 'On Hour Basis', value: 'On Hour Basis' }
];

const workplaceTypes = [
  { label: 'Remote', value: 'Remote' },
  { label: 'On Site', value: 'On Site' },
  { label: 'Hybrid', value: 'Hybrid' }
];

const addJobProcess = async () => {
  try {
    const response = await axios.post(`/api/apitest`, {
      action: 'addJobProcess',
      job_category: newJob.value.job_category,
      job_title: newJob.value.job_title,
      job_details: newJob.value.job_details,
      workplace_type: newJob.value.workplace_type,
      job_type: newJob.value.job_type,
      salary_range: newJob.value.salary_range,
      role_description: newJob.value.role_description,
      responsibilities: newJob.value.responsibilities,
      preferred_certifications: newJob.value.preferred_certifications,
      qualifications: newJob.value.qualifications,
      linkedin_url: newJob.value.linkedin_url
    });

    if (response.data.success) {
      apiResponse.value = 'Job added successfully';
      toast.add({ severity: 'success', summary: 'Success', detail: 'Job added successfully.', life: 3000 });

      await listJobPostings(); // Refresh job list after successful update
      showAddDialog.value = false; // Close the dialog
    } else {
      
      toast.add({ severity: 'error', summary: 'Error adding job', detail: error, life: 3000 });
    }
  } catch (error) {
    console.error('Error adding job:', error);
    toast.add({ severity: 'error', summary: 'Error adding job', detail: error, life: 3000 });
    apiResponse.value = 'Error: ' + error.message;
  }
};



// Update Job Posting
const showEditDialog = ref(false);
const isEditing = ref(false);  // Correctly define the isEditing variable
const editJob = (job) => {
  selectedJob.value = { ...job };
  showEditDialog.value = true;
};




isEditing.value = false; // Exit edit mode
const updateJob = async () => {
  try {
    const response = await axios.post(`/api/apitest`, {
      action: 'updateJobProcess',  // Ensure this is your correct action name
      id: selectedJob.value.id,
      job_category: selectedJob.value.job_category,
      job_title: selectedJob.value.job_title,
      job_details: selectedJob.value.job_details,
      workplace_type: selectedJob.value.Workplace_type,
      job_type: selectedJob.value.job_type,
      linkedin_url: selectedJob.value.linkedin_url,
      role_description: selectedJob.value.role_description,
      responsibilities: selectedJob.value.responsibilities,
      preferred_certifications: selectedJob.value.preferred_certifications,
      qualifications: selectedJob.value.qualifications,
      salary_range: selectedJob.value.salary_range,
      enabled: selectedJob.value.enabled // Add the enabled field here
    });

    if (response.data.success) {
      toast.add({ severity: 'success', summary: 'Success', detail: 'Job updated successfully.', life: 3000 });
      await listJobPostings(); // Refresh job list after successful update
      showEditDialog.value = false; // Close the dialog
    } else {
      toast.add({ severity: 'error', summary: 'Error updating job', detail: 'Failed to update job.', life: 3000 });
    }
  } catch (error) {
    console.error('Error updating job:', error);
    toast.add({ severity: 'error', summary: 'Error updating job', detail: error.message, life: 3000 });
  }
};









// Initialize the router instance
const router = useRouter(); // Add this line

//redirects to unauthorized if the user role is lower than the pagerole
import { getPageAuthorization } from '@/utils/utils';
const pageRole = 3; // Set the required role for this page
getPageAuthorization(pageRole);


// Data and State
const jobs = ref([]);
const apiResponse = ref('');
const filters = ref({
  'job_category': { value: null, matchMode: FilterMatchMode.CONTAINS },
  'job_title': { value: null, matchMode: FilterMatchMode.CONTAINS },
  'job_type': { value: null, matchMode: FilterMatchMode.CONTAINS },
  'enabled': { value: null, matchMode: FilterMatchMode.EQUALS },
});
const selectedJob = ref(null);
const enrolledCandidates = ref([]);
const registeredCandidates = ref([]);
const candidateReviews = ref({});

const idFrozen = ref(false); // Add this line for dynamic toggling

// Helper method to extract initials from a name
const getInitials = (name) => {
  return name.split(' ').map(n => n[0]).join('');
};

// Group reviews by interview type
const groupReviewsByInterviewType = (reviews) => {
  const grouped = { 'First Interview': [], 'Second Interview': [], 'Additional Interview': [] };
  reviews.forEach(review => {
    if (grouped[review.interview]) {
      grouped[review.interview].push(review);
    }
  });
  return grouped;
};

// Fetch Job Postings
const listJobPostings = async () => {
  try {
    const response = await axios.post(`/api/apitest`, {
      action: 'listJobPostings'
    });
    jobs.value = Array.isArray(response.data) ? response.data : [response.data];
    apiResponse.value = 'Jobs listed successfully';
  } catch (error) {
    apiResponse.value = 'Error: ' + error.message;
  }
};

// Fetch Job Details by ID
const fetchJobDetails = async (id) => {
  try {
    const response = await axios.post(`/api/apitest`, {
      action: 'jobDetails',
      id: id
    });
    selectedJob.value = response.data;
    fetchEnrolledCandidates(id); // Fetch enrolled candidates when job details are fetched
    fetchRegisteredCandidates(id); // Fetch registered candidates when job details are fetched
  } catch (error) {
    console.error('Error fetching job details:', error);
    selectedJob.value = null;
  }
};

// Fetch Enrolled Candidates by Process ID
const fetchEnrolledCandidates = async (processId) => {
  try {
    const response = await axios.post(`/api/apitest`, {
      action: 'getCandidatesByProcess',
      processId: processId
    });
    enrolledCandidates.value = response.data;
    // Fetch reviews for each candidate
    enrolledCandidates.value.forEach(candidate => {
      fetchCandidateReviews(candidate.email, processId);
    });
  } catch (error) {
    console.error('Error fetching enrolled candidates:', error);
    enrolledCandidates.value = [];
  }
};
// Fetch Enrolled Candidates by Process ID
const fetchRegisteredCandidates = async (processId) => {
  try {
    const response = await axios.post(`/api/apitest`, {
      action: 'getRegisteredCandidatesByProcess',
      processId: processId
    });
    registeredCandidates.value = response.data;
 
  } catch (error) {
    console.error('Error fetching enrolled candidates:', error);
    registeredCandidates.value = [];
  }
};

// Fetch Candidate Reviews by Email and Process ID
const fetchCandidateReviews = async (email, processId) => {
  try {
    const response = await axios.post(`/api/apitest`, {
      action: 'getCandidateReviews',
      email: email,
      processId: processId
    });
    candidateReviews.value[email] = groupReviewsByInterviewType(response.data);
  } catch (error) {
    console.error('Error fetching candidate reviews:', error);
    candidateReviews.value[email] = { 'First Interview': [], 'Second Interview': [], 'Additional Interview': [] };
  }
};



// Correct the viewProfileDetails function
const viewProfileDetails = (email) => {
    sessionStorage.setItem('candidateEmail', email);
    router.push('/candidatesreviews'); // Modify this line
};

// Lifecycle Hook
onBeforeMount(listJobPostings);
</script>

<template>
  <div class="grid grid-nogutter">
    <div class="col-12">
      <div class="card">
        <h5>Jobs Process</h5>
        <Button label="Add New Job Process" icon="pi pi-plus" class="mb-3" @click="showAddDialog = true" />

        <div>
          <DataTable
            :value="jobs"
            :filters="filters"
            filterDisplay="menu"
            dataKey="id"
            class="job-list-table"
          >
            <Column field="job_category" header="Job Category" filter filterPlaceholder="Search by category"></Column>
            <Column field="job_title" header="Job Title" filter filterPlaceholder="Search by title"></Column>
            <Column field="job_type" header="Job Type" filter filterPlaceholder="Search by type"></Column>
            <Column 
              field="enabled" 
              header="Status" 
              filter 
              filterPlaceholder="Select status" 
              :filterOptions="statusFilterOptions">
              <template #body="slotProps">
                  <span v-if="Number(slotProps.data.enabled) === 1" class="badge badge-success">Open</span>
                  <span v-else class="badge badge-danger">Closed</span>
              </template>
            </Column>
            <Column header="Actions" bodyStyle="text-align: center;">
              <template #body="slotProps">
                <Button icon="pi pi-search" severity="success" text outlined raised @click="fetchJobDetails(slotProps.data.id)"  v-tooltip="'View Job Details'"/>
                <Button icon="pi pi-pencil" severity="info" text outlined raised @click="editJob(slotProps.data)" v-tooltip="'Edit Job Details'" style="margin-left: 5px;"/>

              </template>
            </Column>
          </DataTable>
        </div>
      </div>
    </div>

    <div class="col-12 xl:col-6" v-if="selectedJob">
      <div class="card">
        <div class="flex align-items-center justify-content-between">
          <h5>{{ selectedJob.job_title }}</h5>
          <span v-if="selectedJob.enabled === 1" class="badge badge-success">Open</span>
          <span v-else class="badge badge-danger">Closed</span>
        </div>
      
        <div class="p-3">
          <h5>Salary Range:</h5>
          <p>{{ selectedJob.salary_range }}</p>
          <h5>Job Type:</h5>
          <p>{{ selectedJob.job_type }}</p>
          <h5>Workplace Type:</h5>
          <p>{{ selectedJob.Workplace_type }}</p>
          <h5>Job Details:</h5>
          <p>{{ selectedJob.job_details }}</p>
          <h5>Role Description:</h5>
          <p>{{ selectedJob.role_description }}</p>
          <h5>Responsibilities:</h5>
          <p>{{ selectedJob.responsibilities }}</p>
          <h5>Qualifications:</h5>
          <p>{{ selectedJob.qualifications }}</p>
          <h5>LinkedIn URL:</h5>
          <p><a :href="selectedJob.linkedin_url" target="_blank">{{ selectedJob.linkedin_url }}</a></p>
        </div>
        <div style="text-align: center;">
          <Button icon="pi pi-pencil" severity="info" label="Edit Job Details" text outlined raised @click="showEditDialog = true"  v-tooltip="'Edit Job Details'"/>
        </div>
      </div>
    </div>

    <div class="col-12 xl:col-6" v-if="selectedJob">
      <div class="card">
        <h5>Interviews Results</h5>
        <div class="p-3">
          <DataTable :value="enrolledCandidates" :scrollable="true" scrollHeight="80vh" scrollDirection="both">
            <Column field="name" header="Name">
              <template #body="slotProps">
                <div>
                  <b>{{ slotProps.data.name }}</b>
                  <small style="display: block;">{{ slotProps.data.email }}</small> 
                </div>
              </template>
            </Column>
            <Column header="First Interview">
              <template #body="slotProps">
                <div v-if="candidateReviews[slotProps.data.email]?.['First Interview']">
                  <div v-for="review in candidateReviews[slotProps.data.email]['First Interview']" :key="review.interviewer_name">
                    
                    <Tag :severity="review.approved === 'Yes' ? 'success' : 'danger'">
                      {{ getInitials(review.interviewer_name) }} - {{ review.approved === 'Yes' ? 'Yes' : 'No' }}
                    </Tag>
                  </div>
                </div>
                <div v-else>Loading...</div>
              </template>
            </Column>
            <Column header="Second Interview">
              <template #body="slotProps">
                <div v-if="candidateReviews[slotProps.data.email]?.['Second Interview']">
                  <div v-for="review in candidateReviews[slotProps.data.email]['Second Interview']" :key="review.interviewer_name">
                   
                    <Tag :severity="review.approved === 'Yes' ? 'success' : 'danger'">
                      {{ getInitials(review.interviewer_name) }} - {{ review.approved === 'Yes' ? 'Yes' : 'No' }}
                    </Tag>
                  </div>
                </div>
                <div v-else>Loading...</div>
              </template>
            </Column>
            <Column header="Additional Interview">
              <template #body="slotProps">
                <div v-if="candidateReviews[slotProps.data.email]?.['Additional Interview']">
                  <div v-for="review in candidateReviews[slotProps.data.email]['Additional Interview']" :key="review.interviewer_name">
                    
                    <Tag :severity="review.approved === 'Yes' ? 'success' : 'danger'">
                      {{ getInitials(review.interviewer_name) }} - {{ review.approved === 'Yes' ? 'Yes' : 'No' }}
                    </Tag>
                  </div>
                </div>
                <div v-else>Loading...</div>
              </template>
            </Column>
            <Column header="Profile Details" frozen alignFrozen="right">  
              <template #body="slotProps">
               <Button icon="pi pi-search" text raised outlined severity="success" @click="viewProfileDetails(slotProps.data.email)" />
              </template>
              </Column>
         
          </DataTable>
        </div>
      </div>
      <div class="card">
        <h5>Registered candidates for this process</h5>
        <div class="p-3">
          <DataTable :value="registeredCandidates" :scrollable="true" scrollHeight="80vh" scrollDirection="both">
            <Column field="name" header="Name">
              <template #body="slotProps">
                <div>
                  <b>{{ slotProps.data.name }}</b>
                  <small style="display: block;">{{ slotProps.data.email }}</small> 
                </div>
              </template>
            </Column>



            <Column header="Profile Details" frozen alignFrozen="right">  
              <template #body="slotProps">
               <Button icon="pi pi-search" text raised outlined severity="success" @click="viewProfileDetails(slotProps.data.email)" />
              </template>
              </Column>
         
          </DataTable>
        </div>
      </div>
    </div>





    <Dialog header="Add New Job Process" v-model:visible="showAddDialog" modal class="col-11 md:col-6">
  <form @submit.prevent="addJobProcess">
    <div class="formgrid grid p-fluid">

      <div class="field col-12">
        <label for="job_title">Job Title</label>
        <InputText v-model="newJob.job_title" required />
      </div>
      <div class="field col-12 md:col-6">
        <label for="job_category">Job Category</label>
        <Dropdown v-model="newJob.job_category" :options="jobCategories" optionLabel="label" optionValue="value" required />
      </div>
      <div class="field col-12 md:col-6">
        <label for="job_type">Job Type</label>
        <Dropdown v-model="newJob.job_type" :options="jobTypes" optionLabel="label" optionValue="value" required />
      </div>
      <div class="field col-12 md:col-6">
        <label for="workplace_type">Workplace Type</label>
        <Dropdown v-model="newJob.workplace_type" :options="workplaceTypes" optionLabel="label" optionValue="value" required />
      </div>
      <div class="field col-12 md:col-6">
        <label for="salary_range">Salary Range</label>
        <InputText v-model="newJob.salary_range" required />
      </div>
      <div class="field col-12">
        <label for="job_details">Job Details</label>
        <Textarea v-model="newJob.job_details" autoResize required />
      </div>
      <div class="field col-12">
        <label for="role_description">Role Description</label>
        <Textarea v-model="newJob.role_description" autoResize required />
      </div>
      <div class="field col-12">
        <label for="responsibilities">Responsibilities</label>
        <Textarea v-model="newJob.responsibilities" autoResize required />
      </div>
      <div class="field col-12">
        <label for="preferred_certifications">Preferred Certifications</label>
        <Textarea v-model="newJob.preferred_certifications" autoResize required />
      </div>
      <div class="field col-12">
        <label for="qualifications">Qualifications</label>
        <Textarea v-model="newJob.qualifications" autoResize required />
      </div>
      <div class="field col-12">
        <label for="linkedin_url">LinkedIn URL</label>
        <InputText v-model="newJob.linkedin_url" />
      </div>
    </div>
    <Button label="Submit" type="submit" class="w-full mt-3" />
  </form>
</Dialog>
<Dialog header="Edit Job Process" v-model:visible="showEditDialog" modal class="col-11 md:col-6">
  <form @submit.prevent="updateJob">
    <div class="formgrid grid p-fluid">

      <div class="field col-12  md:col-8">
        <label for="job_title">Job Title</label>
        <InputText v-model="selectedJob.job_title" required />
      </div>
      <div class="field col-12 md:col-4">
        <label for="linkedin_url">Status</label>
        <Dropdown 
          v-model="selectedJob.enabled" 
          :options="[
            { label: 'Open', value: 1 }, 
            { label: 'Closed', value: 0 }
          ]" 
          optionLabel="label" 
          optionValue="value" 
          placeholder="Select Status"
        />
       </div>
      <div class="field col-12  md:col-6">
        <label for="job_category">Job Category</label>
        <Dropdown v-model="selectedJob.job_category" :options="jobCategories" optionLabel="label" optionValue="value" required />
      </div>
      <div class="field col-12  md:col-6">
        <label for="job_type">Job Type</label>
        <Dropdown v-model="selectedJob.job_type" :options="jobTypes" optionLabel="label" optionValue="value" required />
      </div>
      <div class="field col-12 md:col-6">
        <label for="workplace_type">Workplace Type</label>
        <Dropdown v-model="selectedJob.workplace_type" :options="workplaceTypes" optionLabel="label" optionValue="value" required />
      </div>
      <div class="field col-12 md:col-6">
        <label for="salary_range">Salary Range</label>
        <InputText v-model="selectedJob.salary_range" required />
      </div>
      <div class="field col-12">
        <label for="job_details">Job Details</label>
        <textarea v-model="selectedJob.job_details" class="p-inputtext p-component" rows="4" required></textarea>
      </div>
      <div class="field col-12">
        <label for="role_description">Role Description</label>
        <textarea v-model="selectedJob.role_description" class="p-inputtext p-component" rows="4" required></textarea>
      </div>
      <div class="field col-12">
        <label for="responsibilities">Responsibilities</label>
        <textarea v-model="selectedJob.responsibilities" class="p-inputtext p-component" rows="4" required></textarea>
      </div>
      <div class="field col-12">
        <label for="preferred_certifications">Preferred Certifications</label>
        <textarea v-model="selectedJob.preferred_certifications" class="p-inputtext p-component" rows="4" required></textarea>
      </div>
      <div class="field col-12">
        <label for="qualifications">Qualifications</label>
        <textarea v-model="selectedJob.qualifications" class="p-inputtext p-component" rows="4" required></textarea>
      </div>
      <div class="field col-12">
        <label for="linkedin_url">LinkedIn URL</label>
        <InputText v-model="selectedJob.linkedin_url" />
      </div>

    </div>
    <Button label="Save" type="submit" class="w-full mt-3" />
  </form>
</Dialog>
<Toast />
  </div>
</template>


<style>
.badge {
  display: inline-block;
  padding: 0.5em 0.75em;
  font-size: 75%;
  font-weight: 700;
  line-height: 1;
  text-align: center;
  white-space: nowrap;
  vertical-align: baseline;
  border-radius: 0.375rem;
}
.badge-success {
  background-color: #4CAF50;
  color: white;
}
.badge-danger {
  background-color: #f44336;
  color: white;
}
.grid-nogutter {
  margin-left: 0;
  margin-right: 0;
}
.grid-nogutter > [class*="col-"] {
  padding-left: 0;
  padding-right: 0;
}
@media (max-width: 767px) { /* Adjust breakpoint as needed */
  .job-list-table .p-datatable-thead > tr > th:nth-child(1), /* Job Category column (index 0) */
  .job-list-table .p-datatable-thead > tr > th:nth-child(3), /* Job Type column (index 2) */
  .job-list-table .p-datatable-tbody > tr > td:nth-child(1), /* Job Category column (index 0) */
  .job-list-table .p-datatable-tbody > tr > td:nth-child(3)  /* Job Type column (index 2) */ 
   {
    display: none; 
  }
  .card { /* Adjust the card width or margin as needed */
    width: 100%; 
    margin-bottom: 1rem;
  }

  .card .p-3 > div { /* Adjust the spacing between elements in the card */
    margin-bottom: 0.5rem;
  }

  /* Enrolled Candidates Table */
  .enrolled-candidates-table {
    width: 100%; /* Ensure table takes full width on mobile */
  }

  .enrolled-candidates-table .p-datatable-header {
    font-size: 0.9rem; /* Slightly smaller header font on mobile */
  }

  .enrolled-candidates-table .p-datatable-tbody > tr > td {
    padding: 0.5rem;  /* Adjust cell padding for better spacing on mobile */
  }

  .enrolled-candidates-table .p-tag {
    font-size: 0.8rem;  /* Adjust tag font size on mobile */
  }
}
</style>