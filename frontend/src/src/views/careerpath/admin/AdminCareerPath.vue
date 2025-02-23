<script setup>
import { ref, onMounted, watch } from 'vue';
import { useToast } from 'primevue/usetoast';
import { useConfirm } from 'primevue/useconfirm';
import Button from 'primevue/button';
import Card from 'primevue/card';
import Dialog from 'primevue/dialog';
import InputText from 'primevue/inputtext';
import Chips from 'primevue/chips';
import ConfirmPopup from 'primevue/confirmpopup';
import Toast from 'primevue/toast';

const toast = useToast();
const confirm = useConfirm();

// Dialogs visibility state
const certificationDialog = ref(false);
const skillsetDialog = ref(false);
const roleDialog = ref(false);
const evaluationFieldDialog = ref(false);

// Form states
const newCertification = ref({
    issuer: '',
    certifications: [{
        certificationName: '',
        certificationShortName: ''
    }]
});

const newSkillset = ref({
    category: '',
    skills: []
});

const newRole = ref({
    roleName: ''
});

const newEvaluationField = ref({
    field: ''
});

// Edit states
const editMode = ref(false);
const editItem = ref(null);

// Existing data refs and loading state
const counts = ref({
    total_certifications: 0,
    total_skillsets: 0,
    total_skills: 0,
    total_roles: 0,
    total_evaluation_fields: 0
});

const loading = ref(false);
const error = ref(null);
const sessionInfo = ref(null);
const careerPath = ref(null);

// Mock data for charts
const certificationTrends = ref([25, 40, 35, 50, 45, 60, 55, 65, 70, 80]);
const skillsetTrends = ref([30, 45, 40, 55, 50, 65, 60, 70, 75, 85]);
const roleTrends = ref([15, 20, 25, 30, 28, 35, 38, 40, 45, 50]);
const evaluationTrends = ref([10, 15, 20, 25, 23, 30, 32, 35, 38, 40]);

// CRUD Operations
const handleAddCertificationIssuer = async () => {
    try {
        loading.value = true;
        const response = await fetch('/graphql', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                query: `
                    mutation AddCertificationIssuer($input: AddCertificationIssuerInput!) {
                        addCertificationIssuer(input: $input) {
                            id
                            certifications { issuer certifications { certificationName certificationShortName } }
                        }
                    }
                `,
                variables: {
                    input: {
                        companyId: sessionInfo.value.companyId,
                        ...newCertification.value
                    }
                }
            })
        });

        const data = await response.json();
        if (data.data?.addCertificationIssuer) {
            toast.add({
                severity: 'success',
                summary: 'Success',
                detail: 'Certification issuer added successfully',
                life: 3000
            });
            certificationDialog.value = false;
            await fetchCareerPath(sessionInfo.value.companyId);
        } else if (data.errors) {
            throw new Error(data.errors[0].message);
        }
    } catch (err) {
        toast.add({
            severity: 'error',
            summary: 'Error',
            detail: err.message,
            life: 3000
        });
    } finally {
        loading.value = false;
    }
};

const handleAddSkillset = async () => {
    try {
        loading.value = true;
        const response = await fetch('/graphql', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                query: `
                    mutation AddSkillset($input: AddSkillsetInput!) {
                        addSkillset(input: $input) {
                            id
                            skillsets { category skills }
                        }
                    }
                `,
                variables: {
                    input: {
                        companyId: sessionInfo.value.companyId,
                        ...newSkillset.value
                    }
                }
            })
        });

        const data = await response.json();
        if (data.data?.addSkillset) {
            toast.add({
                severity: 'success',
                summary: 'Success',
                detail: 'Skillset added successfully',
                life: 3000
            });
            skillsetDialog.value = false;
            await fetchCareerPath(sessionInfo.value.companyId);
        } else if (data.errors) {
            throw new Error(data.errors[0].message);
        }
    } catch (err) {
        toast.add({
            severity: 'error',
            summary: 'Error',
            detail: err.message,
            life: 3000
        });
    } finally {
        loading.value = false;
    }
};

const handleAddRole = async () => {
    try {
        loading.value = true;
        const response = await fetch('/graphql', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                query: `
                    mutation AddRole($input: AddRoleInput!) {
                        addRole(input: $input) {
                            id
                            roles { roleName }
                        }
                    }
                `,
                variables: {
                    input: {
                        companyId: sessionInfo.value.companyId,
                        ...newRole.value
                    }
                }
            })
        });

        const data = await response.json();
        if (data.data?.addRole) {
            toast.add({
                severity: 'success',
                summary: 'Success',
                detail: 'Role added successfully',
                life: 3000
            });
            roleDialog.value = false;
            await fetchCareerPath(sessionInfo.value.companyId);
        } else if (data.errors) {
            throw new Error(data.errors[0].message);
        }
    } catch (err) {
        toast.add({
            severity: 'error',
            summary: 'Error',
            detail: err.message,
            life: 3000
        });
    } finally {
        loading.value = false;
    }
};

const handleAddEvaluationField = async () => {
    try {
        loading.value = true;
        const response = await fetch('/graphql', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                query: `
                    mutation AddEvaluationField($input: AddEvaluationFieldInput!) {
                        addEvaluationField(input: $input) {
                            id
                            evaluationFields
                        }
                    }
                `,
                variables: {
                    input: {
                        companyId: sessionInfo.value.companyId,
                        ...newEvaluationField.value
                    }
                }
            })
        });

        const data = await response.json();
        if (data.data?.addEvaluationField) {
            toast.add({
                severity: 'success',
                summary: 'Success',
                detail: 'Evaluation field added successfully',
                life: 3000
            });
            evaluationFieldDialog.value = false;
            await fetchCareerPath(sessionInfo.value.companyId);
        } else if (data.errors) {
            throw new Error(data.errors[0].message);
        }
    } catch (err) {
        toast.add({
            severity: 'error',
            summary: 'Error',
            detail: err.message,
            life: 3000
        });
    } finally {
        loading.value = false;
    }
};

const handleDelete = async (type, identifier, event) => {
    confirm.require({
        target: event.currentTarget,
        message: 'Are you sure you want to delete this item?',
        icon: 'pi pi-exclamation-triangle',
        accept: async () => {
            try {
                loading.value = true;
                let query = '';
                let variables = {};

                switch (type) {
                    case 'certification':
                        query = `
                            mutation DeleteCertificationIssuer($companyId: String!, $issuer: String!) {
                                deleteCertificationIssuer(companyId: $companyId, issuer: $issuer) {
                                    id
                                }
                            }
                        `;
                        variables = { companyId: sessionInfo.value.companyId, issuer: identifier };
                        break;
                    case 'skillset':
                        query = `
                            mutation DeleteSkillset($companyId: String!, $category: String!) {
                                deleteSkillset(companyId: $companyId, category: $category) {
                                    id
                                }
                            }
                        `;
                        variables = { companyId: sessionInfo.value.companyId, category: identifier };
                        break;
                    case 'role':
                        query = `
                            mutation DeleteRole($companyId: String!, $roleName: String!) {
                                deleteRole(companyId: $companyId, roleName: $roleName) {
                                    id
                                }
                            }
                        `;
                        variables = { companyId: sessionInfo.value.companyId, roleName: identifier };
                        break;
                    case 'evaluationField':
                        query = `
                            mutation DeleteEvaluationField($companyId: String!, $field: String!) {
                                deleteEvaluationField(companyId: $companyId, field: $field) {
                                    id
                                }
                            }
                        `;
                        variables = { companyId: sessionInfo.value.companyId, field: identifier };
                        break;
                }

                const response = await fetch('/graphql', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query, variables })
                });

                const data = await response.json();
                if (data.data) {
                    toast.add({
                        severity: 'success',
                        summary: 'Success',
                        detail: 'Item deleted successfully',
                        life: 3000
                    });
                    await fetchCareerPath(sessionInfo.value.companyId);
                } else if (data.errors) {
                    throw new Error(data.errors[0].message);
                }
            } catch (err) {
                toast.add({
                    severity: 'error',
                    summary: 'Error',
                    detail: err.message,
                    life: 3000
                });
            } finally {
                loading.value = false;
            }
        }
    });
};

// Function to get cookie value by name
const getCookie = (name) => {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
};

// Function to fetch and update session info
const fetchSessionInfo = async () => {
    loading.value = true;
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
    } catch (err) {
        error.value = err.message;
        console.error('Error fetching session info:', err);
    } finally {
        loading.value = false;
    }
};

// Fetch career path data
const fetchCareerPath = async (companyId) => {
    if (!companyId) return;
    
    loading.value = true;
    error.value = null;
    try {
        const response = await fetch('/graphql', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: `
                    query CareerPathByCompany($companyId: String!) {
                        careerpathByCompany(companyId: $companyId) {
                            id
                            companyId
                            companyName
                            certifications {
                                issuer
                                certifications {
                                    certificationName
                                    certificationShortName
                                }
                            }
                            skillsets {
                                category
                                skills
                            }
                            roles {
                                roleName
                            }
                            evaluationFields
                        }
                    }
                `,
                variables: {
                    companyId
                }
            })
        });

        const data = await response.json();
        if (data.data?.careerpathByCompany) {
            careerPath.value = data.data.careerpathByCompany;
        }
    } catch (err) {
        error.value = err.message;
        console.error('Error fetching career path:', err);
    } finally {
        loading.value = false;
    }
};

// Watch for session info changes to fetch career path
watch(() => sessionInfo.value?.companyId, (newCompanyId) => {
    if (newCompanyId) {
        fetchCareerPath(newCompanyId);
    }
});

// Create career path
const handleCreateCareerPath = async () => {
    if (!sessionInfo.value) return;

    loading.value = true;
    error.value = null;
    try {
        const response = await fetch('/graphql', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: `
                    mutation CreateCareerpath($input: CreateCareerPathInput!) {
                        createCareerpath(input: $input) {
                            id
                            companyId
                            companyName
                        }
                    }
                `,
                variables: {
                    input: {
                        companyId: sessionInfo.value.companyId,
                        companyName: sessionInfo.value.companyName
                    }
                }
            })
        });

        const data = await response.json();
        if (data.data?.createCareerpath) {
            console.log('Career path created:', data.data.createCareerpath);
            // Refresh data
            await fetchCareerPath(sessionInfo.value.companyId);
        } else if (data.errors) {
            error.value = data.errors[0].message;
        }
    } catch (err) {
        error.value = err.message;
        console.error('Error creating career path:', err);
    } finally {
        loading.value = false;
    }
};

const handleGenerateCertifications = () => {
    console.log('Generating certifications...');
};

const handleGenerateSkillsets = () => {
    console.log('Generating skillsets...');
};

// Fetch data on mount
onMounted(() => {
    fetchSessionInfo();
});
</script>

<template>
    <div class="card">
        <Toast />
        <ConfirmPopup />
        
        <div class="font-semibold text-xl mb-4">Career Path Management</div>
        <div v-if="loading" class="text-gray-500">Loading...</div>
        <div v-else-if="error" class="text-red-500">{{ error }}</div>
        <div v-else class="flex flex-col gap-4">
            <!-- No Career Path Message -->
            <div v-if="sessionInfo && !careerPath" class="flex flex-col items-center gap-4 p-8 bg-gray-50 dark:bg-gray-900 rounded text-center">
                <i class="pi pi-info-circle text-4xl text-blue-500"></i>
                <h3 class="font-semibold text-lg">No Career Path Found</h3>
                <p class="text-gray-600 dark:text-gray-400">There is no career path created for this company yet.</p>
                <Button 
                    label="Create Career Path" 
                    icon="pi pi-plus" 
                    severity="success" 
                    @click="handleCreateCareerPath"
                    :loading="loading"
                />
            </div>

            <!-- Career Path Dashboard -->
            <div v-if="careerPath" class="grid grid-cols-12 gap-4">
                <!-- Stats Overview -->
                <div class="col-span-12 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
                    <Card class="shadow-sm bg-blue-50 dark:bg-blue-900">
                        <template #title>Certifications</template>
                        <template #content>
                            <div class="text-center">
                                <div class="text-2xl font-bold mb-2">
                                    {{ careerPath.certifications?.reduce((acc, curr) => acc + curr.certifications.length, 0) || 0 }}
                                </div>
                                <div class="text-sm text-gray-600">Total Certifications</div>
                            </div>
                        </template>
                    </Card>

                    <Card class="shadow-sm bg-green-50 dark:bg-green-900">
                        <template #title>Skillsets</template>
                        <template #content>
                            <div class="text-center">
                                <div class="text-2xl font-bold mb-2">
                                    {{ careerPath.skillsets?.length || 0 }}
                                </div>
                                <div class="text-sm text-gray-600">Categories</div>
                            </div>
                        </template>
                    </Card>

                    <Card class="shadow-sm bg-yellow-50 dark:bg-yellow-900">
                        <template #title>Skills</template>
                        <template #content>
                            <div class="text-center">
                                <div class="text-2xl font-bold mb-2">
                                    {{ careerPath.skillsets?.reduce((acc, curr) => acc + curr.skills.length, 0) || 0 }}
                                </div>
                                <div class="text-sm text-gray-600">Total Skills</div>
                            </div>
                        </template>
                    </Card>

                    <Card class="shadow-sm bg-purple-50 dark:bg-purple-900">
                        <template #title>Roles</template>
                        <template #content>
                            <div class="text-center">
                                <div class="text-2xl font-bold mb-2">
                                    {{ careerPath.roles?.length || 0 }}
                                </div>
                                <div class="text-sm text-gray-600">Total Roles</div>
                            </div>
                        </template>
                    </Card>

                    <Card class="shadow-sm bg-pink-50 dark:bg-pink-900">
                        <template #title>Evaluation Fields</template>
                        <template #content>
                            <div class="text-center">
                                <div class="text-2xl font-bold mb-2">
                                    {{ careerPath.evaluationFields?.length || 0 }}
                                </div>
                                <div class="text-sm text-gray-600">Total Fields</div>
                            </div>
                        </template>
                    </Card>
                </div>

                <!-- Detailed Sections -->
                <div class="col-span-12 xl:col-span-6">
                    <!-- Certifications Section -->
                    <Card class="mb-4">
                        <template #title>
                            <div class="flex justify-between items-center">
                                <span>Certifications by Issuer</span>
                                <Button icon="pi pi-plus" severity="secondary" text @click="certificationDialog = true" />
                            </div>
                        </template>
                        <template #content>
                            <div v-if="!careerPath.certifications?.length" class="text-gray-500 text-center py-4">
                                No certifications added yet
                            </div>
                            <div v-else class="flex flex-col gap-4">
                                <div v-for="issuer in careerPath.certifications" :key="issuer.issuer" class="border-b pb-4 last:border-b-0">
                                    <div class="flex justify-between items-start mb-2">
                                        <h4 class="font-semibold">{{ issuer.issuer }}</h4>
                                        <div class="flex gap-2">
                                            <Button icon="pi pi-pencil" severity="secondary" text 
                                                @click="editItem = issuer; editMode = true; certificationDialog = true" />
                                            <Button icon="pi pi-trash" severity="danger" text 
                                                @click="handleDelete('certification', issuer.issuer, $event)" />
                                        </div>
                                    </div>
                                    <ul class="list-disc list-inside">
                                        <li v-for="cert in issuer.certifications" :key="cert.certificationName" class="text-sm text-gray-600">
                                            {{ cert.certificationName }}
                                        </li>
                                    </ul>
                                </div>
                            </div>
                        </template>
                    </Card>

                    <!-- Roles Section -->
                    <Card>
                        <template #title>
                            <div class="flex justify-between items-center">
                                <span>Career Roles</span>
                                <Button icon="pi pi-plus" severity="secondary" text @click="roleDialog = true" />
                            </div>
                        </template>
                        <template #content>
                            <div v-if="!careerPath.roles?.length" class="text-gray-500 text-center py-4">
                                No roles defined yet
                            </div>
                            <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div v-for="role in careerPath.roles" :key="role.roleName" 
                                    class="p-3 bg-gray-50 dark:bg-gray-800 rounded flex justify-between items-center">
                                    <span>{{ role.roleName }}</span>
                                    <div class="flex gap-2">
                                        <Button icon="pi pi-pencil" severity="secondary" text 
                                            @click="editItem = role; editMode = true; roleDialog = true" />
                                        <Button icon="pi pi-trash" severity="danger" text 
                                            @click="handleDelete('role', role.roleName, $event)" />
                                    </div>
                                </div>
                            </div>
                        </template>
                    </Card>
                </div>

                <div class="col-span-12 xl:col-span-6">
                    <!-- Skillsets Section -->
                    <Card class="mb-4">
                        <template #title>
                            <div class="flex justify-between items-center">
                                <span>Skillsets</span>
                                <Button icon="pi pi-plus" severity="secondary" text @click="skillsetDialog = true" />
                            </div>
                        </template>
                        <template #content>
                            <div v-if="!careerPath.skillsets?.length" class="text-gray-500 text-center py-4">
                                No skillsets defined yet
                            </div>
                            <div v-else class="flex flex-col gap-4">
                                <div v-for="skillset in careerPath.skillsets" :key="skillset.category" class="border-b pb-4 last:border-b-0">
                                    <div class="flex justify-between items-start mb-2">
                                        <h4 class="font-semibold">{{ skillset.category }}</h4>
                                        <div class="flex gap-2">
                                            <Button icon="pi pi-pencil" severity="secondary" text 
                                                @click="editItem = skillset; editMode = true; skillsetDialog = true" />
                                            <Button icon="pi pi-trash" severity="danger" text 
                                                @click="handleDelete('skillset', skillset.category, $event)" />
                                        </div>
                                    </div>
                                    <div class="flex flex-wrap gap-2">
                                        <span v-for="skill in skillset.skills" :key="skill"
                                            class="px-2 py-1 bg-primary-50 text-primary-700 dark:bg-primary-900 dark:text-primary-100 rounded-full text-sm">
                                            {{ skill }}
                                        </span>
                                    </div>
                                </div>
                            </div>
                        </template>
                    </Card>

                    <!-- Evaluation Fields Section -->
                    <Card>
                        <template #title>
                            <div class="flex justify-between items-center">
                                <span>Evaluation Fields</span>
                                <Button icon="pi pi-plus" severity="secondary" text @click="evaluationFieldDialog = true" />
                            </div>
                        </template>
                        <template #content>
                            <div v-if="!careerPath.evaluationFields?.length" class="text-gray-500 text-center py-4">
                                No evaluation fields defined yet
                            </div>
                            <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div v-for="field in careerPath.evaluationFields" :key="field"
                                    class="p-3 bg-gray-50 dark:bg-gray-800 rounded flex justify-between items-center">
                                    <span>{{ field }}</span>
                                    <div class="flex gap-2">
                                        <Button icon="pi pi-pencil" severity="secondary" text 
                                            @click="editItem = { field }; editMode = true; evaluationFieldDialog = true" />
                                        <Button icon="pi pi-trash" severity="danger" text 
                                            @click="handleDelete('evaluationField', field, $event)" />
                                    </div>
                                </div>
                            </div>
                        </template>
                    </Card>
                </div>
            </div>
        </div>

        <!-- Dialogs -->
        <Dialog v-model:visible="certificationDialog" :modal="true" :header="editMode ? 'Edit Certification Issuer' : 'Add Certification Issuer'">
            <div class="flex flex-col gap-4">
                <div class="field">
                    <label for="issuer">Issuer</label>
                    <InputText id="issuer" v-model="newCertification.issuer" class="w-full" />
                </div>
                <div class="field">
                    <label>Certifications</label>
                    <div v-for="(cert, index) in newCertification.certifications" :key="index" class="flex gap-2 mb-2">
                        <InputText v-model="cert.certificationName" placeholder="Name" class="flex-1" />
                        <InputText v-model="cert.certificationShortName" placeholder="Short Name" class="w-24" />
                        <Button icon="pi pi-times" severity="danger" text @click="newCertification.certifications.splice(index, 1)" />
                    </div>
                    <Button label="Add Certification" icon="pi pi-plus" text @click="newCertification.certifications.push({ certificationName: '', certificationShortName: '' })" />
                </div>
            </div>
            <template #footer>
                <Button label="Cancel" icon="pi pi-times" text @click="certificationDialog = false" />
                <Button label="Save" icon="pi pi-check" @click="handleAddCertificationIssuer" :loading="loading" />
            </template>
        </Dialog>

        <Dialog v-model:visible="skillsetDialog" :modal="true" :header="editMode ? 'Edit Skillset' : 'Add Skillset'">
            <div class="flex flex-col gap-4">
                <div class="field">
                    <label for="category">Category</label>
                    <InputText id="category" v-model="newSkillset.category" class="w-full" />
                </div>
                <div class="field">
                    <label for="skills">Skills</label>
                    <Chips id="skills" v-model="newSkillset.skills" class="w-full" />
                </div>
            </div>
            <template #footer>
                <Button label="Cancel" icon="pi pi-times" text @click="skillsetDialog = false" />
                <Button label="Save" icon="pi pi-check" @click="handleAddSkillset" :loading="loading" />
            </template>
        </Dialog>

        <Dialog v-model:visible="roleDialog" :modal="true" :header="editMode ? 'Edit Role' : 'Add Role'">
            <div class="field">
                <label for="roleName">Role Name</label>
                <InputText id="roleName" v-model="newRole.roleName" class="w-full" />
            </div>
            <template #footer>
                <Button label="Cancel" icon="pi pi-times" text @click="roleDialog = false" />
                <Button label="Save" icon="pi pi-check" @click="handleAddRole" :loading="loading" />
            </template>
        </Dialog>

        <Dialog v-model:visible="evaluationFieldDialog" :modal="true" :header="editMode ? 'Edit Evaluation Field' : 'Add Evaluation Field'">
            <div class="field">
                <label for="field">Field Name</label>
                <InputText id="field" v-model="newEvaluationField.field" class="w-full" />
            </div>
            <template #footer>
                <Button label="Cancel" icon="pi pi-times" text @click="evaluationFieldDialog = false" />
                <Button label="Save" icon="pi pi-check" @click="handleAddEvaluationField" :loading="loading" />
            </template>
        </Dialog>
    </div>
</template>

<style>
.card {
    background: var(--surface-card);
    padding: 1.5rem;
    margin-bottom: 1rem;
    border-radius: var(--border-radius);
    box-shadow: var(--card-shadow);
}

.field {
    margin-bottom: 1rem;
}

.field label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
}
</style>
