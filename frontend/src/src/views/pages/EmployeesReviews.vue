<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import { useToast } from 'primevue/usetoast';
import Rating from 'primevue/rating';
import Dialog from 'primevue/dialog';
import ConfirmPopup from 'primevue/confirmpopup';
import Button from 'primevue/button';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Accordion from 'primevue/accordion';
import AccordionTab from 'primevue/accordiontab';
import { useConfirm } from 'primevue/useconfirm';
import ConfirmDialog from 'primevue/confirmdialog';
import Dropdown from 'primevue/dropdown';
import Tooltip from 'primevue/tooltip';

//redirects to unauthorized if the user role is lower than the pagerole
import { getPageAuthorization } from '@/utils/utils';
const pageRole = 3; // Set the required role for this page
getPageAuthorization(pageRole);



const displayConfirmation = ref(false);
const skillsetToDelete = ref(null); 
const employeeDetails = ref(null);
const apiResponse = ref('');
const categories = ref([]);
const skillsets = ref([]);
const reviewer_id = ref(null);
const reviewer_email = ref(document.cookie.split('; ').find(row => row.startsWith('userEmail')).split('=')[1]);
const reviewer_name = ref('');
const reviewedSkillsets = ref([]);
const employeeSkillsets = ref([]);
const email = sessionStorage.getItem('employeeEmail');
const router = useRouter();
const toast = useToast();
const activeCategory = ref(null);
const confirm = useConfirm();
const employeeReviews = ref([]);
const showObservations = ref({});
const idFrozen = ref(false); // Add this line for dynamic toggling


const evaluationFields = [
    { label: 'Technical Evaluation', value: 'Technical Evaluation' },
    { label: 'Yearly Evaluation', value: 'Yearly Evaluation' },
    { label: 'HR Evaluation', value: 'HR Evaluation' },
    { label: 'Skillsets Evaluation', value: 'Skillsets Evaluation' },
    { label: 'English Evaluation', value: 'English Evaluation' },
    { label: 'Certification Goals', value: 'Certification Goals' }
];

const ratingOptions = [
    { label: '1 - Unsatisfactory', value: 1 },
    { label: '2 - Below Expectations', value: 2 },
    { label: '3 - Meet Expectations', value: 3 },
    { label: '4 - Exceeds Expectations', value: 4 },
    { label: '5 - Outstanding', value: 5 }
];

const publicOptions = ref([
    { label: 'YES', value: 'YES' },
    { label: 'NO', value: 'NO' }
]);

const toggleObservations = (reviewId) => {
    showObservations.value[reviewId] = !showObservations.value[reviewId];
};

const getEmployeeReviews = async (email) => {
    try {
        const response = await axios.post(`/api/apitest`, {
            action: 'listEmployeeReviews',
            email
        });
        const reviews = response.data;

        for (const review of reviews) {
            const reviewerResponse = await axios.post(`/api/apitest`, {
                action: 'getReviewerName',
                email: review.reviewer_email
            });
            review.reviewer_name = reviewerResponse.data.name || 'Unknown';
           
        }

        employeeReviews.value = reviews;
    } catch (error) {
        console.error('Error fetching employee reviews:', error);
    }
};

const getEmployeeDetails = async (email) => {
    try {
        const response = await axios.post(`/api/apitest`, { action: 'getEmployee', email });
        employeeDetails.value = response.data;
        review.value.employee_id = response.data.ID;

    } catch (error) {
        apiResponse.value = 'Error fetching employee details: ' + error.message;
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

const review = ref({
    employee_id: '',
    email: email,
    evaluation_field: '',
    rating: null,
    observations: '',
    reviewer_email: reviewer_email.value,
    date: new Date().toISOString().split('T')[0] 
});

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

            skillsets.value = response.data.map(skillset => ({
                ...skillset,
                category_name: categories.value.find(c => c.id === categoryId).category_name // Add the category name to each skillset
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
        reviewer_name.value = response.data.name;
        reviewer_id.value = response.data.id;

    } catch (error) {
        console.error('Error fetching reviewer name and ID:', error);
    }
};

const setEmployeeSkillSet = async (employeeId, category, skillset, rating, reviewerId, reviewerEmail, comment, timestamp) => {
    try {
        await axios.post(`/api/apitest`, {
            action: 'addEmployeeSkillset',
            employee_id: employeeId,
            email: employeeDetails.value.primaryEmail,
            category,
            skillset,
            rating,
            reviewer_email: reviewerEmail,
            date: timestamp
        });
    } catch (error) {
        console.error('Error setting employee skillset:', error);
    }
};

onMounted(() => {
    if (email) {
        getEmployeeDetails(email);
        getEmployeeReviews(email); // Fetch employee reviews

    } else {
        apiResponse.value = 'No employee email found in session.';
    }
    getReviewerName();
    fetchJobCategories();
    getEmployeeSkillsets(email);
});

const goBack = () => {
    router.back();
};

const getEmployeeSkillsets = async (email) => {
    try {
        const response = await axios.post(`/api/apitest`, { 
            action: 'listEmployeeSkillsets', 
            email 
        });

        // Ensure reviewer_name is populated
        const skillsets = response.data;
        for (const skillset of skillsets) {
            const reviewerResponse = await axios.post(`/api/apitest`, {
                action: 'getReviewerName',
                email: skillset.reviewer_email
            });
            skillset.reviewer_name = reviewerResponse.data.name || 'Unknown';
        }
        
        employeeSkillsets.value = skillsets;
    } catch (error) {
        console.error('Error fetching employee skillsets:', error);
    }
};


const confirmDelete = (event, skillsetId) => {
    confirm.require({
        target: event.currentTarget,
        message: 'Are you sure you want to delete this skillset?',
        header: 'Confirmation',
        icon: 'pi pi-exclamation-triangle',
        accept: () => handleDelete(skillsetId),
    });
};


const handleDelete = async (skillset) => {
    try {
        const response = await axios.post(`/api/apitest`, { action: 'deleteEmployeeSkillset', id: skillset.id });
        
        if (response.data.success) {
            toast.add({ severity: 'success', summary: 'Success', detail: 'Skillset deleted successfully', life: 3000 });
        } else {
            throw new Error(response.data.error || 'Failed to delete skillset');  // Throw an error to trigger the catch block
        }
    } catch (error) {
        console.error('Error deleting skillset:', error); // Log the error for debugging
        toast.add({ severity: 'error', summary: 'Error', detail: error.message || 'An error occurred while deleting the skillset', life: 3000 });
    }

    // Always filter out the deleted skillset
    employeeSkillsets.value = employeeSkillsets.value.filter(s => s.id !== skillset.id);
};


const handleRatingChange = async (skillset, rating) => {
    const employeeId = employeeDetails.value.ID;
    const skillset_name = skillset.skillset_name; 
    const category = skillset.category_name;
    const comment = '';
    const timestamp = new Date().toISOString().slice(0, 19).replace('T', ' ');

    const validRating = Math.max(0, Math.min(5, parseInt(rating, 10)));

    const payload = {
        action: 'addEmployeeSkillset',
        employee_id: employeeId,
        email: employeeDetails.value.primaryEmail,
        category,
        skillset: skillset_name,
        rating: validRating,
        reviewer_email: reviewer_email.value, 
        date: timestamp
    };

    try {
        const response = await axios.post(`/api/apitest`, payload);
        if (response.data && response.data.success) {
            toast.add({ severity: 'success', summary: 'Success', detail: 'Skillset rating saved successfully', life: 3000 });

            const skillsetIndex = skillsets.value.findIndex(s => s.id === skillset.id);
            if (skillsetIndex > -1) {
                skillsets.value[skillsetIndex].rating = validRating; 
            }

            reviewedSkillsets.value.push(skillset.id);

            await getEmployeeSkillsets(employeeDetails.value.primaryEmail);
        } else {
            toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to save rating', life: 3000 });
        }
    } catch (error) {
        console.error('Error setting employee skillset:', error);
        toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to save rating', life: 3000 });
    }
};

const handleRatingHover = (skillset, hoverRating) => {
    skillset.hoverRating = hoverRating;
};

const submitReview = async () => {
    if (!review.value.evaluation_field || review.value.rating === null) {
        toast.add({ severity: 'warn', summary: 'Warning', detail: 'Please fill out all required fields.', life: 3000 });
        return;
    }

    try {
        const response = await axios.post(`/api/apitest`, {
            action: 'addEmployeeReview',
            employee_id: review.value.employee_id,
            email: review.value.email,
            evaluation_field: review.value.evaluation_field,
            rating: review.value.rating,
            reviewer_email: review.value.reviewer_email,
            observations: review.value.observations,
            date: review.value.date,
            public: review.value.public // Include the public value
        });

        if (response.data && response.data.success) {
            toast.add({ severity: 'success', summary: 'Success', detail: 'Review submitted successfully', life: 3000 });
            await getEmployeeReviews(employeeDetails.value.primaryEmail);

            // Optionally clear the form after successful submission
            review.value.evaluation_field = '';
            review.value.rating = null;
            review.value.observations = '';
            review.value.public = 'NO'; // Reset the public field to default value
        } else {
            toast.add({ severity: 'error', summary: 'Error', detail: response.data.error || 'Failed to submit review', life: 3000 });
        }
    } catch (error) {
        console.error('Error submitting review:', error);
        toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to submit review', life: 3000 });
    }
};

const confirmSubmitReview = () => {
    confirm.require({
        message: 'Are you sure to submit your review? This action cannot be undone!',
        header: 'Confirmation',
        icon: 'pi pi-exclamation-triangle',
        accept: () => submitReview(),
    });
};
</script>

<template>
    <div class="grid">
        <div class="col-12 lg:col-6 p-fluid">
            <div class="card">
                <h5>Employee Details</h5>
                <div v-if="employeeDetails">
                    <p><strong>Name:</strong> {{ employeeDetails.fullName }}</p>
                    <p><strong>Email:</strong> {{ employeeDetails.primaryEmail }}</p>
                    <p><strong>Role:</strong> {{ employeeDetails.companyRole }}</p>
                    <p><strong>Contract Type:</strong> {{ employeeDetails.contractType }}</p>
                    <p><strong>Suspended:</strong> {{ employeeDetails.suspended }}</p>
                    <p><strong>Creation Date:</strong> {{ employeeDetails.creationDate }}</p>
                    <Button icon="pi pi-arrow-left" label="Back" @click="goBack" severity="secondary" outlined class="mb-2 mr-2" /> 
                </div>
                <div v-else>
                    <p>{{ apiResponse }}</p>
                </div>
            </div>

            <div class="card">
                <h5>Employee Skillsets</h5>
                <Accordion>
                    <AccordionTab header="Evaluate Skillsets">
                        <div class="grid skillset-grid">
                            <div class="col-12 md:col-6 skillset-categories">
                                <DataTable :value="categories" responsiveLayout="scroll" selectionMode="single" @row-select="onCategorySelect" dataKey="id" :scrollable="true" :class="{'category-table': true}">
                                    <Column field="category_name" header="Category Name">
                                        <template #body="{ data }">
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
                    <AccordionTab header="Review Employee">
                        <div class="card">
                            <div class="p-fluid formgrid grid">
                                <div class="field col-12 md:col-2">
                                    <label for="employee_id">ID</label>
                                    <InputText id="employee_id" type="text" v-model="review.employee_id" :disabled="true" />
                                </div>
                                <div class="field col-12 md:col-10">
                                    <label for="employeeemail">Email</label>
                                    <InputText id="employeeemail" type="text" v-model="review.email" :disabled="true" />
                                </div>
                                <div class="field col-12 md:col-8">
                                    <label for="evaluation_field">Evaluation Field</label>
                                    <Dropdown id="evaluation_field" v-model="review.evaluation_field" :options="evaluationFields" optionLabel="label" optionValue="value" placeholder="Select Evaluation Field" />
                                </div>
                                <div class="field col-12 md:col-4">
                                    <label for="evaluation_rating">Rating</label>
                                    <Dropdown id="evaluation_rating" v-model="review.rating" :options="ratingOptions" optionLabel="label" optionValue="value" placeholder="Select Rating" />
                                </div>
                                <div class="field col-12">
                                    <label for="observations">Observations</label>
                                    <Textarea id="observations" rows="4" v-model="review.observations" />
                                </div>
                                <div class="field col-12 md:col-8">
                                    <label for="reviewer_email">Reviewer Email</label>
                                    <InputText id="reviewer_email" type="text" v-model="review.reviewer_email" :disabled="true" />
                                </div>
                                <div class="field col-12 md:col-4">
                                    <label for="evaluation_date">Date</label>
                                    <InputText id="evaluation_date" type="text" v-model="review.date" :disabled="true" />
                                </div>
                                <div class="field col-12 md:col-4">
                                    <label for="public">Is this a public review? (Employees will be able to see it)</label>
                                    <Dropdown id="public" v-model="review.public" :options="publicOptions" optionLabel="label" optionValue="value" placeholder="Select Public" />
                                </div>
                            </div>
                            <Button label="Submit Review" class="mr-2 mb-2" @click="confirmSubmitReview"></Button>
                        </div>
                    </AccordionTab>

                    
                </Accordion>
            </div>


        </div>
        <div class="col-12 lg:col-6 p-fluid">
            <div class="card">
           
            <div class="card">
                <h5>Employee Skillsets</h5>
                    <DataTable :value="employeeSkillsets" responsiveLayout="scroll" :scrollable="true" scrollHeight="70vh" scrollDirection="vertical">
                        <Column field="skillset" header="Skillset"></Column>
                        <Column field="rating" header="Rating">
                            <template #body="{ data }">
                                <Rating v-model="data.rating" :readonly="true" :cancel="false" v-tooltip="data.reviewer_name"/>
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
            <div class="card" v-if="employeeReviews.length">
                <h5>Employee Reviews</h5>
                <Timeline :value="employeeReviews" class="customized-timeline">
                    <template #marker="slotProps">
                        <small class="p-text-secondary">{{ new Date(slotProps.item.date).toLocaleDateString() }}</small>
                    </template>
                    <template #content="slotProps">
                        <Card>
                            <template #content>
                                <div class="flex flex-column">
                                    <strong>{{ slotProps.item.evaluation_field }}</strong>
                                            <div class="review-rating">
                                                <div class="review-interviewer">
                                                    <Rating :modelValue="slotProps.item.rating" :readonly="true" :cancel="false" />
                                                </div>
                                            </div>
                                    
                                    <div class="review-observations">
                                        <a href="#" @click.prevent="toggleObservations(slotProps.item.id)">Show/Hide Details</a>
                                        <div v-if="showObservations[slotProps.item.id]" class="observations">
                                           
                                       
                                            <p><strong>Observations:</strong> {{ slotProps.item.observations }}</p>
                                            <strong>Reviewer:</strong> {{ slotProps.item.reviewer_name }} ({{ slotProps.item.reviewer_email }})
                                        </div>
                                    </div>
                                </div>
                            </template>
                        </Card>
                    </template>
                </Timeline>
            </div>



            </div>


        </div>
    </div>
    <Toast />
    <ConfirmDialog />
</template>
<style scoped lang="scss">
.grid {
    display: flex;
    flex-wrap: wrap;
}

.card {
    width: 100%;
    margin-bottom: 1rem;
}

.skillset-grid {
    display: flex;
}

.skillset-categories,
.skillset-details {
    flex: 1;
    padding: 1rem;
}

.category-table .p-datatable-tbody > tr > td {
    cursor: pointer;
    text-align: center;
}

.active-category {
    background-color: #f0f0f0;
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

.actions-column {
    text-align: right;
}

.p-rating .p-rating-icon {
    color: #FFC107 !important; /* Yellow color for rating stars */
}

@media (max-width: 768px) {
    .skillsets-table {
        display: block;
        overflow-x: auto;
        white-space: nowrap;
    }
    .col-12 {
        width: 100% !important;
    }

    .card {
        margin-bottom: 1rem;
    }
}
.customized-timeline {
    .p-timeline-event-content {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .p-timeline-event-content .p-card {
        width: 100%;
    }
    .p-card-content {
        display: flex;
        flex-direction: column;
    }
    .observations {
        font-size: 1em;
        margin-top: 0.5rem;
    }
    .p-chip.success {
        background: #C8E6C9;
        color: #388E3C;
    }
    .p-chip.danger {
        background: #FFCDD2;
        color: #C62828;
    }
}

.review-rating {
    display: flex;
    justify-content: space-between;
    align-items: center;
}
</style>
