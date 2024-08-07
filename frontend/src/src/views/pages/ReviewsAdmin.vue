<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import Button from 'primevue/button';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Toast from 'primevue/toast';
import { useToast } from 'primevue/usetoast';
import { useConfirm } from 'primevue/useconfirm';
import ConfirmPopup from 'primevue/confirmpopup';
import InputText from 'primevue/inputtext';
import Dialog from 'primevue/dialog';
//redirects to unauthorized if the user role is lower than the pagerole
import { getPageAuthorization } from '@/utils/utils';
const pageRole = 5; // Set the required role for this page
getPageAuthorization(pageRole);

const toast = useToast();
const confirm = useConfirm();
const showDialog = ref(false);
const reviews = ref([]);

const publicOptions = ref([
  { label: 'YES', value: 'YES' },
  { label: 'NO', value: 'NO' }
]);

const dialogData = ref({
    id: null,
    employee_id: '',
    email: '',
    evaluation_field: '',
    rating: null,
    reviewer_email: '',
    observations: '',
    date: '',
    public: 'NO'
});


onMounted(fetchReviews);

async function fetchReviews() {
    try {
        const response = await axios.post(`/api/apitest`, { action: 'listAllReviews' });
        reviews.value = response.data;
    } catch (error) {
        console.error("Error fetching reviews:", error);
    }
}

function openReviewDialog(item = null) {
    dialogData.value = item
        ? { ...item }
        : {
            id: null,
            employee_id: '',
            email: '',
            evaluation_field: '',
            rating: null,
            reviewer_email: '',
            observations: '',
            date: '',
            public: 'NO'
        };
    showDialog.value = true;
}

async function handleAddOrEdit() {
    if (!dialogData.value.email.trim() || !dialogData.value.evaluation_field.trim()) {
        toast.add({ severity: 'warn', summary: 'Warning', detail: 'Email and Evaluation Field are required', life: 3000 });
        return;
    }

    const action = dialogData.value.id ? 'updateEmployeeReview' : 'addEmployeeReview';
    const payload = {
        action,
        ...dialogData.value
    };

    try {
        const response = await axios.post(`/api/apitest`, payload);

        if (response.data.success) {
            toast.add({ severity: 'success', summary: 'Success', detail: 'Review saved!', life: 3000 });
            fetchReviews();
            showDialog.value = false;
        } else {
            toast.add({ severity: 'error', summary: 'Error', detail: response.data.error || 'Failed to save review' });
        }
    } catch (error) {
        console.error(`Error adding/updating review:`, error);
        toast.add({ severity: 'error', summary: 'Error', detail: 'An error occurred', life: 3000 });
    }
}

async function handleDelete(id) {
    try {
        const response = await axios.post(`/api/apitest`, {
            action: 'deleteEmployeeReview',
            id: id,
        });

        if (response.data.success) {
            toast.add({ severity: 'success', summary: 'Success', detail: 'Review deleted!', life: 3000 });
            fetchReviews();
        } else {
            toast.add({ severity: 'error', summary: 'Error', detail: response.data.error || 'Failed to delete review' });
        }
    } catch (error) {
        console.error(`Error deleting review:`, error);
        toast.add({ severity: 'error', summary: 'Error', detail: 'An error occurred', life: 3000 });
    }
}

function confirmDelete(event, id) {
    confirm.require({
        target: event.currentTarget,
        message: `Are you sure you want to delete this review?`,
        header: 'Confirmation',
        icon: 'pi pi-exclamation-triangle',
        accept: () => handleDelete(id),
    });
}
</script>

<template>
    <div class="card">
        <div class="grid">
            <div class="col-12">
                <h5>Employee Reviews</h5>
                <DataTable :value="reviews" responsiveLayout="scroll" :bodyStyle="{ textAlign: 'right' }">
                    <Column field="email" header="Email"></Column>
                    <Column field="evaluation_field" header="Evaluation Field"></Column>
                    <Column field="rating" header="Rating"></Column>
                    <Column field="reviewer_email" header="Reviewer Email"></Column>
                    <Column field="observations" header="Observations"></Column>
                    <Column field="date" header="Date"></Column>
                    <Column field="public" header="Public"></Column>
                    <Column header="Actions" class="actions-column">
                        <template #body="slotProps">
                            <div style="display: flex; justify-content: flex-end;">
                                <Button icon="pi pi-pencil" severity="warning" text raised @click="openReviewDialog(slotProps.data)" />
                                <Button icon="pi pi-trash" severity="danger" text raised @click="confirmDelete($event, slotProps.data.id)" />
                            </div>
                        </template>
                    </Column>
                </DataTable>
                <Button label="Add Review" raised @click="openReviewDialog()" class="mt-3" />
                <div v-if="reviews.length == 0">Loading reviews...</div>
            </div>
        </div>
    </div>

    <Dialog v-model:visible="showDialog" header="Review Details" :modal="true" :closable="true" :style="{ width: '70vw' }">
        <template #footer>
            <Button label="Cancel" @click="showDialog = false" class="p-button-text" />
            <Button label="Save" @click="handleAddOrEdit" />
        </template>
        <div>
            <div class="p-fluid grid">
                <div class="field col-12">
                    <label for="employee_id">Employee ID</label>
                    <InputText v-model="dialogData.employee_id" id="employee_id" disabled/>
                </div>
                <div class="field col-12">
                    <label for="email">Email</label>
                    <InputText v-model="dialogData.email" id="email" disabled/>
                </div>
                <div class="field col-12">
                    <label for="evaluation_field">Evaluation Field</label>
                    <InputText v-model="dialogData.evaluation_field" id="evaluation_field" disabled/>
                </div>
                <div class="field col-12">
                    <label for="rating">Rating</label>
                    <InputText v-model="dialogData.rating" id="rating" type="number" disabled />
                </div>
                <div class="field col-12">
                    <label for="reviewer_email">Reviewer Email</label>
                    <InputText v-model="dialogData.reviewer_email" id="reviewer_email" disabled/>
                </div>
                <div class="field col-12">
                    <label for="observations">Observations</label>
                    <InputText v-model="dialogData.observations" id="observations" disabled/>
                </div>
                <div class="field col-12">
                    <label for="date">Date</label>
                    <InputText v-model="dialogData.date" id="date" type="date" disabled/>
                </div>
                <div class="field col-12">
                    <label for="public">Public</label>
                    <Dropdown v-model="dialogData.public" :options="publicOptions" optionLabel="label" optionValue="value" placeholder="Select Public" />
                </div>
            </div>
        </div>
    </Dialog>

    <Toast />
    <ConfirmPopup />
</template>

<style scoped>
.actions-column {
    text-align: center;
}
</style>