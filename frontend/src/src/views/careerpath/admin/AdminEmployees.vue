<template>
    <div class="card">
        <Toast />
        <ConfirmDialog />

        <!-- Header Section -->
        <div class="flex flex-col gap-4">
            <div class="flex items-center justify-between">
                <div>
                    <h1 class="text-2xl font-medium text-900">Employees</h1>
                    <p class="text-sm font-medium text-500">Manage your organization's employees</p>
                </div>
                <Button 
                    label="Add Employee" 
                    icon="pi pi-plus" 
                    outlined 
                    raised 
                    class="bg-white" 
                    @click="openNewEmployee" 
                />
            </div>

            <!-- Search and Filter Bar -->
            <div class="flex justify-between items-center bg-white p-4 rounded-lg shadow-sm">
                <IconField class="w-96">
                    <InputIcon class="pi pi-search" />
                    <InputText 
                        v-model="filters['global'].value" 
                        placeholder="Search employees..." 
                        class="w-full"
                    />
                </IconField>
                <div class="flex items-center gap-3">
                    <label class="text-gray-600">Show Inactive</label>
                    <ToggleSwitch v-model="showInactive" @change="filterEmployees" />
                </div>
            </div>

            <!-- Employees List -->
            <div class="bg-white rounded-lg shadow-sm">
                <DataTable
                    :value="employees"
                    :loading="loading"
                    dataKey="id"
                    :paginator="true"
                    :rows="10"
                    :rowsPerPageOptions="[5, 10, 20, 50]"
                    responsiveLayout="scroll"
                    v-model:filters="filters"
                    filterDisplay="menu"
                    :globalFilterFields="['name', 'email', 'role', 'country']"
                    class="p-4"
                >
                    <Column field="name" header="Name" sortable>
                        <template #body="{ data }">
                            <div class="flex items-center gap-2">
                                <div class="w-8 h-8 rounded-full bg-primary-100 flex items-center justify-center">
                                    {{ data.name.charAt(0).toUpperCase() }}
                                </div>
                                <div class="flex flex-col">
                                    <span class="font-medium">{{ data.name }}</span>
                                    <span class="text-sm text-gray-500">{{ data.email }}</span>
                                </div>
                            </div>
                        </template>
                    </Column>

                    <Column field="role" header="Role" sortable>
                        <template #body="{ data }">
                            <span class="text-gray-700">{{ data.role }}</span>
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

                    <Column field="status" header="Status" sortable>
                        <template #body="{ data }">
                            <Tag 
                                :severity="data.status === 'active' ? 'success' : 'danger'" 
                                :value="data.status"
                                class="text-xs"
                            />
                        </template>
                    </Column>

                    <Column :exportable="false" style="width:100px">
                        <template #body="{ data }">
                            <div class="flex gap-2">
                                <Button 
                                    icon="pi pi-pencil" 
                                    text 
                                    rounded 
                                    @click="editEmployee(data)"
                                    class="text-gray-500 hover:text-primary-500"
                                />
                                <Button 
                                    icon="pi pi-trash" 
                                    text 
                                    rounded 
                                    severity="danger" 
                                    @click="confirmDelete(data)"
                                    class="hover:text-red-600"
                                />
                            </div>
                        </template>
                    </Column>
                </DataTable>
            </div>
        </div>

        <!-- Employee Dialog -->
        <Dialog 
            v-model:visible="employeeDialog" 
            :style="{ width: '95%', maxWidth: '900px' }" 
            header="Employee Details" 
            :modal="true" 
            class="p-fluid"
        >
            <form @submit.prevent="saveEmployee">
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
                                        id="name" 
                                        v-model="employee.name" 
                                        :class="{'p-invalid': submitted && !employee.name}"
                                        autofocus
                                    />
                                    <label for="name">Full Name*</label>
                                </FloatLabel>
                                <small class="p-error" v-if="submitted && !employee.name">Name is required.</small>
                            </div>
                            
                            <div class="flex flex-col gap-2">
                                <FloatLabel variant="on">
                                    <InputText 
                                        id="email" 
                                        v-model="employee.email"
                                        :class="{'p-invalid': !isValidEmail(employee.email) && employee.email}"
                                        @input="validateEmail"
                                    />
                                    <label for="email">Email*</label>
                                </FloatLabel>
                                <Message 
                                    v-if="employee.email && !isValidEmail(employee.email)" 
                                    severity="error" 
                                    variant="simple" 
                                    size="small"
                                >
                                    Please enter a valid email address
                                </Message>
                                <small class="p-error" v-if="submitted && !employee.email">Email is required.</small>
                            </div>

                            <div class="flex flex-col gap-2">
                                <FloatLabel variant="on">
                                    <Select
                                        id="role"
                                        v-model="employee.role"
                                        :options="roles"
                                        optionLabel="label"
                                        optionValue="value"
                                        :class="{'p-invalid': submitted && !employee.role}"
                                    />
                                    <label for="role">Role*</label>
                                </FloatLabel>
                                <small class="p-error" v-if="submitted && !employee.role">Role is required.</small>
                            </div>

                            <div class="flex flex-col gap-2">
                                <FloatLabel variant="on">
                                    <AutoComplete
                                        id="country"
                                        v-model="employee.country"
                                        :suggestions="filteredCountries"
                                        @complete="searchCountries"
                                        :field="'name'"
                                        optionLabel="name"
                                        @item-select="onCountrySelect"
                                        :class="{'p-invalid': submitted && !employee.country}"
                                    />
                                    <label for="country">Country*</label>
                                </FloatLabel>
                                <small class="p-error" v-if="submitted && !employee.country">Country is required.</small>
                            </div>

                            <div class="flex flex-col gap-2">
                                <FloatLabel variant="on">
                                    <InputText 
                                        id="phone" 
                                        v-model="employee.phone"
                                        :class="{'p-invalid': submitted && !employee.phone}"
                                    />
                                    <label for="phone">Phone*</label>
                                </FloatLabel>
                                <small class="p-error" v-if="submitted && !employee.phone">Phone is required.</small>
                            </div>

                            <div class="flex flex-col gap-2">
                                <div class="flex items-center gap-2">
                                    <ToggleSwitch 
                                        v-model="employeeStatus" 
                                        id="status"
                                    />
                                    <span class="text-sm text-surface-500">{{ employeeStatus ? 'Active' : 'Inactive' }}</span>
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
            v-model:visible="deleteEmployeeDialog"
            :style="{ width: '450px' }"
            header="Delete Employee"
            :modal="true"
            class="p-fluid"
        >
            <div class="flex flex-col gap-4">
                <div class="text-red-600 font-semibold">Warning: This action cannot be undone</div>
                
                <div class="text-gray-700">
                    To confirm deletion, type the employee's email:
                    <span class="font-semibold">{{ employeeToDelete?.email }}</span>
                </div>
                
                <div class="flex flex-col gap-2">
                    <InputText
                        v-model="confirmationEmail"
                        :class="{'p-invalid': deleteSubmitted && confirmationEmail !== employeeToDelete?.email}"
                        placeholder="Enter employee email"
                    />
                    <small class="p-error" v-if="deleteSubmitted && confirmationEmail !== employeeToDelete?.email">
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
                        @click="deleteEmployeeDialog = false"
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
import Select from 'primevue/select';
import ToggleSwitch from 'primevue/toggleswitch';
import FloatLabel from 'primevue/floatlabel';
import Fieldset from 'primevue/fieldset';
import Message from 'primevue/message';
import { useRouter } from 'vue-router';
import AutoComplete from 'primevue/autocomplete';
import { CountryService } from '@/service/CountryService';

const toast = useToast();
const confirm = useConfirm();
const router = useRouter();
const loading = ref(false);
const employeeDialog = ref(false);
const deleteEmployeeDialog = ref(false);
const submitted = ref(false);
const allEmployees = ref([]); // Store all employees
const employees = ref([]); // Filtered employees to display
const employee = ref({});
const employeeToDelete = ref(null);
const showInactive = ref(false);
const sessionInfo = ref(null);
const confirmationEmail = ref('');
const deleteSubmitted = ref(false);

// Simple filter setup
const filters = ref({
    global: { value: null }
});

// Add roles list after the filters ref
const roles = [
    { label: 'CEO', value: 'CEO' },
    { label: 'CTO', value: 'CTO' },
    { label: 'CFO', value: 'CFO' },
    { label: 'COO', value: 'COO' },
    { label: 'Service Desk Engineer L1', value: 'Service Desk Engineer L1' },
    { label: 'Service Desk Engineer L2', value: 'Service Desk Engineer L2' },
    { label: 'Service Desk Engineer L3', value: 'Service Desk Engineer L3' },
    { label: 'Service Delivery Manager', value: 'Service Delivery Manager' },
    { label: 'External Contractor', value: 'External Contractor' },
    { label: 'Enterprise Architect', value: 'Enterprise Architect' },
    { label: 'Consultant', value: 'Consultant' },
    { label: 'Senior Consultant', value: 'Senior Consultant' }
];

// Add after the roles constant
const countries = ref([]);
const filteredCountries = ref([]);

// GraphQL Queries
const LIST_EMPLOYEES = `
    query EmployeesByCompany($companyId: String!) {
        employeesByCompany(companyId: $companyId) {
            id
            companyId
            companyName
            name
            email
            country
            role
            phone
            status
            createdAt
            updatedAt
        }
    }
`;

const CREATE_EMPLOYEE = `
    mutation CreateEmployee($input: CreateEmployeeInput!) {
        createEmployee(input: $input) {
            id
            companyId
            companyName
            name
            email
            country
            role
            phone
            status
            createdAt
            updatedAt
        }
    }
`;

const UPDATE_EMPLOYEE = `
    mutation UpdateEmployee($id: String!, $input: UpdateEmployeeInput!) {
        updateEmployee(id: $id, input: $input) {
            id
            companyId
            companyName
            name
            email
            country
            role
            phone
            status
            createdAt
            updatedAt
        }
    }
`;

const DELETE_EMPLOYEE = `
    mutation DeleteEmployee($id: String!) {
        deleteEmployee(id: $id)
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

// Load employees
async function loadEmployees() {
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
                query: LIST_EMPLOYEES,
                variables: {
                    companyId: sessionInfo.value.companyId
                }
            })
        });
        const result = await response.json();
        if (result.errors) {
            throw new Error(result.errors[0]?.message || 'Failed to load employees');
        }
        allEmployees.value = result.data.employeesByCompany;
        filterEmployees();
    } catch (error) {
        toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to load employees', life: 3000 });
    }
    loading.value = false;
}

// Filter employees
function filterEmployees() {
    if (showInactive.value) {
        employees.value = [...allEmployees.value].sort((a, b) => a.name.localeCompare(b.name));
    } else {
        employees.value = [...allEmployees.value]
            .filter(employee => employee.status === 'active')
            .sort((a, b) => a.name.localeCompare(b.name));
    }
}

// Open new employee dialog
function openNewEmployee() {
    employee.value = {
        name: '',
        email: '',
        role: 'Service Desk Engineer L1', // Default role
        country: '',
        phone: '+0000000000',
        status: 'active'
    };
    submitted.value = false;
    employeeDialog.value = true;
}

// Edit employee
function editEmployee(data) {
    employee.value = { ...data };
    employeeDialog.value = true;
}

// Hide dialog
function hideDialog() {
    employeeDialog.value = false;
    submitted.value = false;
}

// Email validation
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Save employee
async function saveEmployee() {
    submitted.value = true;

    if (!employee.value.name?.trim() || !employee.value.email?.trim() || 
        !employee.value.role?.trim() || !employee.value.country?.trim() || 
        !employee.value.phone?.trim()) {
        toast.add({ severity: 'error', summary: 'Required Fields', detail: 'Please fill in all required fields', life: 3000 });
        return;
    }

    if (!isValidEmail(employee.value.email)) {
        toast.add({ severity: 'error', summary: 'Invalid Email', detail: 'Please enter a valid email address', life: 3000 });
        return;
    }

    try {
        const isNewEmployee = !employee.value.id;
        const query = isNewEmployee ? CREATE_EMPLOYEE : UPDATE_EMPLOYEE;
        
        const variables = isNewEmployee 
            ? { 
                input: {
                    companyId: sessionInfo.value.companyId,
                    companyName: sessionInfo.value.companyName,
                    name: employee.value.name,
                    email: employee.value.email.toLowerCase(),
                    country: employee.value.country,
                    role: employee.value.role,
                    phone: employee.value.phone,
                    status: employee.value.status
                }
            }
            : { 
                id: employee.value.id,
                input: {
                    name: employee.value.name,
                    email: employee.value.email.toLowerCase(),
                    country: employee.value.country,
                    role: employee.value.role,
                    phone: employee.value.phone,
                    status: employee.value.status
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
            throw new Error(result.errors[0]?.message || 'Failed to save employee');
        }

        toast.add({
            severity: 'success',
            summary: 'Success',
            detail: isNewEmployee ? 'Employee Created' : 'Employee Updated',
            life: 3000
        });

        employeeDialog.value = false;
        await loadEmployees();
    } catch (error) {
        toast.add({
            severity: 'error',
            summary: 'Error',
            detail: error.message || 'Failed to save employee',
            life: 3000
        });
    }
}

// Confirm delete
function confirmDelete(data) {
    employeeToDelete.value = data;
    confirmationEmail.value = '';
    deleteSubmitted.value = false;
    deleteEmployeeDialog.value = true;
}

function handleDeleteConfirm() {
    deleteSubmitted.value = true;
    
    if (confirmationEmail.value !== employeeToDelete.value.email) {
        return;
    }
    
    deleteEmployee(employeeToDelete.value.id);
    deleteEmployeeDialog.value = false;
    employeeToDelete.value = null;
    confirmationEmail.value = '';
}

async function deleteEmployee(id) {
    try {
        const response = await fetch(`${import.meta.env.VITE_API_URL}/graphql`, {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                credentials: 'include'
            },
            body: JSON.stringify({
                query: DELETE_EMPLOYEE,
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
            detail: 'Employee deleted successfully', 
            life: 3000 
        });
        
        await loadEmployees();
    } catch (error) {
        console.error('Failed to delete employee:', error);
        toast.add({ 
            severity: 'error', 
            summary: 'Error', 
            detail: error.message || 'Failed to delete employee', 
            life: 3000 
        });
    }
}

// Email validation
const validateEmail = () => {
    // This empty function is needed to satisfy template reference
    // Actual validation is handled by isValidEmail in the Message component
};

// Employee status computed property
const employeeStatus = computed({
    get: () => employee.value.status === 'active',
    set: (newValue) => {
        employee.value.status = newValue ? 'active' : 'inactive'
    }
});

// Add these functions before onMounted
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
    employee.value.country = event.value.name;
}

// Update onMounted
onMounted(async () => {
    try {
        await fetchSessionInfo();
        await loadCountries();
        await loadEmployees();
    } catch (error) {
        console.error('Error initializing employees page:', error);
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

/* InputNumber Specific */
:deep(.p-inputnumber-input) {
    height: 40px;
    padding: 0.5rem 0.75rem;
}

:deep(.p-inputnumber-button-group) {
    height: 40px;
}

:deep(.p-inputnumber-button) {
    height: 20px;
    width: 40px;
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
</style> 