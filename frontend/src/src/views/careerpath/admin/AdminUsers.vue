<template>
    <div class="card">
      <Toast />
      <ConfirmDialog />
  
      <!-- Header Section -->
      <div class="flex flex-col gap-4">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-2xl font-medium text-900">Users Administration</h1>
            <p class="text-sm font-medium text-500">Manage your organization's team members</p>
          </div>
          <Button 
            label="Add User" 
            icon="pi pi-plus" 
            outlined 
            raised 
            class="bg-white" 
            @click="openNewUser" 
          />
        </div>
  
        <!-- Search and Filter Bar -->
        <div class="flex justify-between items-center bg-white p-4 rounded-lg shadow-sm">
          <IconField class="w-96">
            <InputIcon class="pi pi-search" />
            <InputText 
              v-model="filters['global'].value" 
              placeholder="Search users..." 
              class="w-full"
            />
          </IconField>
          <div class="flex items-center gap-3">
            <label class="text-gray-600">Show Inactive</label>
            <ToggleSwitch v-model="showInactive" @change="filterUsers" />
          </div>
        </div>
  
        <!-- Users List -->
        <div class="bg-white rounded-lg shadow-sm">
          <DataTable
            :value="users"
            :loading="loading"
            dataKey="id"
            :paginator="true"
            :rows="10"
            :rowsPerPageOptions="[5, 10, 20, 50]"
            responsiveLayout="scroll"
            v-model:filters="filters"
            filterDisplay="menu"
            :globalFilterFields="['name', 'email', 'role', 'license']"
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
  
            <Column field="status" header="Status" sortable>
              <template #body="{ data }">
                <Tag 
                  :severity="data.status === 'active' ? 'success' : 'danger'" 
                  :value="data.status"
                  class="text-xs"
                />
              </template>
            </Column>
  
            <Column field="license" header="License" sortable>
              <template #body="{ data }">
                <span class="text-gray-700">{{ data.license }}</span>
              </template>
            </Column>
  
            <Column :exportable="false" style="width:100px">
              <template #body="{ data }">
                <div class="flex gap-2">
                  <Button 
                    icon="pi pi-pencil" 
                    text 
                    rounded 
                    @click="editUser(data)"
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
  
      <!-- User Dialog -->
      <Dialog 
          v-model:visible="userDialog" 
          :style="{ width: '95%', maxWidth: '900px' }" 
          header="User Details" 
          :modal="true" 
          class="p-fluid"
      >
          <form @submit.prevent="saveUser">
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
                                      v-model="user.name" 
                                      :class="{'p-invalid': submitted && !user.name}"
                                      autofocus
                                  />
                                  <label for="name">Full Name*</label>
                              </FloatLabel>
                              <small class="p-error" v-if="submitted && !user.name">Name is required.</small>
                          </div>
                          
                          <div class="flex flex-col gap-2">
                              <FloatLabel variant="on">
                                  <InputText 
                                      id="email" 
                                      v-model="user.email"
                                      :class="{'p-invalid': !isValidEmail(user.email) && user.email}"
                                      :disabled="!!user.id"
                                      @input="validateEmail"
                                  />
                                  <label for="email">Email*</label>
                              </FloatLabel>
                              <Message 
                                  v-if="user.email && !isValidEmail(user.email)" 
                                  severity="error" 
                                  variant="simple" 
                                  size="small"
                              >
                                  Please enter a valid email address
                              </Message>
                              <small class="p-error" v-if="submitted && !user.email">Email is required.</small>
                          </div>
                          
                          <div class="flex flex-col gap-2">
                              <FloatLabel variant="on">
                                  <AutoComplete
                                      id="country"
                                      v-model="user.country"
                                      :suggestions="filteredCountries"
                                      @complete="searchCountries"
                                      :field="'name'"
                                      optionLabel="name"
                                      @item-select="onCountrySelect"
                                  />
                                  <label for="country">Country</label>
                              </FloatLabel>
                          </div>
                          
                          <div class="flex flex-col gap-2">
                              <FloatLabel variant="on">
                                  <InputText 
                                      id="phone" 
                                      v-model="user.phone" 
                                  />
                                  <label for="phone">Phone Number</label>
                              </FloatLabel>
                          </div>
                          
                          <!-- Role and License in the same row -->
                          <div class="grid grid-cols-2 gap-4">
                              <div class="flex flex-col gap-2">
                                  <FloatLabel variant="on">
                                      <Select
                                          id="role"
                                          v-model="user.role"
                                          :options="roles"
                                          optionLabel="label"
                                          optionValue="value"
                                      />
                                      <label for="role">Role</label>
                                  </FloatLabel>
                              </div>
                              <div class="flex flex-col gap-2">
                                  <FloatLabel variant="on">
                                      <Select
                                          id="license"
                                          v-model="user.license"
                                          :options="licenseTypes"
                                          optionLabel="label"
                                          optionValue="value"
                                      />
                                      <label for="license">License</label>
                                  </FloatLabel>
                              </div>
                          </div>
                          
                          <div class="flex flex-col gap-2">
                              <div class="flex items-center gap-2">
                                  <ToggleSwitch 
                                      v-model="userStatus" 
                                      id="status"
                                  />
                                  <span class="text-sm text-surface-500">{{ userStatus ? 'Active' : 'Inactive' }}</span>
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
          v-model:visible="deleteUserDialog"
          :style="{ width: '450px' }"
          header="Delete User"
          :modal="true"
          class="p-fluid"
      >
          <div class="flex flex-col gap-4">
              <div class="text-red-600 font-semibold">Warning: This action cannot be undone</div>
              
              <div class="text-gray-700">
                  To confirm deletion, type the user's email:
                  <span class="font-semibold">{{ userToDelete?.email }}</span>
              </div>
              
              <div class="flex flex-col gap-2">
                  <InputText
                      v-model="confirmationEmail"
                      :class="{'p-invalid': deleteSubmitted && confirmationEmail !== userToDelete?.email}"
                      placeholder="Enter user email"
                  />
                  <small class="p-error" v-if="deleteSubmitted && confirmationEmail !== userToDelete?.email">
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
                      @click="deleteUserDialog = false"
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
  import { CountryService } from '@/service/CountryService';
  import { useRouter } from 'vue-router';
  import Select from 'primevue/select';
  import ToggleSwitch from 'primevue/toggleswitch';
  import AutoComplete from 'primevue/autocomplete';
  import FloatLabel from 'primevue/floatlabel';
  import Fieldset from 'primevue/fieldset';
  import Message from 'primevue/message';
  
  const toast = useToast();
  const confirm = useConfirm();
  const loading = ref(false);
  const userDialog = ref(false);
  const submitted = ref(false);
  const allUsers = ref([]); // Store all users
  const users = ref([]); // Filtered users to display
  const user = ref({});
  const countries = ref([]);
  const filteredCountries = ref([]);
  const licenseTypes = [
      { label: 'Basic (T0)', value: 't0' },
      { label: 'Standard (T1)', value: 't1' },
      { label: 'Premium (T2)', value: 't2' }
  ];
  const showInactive = ref(false);
  const companyName = ref('');
  const deleteUserDialog = ref(false);
  const userToDelete = ref(null);
  const confirmationEmail = ref('');
  const deleteSubmitted = ref(false);
  const sessionInfo = ref(null);
  
  // Simple filter setup
  const filters = ref({
    global: { value: null }
  });
  
  // GraphQL Queries
  const LIST_USERS = `
    query ListUsersByCompany($companyId: String!) {
      usersByCompany(companyId: $companyId) {
        id
        name
        email
        role
        status
        country
        phone
        license
        companyId
        companyName
        createdAt
        updatedAt
      }
    }
  `;
  
  const CREATE_USER = `
    mutation CreateUser($input: CreateUserInput!) {
      createUser(input: $input) {
        id
        name
        email
        role
        status
        country
        phone
        license
        companyId
      }
    }
  `;
  
  const UPDATE_USER = `
    mutation UpdateUser($id: String!, $input: UpdateUserInput!) {
      updateUser(id: $id, input: $input) {
        id
        name
        email
        role
        status
        country
        phone
        license
        companyId
      }
    }
  `;
  
  const DELETE_USER = `
    mutation DeleteUser($id: String!) {
      deleteUser(id: $id)
    }
  `;
  
  const router = useRouter();
  
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
              companyName.value = data.user.companyName; // Set company name from session
          }
      } catch (error) {
          console.error('Error fetching session info:', error);
          router.push({ name: 'companies' });
      }
  };
  
  // Update loadUsers to use sessionInfo
  async function loadUsers() {
      if (!sessionInfo.value?.companyId) {
          toast.add({ severity: 'warn', summary: 'No Company Selected', detail: 'Please select a company first', life: 3000 });
          router.push({ name: 'companies' });
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
                  query: LIST_USERS,
                  variables: {
                      companyId: sessionInfo.value.companyId
                  }
              })
          });
          const result = await response.json();
          if (result.errors) {
              toast.add({ 
                  severity: 'error', 
                  summary: 'Error', 
                  detail: result.errors[0]?.message || 'Failed to load users', 
                  life: 3000 
              });
              return;
          }
          allUsers.value = result.data.usersByCompany;
          filterUsers(); // Apply the filter
      } catch (error) {
          toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to load users', life: 3000 });
      }
      loading.value = false;
  }
  
  // Add filter function
  function filterUsers() {
      if (showInactive.value) {
          users.value = allUsers.value;
      } else {
          users.value = allUsers.value.filter(user => 
              user.status === 'active'
          );
      }
  }
  
  // Modify openNew to use sessionInfo
  function openNewUser() {
      if (!sessionInfo.value?.companyId) {
          toast.add({
              severity: 'warn',
              summary: 'No Company Selected',
              detail: 'Please select a company first',
              life: 3000
          });
          router.push({ name: 'companies' });
          return;
      }
  
      user.value = {
          name: '',
          email: '',
          role: 'user',
          status: 'active',
          country: '',
          phone: '+0000000000', // Default phone number
          license: 't0'
      };
      submitted.value = false;
      userDialog.value = true;
  }
  
  // Edit user
  function editUser(data) {
      user.value = { 
          id: data.id,
          name: data.name || '',
          email: data.email || '',
          role: data.role || 'user',
          status: data.status || 'active',
          country: data.country || '',
          phone: data.phone || '+0000000000',
          license: data.license || 't0'
      };
      userDialog.value = true;
  }
  
  // Hide dialog
  function hideDialog() {
    userDialog.value = false;
    submitted.value = false;
  }
  
  // Add a function to parse MongoDB error messages
  function parseMongoError(error) {
      if (error.includes('duplicate key error') && error.includes('email_1')) {
          return 'A user with this email already exists';
      }
      return error;
  }
  
  // Add this email validation function
  function isValidEmail(email) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return emailRegex.test(email);
  }
  
  // Update the saveUser function
  async function saveUser() {
      submitted.value = true;
  
      // Validate required fields
      if (!user.value.name?.trim() || !user.value.email?.trim() || !user.value.phone?.trim()) {
          toast.add({ severity: 'error', summary: 'Required Fields', detail: 'Please fill in all required fields', life: 3000 });
          return;
      }
  
      // Validate email format
      if (!isValidEmail(user.value.email)) {
          toast.add({ severity: 'error', summary: 'Invalid Email', detail: 'Please enter a valid email address', life: 3000 });
          return;
      }
  
      try {
          const isNewUser = !user.value.id;
          const query = isNewUser ? CREATE_USER : UPDATE_USER;
          
          // Convert email to lowercase
          const email = user.value.email.toLowerCase();

          // Prepare input data according to backend schemas
          const variables = isNewUser 
              ? { 
                  input: {
                      companyId: sessionInfo.value.companyId,
                      companyName: companyName.value,
                      name: user.value.name,
                      email: email, // Use lowercase email
                      role: user.value.role,
                      status: user.value.status,
                      country: user.value.country,
                      phone: user.value.phone,
                      license: user.value.license
                  }
              }
              : { 
                  id: user.value.id,
                  input: {
                      name: user.value.name,
                      email: email, // Use lowercase email
                      role: user.value.role,
                      status: user.value.status,
                      country: user.value.country,
                      phone: user.value.phone,
                      license: user.value.license
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
              throw new Error(result.errors[0]?.message || 'Failed to save user');
          }
  
          toast.add({
              severity: 'success',
              summary: 'Success',
              detail: isNewUser ? 'User Created' : 'User Updated',
              life: 3000
          });
  
          userDialog.value = false;
          await loadUsers();
      } catch (error) {
          console.error('Save error:', error);
          toast.add({
              severity: 'error',
              summary: 'Error',
              detail: error.message || 'Failed to save user',
              life: 3000
          });
      }
  }
  
  // Delete user
  function confirmDelete(data) {
      userToDelete.value = data;
      confirmationEmail.value = '';
      deleteSubmitted.value = false;
      deleteUserDialog.value = true;
  }
  
  function handleDeleteConfirm() {
      deleteSubmitted.value = true;
      
      if (confirmationEmail.value !== userToDelete.value.email) {
          return;
      }
      
      deleteUser(userToDelete.value.id);
      deleteUserDialog.value = false;
      userToDelete.value = null;
      confirmationEmail.value = '';
  }
  
  async function deleteUser(id) {
      try {
          const response = await fetch(`${import.meta.env.VITE_API_URL}/graphql`, {
              method: 'POST',
              headers: { 
                  'Content-Type': 'application/json',
                  credentials: 'include'
              },
              body: JSON.stringify({
                  query: DELETE_USER,
                  variables: { id: id }
              })
          });
          
          const result = await response.json();
          if (result.errors) {
              throw new Error(result.errors[0].message);
          }
  
          if (!result.data?.deleteUser) {
              throw new Error('Failed to delete user');
          }
  
          toast.add({ 
              severity: 'success', 
              summary: 'Success', 
              detail: 'User deleted successfully', 
              life: 3000 
          });
          
          await loadUsers();
      } catch (error) {
          console.error('Failed to delete user:', error);
          toast.add({ 
              severity: 'error', 
              summary: 'Error', 
              detail: error.message || 'Failed to delete user', 
              life: 3000 
          });
      }
  }
  
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
      user.value.country = event.value.name;
  }
  
  // Add ref for filtered managers
  const filteredManagers = ref([]);
  const enabledUsers = ref([]);
  
  // Add function to load enabled users
  async function loadEnabledUsers() {
      try {
          enabledUsers.value = allUsers.value.filter(user => 
              user.status === 'active'
          );
      } catch (error) {
          console.error('Failed to load enabled users:', error);
      }
  }
  
  // Add search function for managers
  function searchManagers(event) {
      const query = event.query.toLowerCase();
      filteredManagers.value = enabledUsers.value.filter(user => 
          user.name.toLowerCase().includes(query)
      );
  }
  
  // Add manager selection handler
  function onManagerSelect(event) {
      user.value.manager = event.value.name;
  }
  
  // Initialize on mount
  onMounted(async () => {
      await fetchSessionInfo();
      
      if (!sessionInfo.value?.companyId) {
          toast.add({
              severity: 'warn',
              summary: 'No Company Selected',
              detail: 'Please select a company first',
              life: 3000
          });
          router.push({ name: 'companies' });
          return;
      }
  
      try {
          await loadUsers();
          await loadCountries();
          await loadEnabledUsers();
      } catch (error) {
          console.error('Error initializing users page:', error);
          toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to load data', life: 3000 });
      }
  });
  
  // Add these constants
  const roles = [
    { label: 'Administrator', value: 'Administrator' },
    { label: 'Reviewer', value: 'Reviewer' },
    { label: 'SuperAdmin', value: 'SuperAdmin' }
  ];

  
  // Add the computed property for user status
  const userStatus = computed({
      get: () => user.value.status === 'active',
      set: (newValue) => {
          user.value.status = newValue ? 'active' : 'inactive'
      }
  });
  
  // Add this method for real-time validation
  const validateEmail = () => {
    // This will trigger the Message component to show/hide automatically
    // based on the isValidEmail check
  };
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