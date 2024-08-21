<script setup>
import { ref, onBeforeMount, computed } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import Tooltip from 'primevue/tooltip';
import { useToast } from 'primevue/usetoast';
import { useConfirm } from 'primevue/useconfirm';
import InputSwitch from 'primevue/inputswitch';
const confirm = useConfirm(); // Initialize confirm
const toast = useToast();


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
//Function to delete candidate
const deleteCandidate = async (id) => {
    try {
        const response = await axios.post(`/api/api`, {
            action: 'deleteCandidate',
            id: id
        });

        if (response.data.success) {
            candidatesList.value = candidatesList.value.filter(candidate => candidate.id !== id);
            toast.add({ severity: 'success', summary: 'Success', detail: 'Candidate deleted successfully', life: 3000 });
        } else {
            toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to delete candidate', life: 3000 });
        }
    } catch (error) {
        toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to delete candidate', life: 3000 });
    }
};
//function to update the candidate
const showEditDialog = ref(false); // State for controlling edit dialog visibility
const editedCandidate = ref({}); // Store the candidate being edited

const openEditDialog = (candidate) => {
    editedCandidate.value = { ...candidate }; // Clone the candidate object to avoid direct mutations
    showEditDialog.value = true; // Show the dialog
};

const updateCandidate = async () => {
    try {
        const response = await axios.post(`/api/api`, {
            action: 'updateCandidate',
            id: editedCandidate.value.id,
            name: editedCandidate.value.name,
            email: editedCandidate.value.email,
            phone_number: editedCandidate.value.phone_number,
            location: editedCandidate.value.location,
            english_level: editedCandidate.value.english_level,
            profile_photo: editedCandidate.value.profile_photo,
            candidate_cv: editedCandidate.value.candidate_cv,
            enabled: editedCandidate.value.enabled
        });

        if (response.data.success) {
            const index = candidatesList.value.findIndex(candidate => candidate.id === editedCandidate.value.id);
            if (index !== -1) {
                candidatesList.value[index] = { ...editedCandidate.value };
            }
            toast.add({ severity: 'success', summary: 'Success', detail: 'Candidate updated successfully', life: 3000 });
            showEditDialog.value = false; // Close the dialog after successful update
        } else {
            toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to update candidate', life: 3000 });
        }
    } catch (error) {
        toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to update candidate', life: 3000 });
    }
};

const listCandidateProfiles = async () => {
    try {
        const response = await axios.post(`/api/api`, {
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
        const response = await axios.post(`/api/api`, {
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
                <h5>Candidates Admin</h5>
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
                            <Button icon="pi pi-search" text raised outlined severity="success" @click="viewProfileDetails(data.email)" v-tooltip="'View Profile Details'" />
                            <Button icon="pi pi-pencil" severity="info" outlined text raised @click="openEditDialog(data)" v-tooltip="'Edit Candidate'" />
                            <Button icon="pi pi-trash" severity="danger" outlined text raised @click="() => $confirm.require({
                                    message: 'Are you sure you want to delete this candidate?',
                                    header: 'Confirm',
                                    icon: 'pi pi-exclamation-triangle',
                                    accept: () => deleteCandidate(data.id)
                                })" v-tooltip="'Delete Candidate'"/>


                        </template>
                    </Column>
                </DataTable>
            </div>
        </div>
        <Dialog header="Edit Candidate" v-model:visible="showEditDialog" class="col-11 md:col-6">
            <form @submit.prevent="updateCandidate">
                <div class="p-fluid">
                    <div class="field">
                        <label for="name">Name</label>
                        <InputText v-model="editedCandidate.name" id="name" type="text" required />
                    </div>
                    <div class="field">
                        <label for="email">Email</label>
                        <InputText v-model="editedCandidate.email" id="email" type="email" required disabled/>
                    </div>
                    <div class="field">
                        <label for="phone_number">Phone Number</label>
                        <InputText v-model="editedCandidate.phone_number" id="phone_number" type="text" />
                    </div>
                    <div class="field">
                        <label for="location">Location</label>
                        <InputText v-model="editedCandidate.location" id="location" type="text" disabled/>
                    </div>
                    <div class="field">
                        <label for="english_level">English Level</label>
                        <InputText v-model="editedCandidate.english_level" id="english_level" type="text" disabled/>
                    </div>
                    <div class="field">
                        <label for="profile_photo">Profile Photo</label>
                        <InputText v-model="editedCandidate.profile_photo" id="profile_photo" type="text" disabled />
                    </div>
                    <div class="field">
                        <label for="candidate_cv">Candidate CV</label>
                        <InputText v-model="editedCandidate.candidate_cv" id="candidate_cv" type="text" disabled/>
                    </div>
                    <div class="field">
                        <label for="enabled">Status</label>
                        <InputSwitch v-model="editedCandidate.enabled" :true-value="1" :false-value="0" />
                        
                    </div>
                </div>
                <Button label="Update Candidate" type="submit" class="w-full" />
            </form>
        </Dialog>
    </div>

    <Toast />
<ConfirmDialog /> <!-- Add this component to use the confirmation dialog -->

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