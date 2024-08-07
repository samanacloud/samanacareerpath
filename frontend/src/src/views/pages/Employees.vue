<script setup>
import { ref, onBeforeMount, computed } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import { useToast } from 'primevue/usetoast';
import Tooltip from 'primevue/tooltip';


//redirects to unauthorized if the user role is lower than the pagerole
import { getPageAuthorization } from '@/utils/utils';
const pageRole = 2; // Set the required role for this page
getPageAuthorization(pageRole);

// Function to get the base URL
const baseURL = import.meta.env.VITE_SITE_URL 
    ? `https://${import.meta.env.VITE_SITE_URL}` // Use https if VITE_SITE_URL is defined
    : 'http://localhost:8080'; // Use localhost for development

    
const employeesList = ref([]);
const apiResponse = ref('');
const searchName = ref(''); // reactive variable to store search input
const employeeDialog = ref(false);
const isEdit = ref(false);
const employee = ref({
    ID: null,
    primaryEmail: '',
    recoveryEmail: '',
    fullName: '',
    phone_mobile: '',
    thumbnailPhotoURL: '',
    companyRole: '',
    contractType: '',
    suspended: '',
    creationDate: ''
});
const enrollmentStatus = ref('');

const idFrozen = ref(false); // Add this line for dynamic toggling

const router = useRouter();
const toast = useToast();

const filteredEmployeesList = computed(() => {
  if (!searchName.value) return employeesList.value.filter(employee => employee.primaryEmail.includes('samanagroup.co'));
  const searchTerm = searchName.value.toLowerCase();
  return employeesList.value.filter(employee =>
    employee.fullName.toLowerCase().includes(searchTerm) &&
    employee.primaryEmail.includes('samanagroup.co')
  );
});



// Function to fetch enrollment status for a specific employee
const fetchEnrollmentStatus = async (email) => {
  try {
    const response = await axios.post(`${baseURL}/api/apitest.php`, {
      action: 'getEnrollmentStatus',
      email: email
    });
    // Update the specific employee's enrollment status in employeesList
    const employee = employeesList.value.find(emp => emp.primaryEmail === email);
    if (employee) {
      employee.enrollmentStatus = response.data.percentage || '0%';
    }
  } catch (error) {
    console.error('Error fetching enrollment status:', error);
  }
};

const listEmployees = async () => {
    try {
        const response = await axios.post(`${baseURL}/api/apitest.php`, {
            action: 'listEmployees'
        });
        employeesList.value = response.data;
        apiResponse.value = 'Employees listed successfully';
        // Fetch enrollment status for each employee

    } catch (error) {
        apiResponse.value = 'Error: ' + error.message;
    }
};

const openNew = () => {
    employee.value = {
        ID: null,
        primaryEmail: '',
        recoveryEmail: '',
        fullName: '',
        phone_mobile: '',
        thumbnailPhotoURL: '',  
        companyRole: '',
        contractType: '',
        suspended: '',
        creationDate: ''
    };
    isEdit.value = false;
    employeeDialog.value = true;
};

const editEmployee = (employeeData) => {
    employee.value = { ...employeeData };
    isEdit.value = true;
    employeeDialog.value = true;
};


const deleteEmployee = async (employeeId) => {
    try {
        await axios.post(`${baseURL}/api/apitest.php`, {
            action: 'deleteEmployee',
            id: employeeId
        });
        toast.add({ severity: 'success', summary: 'Success', detail: 'Employee deleted successfully' });
        listEmployees();
    } catch (error) {
        toast.add({ severity: 'error', summary: 'Error', detail: 'Error deleting employee' });
    }
};

const viewProfileDetails = (email) => {
    sessionStorage.setItem('employeeEmail', email);
    router.push('/employeeprofile');
};



const employeeReviews = (email) => {
    sessionStorage.setItem('employeeEmail', email);
    router.push('/employeesreviews');
};

const saveEmployee = async () => {
    try {
        const action = isEdit.value ? 'updateEmployee' : 'addEmployee';
        const employeePayload = {
            action: action,
            ID: employee.value.ID,
            primaryEmail: employee.value.primaryEmail,
            recoveryEmail: employee.value.recoveryEmail,
            fullName: employee.value.fullName,
            phone_mobile: employee.value.phone_mobile,
            thumbnailPhotoURL: employee.value.thumbnailPhotoURL,
            companyRole: employee.value.companyRole,
            contractType: employee.value.contractType,
            suspended: employee.value.suspended,
            creationDate: employee.value.creationDate
        };
        
        // Remove the ID field if the action is addEmployee
        if (action === 'addEmployee') {
            delete employeePayload.id;
        }

        await axios.post(`${baseURL}/api/apitest.php`, employeePayload);
        toast.add({ severity: 'success', summary: 'Success', detail: `Employee ${isEdit.value ? 'updated' : 'added'} successfully` });
        employeeDialog.value = false;
        listEmployees();
    } catch (error) {
        toast.add({ severity: 'error', summary: 'Error', detail: `Error ${isEdit.value ? 'updating' : 'adding'} employee` });
    }
};


onBeforeMount(async () => {
    await listEmployees(); // Wait for data to load
});




const rowClass = (data) => {
    return { 'suspended-row': data.suspended === true };
};
const roles = [
    { label: 'Enterprise Architect', value: 'Enterprise Architect' },
    { label: 'L1 - Service Desk Engineer', value: 'L1 - Service Desk Engineer' },
    { label: 'L2 - Service Desk Engineer', value: 'L2 - Service Desk Engineer' },
    { label: 'L3 - Service Desk Engineer', value: 'L3 - Service Desk Engineer' },
    { label: 'CTO', value: 'CTO' },
    { label: 'CFO', value: 'CFO' },
    { label: 'COO', value: 'COO' },
    { label: 'SDM', value: 'SDM' },
    { label: 'SRM', value: 'SRM' },
    { label: 'Consultant', value: 'Consultant' },
    { label: 'Senior Consultant', value: 'Senior Consultant' },
    { label: 'Service Delivery Director', value: 'Service Delivery Director' }
];

const contractTypes = [
    { label: 'Full Time', value: 'Full Time' },
    { label: 'Contractor', value: 'Contractor' },
    { label: 'Owner', value: 'Owner' },
    { label: 'Partner', value: 'Partner' }
];

</script>


<template>
    <div class="grid">
        <div class="col-12">
            <div class="card">
                <h5>Employees Dashboard</h5>
                <div class="flex justify-content-between flex-column sm:flex-row">
                    <h6>Search by Name</h6>
                    <InputText type="text" v-model="searchName" placeholder="Search by name" class="p-inputtext-sm" />
                    <Button label="New Employee" icon="pi pi-plus" class="p-button-success" @click="openNew" />
                </div>
                <DataTable :value="filteredEmployeesList" paginator :rows="10" dataKey="ID" rowHover :rowClass="rowClass" :scrollable="true" scrollHeight="70vh" scrollDirection="vertical">
                    <Column field="thumbnailPhotoURL" header="Profile Photo" bodyStyle="text-align: center" frozen alignFrozen="left">
                        <template #body="{ data }">
                            <i v-if="!data.thumbnailPhotoURL" class="pi pi-user profile-photo"></i>
                            <img v-else :src="data.thumbnailPhotoURL" alt="Profile Photo" class="profile-photo" />
                        </template>
                    </Column>
                    <Column field="fullName" header="Name & Email" sortable frozen alignFrozen="left">
                        <template #body="{ data }">
                            <div>
                                <strong class="name">{{ data.fullName }}</strong>
                                <div class="email">{{ data.primaryEmail }}</div>
                            </div>
                        </template>
                    </Column>
                    <Column field="companyRole" header="Role" sortable style="min-width: 100px"></Column>
                    <Column field="enrollmentStatus" header="Enrollment Status" style="min-width: 100px">
                        <template #body="{ data }">
                            {{ data.enrollmentStatus || fetchEnrollmentStatus(data.primaryEmail) }}
                        </template>
                    </Column>


                    <Column field="suspended" header="Status" sortable style="min-width: 100px">
                        <template #body="{ data }">
                            <span :class="data.suspended === 'True' ? 'badge badge-danger' : 'badge badge-success'">
                            {{ data.suspended === 'True' ? 'Inactive' : 'Active' }}
                            </span>
                        </template>
                    </Column>
                    <Column header="Actions" bodyStyle="text-align: center" frozen alignFrozen="right">
                        <template #body="{ data }">
                            <Button icon="pi pi-search" severity="success" text outlined raised @click="viewProfileDetails(data.primaryEmail)"  v-tooltip="'View Profile Details'"/>
                            <Button icon="pi pi-chart-line" severity="info" text outlined raised @click="employeeReviews(data.primaryEmail)" v-tooltip="'View Employee Reviews'" />
                            <Button icon="pi pi-pencil"  severity="warning" outlined text rised  @click="editEmployee(data)" v-tooltip="'Edit Employee'" />
                            <Button icon="pi pi-trash"  severity="danger" outlined text rised  @click="() => $confirm.require({
                                message: 'Are you sure you want to delete this employee?',
                                header: 'Confirm',
                                icon: 'pi pi-exclamation-triangle',
                                accept: () => deleteEmployee(data.ID)
                            })" v-tooltip="'Delete Employee'" />
                        </template>
                    </Column>
                </DataTable>
            </div>
        </div>
    </div>

    <Dialog header="Employee Details" v-model:visible="employeeDialog" :modal="true" :style="{ width: '50vw' }" :closable="false">
        <div class="p-fluid">
            <div class="p-field">
                <label for="fullName">Full Name</label>
                <InputText id="fullName" v-model="employee.fullName" />
            </div>
            <div class="p-field">
                <label for="primaryEmail">Primary Email</label>
                <InputText id="primaryEmail" v-model="employee.primaryEmail" :disabled="isEdit"/>
            </div>
            <div class="p-field">
                <label for="recoveryEmail">Recovery Email</label>
                <InputText id="recoveryEmail" v-model="employee.recoveryEmail" />
            </div>
            <div class="p-field">
                <label for="phone_mobile">Phone Mobile</label>
                <InputText id="phone_mobile" v-model="employee.phone_mobile" />
            </div>
            <div class="p-field">
                <label for="companyRole">Role</label>
                <Dropdown id="companyRole" v-model="employee.companyRole" :options="roles" optionLabel="label" optionValue="value" placeholder="Select Role" />
            </div>
            <div class="p-field">
                <label for="contractType">Contract Type</label>
                <Dropdown id="contractType" v-model="employee.contractType" :options="contractTypes" optionLabel="label" optionValue="value" placeholder="Select Contract Type" />
            </div>
            <div class="p-field">
                Status <InputSwitch v-model="employee.suspended" :true-value="'False'" :false-value="'True'" :checked="employee.suspended === 'False'" />
            </div>
        </div>
        <div class="p-grid">
            <div class="p-col-12 p-md-6">
                <Button label="Cancel" icon="pi pi-times" severity="danger" outlined text raised @click="employeeDialog = false" />
                <Button label="Save" icon="pi pi-check" severity="success" outlined text raised @click="saveEmployee" />
            </div>
        </div>
    </Dialog>
    <ConfirmDialog />
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


// Media query for smaller screens (adjust breakpoint as needed)
@media (max-width: 768px) { 
    .email {
        font-size: 0.8rem;  // Reduce font size for mobile
    }
}


</style>