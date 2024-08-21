<script setup>
import { watch, ref, onMounted, computed } from 'vue'; // Keep this import
import AppTopbar from '../../layout/AppTopbarCandidate.vue';
import { useToast } from 'primevue/usetoast';
import { useLayout } from '@/layout/composables/layout';
import { uploadToAWSS3 } from '../../service/customScript';
import { sendSlackNotification } from '../../service/customScript';
import { CountryService } from '../../service/CountryService';

import { useRouter } from 'vue-router';
import axios from 'axios';
const logoUrl = 'samana-logo-dark.png';

const router = useRouter();

//country service
const countryService = new CountryService();
const autoValue = ref(null);
const selectedAutoValue = ref(null);

const autoFilteredValue = ref([]);


const searchCountry = (event) => {
    setTimeout(() => {
        if (!event.query.trim().length) {
            autoFilteredValue.value = [...autoValue.value];
        } else {
            autoFilteredValue.value = autoValue.value.filter((country) => {
                return country.name.toLowerCase().startsWith(event.query.toLowerCase());
            });
        }
    }, 250);
};

const selectedJobTitle = ref('');
const toast = useToast();
const showDialog = ref(false);
const loadingCV = ref(false);
const loadingProfilePhoto = ref(false);
const fileInput = ref(null);
const showCertificationDialog = ref(false);
const searchQuery = ref('');
const certifications = ref([]);
const filteredCertifications = ref([]);
const availableCertifications = ref([]);
const candidateCertifications = ref([]);
const showApplyDialog = ref(false);
const candidateRegistrations = ref([]);

const candidateAvailability = [
    { label: 'Immediately', value: 'Immediately' },
    { label: 'Within two weeks', value: 'Within two weeks' },
    { label: 'Within one month', value: 'Within one month' },
    { label: 'More than a month', value: 'More than a month' }
];

// Initialize form fields
const application = ref({
  email: document.cookie.replace(/(?:(?:^|.*;\s*)CandidateEmail\s*\=\s*([^;]*).*$)|^.*$/, "$1"),
  process: '',
  salary_expectation: '',
  availability: null,
  interview: 'Registration',
  interviewer_name: '',
  interviewer_email: '',
  evaluation_field: '',
  rating: '',
  observations: '',
  approved: '',
  v1: false,
  v2: false,
  v3: false,
  review_date: new Date().toISOString().slice(0, 19).replace('T', ' '), // Current date and time in MySQL format
});


// Computed property to check if all switches are on
const isFormValid = computed(() => {
  return application.value.v1 && application.value.v2 && application.value.v3;
});



const openApplyDialog = (jobId, jobTitle) => {
  application.value.process = jobId; // Set the job ID as the process
  selectedJobTitle.value = jobTitle; // Set the job title
  showApplyDialog.value = true; // Open the dialog
};

const handleSubmit = () => {
  if (isFormValid.value) {
    // Call your submit function
    submitApplication();
  } else {
    toast.add({ severity: 'error', summary: 'Error', detail: 'Please confirm all the statements before submitting.', life: 3000 });
  }
};


const submitApplication = async () => {
  try {
    const response = await axios.post(`/api/apireg`, {
      action: 'addCandidateReview',
      ...application.value
    });

    if (response.data && response.data.success) {
      toast.add({ severity: 'success', summary: 'Success', detail: 'Application submitted successfully!', life: 3000 });
      showApplyDialog.value = false; // Close the dialog after successful submission
      // Send Slack notification
      const message = `Candidate ${newCandidate.value.name} has applied for the position ${selectedJobTitle.value} on ${new Date().toLocaleString()}`;
      await sendSlackNotification(message, "#samana-careerpath");
        // Refresh candidate registrations to hide the "Apply Now" button if already submitted
      await getCandidateRegistrations(candidateEmail.value);
    } else {
      toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to submit application.', life: 3000 });
    }
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Error', detail: 'Please complete all the fields before submitting your application.', life: 3000 });
  }
      // Refresh the job list to reflect changes in the UI
      await listJobPostings();
};


const { layoutConfig } = useLayout();
const onSelectCV = (event) => {
    selectedFile.value = event.files[0];
};
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

// List candidate applications submitted

const getCandidateRegistrations = async (email) => {
    try {
        const response = await axios.post(`/api/apireg`, { action: 'listCandidateRegistrations', email });
        candidateRegistrations.value = response.data;
    } catch (error) {
        
    }
};




// List candidates certifications
const getCandidateCertifications = async (email) => {
    try {
        const response = await axios.post(`/api/apireg`, { action: 'listCandidateCertifications', email });
        candidateCertifications.value = response.data;
    } catch (error) {
        apiResponse.value = 'Error fetching candidate certifications: ' + error.message;
    }
};

// Fetch Job Postings
const listJobPostings = async () => {
  try {
    const response = await axios.post(`/api/apireg`, {
     //  action: 'listJobPostings'
       action: 'listAvailableJobs'
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



// Initialize form fields with cookies
const newCandidate = ref({
    name: document.cookie.replace(/(?:(?:^|.*;\s*)CandidateName\s*\=\s*([^;]*).*$)|^.*$/, "$1"),
    email: document.cookie.replace(/(?:(?:^|.*;\s*)CandidateEmail\s*\=\s*([^;]*).*$)|^.*$/, "$1"),
    profile_photo: document.cookie.replace(/(?:(?:^|.*;\s*)ProfileImage\s*\=\s*([^;]*).*$)|^.*$/, "$1"),
    phone_number: '',
    location: '',
    english_level: '',
    candidate_cv: '',
    created_at: new Date().toISOString().slice(0, 19).replace('T', ' '), // Current date and time in MySQL format
    enabled: 1
});


//Upload file
const onUpload = async (event, type) => {
    const file = event.files[0];
    if (!file) {
        toast.add({ severity: 'warn', summary: 'No File Selected', detail: 'Please select a file to upload.', life: 3000 });
        return;
    }

    // Set the correct loading state
    if (type === 'CVs') {
        loadingCV.value = true;
    } else if (type === 'images') {
        loadingProfilePhoto.value = true;
    }

    // Call the custom script to upload the file
    const result = await uploadToAWSS3(file, type, candidate.value.email);

    // Reset the loading state
    if (type === 'CVs') {
        loadingCV.value = false;
    } else if (type === 'images') {
        loadingProfilePhoto.value = false;
    }

    if (result && result.success) {
        if (type === 'CVs') {
            candidate.value.candidate_cv = result.url; // Prepopulate the CV URL field with the uploaded file URL
        } else if (type === 'images') {
            candidate.value.profile_photo = result.url; // Update profile photo with the new URL
        }
        toast.add({ severity: 'success', summary: 'Upload Successful', detail: 'File uploaded successfully.', life: 3000 });
    } else {
        toast.add({ severity: 'error', summary: 'Upload Failed', detail: result.message, life: 3000 });
    }
};

// Register the Candidate Profile
const submitProfile = async () => {
        // Make sure location is set
        if (!newCandidate.value.location && selectedAutoValue.value) {
            newCandidate.value.location = selectedAutoValue.value.name;
        }


    try {
        const response = await axios.post(`/api/apireg`, {
            action: 'addCandidate',
            ...newCandidate.value
        });

        if (response.data && !response.data.error) {
            candidate.value = response.data; // Update candidate with the new data
            toast.add({ severity: 'success', summary: 'Registration Successful', detail: 'Candidate profile has been registered successfully.', life: 3000 });
            showDialog.value = false; // Close the dialog after successful registration
                  // Refresh candidate registrations to hide the "Apply Now" button if already submitted
            await getCandidateRegistrations(candidateEmail.value);
            // Send Slack notification
            const message = `Candidate ${newCandidate.value.name} has applied for the position ${selectedJobTitle.value} on ${new Date().toLocaleString()}`;
            await sendSlackNotification(message, "#samana-careerpath");
            
        } else {
            console.error('Error saving profile:', response.data.error);
            toast.add({ severity: 'error', summary: 'Registration Failed', detail: 'Failed to register candidate profile.', life: 3000 });
        }
    } catch (error) {
        console.error('Error saving profile:', error);
        toast.add({ severity: 'error', summary: 'Registration Failed', detail: 'An error occurred while saving the profile.', life: 3000 });
    }
    getCandidate(candidateEmail.value);
     // Refresh the job list to reflect changes in the UI
     await listJobPostings();



};


const addCertificationToCandidate = async (certification) => {
    try {
        const response = await axios.post(`/api/apireg`, {
            action: 'addCandidateCertification',
            email: candidateEmail.value,
            certification: certification.certification,
        });
        if (response.data.success) {
            toast.add({ severity: 'success', summary: 'Success', detail: 'Certification added successfully', life: 3000 });
          
        } else {
            toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to add certification. Certification already registered.', life: 3000 });
        }
    } catch (error) {
        console.error('Error adding certification:', error.message);
        toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to add certification', life: 3000 });
    }
    getCandidateCertifications(candidateEmail.value); // Fetch certifications

};
const listAvailableCertifications = async () => {
    try {
        const response = await axios.post(`/api/apireg`, { action: 'listCertifications' });
        if (response.data && Array.isArray(response.data)) { // Ensure the response is an array
            availableCertifications.value = response.data;
            filteredCertifications.value = availableCertifications.value; // Initialize filtered certifications
        } else {
            toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to fetch certifications', life: 3000 });
        }
    } catch (error) {
        console.error('Error fetching available certifications:', error.message);
        toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to fetch certifications', life: 3000 });
    }
};
// Watcher to update location name when selectedAutoValue changes
watch(selectedAutoValue, (newVal) => {
    if (newVal && typeof newVal === 'object') {
        newCandidate.value.location = newVal.name;
    } else {
        newCandidate.value.location = newVal; // Handle any other cases
    }
});

watch(searchQuery, (newQuery) => {
    filteredCertifications.value = availableCertifications.value.filter(cert =>
        cert.certification.toLowerCase().includes(newQuery.toLowerCase())
    );
});
// Back to job list view
const goBackToJobList = () => {
  showJobDetails.value = false;
};

onMounted(() => {
    if (candidateEmail.value !== null) {
        getCandidate(candidateEmail.value);
        getCandidateCertifications(candidateEmail.value); // Fetch certifications
        getCandidateRegistrations(candidateEmail.value); // Fetch where the candidate apply
    }
    listAvailableCertifications(); // Fetch available certifications
    listJobPostings();
    countryService.getCountries().then((data) => (autoValue.value = data));



});

const showJobDialog = ref(false);

const openJobDetailsDialog = async (id) => {
  await fetchJobDetails(id);
  showJobDialog.value = true;
};

const closeJobDialog = () => {
  showJobDialog.value = false;
};


// Update Candidate Details
const showUpdateDialog = ref(false);

const updateCandidateProfile = async () => {
    try {
        const response = await axios.post(`/api/apireg`, {
            action: 'updateCandidate',
            ...candidate.value // Assuming `candidate` contains the current candidate data
        });

        if (response.data && !response.data.error) {
            toast.add({ severity: 'success', summary: 'Update Successful', detail: 'Candidate profile has been updated successfully.', life: 3000 });
            showUpdateDialog.value = false; // Close the dialog after successful update
            await getCandidate(candidateEmail.value); // Refresh candidate data
        } else {
            console.error('Error updating profile:', response.data.error);
            toast.add({ severity: 'error', summary: 'Update Failed', detail: 'Failed to update candidate profile.', life: 3000 });
        }
    } catch (error) {
        console.error('Error updating profile:', error);
        toast.add({ severity: 'error', summary: 'Update Failed', detail: 'An error occurred while updating the profile.', life: 3000 });
    }
};
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
            <h3 class="text-6xl font-bold text-gray-900 line-height-2"><span class="font-light block">Welcome to</span>Samana CareerPath</h3>
            <p class="font-normal text-2xl line-height-3 md:mt-3 text-gray-700">Discover top job opportunities that align with your skills and career goals. Join our team of experts in Cloud Computing and Managed Services technologies.</p>
            <br> <br> <br> <br>   
        </div>
    </div>
    


<div v-if="candidateEmail !== null" class="card grid">
    <div class="col-12 lg:col-6">
        <h3>Candidate Profile</h3>
        <Button v-if="candidate === null" label="Register Your Profile" class="mt-2" @click="showDialog = true" />

        <!-- Display candidate profile information if the candidate is not null -->
        <div v-if="candidate !== null" class="card candidate-details mt-3">
            <div class="card-header ">
                <img :src="candidate.profile_photo" alt="Profile Photo" height="100" />
            </div>
            <div class="card-body">
              
                <p><strong>Name:</strong> {{ candidate.name }}</p>
                <p><strong>Email:</strong> {{ candidate.email }}</p>
                <p><strong>Phone Number:</strong> {{ candidate.phone_number }}</p>
                <p><strong>Location:</strong> {{ candidate.location }}</p>
                <p><strong>English Level:</strong> {{ candidate.english_level }}</p>
                <p><strong>Candidate CV:</strong> <a :href="candidate.candidate_cv" target="_blank">View CV</a></p>
            </div>
            <div class="card-footer">
                <Button v-if="candidate !== null" label="Update Profile" class="mt-2" @click="showUpdateDialog = true" />
            </div>
        </div>
    </div>
    <div class="col-12 lg:col-6 "  v-if="candidate !== null" >
        <h3>Candidate Certifications</h3>
       <p> <Button  v-if="candidate !== null" icon="pi pi-plus" label="Add Certifications" @click="showCertificationDialog = true" severity="warning" outlined class="mb-2 mr-2" />       </p>   
       <div class="card" v-if="candidateCertifications.length" >
             
                <div class="grid">
                    <div class="col-12 md:col-6" v-for="certification in candidateCertifications" :key="certification.id">
                        <div class="certification-card">
                            <p>{{ certification.certification }}</p>
                        </div>
                    </div>
                </div>
            </div>
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
                                <Button label="Details" severity="info" outlined raised class="w-full" @click="fetchJobDetails(job.id)" />

                                <!-- Show the "Sign in to Apply" button if candidateEmail does not exist -->
                                <Button
                                    v-if="!candidateEmail"
                                    label="Sign in to Apply"
                                    class="w-full"
                                    outlined
                                    raised
                                    @click="router.push('/auth/register')"
                                />

                                <!-- Show the "Register Your Profile" button if candidateEmail exists but candidate.email does not exist -->
                                <Button
                                    v-if="candidateEmail && (!candidate || !candidate.email)"
                                    label="Register to apply"
                                    class="w-full"
                                    raised
                                    outlined
                                    @click="showDialog = true"
                                />

                                <!-- Show the "Apply Now" button if both candidateEmail and candidate.email exist and the job ID is not in candidateRegistrations -->
                                <Button
                                    v-if="candidateEmail && candidate && candidate.email && !candidateRegistrations.some(registration => registration.process == job.id)"
                                    label="Apply Now"
                                    class="w-full"
                                    severity="success"
                                    outlined
                                    raised
                                    @click="openApplyDialog(job.id, job.job_title)"
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
                        <Button label="Back to Jobs" severity="danger" outlined   class="w-full" raised @click="goBackToJobList" />
                        
                        
                    </template>
                </Card>
            </div>
        </div>
    </div>
    

    <!-- Register Candidate details -->
    <Dialog header="Register Candidate Profile" v-if="candidate === null" v-model:visible="showDialog" class=" col-11 md:col-6" modal>
    <form @submit.prevent="submitProfile">
        <div class="formgrid grid p-fluid">
            <div class="field col-12 md:col-6">
                <label for="name">Name</label>
                <InputText v-model="newCandidate.name" id="name" type="text" required />
            </div>
            <div class="field col-12 md:col-6">
                <label for="email">Email</label>
                <InputText v-model="newCandidate.email" id="email" type="email" required disabled :value="candidateEmail" />
            </div>
            <div class="field col-12 md:col-4">
                <label for="phone_number">Phone Number</label>
                <InputText v-model="newCandidate.phone_number" id="phone_number" type="text" placeholder="+(Country Code) Number" required />
            </div>
            <div class="field col-12 md:col-4">
                <label for="location">Location</label>
        
                <AutoComplete
                placeholder="Search"
                id="location"
                required
                :dropdown="true"
                v-model="selectedAutoValue"
                :suggestions="autoFilteredValue"
                @complete="searchCountry($event)"
                field="name"
                />       
                 </div>
            <div class="field col-12 md:col-4">
                <label for="english_level">English Level</label>
                <Dropdown id="english_level" v-model="newCandidate.english_level" :options="['A1', 'B1', 'B2', 'C1', 'C2']" placeholder="Select English Level" required />
            </div>
            <div class="field col-12 md:col-6">
                <label for="profile_photo">Profile Photo </label>
                <div class="flex align-items-center">
                <InputText v-model="newCandidate.profile_photo" id="profile_photo" type="text" required disabled />
                <FileUpload 
              
                    mode="basic" 
                    name="profile_photo" 
                    chooseLabel="Photo"
                    accept="image/*" 
                    :maxFileSize="5000000" 
                    @select="(event) => onUpload(event, 'images')" 
                     
                />
                <ProgressSpinner v-if="loadingProfilePhoto" style="width: 40px; height: 40px;" strokeWidth="8" fill="#EEEEEE" animationDuration=".5s" />
            </div>
            </div>
            <div class="field col-12 md:col-6">
                <label for="candidate_cv">Candidate CV (PDF Only)</label>
                <div class="flex align-items-center">

                <InputText v-model="newCandidate.candidate_cv" id="candidate_cv" type="text" required disabled />
                <FileUpload 
                    mode="basic" 
                    name="candidate_cv" 
                    accept=".pdf" 
                    chooseLabel="CV"
                    :auto="false" 
                    :maxFileSize="10000000" 
                    @select="(event) => onUpload(event, 'CVs')" 
                     
                />
                <ProgressSpinner v-if="loadingCV" style="width: 40px; height: 40px;" strokeWidth="8" fill="#EEEEEE" animationDuration=".5s" />        
                </div>    
            </div>
            <input type="hidden" v-model="newCandidate.created_at" />
            <input type="hidden" v-model="newCandidate.enabled" />
        </div>
        <Button label="Register Profile" type="button" class="w-full" @click="submitProfile" />
    </form>
</Dialog>



    <!-- Update Candidate details -->
<Dialog header="Update Candidate Profile" v-if="candidate !== null" v-model:visible="showUpdateDialog" class="col-11 md:col-6" modal>
    <form @submit.prevent="updateCandidateProfile">
        <div class="formgrid grid p-fluid">
            <div class="field col-12 md:col-6">
                <label for="name">Name</label>
                <InputText v-model="candidate.name" id="name" type="text" required />
            </div>
            <div class="field col-12 md:col-6">
                <label for="email">Email</label>
                <InputText v-model="candidate.email" id="email" type="email" required disabled />
            </div>
            <div class="field col-12 md:col-4">
                <label for="phone_number">Phone Number</label>
                <InputText v-model="candidate.phone_number" id="phone_number" type="text" placeholder="+(Country Code) Number" required />
            </div>
            <div class="field col-12 md:col-4">
                <label for="location">Location</label>
        
                <InputText
    placeholder="Enter Location"
    id="location"
    required
    v-model="candidate.location"
/>
            </div>
            <div class="field col-12 md:col-4">
                <label for="english_level">English Level</label>
                <Dropdown id="english_level" v-model="candidate.english_level" :options="['A1', 'B1', 'B2', 'C1', 'C2']" placeholder="Select English Level" required />
            </div>
            <div class="field col-12 md:col-6">
                <label for="profile_photo">Profile Photo </label>
                <div class="flex align-items-center">
                <InputText v-model="candidate.profile_photo" id="profile_photo" type="text" required disabled />
                <FileUpload 
              
                    mode="basic" 
                    name="profile_photo" 
                    chooseLabel="Photo"
                    accept="image/*" 
                    :maxFileSize="5000000" 
                    @select="(event) => onUpload(event, 'images')" 
                     
                />
                <ProgressSpinner v-if="loadingProfilePhoto" style="width: 40px; height: 40px;" strokeWidth="8" fill="#EEEEEE" animationDuration=".5s" />
            </div>
            </div>
            <div class="field col-12 md:col-6">
                <label for="candidate_cv">Candidate CV (PDF Only)</label>
                <div class="flex align-items-center">

                <InputText v-model="candidate.candidate_cv" id="candidate_cv" type="text" required disabled />
                <FileUpload 
                    mode="basic" 
                    name="candidate_cv" 
                    accept=".pdf" 
                    chooseLabel="CV"
                    :auto="false" 
                    :maxFileSize="10000000" 
                    @select="(event) => onUpload(event, 'CVs')" 
                     
                />
                <ProgressSpinner v-if="loadingCV" style="width: 40px; height: 40px;" strokeWidth="8" fill="#EEEEEE" animationDuration=".5s" />        
                </div>    
            </div>
        </div>
        <Button label="Update Profile" type="button" class="w-full" @click="updateCandidateProfile" />
    </form>
</Dialog>



    <!-- Register Candidate Certifications -->
<Dialog header="Add Certifications" v-model:visible="showCertificationDialog" :modal="true" :closable="true" class=" col-11 md:col-6"  >
        <div class="p-fluid">
            <InputText type="text" v-model="searchQuery" placeholder="Search certifications..." />

            <DataTable :value="filteredCertifications" class="p-datatable-gridlines" :scrollable="true" scrollHeight="70vh" scrollDirection="vertical">
              <Column field="certification" header="Certification"></Column>
                <Column header="Actions" bodyStyle="text-align: center" frozen alignFrozen="right">
                    <template #body="slotProps">
                        <Button 
                            icon="pi pi-plus" 
                           text raised  class="mb-2 mr-2"
                            @click="addCertificationToCandidate(slotProps.data)" 
                        />
                    </template>
                </Column>
            </DataTable>
        </div>
    </Dialog>





 <!-- Add the Apply Now Dialog -->
 <Dialog header="Apply for this Job" v-model:visible="showApplyDialog" modal class=" col-11 md:col-6" >
    <form @submit.prevent="submitApplication">
      <div class="formgrid grid">
  
       
          <InputText v-model="application.process" id="process" type="text" hidden />
    
       
         
          <InputText v-model="application.process" id="process" type="text" :value="candidate.email"  required hidden />

          <div class="field col-12 md:col-12">
            <label for="v1">I accept the terms and conditions of this job offer.</label>
            <InputSwitch v-model="application.v1" id="v1" /><br>
            <label for="v2">I have reviewed the job description, including the responsibilities, preferred certifications, and required qualifications.</label>
            <InputSwitch v-model="application.v2" id="v2" /><br>
            <label for="v3">I verify that the information on my CV is accurate and that I meet the requirements for this role.</label>
            <InputSwitch v-model="application.v3" id="v3" /><br>
        </div>
     
        <div class="field col-12 md:col-6">
          <p for="salary_expectation">What is your monthly salary expectation?</p>
          <InputText v-model="application.salary_expectation" id="salary_expectation" type="text" required />
        </div>
        <div class="field col-12 md:col-6">
          <p for="availability">When is your Availability to start?</p>
          <Dropdown v-model="application.availability" id="availability"  :options="candidateAvailability" optionLabel="label" optionValue="value" placeholder="Availability" required />

        </div>

   


 
        <input type="hidden" v-model="application.review_date" />
        <input type="hidden" v-model="selectedJobTitle" />
      </div>
      <Button label="Submit" type="submit" class="mt-2" :disabled="!isFormValid" />
    </form>
  </Dialog>




<Toast />

    <div class="sticky-footer">
        <div class="layout-footer">
        <img :src="logoUrl" alt="Logo" height="20" class="mr-2" />
        by
        <span class="font-medium ml-2">Samana Group LLC </span>
         , All Rights Reserved
         <div class="ml-4">
          <a href="/TermsOfService.html" class="text-primary">Terms of Use</a> | 
          <a href="/privacy.html" class="text-primary">Privacy Policy</a>
      </div>
    </div>

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

.certification-card {
    margin-bottom: -2rem;
    text-align: left;
}

.certification-card p {
    margin-bottom: 0;
}

.p-fileupload-content .p-fileupload-filename {
    display: none;
}

</style>