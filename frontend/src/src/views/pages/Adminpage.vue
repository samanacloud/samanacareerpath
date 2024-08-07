<script setup>
import { ref, onBeforeMount, computed } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import RadioButton from 'primevue/radiobutton';
import Toast from 'primevue/toast';
import { useToast } from 'primevue/usetoast'; // Add this line

//redirects to unauthorized if the user role is lower than the pagerole
import { getPageAuthorization } from '@/utils/utils';
const pageRole = 5; // Set the required role for this page
getPageAuthorization(pageRole);


// Function to get the base URL
const baseURL = import.meta.env.VITE_SITE_URL 
    ? `https://${import.meta.env.VITE_SITE_URL}` 
    : 'http://localhost:8080'; 

const usersList = ref([]);
const apiResponse = ref('');
const searchName = ref('');
const toast = useToast();
const addUserDialog = ref(false);
const editUserDialog = ref(false);
const userForm = ref({
  id: null,
  google_id: '',
  name: '',
  email: '',
  profile_image: '',
  admin: 0
});


const confirmDeleteDialog = ref(false);
const userIdToDelete = ref(null);

const showConfirmDeleteDialog = (id) => {
    userIdToDelete.value = id;
    confirmDeleteDialog.value = true;
};

const confirmDeleteUser = async () => {
    if (userIdToDelete.value !== null) {
        await deleteUser(userIdToDelete.value);
        confirmDeleteDialog.value = false;
        userIdToDelete.value = null;
    }
};
const roles = [
  'Registered User',
  'Employee',
  'Reviewer Read Only',
  'Reviewer Advanced',
  'Admin',
  'Super Admin'
];
const idFrozen = ref(false); // Add this line for dynamic toggling
const router = useRouter();

const filteredUsersList = computed(() => {
  if (!searchName.value) return usersList.value;
  const searchTerm = searchName.value.toLowerCase();
  return usersList.value.filter(user =>
    user.name.toLowerCase().includes(searchTerm)
  );
});

const listSystemUsers = async () => {
  try {
    const response = await axios.post(`${baseURL}/api/apitest.php`, {
      action: 'listSystemUsers'
    });
    usersList.value = response.data;
    apiResponse.value = 'Users listed successfully';
  } catch (error) {
    apiResponse.value = 'Error: ' + error.message;
  }
};

const showAddUserDialog = () => {
  userForm.value = {
    id: null,
    google_id: '',
    name: '',
    email: '',
    profile_image: '',
    admin: 0
  };
  addUserDialog.value = true;
};

const showEditUserDialog = (user) => {
  userForm.value = { ...user };
  editUserDialog.value = true;
};

const addUser = async () => {
  try {
    await axios.post(`${baseURL}/api/apitest.php`, {
      action: 'addSystemUser',
      google_id: userForm.value.google_id,
      name: userForm.value.name,
      email: userForm.value.email,
      profile_image: userForm.value.profile_image,
      admin: userForm.value.admin
    });
    apiResponse.value = 'User added successfully';
    toast.add({ severity:'success', summary: 'Success', detail:'User Updated Successfully', life: 3000 });

    addUserDialog.value = false;
    listSystemUsers();
  } catch (error) {
    apiResponse.value = 'Error: ' + error.message;
    toast.add({ severity:'error', summary: 'Error', detail:'There was an error', life: 3000 });

  }
};

const updateUser = async () => {
  try {
    await axios.post(`${baseURL}/api/apitest.php`, {
      action: 'updateSystemUser',
      id: userForm.value.id,
      google_id: userForm.value.google_id,
      name: userForm.value.name,
      email: userForm.value.email,
      profile_image: userForm.value.profile_image,
      admin: userForm.value.admin
    });
    apiResponse.value = 'User updated successfully';
    toast.add({ severity:'success', summary: 'Success', detail:'User Updated Successfully', life: 3000 });

    editUserDialog.value = false;
    listSystemUsers();
  } catch (error) {
    apiResponse.value = 'Error: ' + error.message;
    toast.add({ severity:'error', summary: 'Error', detail:'There was an error', life: 3000 });

  }
};

const deleteUser = async (id) => {
  try {
    await axios.post(`${baseURL}/api/apitest.php`, {
      action: 'deleteSystemUser',
      id: id
    });
    apiResponse.value = 'User deleted successfully';
    toast.add({ severity:'success', summary: 'Success', detail:'User Deleted Successfully', life: 3000 });

    listSystemUsers();
  } catch (error) {
    apiResponse.value = 'Error: ' + error.message;
    toast.add({ severity:'error', summary: 'Error', detail:'There was an error', life: 3000 });

  }
};

const roleText = (adminValue) => {
  return roles[adminValue] || 'Unknown';
};

onBeforeMount(() => {
  listSystemUsers();
});
</script>

<template>
  <div class="grid">
    <div class="col-12">
      <div class="card">
        <h5>User Management</h5>
        <div class="flex justify-content-between flex-column sm:flex-row">
          <h6>Search by Name</h6>
          <InputText type="text" v-model="searchName" placeholder="Search by name" class="p-inputtext-sm" />
          <Button label="Add User" icon="pi pi-plus" @click="showAddUserDialog"  />
        </div>
        <DataTable :value="filteredUsersList" paginator :rows="10" dataKey="id" rowHover :scrollable="true" scrollHeight="70vh" scrollDirection="vertical">
          <Column class="hide-on-mobile" field="profile_image" header="Profile Photo" bodyStyle="text-align: center" frozen alignFrozen="left">
            <template #body="{ data }">
              <i v-if="!data.profile_image || data.profile_image === '0'" class="pi pi-user profile-photo"></i>
              <img v-else :src="data.profile_image" alt="Profile Photo" class="profile-photo" />
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
          <Column class="hide-on-mobile" field="google_id" header="Google ID" sortable></Column>
          <Column field="admin" header="Role" sortable>
            <template #body="{ data }">{{ roleText(data.admin) }}</template>
          </Column>
          <Column class="hide-on-mobile" field="created_at"  header="Created At" sortable>
            <template #body="{ data }">{{ new Date(data.created_at).toLocaleDateString() }}</template>
          </Column>
          <Column header="Actions" bodyStyle="text-align: center" frozen alignFrozen="right">
            <template #body="{ data }">
              <Button icon="pi pi-pencil" text raised severity="warning" @click="showEditUserDialog(data)" />
              <Button icon="pi pi-trash" text raised severity="danger" @click="showConfirmDeleteDialog(data.id)" />
            </template>
          </Column>
        </DataTable>
      </div>
    </div>
  </div>

  <Dialog header="Add User" v-model:visible="addUserDialog" :modal="true" :closable="false">
    <form @submit.prevent="addUser">
      <div class="field">
        <label for="google_id">Google ID</label>
        <InputText id="google_id" v-model="userForm.google_id" required />
      </div>
      <div class="field">
        <label for="name">Name</label>
        <InputText id="name" v-model="userForm.name" required />
      </div>
      <div class="field">
        <label for="email">Email</label>
        <InputText id="email" v-model="userForm.email" required />
      </div>
      <div class="field">
        <label for="profile_image">Profile Image</label>
        <InputText id="profile_image" v-model="userForm.profile_image" />
      </div>
      <div class="field">
        <label>Role</label>
        <div v-for="(role, index) in roles" :key="index">
          <RadioButton v-model="userForm.admin" :value="index" />
          <label :for="`role-${index}`">{{ role }}</label> 
        </div>
      </div>
      <Button type="submit" label="Add" text raised severity="success" />
      <Button type="button" label="Cancel" text raised severity="danger" @click="addUserDialog = false" />
    </form>
  </Dialog>

  <Dialog header="Edit User" v-model:visible="editUserDialog" :modal="true" :closable="false">
    <form @submit.prevent="updateUser">
      <div class="field">
        <label for="google_id">Google ID</label>
        <InputText id="google_id" v-model="userForm.google_id" required :disabled="userForm.id !== null" />
      </div>
      <div class="field">
        <label for="name">Name</label>
        <InputText id="name" v-model="userForm.name" required />
      </div>
      <div class="field">
        <label for="email">Email</label>
        <InputText id="email" v-model="userForm.email" required :disabled="userForm.id !== null" />
      </div>
      <div class="field">
        <label for="profile_image">Profile Image</label>
        <InputText id="profile_image" v-model="userForm.profile_image" />
      </div>
      <div class="field">
        <label>Role</label>
        <div v-for="(role, index) in roles" :key="index">
          <RadioButton v-model="userForm.admin" :value="index" />
          <label :for="`role-${index}`">{{ role }}</label> 
        </div>
      </div>
      <Button type="submit" label="Update" text raised severity="success" />
      <Button type="button" label="Cancel" text raised severity="danger" @click="editUserDialog = false" />
    </form>
  </Dialog>
  <Dialog header="Confirm Deletion" v-model:visible="confirmDeleteDialog" :modal="true" :closable="false">
    <p>Are you sure you want to delete this user?</p>
    <div class="p-d-flex p-ai-center p-jc-between p-mt-4">
        <Button label="Cancel" icon="pi pi-times" @click="confirmDeleteDialog = false" class="p-button-text" />
        <Button label="Delete" icon="pi pi-check" @click="confirmDeleteUser" class="p-button-danger" />
    </div>
</Dialog>
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

@media (max-width: 768px) { 
    .email {
        font-size: 0.8rem;  
    }

    .hide-on-mobile {
        display: none;
    }
}
</style>