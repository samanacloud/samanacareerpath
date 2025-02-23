<template>
    <div class="card">
        <Toast />
        <ConfirmDialog />

        <!-- Header Section -->
        <div class="flex flex-col gap-4">
            <div class="flex items-center justify-between">
                <div>
                    <h1 class="text-2xl font-medium text-900">Candidates</h1>
                    <p class="text-sm font-medium text-500">Manage your organization's candidates</p>
                </div>
                <Button 
                    label="Add Candidate" 
                    icon="pi pi-plus" 
                    outlined 
                    raised 
                    class="bg-white" 
                    @click="openNewCandidate" 
                />
            </div>

            <!-- Search and Filter Bar -->
            <div class="flex justify-between items-center bg-white p-4 rounded-lg shadow-sm">
                <IconField class="w-96">
                    <InputIcon class="pi pi-search" />
                    <InputText 
                        v-model="filters['global'].value" 
                        placeholder="Search candidates..." 
                        class="w-full"
                    />
                </IconField>
                <div class="flex items-center gap-3">
                    <label class="text-gray-600">Show Inactive</label>
                    <ToggleSwitch v-model="showInactive" @change="filterCandidates" />
                </div>
            </div>

            <!-- Candidates List -->
            <div class="bg-white rounded-lg shadow-sm">
                <DataTable
                    :value="candidates"
                    :loading="loading"
                    dataKey="id"
                    :paginator="true"
                    :rows="10"
                    :rowsPerPageOptions="[5, 10, 20, 50]"
                    responsiveLayout="scroll"
                    v-model:filters="filters"
                    filterDisplay="menu"
                    :globalFilterFields="['candidateName', 'email', 'country']"
                    class="p-4"
                >
                    <Column field="candidateName" header="Name" sortable>
                        <template #body="{ data }">
                            <div class="flex items-center gap-2">
                                <div class="w-8 h-8 rounded-full bg-primary-100 flex items-center justify-center">
                                    {{ data.candidateName.charAt(0).toUpperCase() }}
                                </div>
                                <div class="flex flex-col">
                                    <span class="font-medium">{{ data.candidateName }}</span>
                                    <span class="text-sm text-gray-500">{{ data.email }}</span>
                                </div>
                            </div>
                        </template>
                    </Column>

                    <Column field="country" header="Country" sortable>
                        <template #body="{ data }">
                            <span class="text-gray-700">{{ data.country }}</span>
                        </template>
                    </Column>

                    <Column field="phone" header="Phone" sortable>
                        <template #body="{ data }">
                            <span class="text-gray-700">{{ data.phone }}</span>
                        </template>
                    </Column>

                    <Column field="candidateCV" header="CV" sortable>
                        <template #body="{ data }">
                            <a 
                                v-if="data.candidateCV" 
                                :href="data.candidateCV" 
                                target="_blank"
                                class="text-primary-500 hover:underline"
                            >
                                View CV
                            </a>
                            <span v-else class="text-gray-400">No CV</span>
                        </template>
                    </Column>

                    <Column field="status" header="Status" sortable>
                        <template #body="{ data }">
                            <Tag 
                                :severity="data.status === 'active' ? 'success' : 'danger'" 
                                :value="data.status"
                                class="text-xs"
                            />
                        </template>
                    </Column>

                    <Column field="recruitmentProcessName" header="Recruitment Process" sortable>
                        <template #body="{ data }">
                            <span class="text-gray-700">
                                {{ data.recruitmentProcessName || 'Not assigned' }}
                            </span>
                        </template>
                    </Column>

                    <Column :exportable="false" style="width:100px">
                        <template #body="{ data }">
                            <div class="flex gap-2">
                                <!-- Edit and Delete buttons removed -->
                            </div>
                        </template>
                    </Column>
                </DataTable>
            </div>
        </div>

        <!-- Candidate Dialog -->
        <Dialog 
            v-model:visible="candidateDialog" 
            :style="{ width: '95%', maxWidth: '900px' }" 
            header="Candidate Details" 
            :modal="true" 
            class="p-fluid"
        >
            <form @submit.prevent="saveCandidate">
                <div class="card flex flex-col gap-4">
                    <Fieldset 
                        legend="Basic Information" 
                        :toggleable="true" 
                        class="mb-4 p-2 md:p-3"
                    >
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div class="flex flex-col gap-2">
                                <FloatLabel variant="on">
                                    <InputText 
                                        id="candidateName" 
                                        v-model="candidate.candidateName" 
                                        :class="{'p-invalid': submitted && !candidate.candidateName}"
                                        autofocus
                                    />
                                    <label for="candidateName">Full Name*</label>
                                </FloatLabel>
                                <small class="p-error" v-if="submitted && !candidate.candidateName">Name is required.</small>
                            </div>
                            
                            <div class="flex flex-col gap-2">
                                <FloatLabel variant="on">
                                    <InputText 
                                        id="email" 
                                        v-model="candidate.email"
                                        :class="{'p-invalid': !isValidEmail(candidate.email) && candidate.email}"
                                        @input="validateEmail"
                                    />
                                    <label for="email">Email*</label>
                                </FloatLabel>
                                <Message 
                                    v-if="candidate.email && !isValidEmail(candidate.email)" 
                                    severity="error" 
                                    variant="simple" 
                                    size="small"
                                >
                                    Please enter a valid email address
                                </Message>
                                <small class="p-error" v-if="submitted && !candidate.email">Email is required.</small>
                            </div>

                            <div class="flex flex-col gap-2">
                                <FloatLabel variant="on">
                                    <AutoComplete
                                        id="country"
                                        v-model="candidate.country"
                                        :suggestions="filteredCountries"
                                        @complete="searchCountries"
                                        :field="'name'"
                                        optionLabel="name"
                                        @item-select="onCountrySelect"
                                        :class="{'p-invalid': submitted && !candidate.country}"
                                    />
                                    <label for="country">Country*</label>
                                </FloatLabel>
                                <small class="p-error" v-if="submitted && !candidate.country">Country is required.</small>
                            </div>

                            <div class="flex flex-col gap-2">
                                <FloatLabel variant="on">
                                    <InputText 
                                        id="phone" 
                                        v-model="candidate.phone"
                                        :class="{'p-invalid': submitted && !candidate.phone}"
                                    />
                                    <label for="phone">Phone*</label>
                                </FloatLabel>
                                <small class="p-error" v-if="submitted && !candidate.phone">Phone is required.</small>
                            </div>

                            <div class="flex flex-col gap-2">
                                <FloatLabel variant="on">
                                    <InputText 
                                        id="candidateCV" 
                                        v-model="candidate.candidateCV"
                                        placeholder="https://example.com/cv.pdf"
                                    />
                                    <label for="candidateCV">CV URL</label>
                                </FloatLabel>
                            </div>

                            <div class="flex flex-col gap-2">
                                <div class="flex items-center gap-2">
                                    <ToggleSwitch 
                                        v-model="candidateStatus" 
                                        id="status"
                                    />
                                    <span class="text-sm text-surface-500">{{ candidateStatus ? 'Active' : 'Inactive' }}</span>
                                </div>
                            </div>

                            <div class="flex flex-col gap-2">
                                <FloatLabel variant="on">
                                    <InputText 
                                        id="recruitmentProcessId" 
                                        v-model="candidate.recruitmentProcessId"
                                        placeholder="Process ID"
                                    />
                                    <label for="recruitmentProcessId">Recruitment Process ID</label>
                                </FloatLabel>
                            </div>

                            <div class="flex flex-col gap-2">
                                <FloatLabel variant="on">
                                    <InputText 
                                        id="recruitmentProcessName" 
                                        v-model="candidate.recruitmentProcessName"
                                        placeholder="Process Name"
                                    />
                                    <label for="recruitmentProcessName">Recruitment Process Name</label>
                                </FloatLabel>
                            </div>
                        </div>
                    </Fieldset>
                    
                    <div class="flex justify-end gap-2 mt-4">
                        <Button 
                            type="button" 
                            label="Cancel" 
                            icon="pi pi-times" 
                            outlined 
                            @click="hideDialog" 
                        />
                        <Button 
                            type="submit"
                            label="Save" 
                            icon="pi pi-check" 
                        />
                    </div>
                </div>
            </form>
        </Dialog>

        <!-- Delete Confirmation Dialog -->
        <Dialog
            v-model:visible="deleteCandidateDialog"
            :style="{ width: '450px' }"
            header="Delete Candidate"
            :modal="true"
            class="p-fluid"
        >
            <div class="flex flex-col gap-4">
                <div class="text-red-600 font-semibold">Warning: This action cannot be undone</div>
                
                <div class="text-gray-700">
                    To confirm deletion, type the candidate's email:
                    <span class="font-semibold">{{ candidateToDelete?.email }}</span>
                </div>
                
                <div class="flex flex-col gap-2">
                    <InputText
                        v-model="confirmationEmail"
                        :class="{'p-invalid': deleteSubmitted && confirmationEmail !== candidateToDelete?.email}"
                        placeholder="Enter candidate email"
                    />
                    <small class="p-error" v-if="deleteSubmitted && confirmationEmail !== candidateToDelete?.email">
                        Email doesn't match
                    </small>
                </div>
            </div>
            
            <template #footer>
                <div class="flex justify-end gap-2">
                    <Button
                        label="Cancel"
                        icon="pi pi-times"
                        outlined
                        @click="deleteCandidateDialog = false"
                    />
                    <Button
                        label="Delete"
                        icon="pi pi-trash"
                        severity="danger"
                        @click="handleDeleteConfirm"
                    />
                </div>
            </template>
        </Dialog>
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useToast } from 'primevue/usetoast';
import { useConfirm } from 'primevue/useconfirm';
import { useRouter } from 'vue-router';
import AutoComplete from 'primevue/autocomplete';
import FloatLabel from 'primevue/floatlabel';
import Fieldset from 'primevue/fieldset';
import Message from 'primevue/message';
import { CountryService } from '@/service/CountryService';

const toast = useToast();
const confirm = useConfirm();
const router = useRouter();
const loading = ref(false);
const candidateDialog = ref(false);
const deleteCandidateDialog = ref(false);
const submitted = ref(false);
const allCandidates = ref([]);
const candidates = ref([]);
const candidate = ref({});
const candidateToDelete = ref(null);
const showInactive = ref(false);
const sessionInfo = ref(null);
const confirmationEmail = ref('');
const deleteSubmitted = ref(false);

// Filter setup
const filters = ref({
    global: { value: null }
});

// Country data
const countries = ref([]);
const filteredCountries = ref([]);

// GraphQL Queries
const LIST_CANDIDATES = `
    query CandidatesByCompanyId($companyId: String!) {
        candidatesByCompanyId(companyId: $companyId) {
            id
            companyId
            companyName
            candidateName
            email
            country
            phone
            candidateCV
            status
            recruitmentProcessId
            recruitmentProcessName
            createdAt
            updatedAt
        }
    }
`;

const CREATE_CANDIDATE = `
    mutation CreateCandidate($input: CreateCandidateInput!) {
        createCandidate(input: $input) {
            id
            companyId
            companyName
            candidateName
            email
            country
            phone
            candidateCV
            status
            recruitmentProcessId
            recruitmentProcessName
            createdAt
            updatedAt
        }
    }
`;

const UPDATE_CANDIDATE = `
    mutation UpdateCandidate($id: String!, $input: UpdateCandidateInput!) {
        updateCandidate(id: $id, input: $input) {
            id
            companyId
            companyName
            candidateName
            email
            country
            phone
            candidateCV
            status
            recruitmentProcessId
            recruitmentProcessName
            createdAt
            updatedAt
        }
    }
`;

const DELETE_CANDIDATE = `
    mutation DeleteCandidate($id: String!) {
        deleteCandidate(id: $id)
    }
`;

// Session handling
const fetchSessionInfo = async () => {
    try {
        const response = await fetch('core/auth/verify/session', {
            method: 'GET',
            credentials: 'include',
            headers: {
                'Accept': 'application/json',
            }
        });

        if (response.ok) {
            const data = await response.json();
            sessionInfo.value = data.user;
        }
    } catch (error) {
        console.error('Error fetching session info:', error);
        router.push({ name: 'login' });
    }
};

// Load candidates
async function loadCandidates() {
    if (!sessionInfo.value?.companyId) {
        toast.add({ severity: 'warn', summary: 'No Company Selected', detail: 'Please select a company first', life: 3000 });
        return;
    }

    try {
        loading.value = true;
        const response = await fetch(`${import.meta.env.VITE_API_URL}/graphql`, {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json'
            },
            credentials: 'include',
            body: JSON.stringify({
                query: LIST_CANDIDATES,
                variables: {
                    companyId: sessionInfo.value.companyId
                }
            })
        });
        const result = await response.json();
        if (result.errors) {
            throw new Error(result.errors[0]?.message || 'Failed to load candidates');
        }
        allCandidates.value = result.data.candidatesByCompanyId;
        filterCandidates();
    } catch (error) {
        toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to load candidates', life: 3000 });
    }
    loading.value = false;
}

// Filter candidates
function filterCandidates() {
    if (showInactive.value) {
        candidates.value = [...allCandidates.value].sort((a, b) => 
            a.candidateName.localeCompare(b.candidateName)
        );
    } else {
        candidates.value = [...allCandidates.value]
            .filter(candidate => candidate.status === 'active')
            .sort((a, b) => a.candidateName.localeCompare(b.candidateName));
    }
}

// Dialog handlers
function openNewCandidate() {
    candidate.value = {
        candidateName: '',
        email: '',
        country: '',
        phone: '+0000000000',
        candidateCV: '',
        status: 'active'
    };
    submitted.value = false;
    candidateDialog.value = true;
}

function editCandidate(data) {
    candidate.value = { ...data };
    candidateDialog.value = true;
}

function hideDialog() {
    candidateDialog.value = false;
    submitted.value = false;
}

// Validation
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Save candidate
async function saveCandidate() {
    submitted.value = true;

    if (!candidate.value.candidateName?.trim() || 
        !candidate.value.email?.trim() || 
        !candidate.value.country?.trim() || 
        !candidate.value.phone?.trim()) {
        toast.add({ severity: 'error', summary: 'Required Fields', detail: 'Please fill in all required fields', life: 3000 });
        return;
    }

    if (!isValidEmail(candidate.value.email)) {
        toast.add({ severity: 'error', summary: 'Invalid Email', detail: 'Please enter a valid email address', life: 3000 });
        return;
    }

    try {
        const isNewCandidate = !candidate.value.id;
        const query = isNewCandidate ? CREATE_CANDIDATE : UPDATE_CANDIDATE;
        
        const variables = isNewCandidate 
            ? { 
                input: {
                    companyId: sessionInfo.value.companyId,
                    companyName: sessionInfo.value.companyName,
                    candidateName: candidate.value.candidateName,
                    email: candidate.value.email.toLowerCase(),
                    country: candidate.value.country,
                    phone: candidate.value.phone,
                    candidateCV: candidate.value.candidateCV,
                    status: candidate.value.status,
                    recruitmentProcessId: candidate.value.recruitmentProcessId,
                    recruitmentProcessName: candidate.value.recruitmentProcessName
                }
            }
            : { 
                id: candidate.value.id,
                input: {
                    candidateName: candidate.value.candidateName,
                    email: candidate.value.email.toLowerCase(),
                    country: candidate.value.country,
                    phone: candidate.value.phone,
                    candidateCV: candidate.value.candidateCV,
                    status: candidate.value.status,
                    recruitmentProcessId: candidate.value.recruitmentProcessId,
                    recruitmentProcessName: candidate.value.recruitmentProcessName
                }
            };

        const response = await fetch(`${import.meta.env.VITE_API_URL}/graphql`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({ query, variables })
        });

        const result = await response.json();
        
        if (result.errors) {
            throw new Error(result.errors[0]?.message || 'Failed to save candidate');
        }

        toast.add({
            severity: 'success',
            summary: 'Success',
            detail: isNewCandidate ? 'Candidate Created' : 'Candidate Updated',
            life: 3000
        });

        candidateDialog.value = false;
        await loadCandidates();
    } catch (error) {
        toast.add({
            severity: 'error',
            summary: 'Error',
            detail: error.message || 'Failed to save candidate',
            life: 3000
        });
    }
}

// Delete handlers
function confirmDelete(data) {
    candidateToDelete.value = data;
    confirmationEmail.value = '';
    deleteSubmitted.value = false;
    deleteCandidateDialog.value = true;
}

function handleDeleteConfirm() {
    deleteSubmitted.value = true;
    
    if (confirmationEmail.value !== candidateToDelete.value.email) {
        return;
    }
    
    deleteCandidate(candidateToDelete.value.id);
    deleteCandidateDialog.value = false;
    candidateToDelete.value = null;
    confirmationEmail.value = '';
}

async function deleteCandidate(id) {
    try {
        const response = await fetch(`${import.meta.env.VITE_API_URL}/graphql`, {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                credentials: 'include'
            },
            body: JSON.stringify({
                query: DELETE_CANDIDATE,
                variables: { id: id }
            })
        });
        
        const result = await response.json();
        if (result.errors) {
            throw new Error(result.errors[0].message);
        }

        toast.add({ 
            severity: 'success', 
            summary: 'Success', 
            detail: 'Candidate deleted successfully', 
            life: 3000 
        });
        
        await loadCandidates();
    } catch (error) {
        toast.add({ 
            severity: 'error', 
            summary: 'Error', 
            detail: error.message || 'Failed to delete candidate', 
            life: 3000 
        });
    }
}

// Country handling
async function loadCountries() {
    try {
        countries.value = await CountryService.getCountries();
    } catch (error) {
        console.error('Failed to load countries:', error);
        toast.add({
            severity: 'error',
            summary: 'Error',
            detail: 'Failed to load countries',
            life: 3000
        });
    }
}

function searchCountries(event) {
    const query = event.query.toLowerCase();
    filteredCountries.value = countries.value.filter(country => 
        country.name.toLowerCase().includes(query)
    ).map(country => ({
        name: country.name
    }));
}

function onCountrySelect(event) {
    candidate.value.country = event.value.name;
}

// Status computed property
const candidateStatus = computed({
    get: () => candidate.value.status === 'active',
    set: (newValue) => {
        candidate.value.status = newValue ? 'active' : 'inactive'
    }
});

// Initialize component
onMounted(async () => {
    try {
        await fetchSessionInfo();
        await loadCountries();
        await loadCandidates();
    } catch (error) {
        console.error('Error initializing candidates page:', error);
        toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to load data', life: 3000 });
    }
});

const validateEmail = () => {
    // This empty function is needed to satisfy template reference
    // Actual validation is handled by isValidEmail in the Message component
};
</script>

<style scoped>
/* Reuse existing styles from Employees.vue */
:deep(.p-inputtext),
:deep(.p-dropdown),
:deep(.p-autocomplete) {
    width: 100%;
    height: 40px;
}

:deep(.p-inputtext),
:deep(.p-autocomplete-input) {
    padding: 0.5rem 0.75rem;
    font-size: 14px;
    line-height: 1.5;
}

:deep(.p-fieldset-content) {
    padding: 0.75rem;
}

@media (max-width: 768px) {
    :deep(.p-fieldset-content) {
        padding: 1rem;
    }
    
    .grid {
        gap: 0.75rem;
    }
    
    :deep(.p-inputtext),
    :deep(.p-dropdown),
    :deep(.p-autocomplete) {
        height: 44px;
        font-size: 15px;
    }
}
</style> 