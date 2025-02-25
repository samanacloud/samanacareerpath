<template>
  <div class="card">
    <Toast />
    <ConfirmDialog />
    <div class="flex items-center justify-between mb-4">
        <div>
          <h1 class="text-2xl font-medium text-900">Recruitment Leads</h1>
          <p class="text-sm font-medium text-500">Manage your recruitment processes</p>
        </div>
        <Button 
          label="Add Process" 
          icon="pi pi-plus" 
          outlined raised 
          @click="openNewProcess" 
        />
      </div>
    <!-- Header Section -->
    <div class="card p-4">
      <Toast />
      <ConfirmDialog />

      <!-- Header with title and add button -->
   

      <!-- Processes Section -->
      <div class="bg-white p-4 rounded-lg shadow-sm">
        <div class="flex justify-between items-center mb-4">
          <!-- Search Bar -->
          <IconField class="w-96">
            <InputIcon class="pi pi-search" />
            <InputText 
              v-model="filters.global.value" 
              placeholder="Search processes..." 
              class="w-full"
            />
          </IconField>

          <!-- Show Inactive Toggle -->
          <div class="flex items-center gap-3">
            <label class="text-gray-600">Show Inactive</label>
            <ToggleSwitch v-model="showInactive" @change="filterProcesses" />
          </div>
        </div>

        <!-- Processes Grid -->
        <template v-if="processes.length === 0">
          <div class="text-gray-500 text-center py-4">
            No recruitment processes available.
          </div>
        </template>
        <template v-else>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div v-for="process in filteredProcesses" 
                 :key="process.id" 
                 class="border rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer"
                 @click="fetchCandidates(process.id)">
              <div class="flex justify-between items-start mb-2">
                <div class="flex flex-col">
                  <h3 class="text-lg font-semibold">{{ process.jobName }}</h3>
                  <span class="text-sm text-gray-500">{{ process.jobCategory }}</span>

            
                </div>
                
                <div class="flex gap-2">
                  <Button 
                    icon="pi pi-pencil" 
                    text 
                    rounded 
                    @click="editProcess(process)"
                    class="text-green-500 hover:text-green-700"
                  />
                  <Button 
                    icon="pi pi-trash" 
                    text 
                    rounded 
                    @click="confirmDelete(process)"
                    class="text-red-500 hover:text-red-700"
                    severity="danger"
                  />
                  
                </div>
              </div>
              <div class="text-sm">
                <span class="font-medium text-gray-700">Workplace:</span>
                <span class="text-gray-600 ml-1">{{ process.workplaceType }}</span>
              </div>
              <div class="text-sm">
                <span class="font-medium text-gray-700">Type:</span>
                <span class="text-gray-600 ml-1">{{ process.jobType }}</span>
              </div>
              <div class="text-sm">
                <span class="font-medium text-gray-700">Salary Range:</span>
                <span class="text-gray-600 ml-1">{{ process.salaryRange }}</span>
              </div>
              <div class="text-sm text-gray-500 mb-2">
                <i class="pi pi-calendar mr-1"></i>
                Created: {{ new Date(process.createdAt).toLocaleDateString('en-US', {
                  year: 'numeric',
                  month: 'long',
                  day: 'numeric'
                }) }}
              </div>
              <div class="mt-2 flex justify-end">
                <Tag 
                  :value="process.status" 
                  :severity="process.status === 'active' ? 'success' : 'danger'" 
                  class="text-xs"
                />
              </div>
            </div>
          </div>

          <!-- New Details Section -->
          <div class="mt-6 p-4 bg-gray-50 rounded-lg border border-gray-200">
            <h3 class="text-lg font-semibold mb-4">Details</h3>
            <div class="text-gray-600">
              Recruitment process statistics and detailed insights will be displayed here.
              <!-- Example content (commented out for now) -->
              <!-- <div class="grid grid-cols-2 gap-4">
                <div class="p-4 bg-white rounded shadow">
                  <h4 class="font-medium mb-2">Application Status</h4>
                  <p class="text-sm">Chart or statistics here</p>
                </div>
                <div class="p-4 bg-white rounded shadow">
                  <h4 class="font-medium mb-2">Candidate Pipeline</h4>
                  <p class="text-sm">Pipeline visualization here</p>
                </div>
              </div> -->
            </div>
          </div>
        </template>
      </div>
    </div>

    <!-- Process Dialog -->
    <Dialog 
      v-model:visible="processDialog" 
      :style="{ width: '95%', maxWidth: '900px' }" 
      header="Process Details" 
      :modal="true" 
      class="p-fluid"
    >
      <form @submit.prevent="saveProcess">
        <div class="card flex flex-col gap-4">
          <Fieldset 
            legend="Process Information" 
            :toggleable="true" 
            class="mb-4 p-2 md:p-3"
          >
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="flex flex-col gap-2">
                <FloatLabel variant="on">
                  <InputText 
                    id="jobName" 
                    v-model="process.jobName" 
                    :class="{'p-invalid': submitted && !process.jobName}"
                    autofocus
                  />
                  <label for="jobName">Job Name*</label>
                </FloatLabel>
                <small class="p-error" v-if="submitted && !process.jobName">Job Name is required.</small>
              </div>

              <div class="flex flex-col gap-2">
                <FloatLabel variant="on">
                  <InputText 
                    id="jobCategory" 
                    v-model="process.jobCategory"
                    :class="{'p-invalid': submitted && !process.jobCategory}"
                  />
                  <label for="jobCategory">Job Category*</label>
                </FloatLabel>
                <small class="p-error" v-if="submitted && !process.jobCategory">Job Category is required.</small>
              </div>

              <div class="flex flex-col gap-2">
                <FloatLabel variant="on">
                  <InputText 
                    id="workplaceType" 
                    v-model="process.workplaceType"
                    :class="{'p-invalid': submitted && !process.workplaceType}"
                  />
                  <label for="workplaceType">Workplace Type*</label>
                </FloatLabel>
                <small class="p-error" v-if="submitted && !process.workplaceType">Workplace Type is required.</small>
              </div>

              <div class="flex flex-col gap-2">
                <FloatLabel variant="on">
                  <InputText 
                    id="jobType" 
                    v-model="process.jobType"
                    :class="{'p-invalid': submitted && !process.jobType}"
                  />
                  <label for="jobType">Job Type*</label>
                </FloatLabel>
                <small class="p-error" v-if="submitted && !process.jobType">Job Type is required.</small>
              </div>

              <div class="flex flex-col gap-2">
                <FloatLabel variant="on">
                  <InputText 
                    id="salaryRange" 
                    v-model="process.salaryRange"
                    :class="{'p-invalid': submitted && !process.salaryRange}"
                  />
                  <label for="salaryRange">Salary Range*</label>
                </FloatLabel>
                <small class="p-error" v-if="submitted && !process.salaryRange">Salary Range is required.</small>
              </div>

              <div class="flex flex-col gap-2" v-if="process.id">
                <FloatLabel variant="on">
                  <InputText 
                    id="createdAt" 
                    v-model="process.createdAt" 
                    readonly
                  />
                  <label for="createdAt">Creation Date</label>
                </FloatLabel>
              </div>

              <div class="flex flex-col gap-2">
                <div class="flex items-center gap-2">
                  <ToggleSwitch 
                    v-model="processStatus" 
                    id="status"
                  />
                  <span class="text-sm text-surface-500">{{ processStatus ? 'Active' : 'Inactive' }}</span>
                </div>
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
      v-model:visible="deleteDialog"
      :style="{ width: '450px' }"
      header="Delete Confirmation"
      :modal="true"
      class="p-fluid"
    >
      <div class="flex flex-col gap-4">
        <div class="text-red-600 font-semibold">Warning: This action cannot be undone</div>
        
        <div class="text-gray-700">
          To confirm deletion, type the {{ deleteType === 'process' ? 'job name' : 'category' }}:
          <span class="font-semibold">{{ deleteType === 'process' ? itemToDelete?.jobName : itemToDelete?.category }}</span>
        </div>
        
        <div class="flex flex-col gap-2">
          <InputText
            v-model="confirmationText"
            :class="{'p-invalid': deleteSubmitted && !isConfirmationValid}"
            :placeholder="deleteType === 'process' ? 'Enter job name' : 'Enter category'"
          />
          <small class="p-error" v-if="deleteSubmitted && !isConfirmationValid">
            {{ deleteType === 'process' ? 'Job name' : 'Category' }} doesn't match
          </small>
        </div>
      </div>
      
      <template #footer>
        <div class="flex justify-end gap-2">
          <Button
            label="Cancel"
            icon="pi pi-times"
            outlined
            @click="deleteDialog = false"
          />
          <Button
            label="Delete"
            icon="pi pi-trash"
            severity="danger"
            @click="handleDelete"
          />
        </div>
      </template>
    </Dialog>

    <!-- Candidates Section -->
    <div class="mt-6 p-4 bg-white rounded-lg border border-gray-200" v-if="selectedProcess">
      <h3 class="text-lg font-semibold mb-4">Candidates for {{ selectedProcess.jobName }}</h3>
      
      <div v-if="loadingCandidates" class="text-center py-4">
        <i class="pi pi-spin pi-spinner text-2xl"></i>
        <p class="text-gray-600 mt-2">Loading candidates...</p>
      </div>

      <div v-else>
        <DataTable
          :value="candidates" 
          dataKey="id"
          class="p-datatable-sm"
          :paginator="true" 
          :rows="10"
          :rowsPerPageOptions="[5, 10, 20, 50]"
          responsiveLayout="scroll"
          :loading="loadingCandidates"
          :globalFilterFields="['candidateName', 'email', 'country', 'status']"
          v-model:filters="filters"
          filterDisplay="menu"
          @row-click="onRowClick"
        >
          <Column field="candidateName" header="Candidate" sortable>
            <template #body="{ data }">
              <div class="flex items-center gap-2">
                <Avatar 
                  :label="getInitials(data.candidateName)" 
                  class="w-8 h-8 bg-primary-100 text-primary-700 font-medium" 
                  size="normal" 
                  shape="circle"
                />
                <div class="flex flex-col">
                  <span class="font-medium">{{ data.candidateName }}</span>
                  <span class="text-sm text-gray-500">{{ data.email }}</span>
                </div>
              </div>
            </template>
          </Column>

          <Column field="country" header="Country" sortable>
            <template #body="{ data }">
              <span class="text-gray-700 capitalize">{{ data.country?.toLowerCase() }}</span>
            </template>
          </Column>

          <Column field="status" header="Status" sortable>
            <template #body="{ data }">
              <Tag 
                :severity="getStatusSeverity(data.status)" 
                :value="data.status"
                class="text-xs"
              />
            </template>
            <template #filter="{ filterModel, filterCallback }">
              <Dropdown 
                v-model="filterModel.value" 
                :options="statusOptions" 
                placeholder="Any Status" 
                class="p-column-filter" 
                @change="filterCallback()"
              />
            </template>
          </Column>

          <Column field="createdAt" header="Applied" sortable>
            <template #body="{ data }">
              <span class="text-gray-700">
                {{ new Date(data.createdAt).toLocaleDateString() }}
              </span>
            </template>
          </Column>

          <Column header="Metrics" style="min-width: 250px">
            <template #body="{ data }">
              <div v-if="candidateAnalytics[data.email]" class="flex items-center gap-3 text-sm">
                <div class="flex items-center gap-1" v-tooltip="`Average Skillset Rating`">
                  <i class="pi pi-star-fill text-yellow-500"></i>
                  <span>{{ candidateAnalytics[data.email].skillsetAvg?.toFixed(1) || '0.0' }}</span>
                </div>
                <div class="flex items-center gap-1" v-tooltip="`Approved Interviews`">
                  <i class="pi pi-check-circle text-green-500"></i>
                  <span>{{ candidateAnalytics[data.email].interviewYes }}</span>
                </div>
                <div class="flex items-center gap-1" v-tooltip="`Pending Interviews`">
                  <i class="pi pi-clock text-yellow-500"></i>
                  <span>{{ candidateAnalytics[data.email].interviewMaybe }}</span>
                </div>
                <div class="flex items-center gap-1" v-tooltip="`Rejected Interviews`">
                  <i class="pi pi-times-circle text-red-500"></i>
                  <span>{{ candidateAnalytics[data.email].interviewNo }}</span>
                </div>
                <div class="flex items-center gap-1" v-tooltip="`Certifications`">
                  <i class="pi pi-certificate text-blue-500"></i>
                  <span>{{ candidateAnalytics[data.email].certificationCount }}</span>
                </div>
              </div>
              <div v-else class="text-gray-400 text-sm">
                Loading metrics...
              </div>
            </template>
          </Column>

          <Column :exportable="false" style="width:100px">
            <template #body="{ data }">
              <div class="flex gap-2">
                <Button 
                  icon="pi pi-eye" 
                  text 
                  rounded 
                  class="text-gray-500 hover:text-primary-500"
                  @click="viewCandidate(data)"
                />
                <Button 
                  icon="pi pi-trash" 
                  text 
                  rounded 
                  severity="danger" 
                  class="hover:text-red-600"
                  @click="confirmDeleteCandidate(data)"
                />
              </div>
            </template>
          </Column>
        </DataTable>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useToast } from 'primevue/usetoast';
import { useConfirm } from 'primevue/useconfirm';
import Select from 'primevue/select';
import ToggleSwitch from 'primevue/toggleswitch';
import FloatLabel from 'primevue/floatlabel';
import Fieldset from 'primevue/fieldset';
import { useRouter } from 'vue-router';
import IconField from 'primevue/iconfield';
import InputIcon from 'primevue/inputicon';
import Avatar from 'primevue/avatar';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Dropdown from 'primevue/dropdown';

const toast = useToast();
const confirm = useConfirm();
const router = useRouter();
const loading = ref(false);
const processDialog = ref(false);
const deleteDialog = ref(false);
const submitted = ref(false);
const processes = ref([]);
const process = ref({});
const sessionInfo = ref(null);
const deleteType = ref('');
const itemToDelete = ref(null);
const confirmationText = ref('');
const deleteSubmitted = ref(false);
const showInactive = ref(false);
const allProcesses = ref([]);
const candidates = ref([]);
const selectedProcessId = ref(null);
const loadingCandidates = ref(false);
const statusOptions = ref(['new', 'reviewed', 'interviewed', 'rejected']);
const candidateAnalytics = ref({});

// Simple filter setup
const filters = ref({
  global: { value: null }
});

// Add this computed property after your existing computed properties
const filteredProcesses = computed(() => {
  let filtered = showInactive.value 
    ? processes.value 
    : processes.value.filter(process => process.status === 'active');
  
  if (filters.value.global.value) {
    const query = filters.value.global.value.toLowerCase();
    filtered = filtered.filter(process => 
      process.jobName?.toLowerCase().includes(query) ||
      process.jobCategory?.toLowerCase().includes(query) ||
      process.workplaceType?.toLowerCase().includes(query) ||
      process.jobType?.toLowerCase().includes(query) ||
      process.salaryRange?.toLowerCase().includes(query)
    );
  }
  
  return filtered.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
});

// GraphQL Queries
const LIST_PROCESSES = `
    query getRecruitmentProcessByCompanyId($companyId: String!) {
        getRecruitmentProcessByCompanyId(companyId: $companyId) {
            id
            companyId
            jobName
            jobCategory
            workplaceType
            jobType
            salaryRange
            status
            jobDetails
            createdAt
            updatedAt
        }
    }
`;

const CREATE_PROCESS = `
    mutation CreateRecruitmentProcess($input: CreateRecruitmentProcessInput!) {
        createRecruitmentProcess(input: $input) {
            id
            companyId
            jobName
            jobCategory
            workplaceType
            jobType
            salaryRange
            status
            createdAt
            updatedAt
        }
    }
`;

const UPDATE_PROCESS = `
    mutation UpdateRecruitmentProcess($id: String!, $input: UpdateRecruitmentProcessInput!) {
        updateRecruitmentProcess(id: $id, input: $input) {
            id
            companyId
            jobName
            jobCategory
            workplaceType
            jobType
            salaryRange
            status
            createdAt
            updatedAt
        }
    }
`;

const DELETE_PROCESS = `
    mutation DeleteRecruitmentProcess($id: String!) {
        deleteRecruitmentProcess(id: $id)
    }
`;

const CANDIDATES_QUERY = `
  query CandidatesByRecruitmentProcessId($recruitmentProcessId: String!) {
    candidatesByRecruitmentProcessId(recruitmentProcessId: $recruitmentProcessId) {
      id
      candidateCV
      candidateName
      companyId
      country
      companyName
      createdAt
      email
      salaryExpectation
      status
    }
  }
`;

const CANDIDATE_ANALYTICS_QUERY = `
  query CandidateAnalytics($email: String!) {
    candidateAnalytics(email: $email) {
      skillsetAvg
      interviewYes
      interviewMaybe
      interviewNo
      interviewRating
      certificationCount
    }
  }
`;

// Add fetchSessionInfo function
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

// Modify the loadProcesses function
async function loadProcesses() {
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
        query: LIST_PROCESSES,
        variables: {
          companyId: sessionInfo.value.companyId
        }
      })
    });
    const result = await response.json();
    
    if (result.data?.getRecruitmentProcessByCompanyId) {
      allProcesses.value = result.data.getRecruitmentProcessByCompanyId.map(process => ({
        ...process,
        jobDetailsArray: process.jobDetailsArray || []
      }));
      processes.value = [...allProcesses.value];
      filterProcesses();
    } else if (result.errors) {
      // Ignore jobDetailsArray errors as they are expected when null
      const nonJobDetailsErrors = result.errors.filter(error => 
        !error.message.includes("'dict' object has no attribute 'category'") &&
        !error.path?.some(p => p === 'jobDetailsArray')
      );
      
      if (nonJobDetailsErrors.length > 0) {
        throw new Error(nonJobDetailsErrors[0]?.message || 'Failed to load processes');
      }
    }
  } catch (error) {
    console.error('Error loading processes:', error);
    toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to load processes', life: 3000 });
  } finally {
    loading.value = false;
  }
}

// Add this function after loadProcesses
function filterProcesses() {
  if (showInactive.value) {
    processes.value = [...allProcesses.value];
  } else {
    processes.value = allProcesses.value.filter(process => process.status === 'active');
  }
}

// Dialog management functions
function openNewProcess() {
  process.value = {
    jobName: '',
    jobCategory: '',
    workplaceType: '',
    jobType: '',
    salaryRange: '',
    status: 'active'
  };
  submitted.value = false;
  processDialog.value = true;
}

function editProcess(data) {
  process.value = { ...data };
  processDialog.value = true;
}

function hideDialog() {
  processDialog.value = false;
  submitted.value = false;
}

// Save functions
async function saveProcess() {
  submitted.value = true;

  if (!process.value.jobName?.trim() || !process.value.jobCategory?.trim() || 
      !process.value.workplaceType?.trim() || !process.value.jobType?.trim() || 
      !process.value.salaryRange?.trim()) {
    toast.add({ severity: 'error', summary: 'Required Fields', detail: 'Please fill in all required fields', life: 3000 });
    return;
  }

  try {
    const isNewProcess = !process.value.id;
    const query = isNewProcess ? CREATE_PROCESS : UPDATE_PROCESS;
    
    const variables = isNewProcess 
      ? { 
          input: {
            companyId: sessionInfo.value.companyId,
            companyName: sessionInfo.value.companyName,
            jobName: process.value.jobName,
            jobCategory: process.value.jobCategory,
            workplaceType: process.value.workplaceType,
            jobType: process.value.jobType,
            salaryRange: process.value.salaryRange,
            status: process.value.status,
            jobDetails: process.value.jobDetails || '',
            postUrl: process.value.postUrl || '',
            createdBy: sessionInfo.value.email,
            updatedBy: sessionInfo.value.email
          }
        }
      : { 
          id: process.value.id,
          input: {
            jobName: process.value.jobName,
            jobCategory: process.value.jobCategory,
            workplaceType: process.value.workplaceType,
            jobType: process.value.jobType,
            salaryRange: process.value.salaryRange,
            status: process.value.status,
            jobDetails: process.value.jobDetails || '',
            postUrl: process.value.postUrl || '',
            updatedBy: sessionInfo.value.email
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
      throw new Error(result.errors[0]?.message || 'Failed to save process');
    }

    toast.add({
      severity: 'success',
      summary: 'Success',
      detail: isNewProcess ? 'Process Created' : 'Process Updated',
      life: 3000
    });

    processDialog.value = false;
    await loadProcesses();
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: error.message || 'Failed to save process',
      life: 3000
    });
  }
}

// Delete functions
function confirmDelete(data) {
  deleteType.value = 'process';
  itemToDelete.value = data;
  confirmationText.value = '';
  deleteSubmitted.value = false;
  deleteDialog.value = true;
}

async function handleDelete() {
  deleteSubmitted.value = true;
  
  if (!isConfirmationValid.value) {
    return;
  }
  
  await deleteProcess();
  
  deleteDialog.value = false;
  deleteSubmitted.value = false;
  confirmationText.value = '';
}

async function deleteProcess() {
  try {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/graphql`, {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json'
      },
      credentials: 'include',
      body: JSON.stringify({
        query: DELETE_PROCESS,
        variables: { 
          id: itemToDelete.value.id 
        }
      })
    });
    
    const result = await response.json();
    if (result.errors) {
      throw new Error(result.errors[0].message);
    }

    toast.add({ 
      severity: 'success', 
      summary: 'Success', 
      detail: 'Process deleted successfully', 
      life: 3000 
    });
    
    await loadProcesses();
  } catch (error) {
    toast.add({ 
      severity: 'error', 
      summary: 'Error', 
      detail: error.message || 'Failed to delete process', 
      life: 3000 
    });
  }
}

// Computed properties
const processStatus = computed({
  get: () => process.value.status === 'active',
  set: (newValue) => {
    process.value.status = newValue ? 'active' : 'inactive'
  }
});

const isConfirmationValid = computed(() => {
  if (deleteType.value === 'process') {
    return confirmationText.value === itemToDelete.value?.jobName;
  } else {
    return confirmationText.value === itemToDelete.value?.category;
  }
});

// Add fetch method
async function fetchCandidates(processId) {
  try {
    loadingCandidates.value = true;
    selectedProcessId.value = processId;
    
    const response = await fetch(`${import.meta.env.VITE_API_URL}/graphql`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({
        query: CANDIDATES_QUERY,
        variables: { recruitmentProcessId: processId }
      })
    });

    const result = await response.json();
    
    if (result.errors) {
      throw new Error(result.errors[0]?.message || 'Failed to fetch candidates');
    }

    candidates.value = result.data?.candidatesByRecruitmentProcessId || [];
    
    // Fetch analytics for each candidate
    const analyticsPromises = candidates.value.map(async candidate => {
      const res = await fetch(`${import.meta.env.VITE_API_URL}/graphql`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: CANDIDATE_ANALYTICS_QUERY,
          variables: { email: candidate.email }
        })
      });
      return res.json();
    });

    const analyticsResults = await Promise.all(analyticsPromises);
    analyticsResults.forEach((result, index) => {
      candidateAnalytics.value[candidates.value[index].email] = result.data?.candidateAnalytics;
    });

  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: error.message || 'Failed to load candidates',
      life: 3000
    });
  } finally {
    loadingCandidates.value = false;
  }
}

// Add computed property to find selected process
const selectedProcess = computed(() => 
  processes.value.find(p => p.id === selectedProcessId.value)
);

// Add initials generator
const getInitials = (name) => {
  if (!name) return '??';
  const names = name.split(' ');
  let initials = names[0].substring(0, 1).toUpperCase();
  if (names.length > 1) {
    initials += names[names.length - 1].substring(0, 1).toUpperCase();
  }
  return initials;
};

// Update status severity mapping to handle all cases
const getStatusSeverity = (status) => {
  const statusMap = {
    'new': 'info',
    'reviewed': 'warning',
    'interviewed': 'success',
    'rejected': 'danger'
  };
  return statusMap[status?.toLowerCase()] || 'info';
};

// Add to script section
function viewCandidate(candidate) {
  // Implement candidate detail view
  console.log('View candidate:', candidate);
}

function confirmDeleteCandidate(candidate) {
  // Implement candidate deletion logic
  console.log('Delete candidate:', candidate);
}

// Add to script section
function onRowClick(event) {
  // Only navigate if clicking the row (not buttons)
  const isButton = event.originalEvent.target.closest('button') || 
                  event.originalEvent.target.closest('.p-column-header');
  
  if (!isButton && event.data?.id) {
    router.push({
      name: 'profiles-id',
      params: { id: event.data.id }
    });
  }
}

// Initialize component
onMounted(async () => {
  try {
    await fetchSessionInfo();
    await loadProcesses();
  } catch (error) {
    console.error('Error initializing recruitment leads page:', error);
    toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to load data', life: 3000 });
  }
});
</script>

<style scoped>
/* Form Control Base Styles */
:deep(.p-inputtext),
:deep(.p-dropdown),
:deep(.p-autocomplete),
:deep(.p-inputnumber) {
  width: 100%;
  height: 40px;
}

/* Input Text and AutoComplete */
:deep(.p-inputtext),
:deep(.p-autocomplete-input) {
  padding: 0.5rem 0.75rem;
  font-size: 14px;
  line-height: 1.5;
}

/* Dropdown Specific */
:deep(.p-dropdown) {
  display: flex;
  align-items: center;
}

:deep(.p-dropdown-label) {
  padding: 0.5rem 0.75rem;
  line-height: 1.5;
}

:deep(.p-dropdown-trigger) {
  width: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* ToggleSwitch Adjustments */
:deep(.p-toggleswitch) {
  height: 24px;
}

:deep(.p-toggleswitch .p-toggleswitch-slider) {
  border-radius: 12px;
}

/* Form Layout Spacing */
.form-field {
  margin-bottom: 1rem;
}

/* Label Styling */
label {
  display: block;
  margin-bottom: 0.5rem;
  font-size: 14px;
  color: var(--text-color);
}

.p-dialog .p-dialog-content {
  padding: 2rem;
}

/* Update Fieldset padding */
:deep(.p-fieldset-content) {
  padding: 0.75rem;
}

@media (max-width: 768px) {
  :deep(.p-fieldset-content) {
    padding: 1rem;
  }
  
  /* Adjust grid gap for mobile */
  .grid {
    gap: 0.75rem;
  }
  
  /* Make form fields slightly larger on mobile */
  :deep(.p-inputtext),
  :deep(.p-dropdown),
  :deep(.p-autocomplete) {
    height: 44px;
    font-size: 15px;
  }
  
  /* Adjust toggle switch size */
  :deep(.p-toggleswitch) {
    height: 28px;
  }
}

/* Add to the style section */
:deep(.p-datatable .p-datatable-tbody tr:hover) {
  background-color: #f8f9fa;
  cursor: pointer;
  transition: background-color 0.2s;
}

:deep(.p-datatable .p-datatable-tbody tr:focus) {
  outline: none;
  background-color: #e9ecef;
}

/* For better visual hierarchy */
:deep(.p-datatable .p-datatable-tbody td) {
  transition: background-color 0.2s;
}
</style>
