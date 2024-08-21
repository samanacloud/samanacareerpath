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
const pageRole = 3; // Set the required role for this page
getPageAuthorization(pageRole);


const toast = useToast();
const confirm = useConfirm();
const showDialog = ref(false);
const categories = ref([]);
const dialogData = ref({ id: null, type: 'category', name: '' });
const skillsets = ref([]);
const showDetailsDialog = ref(false);
const selectedCategoryId = ref(null);
const selectedCategoryName = ref('');

onMounted(fetchCategories);

async function fetchCategories() {
  try {
    const response = await axios.post(`/api/apitest`, { action: 'listJobCategories' });
    categories.value = response.data;
  } catch (error) {
    console.error("Error fetching categories:", error);
  }
}

async function fetchSkillsets(categoryId, categoryName) {
  selectedCategoryId.value = categoryId;
  selectedCategoryName.value = categoryName;
  try {
    const response = await axios.post(`/api/apitest`, { action: 'listJobSkillsets' });
    skillsets.value = response.data.filter(skillset => skillset.category_id === categoryId);
  } catch (error) {
    console.error("Error fetching skillsets:", error);
  }
}

function openCategoryDialog(item = null) {
  dialogData.value = {
    id: item?.id || null,
    type: 'category',
    name: item?.category_name || ''
  };
  showDialog.value = true;
}

function openSkillsetDialog(item = null) {
  dialogData.value = {
    id: item?.id || null,
    type: 'skillset',
    name: item?.skillset_name || ''
  };
  showDialog.value = true;
}

async function handleAddOrEdit() {
  if (!dialogData.value.name.trim()) {
    toast.add({ severity: 'warn', summary: 'Warning', detail: 'Name is required', life: 3000 });
    return;
  }

  const action = dialogData.value.id
    ? dialogData.value.type === 'category' ? 'updateJobCategory' : 'updateJobSkillset'
    : dialogData.value.type === 'category' ? 'addJobCategory' : 'addJobSkillset';
  
  const payload = {
    action,
    id: dialogData.value.id,
    category_name: dialogData.value.type === 'category' ? dialogData.value.name : undefined,
    skillset_name: dialogData.value.type === 'skillset' ? dialogData.value.name : undefined,
    category_id: dialogData.value.type === 'skillset' ? selectedCategoryId.value : undefined
  };

  try {
    const response = await axios.post(`/api/apitest`, payload);

    if (response.data.success) {
      toast.add({ severity: 'success', summary: 'Success', detail: `${dialogData.value.type.charAt(0).toUpperCase() + dialogData.value.type.slice(1)} saved!`, life: 3000 });
      fetchCategories();
      if (dialogData.value.type === 'skillset') {
        fetchSkillsets(selectedCategoryId.value, selectedCategoryName.value);
      }
      showDialog.value = false;
    } else {
      toast.add({ severity: 'error', summary: 'Error', detail: response.data.error || `Failed to save ${dialogData.value.type}` });
    }
  } catch (error) {
    console.error(`Error adding/updating ${dialogData.value.type}:`, error);
    toast.add({ severity: 'error', summary: 'Error', detail: 'An error occurred', life: 3000 });
  }
}

async function handleDelete(id, itemType) {
  const action = itemType === 'category' ? 'deleteJobCategory' : 'deleteJobSkillset';
  try {
    const response = await axios.post(`/api/apitest`, {
      action,
      id: id,
    });

    if (response.data.success) {
      toast.add({ severity: 'success', summary: 'Success', detail: `${itemType.charAt(0).toUpperCase() + itemType.slice(1)} deleted!`, life: 3000 });
      fetchCategories();
      if (itemType === 'skillset') {
        fetchSkillsets(selectedCategoryId.value, selectedCategoryName.value);
      }
    } else {
      toast.add({ severity: 'error', summary: 'Error', detail: response.data.error || `Failed to delete ${itemType}` });
    }
  } catch (error) {
    console.error(`Error deleting ${itemType}:`, error);
    toast.add({ severity: 'error', summary: 'Error', detail: 'An error occurred', life: 3000 });
  }
}

function confirmDelete(event, id, itemType) {
  confirm.require({
    target: event.currentTarget,
    message: `Are you sure you want to delete this ${itemType}?`,
    header: 'Confirmation',
    icon: 'pi pi-exclamation-triangle',
    accept: () => handleDelete(id, itemType),
  });
}
</script>

<template>
  <div class="card"><div class="grid">
    <div class="col-12 xl:col-6">
      <h5>Skillset Categories</h5>
      <DataTable :value="categories" responsiveLayout="scroll" :bodyStyle="{ textAlign: 'right' }">
        <Column field="category_name" header="Category Name"></Column>
        <Column header="Actions" class="actions-column">
          <template #body="slotProps">
            <div style="display: flex; justify-content: flex-end;">
              <Button icon="pi pi-eye" severity="success"   text raised @click="fetchSkillsets(slotProps.data.id, slotProps.data.category_name)" />
              <Button icon="pi pi-pencil" severity="warning"  text raised @click="openCategoryDialog(slotProps.data)" />
              <Button icon="pi pi-trash" severity="danger" text raised @click="confirmDelete($event, slotProps.data.id, 'category')" />
            </div>
          </template>
        </Column>
      </DataTable>

      <Button label="Add Category" raised @click="openCategoryDialog()" class="mt-3" />
      <div v-if="categories.length == 0">Loading categories...</div>
    </div>

    <div class="col-12 xl:col-6" v-if="selectedCategoryId">
      <h5>{{ selectedCategoryName }} Skillsets</h5>
      <DataTable :value="skillsets" responsiveLayout="scroll" :bodyStyle="{ textAlign: 'right' }">
        <Column field="skillset_name" header="Skillset Name"></Column>
        <Column header="Actions" class="actions-column">
          <template #body="slotProps">
            <div style="display: flex; justify-content: flex-end;">
              <Button icon="pi pi-pencil" severity="warning" text raised  class="mb-2 mr-2" @click="openSkillsetDialog(slotProps.data)" />
              <Button icon="pi pi-trash" severity="danger" text raised class="mb-2 mr-2" @click="confirmDelete($event, slotProps.data.id, 'skillset')" />
            </div>
          </template>
        </Column>
      </DataTable>

      <Button label="Add Skillset" raised @click="openSkillsetDialog()" class="mt-3" />
    </div>
  </div>
  </div>

  <Dialog v-model:visible="showDialog" header="Details" :modal="true" :closable="true" :style="{ width: '70vw' }">
    <template #footer>
      <Button label="Cancel" @click="showDialog = false" class="p-button-text"  />
      <Button label="Save" @click="handleAddOrEdit" />
    </template>
    <div>
      <span>Name</span>
      <InputText v-model="dialogData.name" class="w-full" />
    </div>
  </Dialog>

  <Toast />
  <ConfirmPopup /> 
</template>

<style scoped>
.card {
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
}

.mt-3 {
  margin-top: 1rem;
}

.p-button-danger {
  margin-left: 0.5rem;
}

.p-datatable .p-datatable-tbody > tr > td {
  padding: 0.5rem 0.75rem; /* Adjust the padding as needed */
}

.p-datatable .p-datatable-tbody > tr > td .p-button {
  margin: 0 0.25rem; /* Adjust the margin between buttons */
}

.p-datatable .p-datatable-tbody > tr {
  height: auto; /* Allow rows to adjust height based on content */
}

.highlighted-row {
  background-color: #f0f0f0 !important; /* Adjust the highlight color as needed */
}

/* Style the Actions column HEADER */
.p-datatable .p-datatable-thead > tr > th:last-child {
  display: flex; /* Use flexbox to control header content layout */
  justify-content: flex-end; /* Push content to the right */
  align-items: center; /* Vertically center content */
  padding-right: 20px; /* Adjust padding to match button alignment */
}


.p-datatable .p-datatable-thead > tr > th:last-child {
  text-align: right !important; /* Align the header text to the right */
  padding-right: 20px; /* Adjust padding to align with the buttons */
}
.actions-column {
  width: 20px;
}
@media (max-width: 768px) {
  .p-dialog {
    width: '100vw';
   
  }
}
</style>