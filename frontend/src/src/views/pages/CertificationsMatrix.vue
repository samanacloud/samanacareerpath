<script setup>
import { ref, onMounted, computed } from 'vue';
import { getPageAuthorization } from '@/utils/utils';
import axios from 'axios';
import Tag from 'primevue/tag'; // Correctly import the Tag component
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Button from 'primevue/button';
import InputText from 'primevue/inputtext';
import Dropdown from 'primevue/dropdown';

// Redirects to unauthorized if the user role is lower than the pagerole
const pageRole = 3; // Set the required role for this page
getPageAuthorization(pageRole);

const employeeCertifications = ref([]);
const candidateCertifications = ref([]);
const employeeEmails = ref([]);
const candidateEmails = ref([]);
const searchQuery = ref('');
const searchType = ref('certification'); // 'certification' or 'email'
const idFrozen = ref(false); // Add this line for dynamic toggling


const fetchCertifications = async () => {
  try {
    const employeeResponse = await axios.post('/api/api', { action: 'listAllEmployeeCertifications' });
    const candidateResponse = await axios.post('/api/api', { action: 'listAllCandidateCertifications' });

    const employeeData = employeeResponse.data;
    const candidateData = candidateResponse.data;

    const employeeCertMap = {};
    const candidateCertMap = {};

    employeeData.forEach((cert) => {
      if (!employeeCertMap[cert.certification]) {
        employeeCertMap[cert.certification] = {};
      }
      employeeCertMap[cert.certification][cert.email] = true;
      if (!employeeEmails.value.includes(cert.email)) {
        employeeEmails.value.push(cert.email);
      }
    });

    candidateData.forEach((cert) => {
      if (!candidateCertMap[cert.certification]) {
        candidateCertMap[cert.certification] = {};
      }
      candidateCertMap[cert.certification][cert.email] = true;
      if (!candidateEmails.value.includes(cert.email)) {
        candidateEmails.value.push(cert.email);
      }
    });

    employeeCertifications.value = Object.entries(employeeCertMap).map(([certification, emails]) => ({
      certification,
      emails,
    }));

    candidateCertifications.value = Object.entries(candidateCertMap).map(([certification, emails]) => ({
      certification,
      emails,
    }));
  } catch (error) {
    console.error('Error fetching certifications:', error);
  }
};

const filteredEmployeeCertifications = computed(() => {
  if (searchQuery.value === '') return employeeCertifications.value;
  return employeeCertifications.value.filter((cert) => {
    if (searchType.value === 'certification') {
      return cert.certification.toLowerCase().includes(searchQuery.value.toLowerCase());
    } else {
      return Object.keys(cert.emails).some((email) => email.toLowerCase().includes(searchQuery.value.toLowerCase()));
    }
  });
});

const filteredCandidateCertifications = computed(() => {
  if (searchQuery.value === '') return candidateCertifications.value;
  return candidateCertifications.value.filter((cert) => {
    if (searchType.value === 'certification') {
      return cert.certification.toLowerCase().includes(searchQuery.value.toLowerCase());
    } else {
      return Object.keys(cert.emails).some((email) => email.toLowerCase().includes(searchQuery.value.toLowerCase()));
    }
  });
});

onMounted(() => {
  fetchCertifications();
});
</script>

<template>
  <div class="card">
    <h5>Certifications Matrix</h5>
    <p>Use this page to start from scratch and place your custom content.</p>

    <div>
      <h6>Search</h6>
      <div class="p-inputgroup">
        <span class="p-inputgroup-addon">
          <i class="pi pi-search"></i>
        </span>
        <InputText v-model="searchQuery" type="text" placeholder="Search by certification or email" />
        <Dropdown v-model="searchType" :options="[{ label: 'Certification', value: 'certification' }, { label: 'Email', value: 'email' }]" optionLabel="label" optionValue="value" />
      </div>
    </div>

    <div>
      <h6>Employee Certifications</h6>
      <DataTable :value="filteredEmployeeCertifications"  :scrollable="true" scrollHeight="60vh" scrollDirection="vertical">
        <Column field="certification" header="Certification" :sortable="true" frozen alignFrozen="left" ></Column>
        <Column
          v-for="email in employeeEmails"
          :key="email"
          :field="`emails.${email}`"
          :header="email"
          :sortable="true"
        >
          <template #body="slotProps">
            <Tag v-if="slotProps.data.emails[email]"  class="pi pi-check" severity="success" />
            <Tag v-else class="pi pi-times" severity="danger" />
          </template>
        </Column>
      </DataTable>
    </div>


  </div>
</template>

<style>
/* Add any additional styling you need here */
</style>