<script setup>
import { watch, ref, onMounted } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import Rating from 'primevue/rating';
import Accordion from 'primevue/accordion';
import AccordionTab from 'primevue/accordiontab';

import Button from 'primevue/button';
import DataTable from 'primevue/datatable'; // Import DataTable
import Column from 'primevue/column';    // Import Column
import { useToast } from 'primevue/usetoast';
import { useConfirm } from 'primevue/useconfirm';
import ConfirmDialog from 'primevue/confirmdialog';
import Toast from 'primevue/toast';
import Dropdown from 'primevue/dropdown';
import InputText from 'primevue/inputtext';
import RadioButton from 'primevue/radiobutton';

//redirects to unauthorized if the user role is lower than the pagerole
import { getPageAuthorization } from '@/utils/utils';
const pageRole = 3; // Set the required role for this page
getPageAuthorization(pageRole);


const idFrozen = ref(false); // Add this line for dynamic toggling



const displayConfirmation = ref(false);
const skillsetToDelete = ref(null); 
const candidateDetails = ref(null);
const apiResponse = ref('');
const categories = ref([]);
const skillsets = ref([]);
const reviewer_id = ref(null); // Refactor this line
const reviewer_email = ref(document.cookie.split('; ').find(row => row.startsWith('userEmail')).split('=')[1]);
const reviewer_name = ref('');
const reviewedSkillsets = ref([]);
const candidateSkillsets = ref([]);
const email = sessionStorage.getItem('candidateEmail');
const router = useRouter(); // Use the router instance
const toast = useToast(); // Use PrimeVue's toast
const confirm = useConfirm(); // Use PrimeVue's confirm service
const activeCategory = ref(null);
const showCertificationDialog = ref(false);
const searchQuery = ref('');
const certifications = ref([]);
const filteredCertifications = ref([]);
const availableCertifications = ref([]);
const jobProcesses = ref([]);

const candidateReview = ref({
    process: '',
    salary_expectation: null,
    availability: '',
    interview: '',
    evaluation_field: '',
    rating: null,
    observations: '',
    approved: '',
    review_date: new Date().toISOString().slice(0, 19).replace('T', ' ')
});

const candidateAvailability = [
    { label: 'Immediately', value: 'Immediately' },
    { label: 'Within two weeks', value: 'Within two weeks' },
    { label: 'Within one month', value: 'Within one month' },
    { label: 'More than a month', value: 'More than a month' }
];
const evaluationFields = [
    { label: 'HR -General Technical Evaluation', value: 'HR -General Technical Evaluation' },
    { label: 'CTO - Technical Evaluation', value: 'CTO - Technical Evaluation' },
    { label: 'SDD - Portfolio Review', value: 'SDD - Portfolio Review' },
    { label: 'SDM - Problem Solving Skills', value: 'SDM - Problem Solving Skills' },
    { label: 'SDM - Communication Skills', value: 'SDM - Communication Skills' },
    { label: 'CEO - Alignment with Company Vision', value: 'CEO - Alignment with Company Vision' },
    { label: 'ANN - English Evaluation', value: 'ANN - English Evaluation' }
];

const ratingOptions = [
    { label: '1 - Unsatisfactory', value: 1 },
    { label: '2 - Below Expectations', value: 2 },
    { label: '3 - Meet Expectations', value: 3 },
    { label: '4 - Exceeds Expectations', value: 4 },
    { label: '5 - Outstanding', value: 5 }
];

const interviewStages = [
    { label: 'First Interview', value: 'First Interview' },
    { label: 'Second Interview', value: 'Second Interview' },
    { label: 'Additional Interview', value: 'Additional Interview' }
];

const approvalOptions = [
    { label: 'Yes', value: 'Yes' },
    { label: 'No', value: 'No' }
];

const confirmSubmitReview = () => {
    confirm.require({
        message: 'Are you sure you want to submit this review? This action cannot be undone!',
        header: 'Confirmation',
        icon: 'pi pi-exclamation-triangle',
        accept: () => submitReview()
    });
};

const candidateReviews = ref([]);

const getJobProcesses = async () => {
    try {
        const response = await axios.post(`/api/api`, { action: 'getJobProcess' });
        jobProcesses.value = response.data.map(process => ({
            label: `ID:[${process.id}] - ${process.job_title} - [${process.enabled ==='1' ? 'Active' : 'Inactive'}]`,
            value: process.id
        }));
    } catch (error) {
        console.error('Error fetching job processes:', error);
    }
};


const getCandidateReviews = async (email) => {
    try {
        const response = await axios.post(`/api/api`, { action: 'listCandidateReviews', email });
        candidateReviews.value = response.data;
    } catch (error) {
        apiResponse.value = 'Error fetching candidate reviews: ' + error.message;
    }
};
const submitReview = async () => {
    if (!candidateReview.value.evaluation_field || candidateReview.value.rating === null || candidateReview.value.approved === '') {
        toast.add({ severity: 'warn', summary: 'Warning', detail: 'Please fill out all required fields.', life: 3000 });
        return;
    }

    // Ensure salary_expectation and availability are set to 0 if the interview type is "Second Interview" or "Additional Interview"
    if (candidateReview.value.interview === 'Second Interview' || candidateReview.value.interview === 'Additional Interview') {
        candidateReview.value.salary_expectation = 0;
        candidateReview.value.availability = 0;
    }

    try {
        const response = await axios.post(`/api/api`, {
            action: 'addCandidateReview',
            email: candidateDetails.value.email,
            process: candidateReview.value.process,
            salary_expectation: candidateReview.value.salary_expectation,
            availability: candidateReview.value.availability,
            interview: candidateReview.value.interview,
            interviewer_name: reviewer_name.value,
            interviewer_email: reviewer_email.value,
            evaluation_field: candidateReview.value.evaluation_field,
            rating: candidateReview.value.rating,
            observations: candidateReview.value.observations,
            approved: candidateReview.value.approved,
            review_date: candidateReview.value.review_date
        });

        if (response.data && response.data.success) {
            toast.add({ severity: 'success', summary: 'Success', detail: 'Review submitted successfully', life: 3000 });
            // Optionally clear the form after successful submission
            candidateReview.value = {
                process: '',
                salary_expectation: null,
                availability: '',
                interview: '',
                evaluation_field: '',
                rating: null,
                observations: '',
                approved: '',
                review_date: new Date().toISOString().slice(0, 19).replace('T', ' ')
            };
            // Refresh the reviews list
            await getCandidateReviews(candidateDetails.value.email);
        } else {
            toast.add({ severity: 'error', summary: 'Error', detail: response.data.error || 'Failed to submit review', life: 3000 });
        }
    } catch (error) {
        console.error('Error submitting review:', error);
        toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to submit review', life: 3000 });
    }
};
// Helper function to get the auth token from cookies
function getAuthToken() {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; authToken=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

const getReviewerEmail = async () => {
    const token = getAuthToken();
    if (token) {
        try {
            const response = await fetch('https://www.googleapis.com/oauth2/v1/userinfo?alt=json&access_token=' + token);
            const userInfo = await response.json();
            reviewer_email.value = userInfo.email;
        } catch (error) {
            console.error('Error fetching user info:', error);
        }
    }
};

// Fetch candidate details
const getCandidateDetails = async (email) => {
    try {
        const response = await axios.post(`/api/api`, { action: 'getCandidate', email });
        candidateDetails.value = response.data;
    } catch (error) {
        apiResponse.value = 'Error fetching candidate details: ' + error.message;
    }
};

// Fetch job categories
const fetchJobCategories = async () => {
    try {
        const response = await axios.post(`/api/api`, { action: 'listJobCategories' });
        categories.value = response.data;
    } catch (error) {
        console.error('Error fetching job categories:', error);
    }
};

const fetchJobSkillsets = async (categoryId) => {
    if (activeCategory.value === categoryId) {
        activeCategory.value = null;
        skillsets.value = [];
    } else {
        activeCategory.value = categoryId;
        try {
            const response = await axios.post(`/api/api`, {
                action: 'getSkillsetCategory',
                id: categoryId
            });

            const selectedCategory = categories.value.find(c => c.id === categoryId); // Find the category object
            skillsets.value = response.data.map(skillset => ({
                ...skillset,
                rating: skillset.rating || null,
                category_name: selectedCategory.category_name  // Add the category name to each skillset
            }));

        } catch (error) {
            console.error('Error fetching job skillsets:', error);
        }
    }
};


const getReviewerName = async () => {
    try {
        const response = await axios.post(`/api/api`, {
            action: 'getReviewerName',
            email: reviewer_email.value
        });
        reviewer_name.value = response.data.name; // Update this line
        reviewer_id.value = response.data.id;  // Add this line
    } catch (error) {
        console.error('Error fetching reviewer name and ID:', error);
    }
};

const setCandidateSkillSet = async (candidateId, category, skillset, rating, reviewerId, reviewerEmail, comment, timestamp) => {
    try {
        await axios.post(`/api/api`, {
            action: 'setCandidateSkillSet',
            candidate_id: candidateId,
            category,
            skillset,
            rating,
            reviewer_id: reviewerId,
            reviewer_email: reviewerEmail,
            comment,
            timestamp
        });
    } catch (error) {
        console.error('Error setting candidate skillset:', error);
    }
};


onMounted(() => {
    if (email) {
        getCandidateDetails(email);
     
    } else {
        apiResponse.value = 'No candidate email found in session.';
    }
    getReviewerEmail();
    getReviewerName();
    fetchJobCategories();
    getCandidateSkillsets(reviewer_email.value, email);
    listAvailableCertifications(); // Fetch available certifications
    getJobProcesses(); // Fetch job processes
});

const goBack = () => {
    router.back(); // Use router.back() to go to the previous page
}

const getCandidateSkillsets = async (reviewer_email, candidate_email) => {
    try {
        const response = await axios.post(`/api/api`, { 
            action: 'getCandidateSkillset', 
            reviewer_email, 
            candidate_email 
        });
        candidateSkillsets.value = response.data;
    } catch (error) {
        console.error('Error fetching candidate skillsets:', error);
    }
};

const deleteSkillset = (event, data) => {
    confirm.require({
        target: event.currentTarget,
        message: 'Are you sure you want to delete this skillset?',
        header: 'Confirmation',
        icon: 'pi pi-exclamation-triangle',
        accept: () => handleDelete(data),
    });
};

const closeConfirmation = () => {
    displayConfirmation.value = false; 
    skillsetToDelete.value = null;
};

// Modified confirmDelete function
const confirmDelete = (event, skillsetId) => {
    confirm.require({
        target: event.currentTarget,
        message: 'Are you sure you want to delete this skillset?',
        header: 'Confirmation',
        icon: 'pi pi-exclamation-triangle',
        accept: () => handleDelete(skillsetId),
    });
};
// Modified handleDelete function
const handleDelete = async (data) => {
    try {
        const response = await axios.post(`/api/api`, { action: 'deleteCandidateSkillset', id: data.id });

        // Check for successful deletion based on the updated response structure
        if (response.data.success) { // 'success' is now a boolean
            toast.add({ severity: 'success', summary: 'Success', detail: 'Skillset deleted successfully', life: 3000 });
            candidateSkillsets.value = candidateSkillsets.value.filter(skillset => skillset.id !== data.id); // Filter and update the array
        } else {
            toast.add({ severity: 'error', summary: 'Error', detail: response.data.error || 'Failed to delete skillset', life: 3000 });
        }
    } catch (error) {
        toast.add({ severity: 'error', summary: 'Error', detail: 'An error occurred while deleting the skillset', life: 3000 });
    }
};

const handleRatingChange = async (skillset, rating) => {
    const candidateId = candidateDetails.value.id;
    const candidateEmail = candidateDetails.value.email; // Get the candidate email
    const skillset_name = skillset.skillset_name; 
    const category = skillset.category_name; // Get the category name from the skillset data
    const comment = '';
    const timestamp = new Date().toISOString().slice(0, 19).replace('T', ' '); // Convert to MySQL datetime format

    // Ensure rating is within a valid range
    const validRating = Math.max(0, Math.min(5, parseInt(rating, 10))); // Assuming the valid range is 0-5

    const payload = {
        action: 'setCandidateSkillSet',
        candidate_id: candidateId,
        email: candidateEmail, // Include candidate email
        category, // Include category
        skillset: skillset_name,
        rating: validRating, // Ensure rating is valid
        reviewer_id: reviewer_id.value, // Include reviewer ID
        reviewer_email: reviewer_email.value, 
        comment, 
        timestamp
    };

    try {
        const response = await axios.post(`/api/api`, payload);
        if (response.data && response.data.success) {
            toast.add({ severity: 'success', summary: 'Success', detail: 'Skillset rating saved successfully', life: 3000 });

            // Update the skillset's rating in the skillsets array
            const skillsetIndex = skillsets.value.findIndex(s => s.id === skillset.id);
            if (skillsetIndex > -1) {
                skillsets.value[skillsetIndex].rating = validRating; 
            }

            // Add the skillset ID to reviewedSkillsets
            reviewedSkillsets.value.push(skillset.id);

            // Refresh the candidate skillsets
            await getCandidateSkillsets(reviewer_email.value, candidateEmail);
        } else {
            toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to save rating', life: 3000 });
        }
    } catch (error) {
        console.error('Error setting candidate skillset:', error);
        toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to save rating', life: 3000 });
    }
};


const handleRatingHover = (skillset, hoverRating) => {
    skillset.hoverRating = hoverRating; // Update the hoverRating for the skillset
};



watch(searchQuery, (newQuery) => {
    filteredCertifications.value = availableCertifications.value.filter(cert =>
        cert.certification.toLowerCase().includes(newQuery.toLowerCase())
    );
});

watch(() => candidateReview.interview, (newInterview) => {
    if (newInterview === 'Second Interview' || newInterview === 'Additional Interview') {
        candidateReview.salary_expectation = 0;
        candidateReview.availability = 0;
    }
});
const addCertificationToCandidate = async (certification) => {
    try {
        const response = await axios.post(`/api/api`, {
            action: 'addCandidateCertification',
            email: candidateDetails.value.email,
            certification: certification.certification,
        });
        if (response.data.success) {
            toast.add({ severity: 'success', summary: 'Success', detail: 'Certification added successfully' });
          
        } else {
            toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to add certification. Certification already registered.' });
        }
    } catch (error) {
        console.error('Error adding certification:', error.message);
        toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to add certification' });
    }
};
const listAvailableCertifications = async () => {
    try {
        const response = await axios.post(`/api/api`, { action: 'listCertifications' });
        if (response.data && !response.data.error) {
            availableCertifications.value = response.data;
            filteredCertifications.value = availableCertifications.value; // Initialize filtered certifications
        } else {
            toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to fetch certifications' });
        }
    } catch (error) {
        console.error('Error fetching available certifications:', error.message);
        toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to fetch certifications' });
    }
};
</script>

<template>
    <div class="grid">
        <div class="col-12 lg:col-8">
            <div class="card ">
                <h5>Candidate Interview</h5>
                <div v-if="candidateDetails">
                    <p><strong>Name:</strong> {{ candidateDetails.name }}</p>
                    <p><strong>Email:</strong> {{ candidateDetails.email }}</p>
                    <p><strong>Phone Number:</strong> {{ candidateDetails.phone_number }}</p>
                    <p><strong>English Level:</strong> {{ candidateDetails.english_level }}</p>
                    <p><strong>Location:</strong> {{ candidateDetails.location }}</p>
                    <p><strong>Registration Date:</strong> {{ new Date(candidateDetails.created_at).toLocaleDateString() }}</p>
                    <p><strong>Reviewer:</strong> {{ reviewer_name }} / {{ reviewer_email }}</p>
                    <Button icon="pi pi-arrow-left" label="Back" @click="goBack" severity="secondary" outlined class="mb-2 mr-2" /> 
                </div>
                <div v-else>
                    <p>{{ apiResponse }}</p>
                </div>
            </div>
            <div class="card ">
                <h5>Interview Candidate </h5>
                <Accordion>
                    <AccordionTab header="Evaluate Skillsets">
                    <div class="grid skillset-grid">
                        <div class="col-12 md:col-6 skillset-categories">
                            <DataTable :value="categories" responsiveLayout="scroll" selectionMode="single" @row-select="onCategorySelect" dataKey="id" :scrollable="true"  :class="{'category-table': true}">
                                <Column field="category_name" header="Category Name">
                                <template #body="{data}">
                                    <div @click="fetchJobSkillsets(data.id)" :class="{ 'active-category': activeCategory === data.id }">
                                    {{ data.category_name }}
                                    </div>
                                </template>
                                </Column>
                            </DataTable>
                        </div>
                        <div class="col-12 md:col-6 skillset-details" v-if="activeCategory">
                            <DataTable :value="skillsets" responsiveLayout="scroll">
  <Column field="skillset_name" header="Skillset Name"></Column>
  <Column header="Rating [1-5]">
    <template #body="{ data }">
      <div class="rating-radio-container">
        <div v-for="n in 5" :key="n" class="radio-option">
          <RadioButton :inputId="'rating-' + data.id + '-' + n" name="ratingGroup" :value="n" v-model="data.rating" @change="() => handleRatingChange(data, n)" />
        </div>
      </div>
      <div class="rating-labels">  
        <label v-for="n in 5" :key="n" :for="'rating-' + data.id + '-' + n">{{ n }}</label>
      </div>
    </template>
  </Column>
</DataTable>

                            
                        </div>
                    </div>
                </AccordionTab>

                <AccordionTab header="Register Certifications (Optional)">
                    <p class="line-height-3 m-0">
                            <Button icon="pi pi-plus" label="Add Certifications" @click="showCertificationDialog = true" severity="warning" outlined class="mb-2 mr-2" />             </p>
                    </AccordionTab>
                    <AccordionTab header="Review Candidate">
                            <div class="card">
                                <div class="p-fluid formgrid grid">
                                    <div class="field col-12 md:col-3">
                                        <label for="process">Process</label>
                                        <Dropdown id="process" v-model="candidateReview.process" :options="jobProcesses" optionLabel="label" optionValue="value" placeholder="Select Process" />
                                    </div>
                                    <div class="field col-12 md:col-3">
                                        <label for="interview">Interview</label>
                                        <Dropdown id="interview" v-model="candidateReview.interview" :options="interviewStages" optionLabel="label" optionValue="value" placeholder="Select Interview Stage" />
                                    </div>
                                    <div v-if="candidateReview.interview !== 'Second Interview' && candidateReview.interview !== 'Additional Interview'" class="field col-12 md:col-3">
                                        <label for="salary_expectation">Salary Expectation</label>
                                        <InputNumber id="salary_expectation" v-model="candidateReview.salary_expectation" />
                                    </div>
                                    <div v-if="candidateReview.interview !== 'Second Interview' && candidateReview.interview !== 'Additional Interview'" class="field col-12 md:col-3">
                                        <label for="availability">Availability</label>
                                        <Dropdown id="availability" v-model="candidateReview.availability" :options="candidateAvailability" optionLabel="label" optionValue="value" placeholder="Candidate Availability" />
                                    </div>

                                    <div class="field col-12 md:col-6">
                                        <label for="evaluation_field">Evaluation Field</label>
                                        <Dropdown id="evaluation_field" v-model="candidateReview.evaluation_field" :options="evaluationFields" optionLabel="label" optionValue="value" placeholder="Select Evaluation Field" />
                                    </div>
                                    <div class="field col-12 md:col-3">
                                        <label for="rating">Rating</label>
                                        <Dropdown id="rating" v-model="candidateReview.rating" :options="ratingOptions" optionLabel="label" optionValue="value" placeholder="Select Rating" />
                                    </div>
                                    <div class="field col-12 md:col-3">
                                        <label for="approved">Approved</label>
                                        <Dropdown id="approved" v-model="candidateReview.approved" :options="approvalOptions" optionLabel="label" optionValue="value" placeholder="Select Approval" />
                                    </div>
                                    <div class="field col-12">
                                        <label for="observations">Observations</label>
                                        <Textarea id="observations" rows="4" v-model="candidateReview.observations" />
                                    </div>

                                    <div class="field col-12 md:col-3">
                                        <label for="review_date">Review Date</label>
                                        <InputText id="review_date" type="text" v-model="candidateReview.review_date" :disabled="true" />
                                    </div>
                                </div>
                            </div>
                        </AccordionTab>
                </Accordion>
                <Button label="Submit Review" class="mr-2 mb-2" @click="confirmSubmitReview"></Button>
            </div>
         </div>
         <div class="col-12 lg:col-4">
            <div class="card">
                <h5>Results</h5>
                <div class="card">
                    <h6>Candidate Skillsets</h6>
                    <DataTable :value="candidateSkillsets" responsiveLayout="scroll" :scrollable="true" scrollHeight="70vh" scrollDirection="vertical">
                        <Column field="skillset" header="Skillset"></Column>
                        <Column field="rating" header="Rating">
                            <template #body="{ data }">
                                <Rating v-model="data.rating" :readonly="true" :cancel="false" />
                            </template>
                        </Column>
                        <Column header="Actions" class="actions-column" frozen alignFrozen="right">
                            <template #body="slotProps">
                                <div style="display: flex; justify-content: flex-end;">
                                    <Button icon="pi pi-trash" severity="danger" text raised rounded class="mb-2 mr-2" @click="confirmDelete($event, slotProps.data)" />
                                </div>
                            </template>
                        </Column>
                    </DataTable>
                </div>
            </div>
         </div>
         <div class="col-12 lg:col-8 candidate-interview-container">
         </div>
    </div>
    <Dialog header="Add Certifications" v-model:visible="showCertificationDialog" :modal="true" :closable="true" :style="{ width: '100%', maxWidth: '100%' }" class="responsive-dialog">
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
    <Toast />

    <ConfirmDialog />
</template>

<style scoped>
.rating-submit-container {
    display: flex;
    align-items: center;
}

.submit-button {
    margin-left: 10px;
}
.rating-radio-container {
  display: flex;
  align-items: center;
  justify-content: space-between; /* Distribute radio buttons evenly */
}

.rating-labels {
  display: flex;
  justify-content: space-between; /* Distribute labels evenly */
  margin-top: -1rem; /* Add some space between radio buttons and labels */
  font-size: 0.8rem; /* Adjust the font size if needed */
}

.radio-option {
  /* You can remove margin-right here if you're distributing evenly with flexbox */
}

.responsive-dialog {
    max-width: 50vw; /* Default for larger screens */
}

@media (max-width: 768px) {
    .responsive-dialog {
        width: 100% !important;
        max-width: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
        left: 0 !important;
        top: 0 !important;
        transform: none !important;
        border-radius: 0 !important;
    }
}

</style>