<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import Button from 'primevue/button';
import Card from 'primevue/card';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Toast from 'primevue/toast';
import { useToast } from 'primevue/usetoast';
import { useConfirm } from 'primevue/useconfirm';
import ConfirmPopup from 'primevue/confirmpopup';
import InputText from 'primevue/inputtext';

//redirects to unauthorized if the user role is lower than the pagerole
import { getPageAuthorization } from '@/utils/utils';
const pageRole = 4; // Set the required role for this page
getPageAuthorization(pageRole);



const toast = useToast();
const confirm = useConfirm();
const showDialog = ref(false);
const certifications = ref([]);
const dialogData = ref({ id: null, name: '' });
const searchQuery = ref('');

onMounted(fetchCertifications);

async function fetchCertifications() {
  try {
    const response = await axios.post(`/api/api`, { action: 'listCertifications' });
    certifications.value = response.data;
  } catch (error) {
    console.error("Error fetching certifications:", error);
  }
}

const filteredCertifications = computed(() => {
  return certifications.value.filter(certification => 
    certification.certification.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});

function openDialog(item = null) {
  dialogData.value = {
    id: item?.id || null,
    name: item?.certification || ''
  };
  showDialog.value = true;
}

async function handleAddOrEdit() {
  if (!dialogData.value.name.trim()) {
    toast.add({ severity: 'warn', summary: 'Warning', detail: 'Name is required', life: 3000 });
    return;
  }

  const action = dialogData.value.id ? 'updateCertification' : 'addCertification';
  try {
    const response = await axios.post(`/api/api`, {
      action,
      id: dialogData.value.id,
      certification: dialogData.value.name
    });

    if (response.data.success) {
      toast.add({ severity: 'success', summary: 'Success', detail: 'Certification saved!', life: 3000 });
      fetchCertifications();
      showDialog.value = false;
    } else {
      toast.add({ severity: 'error', summary: 'Error', detail: response.data.error || 'Failed to save certification' });
    }
  } catch (error) {
    console.error("Error adding/updating certification:", error);
    toast.add({ severity: 'error', summary: 'Error', detail: 'An error occurred', life: 3000 });
  }
}

async function handleDelete(certificationId) {
  try {
    const response = await axios.post(`/api/api`, {
      action: 'deleteCertification',
      id: certificationId,
    });

    if (response.data.success) {
      toast.add({ severity: 'success', summary: 'Success', detail: 'Certification deleted!', life: 3000 });
      fetchCertifications(); 
    } else {
      toast.add({ severity: 'error', summary: 'Error', detail: response.data.error || 'Failed to delete certification' });
    }
  } catch (error) {
    console.error("Error deleting certification:", error);
    toast.add({ severity: 'error', summary: 'Error', detail: 'An error occurred', life: 3000 });
  }
}

function confirmDelete(event, certificationId) {
  confirm.require({
    target: event.currentTarget,
    message: 'Are you sure you want to delete this certification?',
    header: 'Confirmation',
    icon: 'pi pi-exclamation-triangle',
    accept: () => handleDelete(certificationId),
  });
}
</script>

<template>
  <div class="card">
    <div class="col-12">
      <h5>Certifications</h5>
      <div class="flex-container">
        <div class="p-inputgroup">
          <span class="p-inputgroup-addon"><i class="pi pi-search"></i></span>
          <InputText v-model="searchQuery" placeholder="Search Certification" />
        </div>
        <Button  raised @click="openDialog()" class="add-button" icon="pi pi-plus" />
      </div>
      <div class="certifications-grid">
        <div class="certification-item" v-for="certification in filteredCertifications" :key="certification.id">
          <div>{{ certification.certification }}</div>
          <div class="actions-buttons">
            <Button icon="pi pi-pencil" severity="warning" text raised  class="mb-2 mr-2" @click="openDialog(certification)" />
            <Button icon="pi pi-trash" severity="danger" text raised  class="mb-2 mr-2" @click="confirmDelete($event, certification.id)" />
          </div>
        </div>
      </div>
      <div v-if="certifications.length == 0">Loading certifications...</div>
    </div>
  </div>

  <Dialog v-model:visible="showDialog" header="Certification" :modal="true" :closable="false"  >
    <InputText v-model="dialogData.name" placeholder="Certification Name" autofocus :style="{ width: '70vw', maxWidth: '100vw' }"/>
    <template #footer>
      <Button label="Cancel" @click="showDialog = false" text />
      <Button label="Save" @click="handleAddOrEdit" />
    </template>
  </Dialog>

  <Toast />
  <ConfirmPopup />
</template>

<style scoped>
.flex-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.add-button {
  margin-left: auto;
}

.certifications-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.certification-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.1rem;
  border: 1px dotted #e0e0e0;
  border-radius: 4px;
 
}

.actions-buttons {
  display: flex;
  gap: 0.5rem;
}

@media (max-width: 767px) {
  .certifications-grid {
    grid-template-columns: 1fr;
  }
  .p-dialog {
    width: 100% !important;
    max-width: 100% !important;
  }
}
</style>