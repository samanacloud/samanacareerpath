<template>
    <div class="flex flex-col gap-8">
        <!-- Categories Section - Full Width -->
        <div class="col-12">
            <div class="card">
                <div class="font-semibold text-xl">Skillsets Categories</div>
                <div class="categories-container">
                    <div class="flex flex-wrap gap-2">
                        <div v-for="(category, index) in categories" 
                             :key="category"
                             class="category-tag flex-1 md:flex-none"
                             :class="{ 'selected': selectedCategory === category }"
                             @click="selectedCategory = category">
                            <Tag :value="category"
                                 :severity="getTagSeverity(index)"
                                 class="w-full cursor-pointer"
                            />
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Main Content Area -->
        <div class="col-12">
            <!-- Category Skillsets Card -->
            <div class="card">
                <div class="font-semibold text-xl">{{ selectedCategory || 'Select a Category' }}</div>
                <div class="grid">
                    <div v-for="skillset in filteredSkillsets" 
                         :key="skillset.id" 
                         class="col-12 md:col-6 lg:col-4 xl:col-3 mb-3">
                        <div class="surface-card p-3 border-round h-full">
                            <!-- View Mode -->
                            <div v-if="!editingSkillset || editingSkillset.id !== skillset.id">
                                <div class="flex align-items-center justify-content-between">
                                    <div class="flex-grow-1">
                                        <div class="text-lg font-medium mb-1">{{ skillset.name }}</div>
                                        <p class="text-600 m-0 line-height-3 text-sm">
                                            {{ skillset.description }}
                                        </p>
                                    </div>
                                    <div class="flex gap-2">
                                        <Button 
                                            icon="pi pi-pencil"
                                            class="p-button-rounded p-button-text"
                                            @click="startEdit(skillset)"
                                            tooltip="Edit"
                                        />
                                        <Button 
                                            icon="pi pi-trash"
                                            class="p-button-rounded p-button-text p-button-danger"
                                            @click="confirmDelete(skillset)"
                                            tooltip="Delete"
                                        />
                                    </div>
                                </div>
                            </div>

                            <!-- Edit Mode -->
                            <div v-else class="p-fluid">
                                <div class="field mb-3">
                                    <InputText 
                                        v-model="editingSkillset.name"
                                        placeholder="Skillset name"
                                        class="w-full"
                                    />
                                </div>
                                <div class="field mb-3">
                                    <Textarea 
                                        v-model="editingSkillset.description"
                                        placeholder="Skillset description"
                                        rows="3"
                                        class="w-full"
                                    />
                                </div>
                                <div class="flex justify-content-end gap-2">
                                    <Button 
                                        label="Cancel"
                                        icon="pi pi-times"
                                        class="p-button-text"
                                        @click="cancelEdit"
                                    />
                                    <Button 
                                        label="Save"
                                        icon="pi pi-check"
                                        @click="saveEdit"
                                    />
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Empty State for Category -->
                    <div v-if="selectedCategory && filteredSkillsets.length === 0" 
                         class="col-12">
                        <div class="surface-ground p-4 border-round text-center">
                            <i class="pi pi-folder-open text-xl text-600"></i>
                            <p class="text-600 mt-2 mb-0">
                                No skillsets in this category
                            </p>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Generator Card -->
            <div class="card mb-3">
                <div class="font-semibold text-xl">Generate Skillsets</div>
                <div class="mt-4">
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
            </div>
        </div>
    </div>

    <!-- Delete Confirmation Dialog -->
    <ConfirmDialog></ConfirmDialog>
</template>

<script setup>
import { ref, reactive, computed } from 'vue';
import { useToast } from 'primevue/usetoast';
import { useConfirm } from 'primevue/useconfirm';

const toast = useToast();
const confirm = useConfirm();
const loading = ref(false);
const results = ref([]);
const selectedCategory = ref(null);
const editingSkillset = ref(null);

// Mock data - replace with actual API calls
const categories = ref(['Frontend', 'Backend', 'DevOps', 'Database', 'Mobile']);
const skillsets = ref([
    { id: '1', category: 'Frontend', name: 'React', description: 'React development skills' },
    { id: '2', category: 'Frontend', name: 'Vue', description: 'Vue.js development skills' },
    { id: '3', category: 'Backend', name: 'Node.js', description: 'Node.js development skills' },
    // Add more mock data as needed
]);

const form = reactive({
    topic: ''
});

const filteredSkillsets = computed(() => {
    if (!selectedCategory.value) return [];
    return skillsets.value.filter(s => s.category === selectedCategory.value);
});

const addItem = (item) => {
            toast.add({
                severity: 'success',
                summary: 'Added',
                detail: `${item.name} added to skillsets`,
                life: 3000
            });
};

const startEdit = (skillset) => {
    editingSkillset.value = { ...skillset };
};

const cancelEdit = () => {
    editingSkillset.value = null;
};

const saveEdit = async () => {
    try {
        // TODO: Implement API call to update skillset
        const index = skillsets.value.findIndex(s => s.id === editingSkillset.value.id);
        if (index !== -1) {
            skillsets.value[index] = { ...editingSkillset.value };
                        }
            toast.add({
                severity: 'success',
                summary: 'Success',
                detail: 'Skillset updated successfully',
                life: 3000
            });
        editingSkillset.value = null;
    } catch (error) {
        toast.add({
            severity: 'error',
            summary: 'Error',
            detail: 'Failed to update skillset',
            life: 3000
        });
    }
};

const confirmDelete = (skillset) => {
    confirm.require({
        message: `Are you sure you want to delete "${skillset.name}"?`,
        header: 'Confirm Deletion',
        icon: 'pi pi-exclamation-triangle',
        accept: () => deleteSkillset(skillset),
        reject: () => {
            toast.add({
                severity: 'info',
                summary: 'Cancelled',
                detail: 'Deletion cancelled',
                life: 3000
            });
        }
    });
};

const deleteSkillset = async (skillset) => {
    try {
        // TODO: Implement API call to delete skillset
        const index = skillsets.value.findIndex(s => s.id === skillset.id);
        if (index !== -1) {
            skillsets.value.splice(index, 1);
        }
            toast.add({
                severity: 'success',
                summary: 'Deleted',
                detail: 'Skillset deleted successfully',
                life: 3000
            });
    } catch (error) {
        toast.add({
            severity: 'error',
            summary: 'Error',
            detail: 'Failed to delete skillset',
            life: 3000
        });
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
</style>