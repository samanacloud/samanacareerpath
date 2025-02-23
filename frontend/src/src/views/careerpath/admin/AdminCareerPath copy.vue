<script setup>
import { ref, onMounted } from 'vue';
import Button from 'primevue/button';
import Card from 'primevue/card';

const counts = ref({
    total_certifications: 0,
    total_skillsets: 0,
    total_skills: 0,
    total_roles: 0,
    total_evaluation_fields: 0
});

const loading = ref(false);
const error = ref(null);

// Mock data for charts
const certificationTrends = ref([25, 40, 35, 50, 45, 60, 55, 65, 70, 80]);
const skillsetTrends = ref([30, 45, 40, 55, 50, 65, 60, 70, 75, 85]);
const roleTrends = ref([15, 20, 25, 30, 28, 35, 38, 40, 45, 50]);
const evaluationTrends = ref([10, 15, 20, 25, 23, 30, 32, 35, 38, 40]);

// Function to get cookie value by name
const getCookie = (name) => {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
};

// Extract session data from cookie
const sessionData = ref({});

// Fetch career path data
const fetchCareerPath = async () => {
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
                    companyId: 'demo-company-id' // Replace with actual company ID
                }
            })
        });

        const data = await response.json();
        if (data.data?.careerpathByCompany) {
            const careerPath = data.data.careerpathByCompany;
            counts.value = {
                total_certifications: careerPath.certifications?.reduce((acc, curr) => acc + curr.certifications.length, 0) || 0,
                total_skillsets: careerPath.skillsets?.length || 0,
                total_skills: careerPath.skillsets?.reduce((acc, curr) => acc + curr.skills.length, 0) || 0,
                total_roles: careerPath.roles?.length || 0,
                total_evaluation_fields: careerPath.evaluationFields?.length || 0
            };
        }
    } catch (err) {
        error.value = err.message;
        console.error('Error fetching career path:', err);
    } finally {
        loading.value = false;
    }
};

// Create career path
const handleCreateCareerPath = async () => {
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
                    mutation CreateCareerPath($input: CreateCareerPathInput!) {
                        createCareerPath(input: $input) {
                            id
                            companyId
                            companyName
                        }
                    }
                `,
                variables: {
                    input: {
                        companyId: 'demo-company-id', // Replace with actual company ID
                        companyName: 'Demo Company', // Replace with actual company name
                        certifications: [],
                        skillsets: [],
                        evaluationFields: [],
                        roles: []
                    }
                }
            })
        });

        const data = await response.json();
        if (data.data?.createCareerPath) {
            console.log('Career path created:', data.data.createCareerPath);
            // Refresh data
            await fetchCareerPath();
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
    const sessionCookie = getCookie('session');
    if (sessionCookie) {
        try {
            sessionData.value = JSON.parse(decodeURIComponent(sessionCookie));
        } catch (e) {
            console.error('Error parsing session cookie:', e);
        }
    }
    fetchCareerPath();
});
</script>

<template>
    <section>
        <div class="flex flex-col gap-7">
            <!-- Header with Create Button -->
            <div class="flex justify-between items-center">
                <h2 class="text-2xl font-bold">Career Path Management</h2>
                <Button 
                    label="Create Career Path" 
                    icon="pi pi-plus" 
                    severity="success" 
                    @click="handleCreateCareerPath"
                    :loading="loading"
                />
            </div>

            <!-- Debug: Display session data -->
            <div class="p-4 bg-gray-100 rounded-lg">
                <h3 class="text-lg font-semibold">Session Data (Debug)</h3>
                <pre>{{ sessionData }}</pre>
            </div>

            <!-- Loading State -->
            <div v-if="loading" class="flex justify-center items-center p-4">
                <i class="pi pi-spin pi-spinner text-2xl"></i>
            </div>

            <!-- Error State -->
            <div v-else-if="error" class="p-4 bg-red-100 text-red-700 rounded-lg">
                {{ error }}
            </div>

            <!-- Content -->
            <div v-else class="flex flex-col gap-7">
                <!-- Top Cards Grid -->
                <div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-7">
                    <!-- Certifications Card -->
                    <Card class="flex-1 bg-white dark:bg-gray-900">
                        <template #title>
                            <div class="flex justify-between items-center mb-4">
                                <h3 class="text-xl font-semibold">Certifications</h3>
                                <Button icon="pi pi-plus" severity="success" text rounded aria-label="Add" />
                            </div>
                        </template>
                        <template #content>
                            <div class="flex flex-col">
                                <span class="text-3xl font-bold mb-2">{{ counts.total_certifications }}</span>
                                <div class="flex justify-between items-center">
                                    <span class="text-sm text-gray-600 dark:text-gray-400">Total Certifications</span>
                                    <span class="text-sm text-green-600">+12%</span>
                                </div>
                                <div class="h-16 mt-4">
                                    <div class="flex items-end h-full gap-1">
                                        <div v-for="(value, index) in certificationTrends" :key="index"
                                            class="flex-1 bg-primary-500 opacity-75 hover:opacity-100 transition-all"
                                            :style="{ height: value + '%' }">
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </template>
                    </Card>

                    <!-- Skillsets Card -->
                    <Card class="flex-1 bg-white dark:bg-gray-900">
                        <template #title>
                            <div class="flex justify-between items-center mb-4">
                                <h3 class="text-xl font-semibold">Skillsets</h3>
                                <Button icon="pi pi-plus" severity="success" text rounded aria-label="Add" />
                            </div>
                        </template>
                        <template #content>
                            <div class="flex flex-col">
                                <span class="text-3xl font-bold mb-2">{{ counts.total_skillsets }}</span>
                                <div class="flex justify-between items-center">
                                    <span class="text-sm text-gray-600 dark:text-gray-400">Total Skillsets</span>
                                    <span class="text-sm text-green-600">+8%</span>
                                </div>
                                <div class="h-16 mt-4">
                                    <div class="flex items-end h-full gap-1">
                                        <div v-for="(value, index) in skillsetTrends" :key="index"
                                            class="flex-1 bg-orange-500 opacity-75 hover:opacity-100 transition-all"
                                            :style="{ height: value + '%' }">
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </template>
                    </Card>

                    <!-- Roles Card -->
                    <Card class="flex-1 bg-white dark:bg-gray-900">
                        <template #title>
                            <div class="flex justify-between items-center mb-4">
                                <h3 class="text-xl font-semibold">Roles</h3>
                                <Button icon="pi pi-plus" severity="success" text rounded aria-label="Add" />
                            </div>
                        </template>
                        <template #content>
                            <div class="flex flex-col">
                                <span class="text-3xl font-bold mb-2">{{ counts.total_roles }}</span>
                                <div class="flex justify-between items-center">
                                    <span class="text-sm text-gray-600 dark:text-gray-400">Total Roles</span>
                                    <span class="text-sm text-green-600">+15%</span>
                                </div>
                                <div class="h-16 mt-4">
                                    <div class="flex items-end h-full gap-1">
                                        <div v-for="(value, index) in roleTrends" :key="index"
                                            class="flex-1 bg-blue-500 opacity-75 hover:opacity-100 transition-all"
                                            :style="{ height: value + '%' }">
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </template>
                    </Card>

                    <!-- Evaluation Fields Card -->
                    <Card class="flex-1 bg-white dark:bg-gray-900">
                        <template #title>
                            <div class="flex justify-between items-center mb-4">
                                <h3 class="text-xl font-semibold">Evaluation Fields</h3>
                                <Button icon="pi pi-plus" severity="success" text rounded aria-label="Add" />
                            </div>
                        </template>
                        <template #content>
                            <div class="flex flex-col">
                                <span class="text-3xl font-bold mb-2">{{ counts.total_evaluation_fields }}</span>
                                <div class="flex justify-between items-center">
                                    <span class="text-sm text-gray-600 dark:text-gray-400">Total Fields</span>
                                    <span class="text-sm text-green-600">+5%</span>
                                </div>
                                <div class="h-16 mt-4">
                                    <div class="flex items-end h-full gap-1">
                                        <div v-for="(value, index) in evaluationTrends" :key="index"
                                            class="flex-1 bg-purple-500 opacity-75 hover:opacity-100 transition-all"
                                            :style="{ height: value + '%' }">
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </template>
                    </Card>
                </div>

                <!-- Middle Section -->
                <div class="w-full flex xl:flex-row flex-col gap-6">
                    <!-- AI Suggestions Card -->
                    <Card class="w-full xl:w-auto xl:flex-1">
                        <template #title>
                            <div class="flex justify-between items-center mb-4">
                                <h3 class="text-xl font-semibold">AI Suggestions</h3>
                                <Button icon="pi pi-refresh" severity="secondary" text rounded aria-label="Refresh" />
                            </div>
                        </template>
                        <template #content>
                            <div class="flex flex-col gap-4">
                                <div class="flex justify-between items-center p-4 bg-surface-100 dark:bg-surface-700 rounded-lg">
                                    <div class="flex flex-col">
                                        <span class="font-semibold">Generate Certifications</span>
                                        <span class="text-sm text-gray-600 dark:text-gray-400">Get AI-powered certification suggestions</span>
                                    </div>
                                    <Button label="Generate" severity="primary" @click="handleGenerateCertifications" />
                                </div>
                                <div class="flex justify-between items-center p-4 bg-surface-100 dark:bg-surface-700 rounded-lg">
                                    <div class="flex flex-col">
                                        <span class="font-semibold">Generate Skillsets</span>
                                        <span class="text-sm text-gray-600 dark:text-gray-400">Get AI-powered skillset suggestions</span>
                                    </div>
                                    <Button label="Generate" severity="primary" @click="handleGenerateSkillsets" />
                                </div>
                            </div>
                        </template>
                    </Card>

                    <!-- Recent Activities Card -->
                    <Card class="w-full xl:w-[25rem]">
                        <template #title>
                            <div class="flex justify-between items-center mb-4">
                                <h3 class="text-xl font-semibold">Recent Activities</h3>
                            </div>
                        </template>
                        <template #content>
                            <div class="flex flex-col gap-4">
                                <div class="flex items-center gap-4 p-3 bg-surface-100 dark:bg-surface-700 rounded-lg">
                                    <i class="pi pi-plus-circle text-green-500 text-xl"></i>
                                    <div class="flex flex-col">
                                        <span class="font-medium">New Certification Added</span>
                                        <span class="text-sm text-gray-600 dark:text-gray-400">AWS Solutions Architect</span>
                                    </div>
                                    <span class="text-sm text-gray-500 ml-auto">2m ago</span>
                                </div>
                                <div class="flex items-center gap-4 p-3 bg-surface-100 dark:bg-surface-700 rounded-lg">
                                    <i class="pi pi-pencil text-blue-500 text-xl"></i>
                                    <div class="flex flex-col">
                                        <span class="font-medium">Skillset Updated</span>
                                        <span class="text-sm text-gray-600 dark:text-gray-400">Cloud Computing</span>
                                    </div>
                                    <span class="text-sm text-gray-500 ml-auto">1h ago</span>
                                </div>
                            </div>
                        </template>
                    </Card>
                </div>
            </div>
        </div>
    </section>
</template>

<style>
.card {
    background: var(--surface-card);
    padding: 1.5rem;
    margin-bottom: 1rem;
    border-radius: var(--border-radius);
    box-shadow: var(--card-shadow);
}
</style>
