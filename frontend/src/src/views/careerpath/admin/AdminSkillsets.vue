<template>
    <div class="card">
        <Toast />
        <ConfirmDialog />
        
        <!-- Breadcrumb Navigation -->
        <div class="compact-breadcrumb mb-3">
            <Breadcrumb :home="breadcrumbHome" :model="breadcrumbItems" />
        </div>

        <div class="flex items-center justify-between mb-4">
            <div>
                <h1 class="text-2xl font-medium text-900">Skillset Management</h1>
                <p class="text-sm font-medium text-500">Manage company skillsets and categories</p>
            </div>
            <Button 
                label="Add Skillset" 
                icon="pi pi-plus" 
                outlined raised 
                @click="openNewDialog" 
            />
        </div>

        <!-- Main Content -->
        <div class="grid">
            <!-- Categories Section -->
            <div class="col-12 md:col-3">
                <div class="card p-4">
                    <h3 class="text-lg font-semibold mb-4">Categories</h3>
                    <div class="flex flex-wrap gap-2">
                        <Chip 
                            v-for="category in categories" 
                            :key="category"
                            :label="category"
                            :class="{ 
                                'bg-primary-500 text-white shadow-lg': selectedCategory === category,
                                'hover:bg-primary-500 hover:text-white hover:shadow-lg transition-all duration-200': true
                            }"
                            @click="selectedCategory = category"
                            class="cursor-pointer border-1 border-transparent bg-surface-100 shadow-md"
                        />
                    </div>
                </div>
            </div>

            <!-- Skillsets List -->
            <div class="col-12 md:col-9">
                <div class="card p-4">
                    <div class="mb-4">
                        <h2 class="text-xl font-semibold">
                            Skillsets in 
                            <span class="text-primary-500">{{ selectedCategory || 'All Categories' }}</span>
                        </h2>
                    </div>
                    
                    <DataTable
                        :value="filteredSkillsets"
                        dataKey="id"
                        :loading="loading"
                        :paginator="true"
                        :rows="10"
                        :rowsPerPageOptions="[5, 10, 20, 50]"
                        responsiveLayout="scroll"
                        class="p-4 skillset-table"
                    >
                        <Column field="name" header="Name" sortable>
                            <template #body="{ data }">
                                <div class="flex flex-col">
                                    <span class="font-medium">{{ data.name }}</span>
                                    <span class="text-sm text-500">{{ data.description }}</span>
                                </div>
                            </template>
                        </Column>

                        <Column :exportable="false" style="width:120px">
                            <template #body="{ data }">
                                <div class="flex gap-2">
                                    <Button 
                                        icon="pi pi-pencil" 
                                        class="p-button-text p-button-rounded text-gray-500 hover:text-primary-500" 
                                        @click="startEdit(data)"
                                    />
                                    <Button 
                                        icon="pi pi-trash" 
                                        class="p-button-text p-button-rounded p-button-danger hover:text-red-600" 
                                        @click="confirmDelete(data)"
                                    />
                                </div>
                            </template>
                        </Column>
                    </DataTable>
                </div>
            </div>
        </div>

        <!-- Skillset Dialog -->
        <Dialog
            v-model:visible="dialogVisible"
            :style="{ width: '450px' }"
            header="Skillset Details"
            :modal="true"
        >
            <div class="p-fluid">
                <Fieldset legend="Skillset Information">
                    <div class="field grid">
                        <div class="col-12">
                            <FloatLabel variant="on">
                                <InputText
                                    id="name"
                                    v-model="currentItem.name"
                                    required
                                    autofocus
                                    class="w-full"
                                />
                                <label for="name">Name</label>
                            </FloatLabel>
                        </div>
                        
                        <div class="col-12 mt-3">
                            <FloatLabel variant="on">
                                <Textarea
                                    id="description"
                                    v-model="currentItem.description"
                                    rows="3"
                                    class="w-full"
                                />
                                <label for="description">Description</label>
                            </FloatLabel>
                        </div>

                        <div class="col-12 mt-3">
                            <FloatLabel variant="on">
                                <InputText
                                    id="category"
                                    v-model="currentItem.category"
                                    class="w-full"
                                />
                                <label for="category">Category</label>
                            </FloatLabel>
                        </div>
                    </div>
                </Fieldset>
            </div>
            <template #footer>
                <Button
                    label="Cancel"
                    icon="pi pi-times"
                    class="p-button-text"
                    @click="hideDialog"
                />
                <Button
                    label="Save"
                    icon="pi pi-check"
                    @click="saveItem"
                />
            </template>
        </Dialog>

        <!-- Generator Section (Keep existing implementation) -->
        <div class="card mt-4">
            <!-- Generator Form -->
            <div class="surface-section p-3 flex   gap-2 border-round mb-3">
                <div class="p-inputgroup w-full md:w-80">
                    <InputText 
                        v-model="form.topic" 
                        placeholder="Enter skillset topic..."
                        class="w-full"
                        @keyup.enter="generate"
                    />
                </div>
                <Button 
                        raised
                        icon="pi pi-bolt"
                        @click="generate"
                        :loading="loading"
                        :disabled="!form.topic"
                        class="p-button-primary rounded"
                    />
            </div>

            <!-- Loading State -->
            <div v-if="loading" class="grid">
                <div v-for="n in 2" :key="n" class="col-12 md:col-6">
                    <div class="surface-card p-3 border-round mb-2">
                        <Skeleton height="2rem" class="mb-2"></Skeleton>
                        <Skeleton height="3rem"></Skeleton>
                    </div>
                </div>
            </div>

            <!-- Results -->
            <div v-if="results.length > 0 && !loading" class="grid">
                <div v-for="(item, index) in results" 
                     :key="index" 
                     class="col-12 md:col-6">
                    <div class="surface-card p-3 border-round mb-2 hover:surface-hover transition-colors transition-duration-150">
                        <div class="flex align-items-center justify-content-between">
                            <div class="flex-grow-1">
                                <div class="text-lg font-medium mb-1">{{ item.name }}</div>
                                <p class="text-600 m-0 line-height-3 text-sm">
                                    {{ item.description }}
                                </p>
                            </div>
                            <Button 
                                icon="pi pi-plus"
                                class="p-button-rounded p-button-text"
                                @click="addItem(item)"
                                tooltip="Add to list"
                            />
                        </div>
                        <div class="mt-2">
                            <Tag :value="form.topic" severity="info" class="text-xs"></Tag>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Empty State -->
            <div v-if="!loading && results.length === 0" 
                 class="surface-ground p-4 border-round text-center">
                <i class="pi pi-search text-xl text-600"></i>
                <p class="text-600 mt-2 mb-0">
                    Enter a topic to generate skillsets
                </p>
            </div>
        </div>

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
                    To confirm deletion, type the skillset name:
                    <span class="font-semibold">{{ skillsetToDelete?.name }}</span>
                </div>
                
                <div class="flex flex-col gap-2">
                    <InputText
                        v-model="confirmationText"
                        :class="{'p-invalid': deleteSubmitted && confirmationText !== skillsetToDelete?.name}"
                        placeholder="Enter skillset name"
                    />
                    <small class="p-error" v-if="deleteSubmitted && confirmationText !== skillsetToDelete?.name">
                        Skillset name doesn't match
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
                        @click="deleteSkillset"
                    />
                </div>
            </template>
        </Dialog>
    </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue';
import { useToast } from 'primevue/usetoast';
import { useConfirm } from 'primevue/useconfirm';

const toast = useToast();
const confirm = useConfirm();

// GraphQL Operations
const SKILLSETS_QUERY = `
    query ListSkillsetsByCompanyId($companyId: String!) {
        listSkillsetsByCompanyId(companyId: $companyId) {
            id
            skillsetName
            skillsetDescription
            skillsetCategory
        }
    }
`;

const CATEGORIES_QUERY = `
    query ListSkillsetsCategories($companyId: String!) {
        listSkillsetsCategories(companyId: $companyId)
    }
`;

const CREATE_MUTATION = `
    mutation CreateSkillset($input: CreateSkillsetInput!) {
        createSkillset(input: $input) {
            id
            skillsetName
            skillsetDescription
            skillsetCategory
        }
    }
`;

const UPDATE_MUTATION = `
    mutation ModifySkillset($id: String!, $input: UpdateSkillsetInput!) {
        modifySkillset(id: $id, input: $input) {
            id
            skillsetName
            skillsetDescription
            skillsetCategory
        }
    }
`;

const DELETE_MUTATION = `
    mutation RemoveSkillset($id: String!) {
        removeSkillset(id: $id)
    }
`;

// Component state
const loading = ref(false);
const skillsets = ref([]);
const categories = ref([]);
const selectedCategory = ref(null);
const dialogVisible = ref(false);
const currentItem = ref(emptyItem());

function emptyItem() {
    return {
        id: null,
        name: '',
        description: '',
        category: ''
    };
}

// Add session info ref
const sessionInfo = ref(null);

// Add fetchSessionInfo function from CandidatesProfiles.vue
async function fetchSessionInfo() {
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
  }
}

// Update loadData function to use sessionInfo
async function loadData() {
  if (!sessionInfo.value?.companyId) {
    toast.add({ 
      severity: 'warn', 
      summary: 'No Company Selected', 
      detail: 'Please select a company first', 
      life: 3000 
    });
    return;
  }

  try {
    loading.value = true;
    
    // Update queries to use sessionInfo companyId
    const categoriesResponse = await fetch('/graphql', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query: CATEGORIES_QUERY,
        variables: { companyId: sessionInfo.value.companyId }
      })
    });
    
    const categoriesData = await categoriesResponse.json();
    categories.value = categoriesData.data.listSkillsetsCategories;

    // Fetch skillsets
    const skillsetsResponse = await fetch('/graphql', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query: SKILLSETS_QUERY,
        variables: { companyId: sessionInfo.value.companyId }
      })
    });
    
    const skillsetsData = await skillsetsResponse.json();
    skillsets.value = skillsetsData.data.listSkillsetsByCompanyId.map(item => ({
      id: item.id,
      name: item.skillsetName,
      description: item.skillsetDescription,
      category: item.skillsetCategory
    }));

  } catch (error) {
    toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to load data', life: 3000 });
  } finally {
    loading.value = false;
  }
}

const filteredSkillsets = computed(() => {
    if (!selectedCategory.value) return [];
    return skillsets.value.filter(s => s.category === selectedCategory.value);
});

async function saveItem() {
    try {
        const mutation = currentItem.value.id ? UPDATE_MUTATION : CREATE_MUTATION;
        const variables = currentItem.value.id ? 
            {
                id: currentItem.value.id,
                input: {
                    skillsetName: currentItem.value.name,
                    skillsetDescription: currentItem.value.description,
                    skillsetCategory: currentItem.value.category
                }
            } : 
            {
                input: {
                    companyId: sessionInfo.value.companyId,
                    skillsetName: currentItem.value.name,
                    skillsetDescription: currentItem.value.description,
                    skillsetCategory: currentItem.value.category
                }
            };

        const response = await fetch('/graphql', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: mutation, variables })
        });

        const result = await response.json();
        
        if (result.errors) {
            throw new Error(result.errors[0].message);
        }

        // Update local state
        if (currentItem.value.id) {
            const index = skillsets.value.findIndex(s => s.id === currentItem.value.id);
            if (index !== -1) {
                skillsets.value[index] = {
                    ...currentItem.value,
                    ...result.data.modifySkillset
                };
            }
        } else {
            skillsets.value.push({
                id: result.data.createSkillset.id,
                name: result.data.createSkillset.skillsetName,
                description: result.data.createSkillset.skillsetDescription,
                category: result.data.createSkillset.skillsetCategory
            });
        }

        toast.add({
            severity: 'success',
            summary: 'Success',
            detail: currentItem.value.id ? 'Skillset updated' : 'Skillset created',
            life: 3000
        });
        
        dialogVisible.value = false;
        await loadCategories();
    } catch (error) {
        toast.add({
            severity: 'error',
            summary: 'Error',
            detail: error.message || 'Operation failed',
            life: 3000
        });
    }
}

// Add remaining CRUD functions and dialog handling similar to RecruitmentLeads
// Implement openNewDialog, editItem, confirmDelete functions

onMounted(async () => {
  await fetchSessionInfo();
  if (sessionInfo.value?.companyId) {
    await loadData();
  }
});

const form = reactive({
    topic: ''
});

const results = ref([]);

// Add this function to handle category refresh
async function loadCategories() {
    try {
        const response = await fetch('/graphql', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                query: CATEGORIES_QUERY,
                variables: { companyId: sessionInfo.value.companyId }
            })
        });
        const data = await response.json();
        categories.value = data.data.listSkillsetsCategories;
    } catch (error) {
        toast.add({ 
            severity: 'error', 
            summary: 'Error', 
            detail: 'Failed to refresh categories', 
            life: 3000 
        });
    }
}

// Update the addItem function to refresh categories
const addItem = async (item) => {
    try {
        // Check if skillset already exists
        const alreadyExists = skillsets.value.some(s => 
            s.name === item.name &&
            s.description === item.description &&
            s.category === form.topic
        );

        if (alreadyExists) {
            toast.add({
                severity: 'warn',
                summary: 'Already Added',
                detail: `${item.name} is already in your skillsets`,
                life: 3000
            });
            return;
        }

        const response = await fetch('/graphql', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                query: CREATE_MUTATION,
                variables: {
                    input: {
                        companyId: sessionInfo.value.companyId,
                        skillsetName: item.name,
                        skillsetDescription: item.description,
                        skillsetCategory: form.topic
                    }
                }
            })
        });

        const result = await response.json();
        
        if (result.errors) {
            throw new Error(result.errors[0].message);
        }

        skillsets.value.push({
            id: result.data.createSkillset.id,
            name: result.data.createSkillset.skillsetName,
            description: result.data.createSkillset.skillsetDescription,
            category: result.data.createSkillset.skillsetCategory
        });

        toast.add({
            severity: 'success',
            summary: 'Added',
            detail: `${item.name} added to skillsets`,
            life: 3000
        });

        // Remove added item from results
        results.value = results.value.filter(r => 
            !(r.name === item.name && r.description === item.description)
        );

        // Refresh categories after successful addition
        await loadCategories();

    } catch (error) {
        toast.add({
            severity: 'error',
            summary: 'Error',
            detail: error.message || 'Failed to add skillset',
            life: 3000
        });
    }
};

const startEdit = (skillset) => {
    currentItem.value = { 
        id: skillset.id,
        name: skillset.name,
        description: skillset.description,
        category: skillset.category
    };
    dialogVisible.value = true;
};

const hideDialog = () => {
    currentItem.value = emptyItem();
};

// Add these state variables
const deleteDialog = ref(false);
const skillsetToDelete = ref(null);
const confirmationText = ref('');
const deleteSubmitted = ref(false);

// Update confirmDelete function
const confirmDelete = (skillset) => {
    skillsetToDelete.value = skillset;
    confirmationText.value = '';
    deleteSubmitted.value = false;
    deleteDialog.value = true;
};

// Update deleteSkillset function
const deleteSkillset = async () => {
    deleteSubmitted.value = true;
    
    if (confirmationText.value !== skillsetToDelete.value.name) {
        return;
    }
    
    try {
        const response = await fetch('/graphql', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                query: DELETE_MUTATION,
                variables: { id: skillsetToDelete.value.id }
            })
        });

        const result = await response.json();
        
        if (result.errors) {
            throw new Error(result.errors[0].message);
        }

        if (result.data?.removeSkillset) {
            // Remove from local state
            const index = skillsets.value.findIndex(s => s.id === skillsetToDelete.value.id);
            if (index !== -1) {
                skillsets.value.splice(index, 1);
            }
            
            toast.add({
                severity: 'success',
                summary: 'Deleted',
                detail: 'Skillset deleted successfully',
                life: 3000
            });
            
            await loadCategories();
        } else {
            throw new Error('Failed to delete skillset');
        }
    } catch (error) {
        toast.add({
            severity: 'error',
            summary: 'Error',
            detail: error.message || 'Failed to delete skillset',
            life: 3000
        });
    } finally {
        deleteDialog.value = false;
        skillsetToDelete.value = null;
        confirmationText.value = '';
    }
};

const generate = async () => {
    if (!form.topic) {
        toast.add({ severity: 'warn', summary: 'Warning', detail: 'Please enter a topic', life: 3000 });
        return;
    }

    loading.value = true;
    try {
        const query = {
            query: `
                query GenerateSkillsetTopic($topic: String!) {
                    generateSkillsetTopic(topic: $topic) {
                        status
                        error
                        skillsets {
                            name
                            description
                        }
                    }
                }
            `,
            variables: {
                topic: form.topic
            }
        };

        const response = await fetch('/graphql', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(query)
        });

        const result = await response.json();

        if (result.errors) {
            throw new Error(result.errors[0].message);
        }

        const data = result.data.generateSkillsetTopic;
        
        if (data.status === 'error') {
            throw new Error(data.error);
        }

        results.value = data.skillsets;

        toast.add({ 
            severity: 'success', 
            summary: 'Success', 
            detail: 'Skillsets generated successfully', 
            life: 3000 
        });

    } catch (error) {
        toast.add({ 
            severity: 'error', 
            summary: 'Error', 
            detail: error.message || 'Failed to generate results', 
            life: 3000 
        });
    } finally {
        loading.value = false;
    }
};

// Add this function for tag severities
const getTagSeverity = (index) => {
    const severities = ['info', 'success', 'warning', 'danger', 'primary'];
    return severities[index % severities.length];
};

// Add breadcrumb configuration at the top of the script section
const breadcrumbHome = ref({ 
    icon: 'pi pi-home', 
    to: '/' 
});

const breadcrumbItems = ref([
    { label: 'Career Path', to: '/careerpath' },
    { label: 'Skillsets', disabled: true }
]);

// Add openNewDialog function
const openNewDialog = () => {
    currentItem.value = emptyItem();
    dialogVisible.value = true;
};

// Wait for the DOM to update after showing the form
setTimeout(() => {
  if (skillsetAssessmentCard.value) {
    skillsetAssessmentCard.value.scrollIntoView({ 
      behavior: 'smooth', 
      block: 'start'
    });
  }
}, 100);
</script>

<style scoped>
.surface-card {
    background: var(--surface-card);
    border: 1px solid var(--surface-border);
}

.hover\:surface-hover:hover {
    background: var(--surface-hover);
}

:deep(.p-inputgroup) {
    border-radius: var(--border-radius);
    overflow: hidden;
}

/* Categories container styles */
.categories-container {
    max-height: 60vh;
    overflow-y: auto;
    scrollbar-width: thin;
    padding-right: 0.5rem;
}

.categories-container::-webkit-scrollbar {
    width: 6px;
}

.categories-container::-webkit-scrollbar-track {
    background: var(--surface-ground);
    border-radius: 3px;
}

.categories-container::-webkit-scrollbar-thumb {
    background: var(--surface-border);
    border-radius: 3px;
}

.categories-container::-webkit-scrollbar-thumb:hover {
    background: var(--surface-400);
}

.category-tag {
    transition: transform 0.2s;
}

.category-tag:hover {
    transform: translateX(5px);
}

.category-tag.selected :deep(.p-tag) {
    transform: scale(1.02);
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

:deep(.p-tag) {
    width: 100%;
    justify-content: flex-start;
    cursor: pointer;
    transition: all 0.2s;
}

:deep(.p-tag:hover) {
    opacity: 0.9;
}

/* Mobile responsiveness */
@media screen and (max-width: 768px) {
    .flex-col {
        width: 100%;
    }

    .categories-container {
        max-height: none;
        padding: 0.5rem;
    }

    .category-tag {
        margin-bottom: 0.5rem;
        width: calc(50% - 0.5rem);
    }

    :deep(.p-tag) {
        padding: 0.5rem;
        justify-content: center;
    }
}

/* Update hover effect to use surface color */
:deep(.skillset-table .p-datatable-tbody > tr:hover) {
  background-color: var(--surface-hover) !important; /* Changed from primary-50 to surface-hover */
}

/* Optional: Add subtle border transition */
:deep(.skillset-table .p-datatable-tbody > tr) {
  transition: 
    background-color 0.2s ease,
    box-shadow 0.2s ease;
  border-bottom: 1px solid var(--surface-border);
}

:deep(.skillset-table .p-datatable-tbody > tr:hover) {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

/* Add subtle transition to action buttons */
:deep(.skillset-table .p-button) {
  transition: 
    color 0.2s ease,
    opacity 0.2s ease;
}

:deep(.skillset-table .p-button:hover) {
  opacity: 0.8;
}

/* Add matching table styles */
:deep(.p-datatable) {
  border: 1px solid var(--surface-border);
  border-radius: 6px;
}

:deep(.p-datatable .p-datatable-thead > tr > th) {
  background: var(--surface-card);
  border-color: var(--surface-border);
  color: var(--text-color-secondary);
}

:deep(.p-datatable .p-paginator) {
  border: none;
  border-top: 1px solid var(--surface-border);
}
</style>