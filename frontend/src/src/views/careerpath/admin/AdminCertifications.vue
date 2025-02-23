<template>
    <div class="flex flex-col gap-8">
        <!-- Categories Section - Full Width -->
        <div class="col-12">
            <div class="card">
                <div class="font-semibold text-xl">Certification Vendors</div>
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
            <!-- Category Certifications Card -->
            <div class="card">
                    <div class="font-semibold text-xl">{{ selectedCategory || 'Select a Category' }}</div>
                <div class="grid">
                    <div v-for="certification in filteredCertifications" 
                         :key="certification.id" 
                         class="col-12 md:col-6 lg:col-4 xl:col-3 mb-3">
                        <div class="surface-card p-3 border-round h-full">
                            <!-- View Mode -->
                            <div v-if="!editingCertification || editingCertification.id !== certification.id">
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

                            <!-- Edit Mode -->
                            <div v-else class="p-fluid">
                                <div class="field mb-3">
                                    <InputText 
                                        v-model="editingCertification.certificationName"
                                        placeholder="Certification name"
                                        class="w-full"
                                    />
                                </div>
                                <div class="field mb-3">
                                    <InputText 
                                        v-model="editingCertification.certificationShortName"
                                        placeholder="Certification short name"
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
            
            <!-- Generator Card -->
            <div class="card mb-3">
                <div class="font-semibold text-xl">Generate Certifications</div>
                <div class="mt-4">
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
            </div>
        </div>
    </div>

    <!-- Delete Confirmation Dialog -->
    <confirmPopup></confirmPopup>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue';
import { useToast } from 'primevue/usetoast';
import { useConfirm } from 'primevue/useconfirm';

const toast = useToast();
const confirm = useConfirm();
const loading = ref(false);
const results = ref([]);
const selectedCategory = ref(null);
const editingCertification = ref(null);
const sessionInfo = ref(null);
const certifications = ref([]);
const categories = ref([]); // Will be populated with vendors

const form = reactive({
    vendor: ''
});

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
    editingCertification.value = { ...certification };
};

const cancelEdit = () => {
    editingCertification.value = null;
};

const saveEdit = async () => {
    if (!sessionInfo.value?.companyId) return;

    try {
        const mutation = {
            query: `
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
            `,
            variables: {
                data: {
                    id: editingCertification.value.id,
                    companyId: sessionInfo.value.companyId,
                    certificationVendor: editingCertification.value.certificationVendor,
                    certificationName: editingCertification.value.certificationName,
                    certificationShortName: editingCertification.value.certificationShortName
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

        const data = result.data.updateCertification;
        if (data.status === 'success') {
            await fetchCertifications(); // Refresh the list
            editingCertification.value = null;
            toast.add({
                severity: 'success',
                summary: 'Success',
                detail: 'Certification updated successfully',
                life: 3000
            });
        } else {
            throw new Error(data.error);
        }
    } catch (error) {
        toast.add({
            severity: 'error',
            summary: 'Error',
            detail: error.message || 'Failed to update certification',
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
</style> 