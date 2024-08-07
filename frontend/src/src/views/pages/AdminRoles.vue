<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import { useToast } from 'primevue/usetoast';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import InputText from 'primevue/inputtext';
import Button from 'primevue/button';

//redirects to unauthorized if the user role is lower than the pagerole
import { getPageAuthorization } from '@/utils/utils';
const pageRole = 5; // Set the required role for this page
getPageAuthorization(pageRole);



// Function to get the base URL
const baseURL = import.meta.env.VITE_SITE_URL 
    ? `https://${import.meta.env.VITE_SITE_URL}` 
    : 'http://localhost:8080'; 

const roles = ref([]);
const search = ref('');
const toast = useToast();
const dialogVisible = ref(false);
const deleteDialogVisible = ref(false);
const roleToDelete = ref(null);
const selectedRole = ref({ id: '', functionName: '', authrole: '' });
const showEditDialog = ref(false);
const newRole = ref({ functionName: '', authrole: '' });
const addDialogVisible = ref(false);

const openAddDialog = () => {

    addDialogVisible.value = true;
};

const fetchRoles = async () => {
    try {
        const response = await axios.post(`${baseURL}/api/apitest.php`, {
            action: 'listAdminRoles'
        });
        roles.value = response.data;
    } catch (error) {
        toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to fetch roles', life: 3000 });
    }
};

const openEditDialog = (role) => {
    selectedRole.value = { ...role };
    showEditDialog.value = true;
};

onMounted(async () => {
    await fetchRoles();
});

const filteredRoles = computed(() => {
    if (!search.value) {
        return roles.value;
    }
    return roles.value.filter((role) =>
        role.functionName.toLowerCase().includes(search.value.toLowerCase())
    );
});

const confirmDeleteRole = (role) => {
    roleToDelete.value = role;
    deleteDialogVisible.value = true;
};

const deleteRole = async () => {
    try {
        const response = await axios.post(`${baseURL}/api/apitest.php`, {
            action: 'deleteAdminRole',
            id: roleToDelete.value.id
        });
        if (response.data.success) {
            fetchRoles();
            deleteDialogVisible.value = false;
            roleToDelete.value = null;
            toast.add({ severity: 'success', summary: 'Success', detail: 'Role deleted successfully', life: 3000 });
        } else {
            toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to delete role', life: 3000 });
        }
    } catch (error) {
        toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to delete role', life: 3000 });
    }
};

const updateRole = async () => {
    try {
        const response = await axios.post(`${baseURL}/api/apitest.php`, {
            action: 'updateAdminRole',
            id: selectedRole.value.id,
            functionName: selectedRole.value.functionName,
            authrole: selectedRole.value.authrole
        });
        if (response.data.success) {
            toast.add({ severity: 'success', summary: 'Success', detail: 'Role updated successfully', life: 3000 });
            fetchRoles(); // Fetch roles again to refresh the list
            showEditDialog.value = false;
        } else {
            toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to update role', life: 3000 });
        }
    } catch (error) {
        toast.add({ severity: 'error', summary: 'Error', detail: error.message, life: 3000 });
    }
};

const addRole = async () => {
    try {
        const response = await axios.post(`${baseURL}/api/apitest.php`, {
            action: 'addAdminRole',
            functionName: newRole.value.functionName,
            authrole: newRole.value.authrole
        });
        if (response.data.success) {
            toast.add({ severity: 'success', summary: 'Success', detail: 'Role added successfully', life: 3000 });
            fetchRoles(); // Refresh the list
            addDialogVisible.value = false;
        } else {
            toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to add role', life: 3000 });
        }
    } catch (error) {
        toast.add({ severity: 'error', summary: 'Error', detail: error.message, life: 3000 });
    }
};
</script>

<template>
    <div class="card">
        <h5>Admin Roles</h5>
        <div class="p-d-flex p-ai-center p-jc-between p-mb-2">
            <span class="p-input-icon-left col-9" >
                <i class="pi pi-search" />
                <InputText v-model="search" placeholder="Search..." />
             
            </span>
            <Button label="Add Role" icon="pi pi-plus" class="p-button-success" @click="openAddDialog" />
                </div>
        <DataTable :value="filteredRoles" :paginator="true" :rows="10" :responsiveLayout="'scroll'">
            <Column field="id" header="ID" :sortable="true" />
            <Column field="functionName" header="Function Name" :sortable="true" />
            <Column field="authrole" header="Auth Role" :sortable="true" />
            <Column header="Action">
                <template #body="slotProps">
                    <Button icon="pi pi-pencil" severity="success" text outlined raised @click="openEditDialog(slotProps.data)" />
                    <Button icon="pi pi-trash" severity="danger" text outlined raised @click="confirmDeleteRole(slotProps.data)" />
                </template>
            </Column>
        </DataTable>
        <Toast />
    </div>
    <Dialog header="Confirm Deletion" :visible.sync="deleteDialogVisible" :modal="true" :closable="false">
    <p>Are you sure you want to delete this role?</p>
    <div class="p-d-flex p-ai-center p-jc-between p-mt-4">
        
        <Button label="Cancel" icon="pi pi-times" @click="deleteDialogVisible = false" class="p-button-text" />
        <Button label="Delete" icon="pi pi-check" @click="deleteRole" class="p-button-danger" />
    </div>
</Dialog>
<Dialog header="Edit Role" v-model:visible="showEditDialog" style="width: 50vw" modal>
    <div class="p-fluid">
        <div class="p-field">
            <label for="functionName">Function Name</label>
            <InputText id="functionName" v-model="selectedRole.functionName" />
        </div>
        <div class="p-field">
            <label for="authRole">Auth Role</label>
            <InputText id="authRole" v-model="selectedRole.authrole" />
        </div>
        <div class="p-field">
            <Button label="Save" @click="updateRole" />
        </div>
    </div>
</Dialog>
<Dialog header="Add Role" v-model:visible="addDialogVisible" style="width: 50vw" modal>
    <div class="p-fluid">
        <div class="p-field">
            <label for="newFunctionName">Function Name</label>
            <InputText id="newFunctionName" v-model="newRole.functionName" />
        </div>
        <div class="p-field">
            <label for="newAuthRole">Auth Role</label>
            <InputText id="newAuthRole" v-model="newRole.authrole" />
        </div>
        <div class="p-field">
            <Button label="Save" @click="addRole" />
        </div>
    </div>
</Dialog>
</template>

<style scoped>
.p-input-icon-left .pi {
    left: 0.5rem;
}
</style>