<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import Rating from 'primevue/rating';
import Accordion from 'primevue/accordion';
import AccordionTab from 'primevue/accordiontab';
import Tree from 'primevue/tree';
import Button from 'primevue/button';
import DataTable from 'primevue/datatable'; // Import DataTable
import Column from 'primevue/column';    // Import Column
import { useToast } from 'primevue/usetoast';
import { useConfirm } from 'primevue/useconfirm';
import Dialog from 'primevue/dialog';





const displayConfirmation = ref(false);
const skillsetToDelete = ref(null); 
const candidateDetails = ref(null);
const apiResponse = ref('');
const categories = ref([]);
const skillsets = ref([]);
const reviewer_id = ref(null); // Refactor this line
const reviewer_email = ref('juan.otalvaro@samanagroup.co');
const reviewer_name = ref('');
const reviewedSkillsets = ref([]);
const candidateSkillsets = ref([]);
const email = sessionStorage.getItem('candidateEmail');
const router = useRouter(); // Use the router instance
const toast = useToast(); // Use PrimeVue's toast
const confirm = useConfirm(); // Use PrimeVue's confirm service
const activeCategory = ref(null);


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
        const response = await axios.post(`/api/apitest`, { action: 'getCandidate', email });
        candidateDetails.value = response.data;
    } catch (error) {
        apiResponse.value = 'Error fetching candidate details: ' + error.message;
    }
};

// Fetch job categories
const fetchJobCategories = async () => {
    try {
        const response = await axios.post(`/api/apitest`, { action: 'listJobCategories' });
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
            const response = await axios.post(`/api/apitest`, {
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
        const response = await axios.post(`/api/apitest`, {
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
        await axios.post(`/api/apitest`, {
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
});

const goBack = () => {
    router.back(); // Use router.back() to go to the previous page
}

const getCandidateSkillsets = async (reviewer_email, candidate_email) => {
    try {
        const response = await axios.post(`/api/apitest`, { 
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
        const response = await axios.post(`/api/apitest`, { action: 'deleteCandidateSkillset', id: data.id });

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
        const response = await axios.post(`/api/apitest`, payload);
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
                                    <Column header="Rating">
                                        <template #body="{ data }">
                                            <div class="rating-submit-container">
                                                <Rating 
                                                    v-model="data.ratingInput" 
                                                    cancel="false" 
                                                    @change="(e) => handleRatingChange(data, activeCategory, e.value)" 
                                                />
                                            </div>
                                        </template>
                                    </Column>
                                </DataTable>
                            
                        </div>
                    </div>
                </AccordionTab>

                <AccordionTab header="Register Certifications (Optional)">
                    <p class="line-height-3 m-0">
                        Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo
                        enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Consectetur, adipisci velit, sed quia non numquam eius modi.
                    </p>
                </AccordionTab>
                <AccordionTab header="Review Candidate">
                    <p class="line-height-3 m-0">
                        At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi sint occaecati cupiditate non provident, similique sunt in
                        culpa qui officia deserunt mollitia animi, id est laborum et dolorum fuga. Et harum quidem rerum facilis est et expedita distinctio. Nam libero tempore, cum soluta nobis est eligendi optio cumque nihil impedit quo minus.
                    </p>
                </AccordionTab>
                </Accordion>
                <Button icon="pi pi-check-circle" label="Submit Review" severity="success" outlined class="mb-2 mr-2" /> 
            </div>
         </div>
         <div class="col-12 lg:col-4">
            <div class="card">
                <h5>Results</h5>
                <div class="card">
                    <h6>Candidate Skillsets</h6>
                    <DataTable :value="candidateSkillsets" responsiveLayout="scroll">
                        <Column field="skillset" header="Skillset"></Column>
                        <Column field="rating" header="Rating">
                            <template #body="{ data }">
                                <Rating v-model="data.rating" :readonly="true" :cancel="false" />
                            </template>
                        </Column>
                        <Column header="Actions" class="actions-column">
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
    <Toast />
    <ConfirmPopup />
</template>

<style scoped>
.rating-submit-container {
    display: flex;
    align-items: center;
}

.submit-button {
    margin-left: 10px;
}
</style>