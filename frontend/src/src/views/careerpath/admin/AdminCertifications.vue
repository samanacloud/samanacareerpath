<template>
    <div class="card">
        <Toast />
        <ConfirmPopup />
        
        <!-- Breadcrumb Navigation -->
        <div class="compact-breadcrumb mb-3">
            <Breadcrumb :home="breadcrumbHome" :model="breadcrumbItems" />
        </div>

        <div class="flex items-center justify-between mb-4">
            <div>
                <h1 class="text-2xl font-medium text-900">Certification Management</h1>
                <p class="text-sm font-medium text-500">Manage company certifications and vendors</p>
            </div>
            <Button 
                label="Add Certification" 
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
                    <h3 class="text-lg font-semibold mb-4">Certification Vendors</h3>
                    <div class="flex flex-wrap gap-2">
                        <Chip 
                            v-for="(category, index) in categories" 
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

            <!-- Certifications List -->
            <div class="col-12 md:col-9">
                <div class="card p-4">
                    <div class="mb-4">
                        <h2 class="text-xl font-semibold">
                            Certifications in 
                            <span class="text-primary-500">{{ selectedCategory || 'All Categories' }}</span>
                        </h2>
                    </div>
                    
                    <div class="grid">
                        <div v-for="certification in filteredCertifications" 
                             :key="certification.id" 
                             class="col-12 md:col-6 lg:col-4 xl:col-3 mb-3">
                            <div class="surface-card p-3 border-round h-full">
                                <div class="flex align-items-center justify-content-between">
                                    <div class="flex-grow-1">
                                        <div class="text-lg font-medium mb-1">{{ certification.certificationName }}</div>
                                        <p class="text-600 m-0 line-height-3 text-sm">
                                            {{ certification.certificationShortName }}
                                        </p>
                                    </div>
                                    <div class="flex gap-2">
                                        <Button 
                                            icon="pi pi-pencil"
                                            class="p-button-rounded p-button-text"
                                            @click="startEdit(certification)"
                                            tooltip="Edit"
                                        />
                                        <Button 
                                            icon="pi pi-trash"
                                            class="p-button-rounded p-button-text p-button-danger"
                                            @click="confirmDelete(certification)"
                                            tooltip="Delete"
                                        />
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Empty State for Category -->
                        <div v-if="selectedCategory && filteredCertifications.length === 0" 
                             class="col-12">
                            <div class="surface-ground p-4 border-round text-center">
                                <i class="pi pi-folder-open text-xl text-600"></i>
                                <p class="text-600 mt-2 mb-0">
                                    No certifications in this category
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Generator Card -->
        <div class="card mt-4">
            <div class="font-semibold text-xl mb-4">Generate Certifications</div>
            <!-- Generator Form -->
            <div class="surface-section p-3 flex gap-2 border-round mb-3">
                <div class="p-inputgroup w-full md:w-80">
                    <InputText 
                        v-model="form.vendor" 
                        placeholder="Enter Certification Vendor (e.g., AWS, Microsoft, Cisco)..."
                        class="w-full"
                        @keyup.enter="generate"
                    />
                </div>
                <Button 
                    raised
                    icon="pi pi-bolt"
                    @click="generate"
                    :loading="loading"
                    :disabled="!form.vendor"
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
                                <div class="text-lg font-medium mb-1">{{ item.certificationName }}</div>
                                <p class="text-600 m-0 line-height-3 text-sm">
                                    {{ item.certificationShortName }}
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
                            <Tag :value="form.vendor" severity="info" class="text-xs"></Tag>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Empty State -->
            <div v-if="!loading && results.length === 0" 
                 class="surface-ground p-4 border-round text-center">
                <i class="pi pi-search text-xl text-600"></i>
                <p class="text-600 mt-2 mb-0">
                    Enter a vendor to generate certifications
                </p>
            </div>
        </div>

        <!-- Certification Dialog -->
        <Dialog
            v-model:visible="dialogVisible"
            :style="{ width: '450px' }"
            header="Certification Details"
            :modal="true"
        >
            <div class="p-fluid">
                <Fieldset legend="Certification Information">
                    <div class="field grid">
                        <div class="col-12">
                            <FloatLabel variant="on">
                                <InputText
                                    id="name"
                                    v-model="editingCertification.certificationName"
                                    required
                                    autofocus
                                    class="w-full"
                                />
                                <label for="name">Name</label>
                            </FloatLabel>
                        </div>
                        
                        <div class="col-12 mt-3">
                            <FloatLabel variant="on">
                                <InputText
                                    id="shortName"
                                    v-model="editingCertification.certificationShortName"
                                    class="w-full"
                                />
                                <label for="shortName">Short Name</label>
                            </FloatLabel>
                        </div>

                        <div class="col-12 mt-3">
                            <FloatLabel variant="on">
                                <InputText
                                    id="vendor"
                                    v-model="editingCertification.certificationVendor"
                                    required
                                    class="w-full"
                                />
                                <label for="vendor">Vendor</label>
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
                    @click="cancelEdit"
                />
                <Button
                    label="Save"
                    icon="pi pi-check"
                    @click="saveEdit"
                />
            </template>
        </Dialog>
    </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue';
import { useToast } from 'primevue/usetoast';
import { useConfirm } from 'primevue/useconfirm';
import Dialog from 'primevue/dialog';
import Fieldset from 'primevue/fieldset';
import FloatLabel from 'primevue/floatlabel';
import Skeleton from 'primevue/skeleton';

const toast = useToast();
const confirm = useConfirm();
const loading = ref(false);
const results = ref([]);
const selectedCategory = ref(null);
const editingCertification = ref(null);
const sessionInfo = ref(null);
const certifications = ref([]);
const categories = ref([]); // Will be populated with vendors
const dialogVisible = ref(false);

const form = reactive({
    vendor: ''
});

// Add breadcrumb configuration
const breadcrumbHome = ref({ 
    icon: 'pi pi-home', 
    to: '/' 
});

const breadcrumbItems = ref([
    { label: 'Career Path', to: '/careerpath' },
    { label: 'Certifications', disabled: true }
]);

// Function to open the dialog for a new certification
const openNewDialog = () => {
    editingCertification.value = {
        id: null,
        certificationName: '',
        certificationShortName: '',
        certificationVendor: selectedCategory.value || ''
    };
    dialogVisible.value = true;
};

// Add function to fetch vendors
const fetchVendors = async () => {
    if (!sessionInfo.value?.companyId) return;
    
    try {
        const query = {
            query: `
                query GetCertificationVendors($companyId: String!) {
                    getCertificationVendors(companyId: $companyId)
                }
            `,
            variables: {
                companyId: sessionInfo.value.companyId
            }
        };

        const response = await fetch('/graphql', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(query)
        });

        const result = await response.json();
        if (result.errors) {
            throw new Error(result.errors[0].message);
        }

        categories.value = result.data.getCertificationVendors;
    } catch (error) {
        console.error('Error fetching vendors:', error);
        toast.add({
            severity: 'error',
            summary: 'Error',
            detail: 'Failed to load certification vendors',
            life: 3000
        });
    }
};

// Add fetchCertifications function
const fetchCertifications = async () => {
    if (!sessionInfo.value?.companyId) return;
    
    try {
        const query = {
            query: `
                query GetAllCertifications($companyId: String!) {
                    getAllCertifications(companyId: $companyId) {
                        id
                        companyId
                        certificationVendor
                        certificationName
                        certificationShortName
                    }
                }
            `,
            variables: {
                companyId: sessionInfo.value.companyId
            }
        };

        const response = await fetch('/graphql', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(query)
        });

        const result = await response.json();
        if (result.errors) {
            throw new Error(result.errors[0].message);
        }

        certifications.value = result.data.getAllCertifications;
    } catch (error) {
        console.error('Error fetching certifications:', error);
        toast.add({
            severity: 'error',
            summary: 'Error',
            detail: 'Failed to load certifications',
            life: 3000
        });
    }
};

// Update session handling to fetch vendors
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
            // After getting session, load data
            await Promise.all([
                fetchCertifications(),
                fetchVendors()
            ]);
        }
    } catch (error) {
        console.error('Error fetching session info:', error);
        toast.add({
            severity: 'error',
            summary: 'Error',
            detail: 'Failed to load session information',
            life: 3000
        });
    }
};

// Update filtered certifications to use vendor directly
const filteredCertifications = computed(() => {
    if (!selectedCategory.value) return [];
    return certifications.value.filter(c => c.certificationVendor === selectedCategory.value);
});

// Update addItem to use selected vendor
const addItem = async (item) => {
    if (!sessionInfo.value?.companyId) return;

    try {
        const mutation = {
            query: `
                mutation CreateCertification($data: CertificationInput!) {
                    createCertification(data: $data) {
                        status
                        error
                        certification {
                            id
                            certificationVendor
                            certificationName
                            certificationShortName
                        }
                    }
                }
            `,
            variables: {
                data: {
                    companyId: sessionInfo.value.companyId,
                    certificationVendor: selectedCategory.value || form.vendor,
                    certificationName: item.certificationName,
                    certificationShortName: item.certificationShortName
                }
            }
        };

        const response = await fetch('/graphql', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(mutation)
        });

        const result = await response.json();
        if (result.errors) {
            throw new Error(result.errors[0].message);
        }

        const data = result.data.createCertification;
        if (data.status === 'success') {
            await fetchCertifications(); // Refresh the list
            toast.add({
                severity: 'success',
                summary: 'Added',
                detail: `${item.certificationName} added to certifications`,
                life: 3000
            });
        } else {
            throw new Error(data.error);
        }
    } catch (error) {
        toast.add({
            severity: 'error',
            summary: 'Error',
            detail: error.message || 'Failed to add certification',
            life: 3000
        });
    }
};

const startEdit = (certification) => {
    // When adding a new certification, initialize with proper structure
    if (!certification.id) {
        editingCertification.value = {
            id: null,
            certificationName: '',
            certificationShortName: '',
            certificationVendor: selectedCategory.value || ''
        };
    } else {
        editingCertification.value = { ...certification };
    }
    dialogVisible.value = true;
};

const cancelEdit = () => {
    editingCertification.value = null;
    dialogVisible.value = false;
};

const saveEdit = async () => {
    if (!sessionInfo.value?.companyId) return;
    
    // Validate required fields
    if (!editingCertification.value.certificationName) {
        toast.add({
            severity: 'error',
            summary: 'Validation Error',
            detail: 'Certification name is required',
            life: 3000
        });
        return;
    }
    
    if (!editingCertification.value.certificationVendor && selectedCategory.value) {
        editingCertification.value.certificationVendor = selectedCategory.value;
    }
    
    if (!editingCertification.value.certificationVendor) {
        toast.add({
            severity: 'error',
            summary: 'Validation Error',
            detail: 'Certification vendor is required',
            life: 3000
        });
        return;
    }

    try {
        let mutation, variables;
        const isNewCertification = !editingCertification.value.id;
        
        if (!isNewCertification) {
            // Update existing certification
            mutation = `
                mutation UpdateCertification($data: UpdateCertificationInput!) {
                    updateCertification(data: $data) {
                        status
                        error
                        certification {
                            id
                            certificationVendor
                            certificationName
                            certificationShortName
                        }
                    }
                }
            `;
            variables = {
                data: {
                    id: editingCertification.value.id,
                    companyId: sessionInfo.value.companyId,
                    certificationVendor: editingCertification.value.certificationVendor,
                    certificationName: editingCertification.value.certificationName,
                    certificationShortName: editingCertification.value.certificationShortName
                }
            };
        } else {
            // Create new certification
            mutation = `
                mutation CreateCertification($data: CertificationInput!) {
                    createCertification(data: $data) {
                        status
                        error
                        certification {
                            id
                            certificationVendor
                            certificationName
                            certificationShortName
                        }
                    }
                }
            `;
            variables = {
                data: {
                    companyId: sessionInfo.value.companyId,
                    certificationVendor: editingCertification.value.certificationVendor,
                    certificationName: editingCertification.value.certificationName,
                    certificationShortName: editingCertification.value.certificationShortName || ''
                }
            };
        }

        const response = await fetch('/graphql', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: mutation, variables })
        });

        const result = await response.json();
        if (result.errors) {
            throw new Error(result.errors[0].message);
        }

        const operationName = isNewCertification ? 'createCertification' : 'updateCertification';
        const data = result.data[operationName];
        
        if (data && data.status === 'success') {
            // Store the vendor name before clearing the form
            const vendorName = isNewCertification ? editingCertification.value.certificationVendor : null;
            
            // Clear the form first
            dialogVisible.value = false;
            editingCertification.value = null;
            
            // Then refresh the data
            await fetchCertifications();
            
            // If we added a new vendor, refresh the vendors list
            if (isNewCertification) {
                await fetchVendors();
                // Select the new vendor category
                selectedCategory.value = vendorName;
            }
            
            toast.add({
                severity: 'success',
                summary: 'Success',
                detail: isNewCertification ? 
                    'Certification created successfully' : 
                    'Certification updated successfully',
                life: 3000
            });
        } else {
            throw new Error(data?.error || 'Operation failed');
        }
    } catch (error) {
        console.error('Error saving certification:', error);
        toast.add({
            severity: 'error',
            summary: 'Error',
            detail: error.message || 'Failed to save certification',
            life: 3000
        });
    }
};

const confirmDelete = (certification) => {
    confirm.require({
        message: `Are you sure you want to delete "${certification.certificationName}"?`,
        header: 'Confirm Deletion',
        icon: 'pi pi-exclamation-triangle',
        accept: () => deleteCertification(certification),
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

const deleteCertification = async (certification) => {
    if (!sessionInfo.value?.companyId) return;

    try {
        const mutation = {
            query: `
                mutation DeleteCertification($certificationId: String!, $companyId: String!) {
                    deleteCertification(certificationId: $certificationId, companyId: $companyId) {
                        status
                        error
                    }
                }
            `,
            variables: {
                certificationId: certification.id,
                companyId: sessionInfo.value.companyId
            }
        };

        const response = await fetch('/graphql', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(mutation)
        });

        const result = await response.json();
        if (result.errors) {
            throw new Error(result.errors[0].message);
        }

        const data = result.data.deleteCertification;
        if (data.status === 'success') {
            await fetchCertifications(); // Refresh the list
            toast.add({
                severity: 'success',
                summary: 'Deleted',
                detail: 'Certification deleted successfully',
                life: 3000
            });
        } else {
            throw new Error(data.error);
        }
    } catch (error) {
        toast.add({
            severity: 'error',
            summary: 'Error',
            detail: error.message || 'Failed to delete certification',
            life: 3000
        });
    }
};

const generate = async () => {
    if (!form.vendor) {
        toast.add({ severity: 'warn', summary: 'Warning', detail: 'Please enter a vendor', life: 3000 });
        return;
    }

    loading.value = true;
    try {
        const query = {
            query: `
                query GenerateCertificationsPerProduct($product: String!) {
                    generateCertificationsPerProduct(product: $product) {
                        status
                        error
                        certifications {
                            certificationName
                            certificationShortName
                        }
                    }
                }
            `,
            variables: {
                product: form.vendor
            }
        };

        const response = await fetch('/graphql', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(query)
        });

        const result = await response.json();
        if (result.errors) {
            throw new Error(result.errors[0].message);
        }

        const data = result.data.generateCertificationsPerProduct;
        if (data.status === 'error') {
            throw new Error(data.error);
        }

        results.value = data.certifications;
        toast.add({
            severity: 'success',
            summary: 'Success',
            detail: 'Certifications generated successfully',
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
    const severities = ['info', 'success', 'warning', 'danger', 'primary', 'warn', 'help', 'secondary'];
    return severities[index % severities.length];
};

// Initialize component
onMounted(() => {
    fetchSessionInfo();
});
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
  background-color: var(--surface-hover) !important;
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

/* Compact Breadcrumb Styles */
.compact-breadcrumb {
    padding: 0.5rem 0;
}

.compact-breadcrumb :deep(.p-breadcrumb) {
    border: none;
    padding: 0;
    background-color: transparent;
}

.compact-breadcrumb :deep(.p-breadcrumb .p-breadcrumb-list) {
    margin: 0;
    padding: 0;
}

.compact-breadcrumb :deep(.p-breadcrumb .p-menuitem-text) {
    font-size: 0.875rem;
}

.compact-breadcrumb :deep(.p-breadcrumb .p-menuitem-icon) {
    font-size: 0.875rem;
}

.compact-breadcrumb :deep(.p-breadcrumb-chevron) {
    margin: 0 0.25rem;
    font-size: 0.75rem;
}
</style> 