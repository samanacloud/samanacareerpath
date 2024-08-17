<script setup>
import { onMounted, reactive, ref, watch } from 'vue';
import { useLayout } from '@/layout/composables/layout';
import {  onBeforeMount } from 'vue';
import { useRouter } from 'vue-router';


const { isDarkTheme } = useLayout();

// Function to get the base URL
const baseURL = import.meta.env.VITE_SITE_URL 
    ? `https://${import.meta.env.VITE_SITE_URL}` // Use https if VITE_SITE_URL is defined
    : 'http://localhost:8080'; // Use localhost for development

const tableData = ref([]);

const lineOptions = ref(null);
const userEmail = ref('');
const admin = ref('');
const router = useRouter();


onBeforeMount(() => {

    userEmail.value = document.cookie.replace(/(?:(?:^|.*;\s*)userEmail\s*\=\s*([^;]*).*$)|^.*$/, "$1");
    admin.value = document.cookie.replace(/(?:(?:^|.*;\s*)admin\s*\=\s*([^;]*).*$)|^.*$/, "$1");


 
    if (admin.value === '1') {
        sessionStorage.setItem('employeeEmail', userEmail.value);
        router.push('/employeeprofile');
    }
});
onMounted(() => {
    const userEmail = document.cookie.replace(/(?:(?:^|.*;\s*)userEmail\s*\=\s*([^;]*).*$)|^.*$/, "$1");
    const candidateEmail = document.cookie.replace(/(?:(?:^|.*;\s*)CandidateEmail\s*\=\s*([^;]*).*$)|^.*$/, "$1");

    if (userEmail.includes('@gmail.com') || candidateEmail) {
        router.push('/landing');
        return;
    }

   
    fetchTableData();
});

const fetchTableData = async () => {
    try {
        const response = await fetch(`${baseURL}/api/apitest.php`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ action: 'getOverallInfo' })
        });
        const data = await response.json();
        const allowedTables = {
            candidate: [
                'candidate_certifications',
                'candidate_profiles',
                'candidate_review',
                'candidate_skillsets'
            ],
            employee: [
                'employee_certifications',
                'employee_profiles',
                'employee_reviews',
                'employee_skillsets'
            ],
            users: ['users']
        };

        const formatTableName = (tableName) => {
            const parts = tableName.split('_');
            return parts.slice(1).join(' ').replace(/(^|\s)\S/g, (letter) => letter.toUpperCase());
        };

        tableData.value = {
            candidate: data
                .filter(table => allowedTables.candidate.includes(table.table_name))
                .map(table => ({ ...table, formatted_name: formatTableName(table.table_name) })),
            employee: data
                .filter(table => allowedTables.employee.includes(table.table_name))
                .map(table => ({ ...table, formatted_name: formatTableName(table.table_name) })),
            users: data
                .filter(table => allowedTables.users.includes(table.table_name))
                .map(table => ({ ...table, formatted_name: formatTableName(table.table_name) }))
        };
    } catch (error) {
        console.error('Error fetching table data:', error);
    }
};



const applyLightTheme = () => {
    lineOptions.value = {
        plugins: {
            legend: {
                labels: {
                    color: '#495057'
                }
            }
        },
        scales: {
            x: {
                ticks: {
                    color: '#495057'
                },
                grid: {
                    color: '#ebedef'
                }
            },
            y: {
                ticks: {
                    color: '#495057'
                },
                grid: {
                    color: '#ebedef'
                }
            }
        }
    };
};

const applyDarkTheme = () => {
    lineOptions.value = {
        plugins: {
            legend: {
                labels: {
                    color: '#ebedef'
                }
            }
        },
        scales: {
            x: {
                ticks: {
                    color: '#ebedef'
                },
                grid: {
                    color: 'rgba(160, 167, 181, .3)'
                }
            },
            y: {
                ticks: {
                    color: '#ebedef'
                },
                grid: {
                    color: 'rgba(160, 167, 181, .3)'
                }
            }
        }
    };
};

watch(
    isDarkTheme,
    (val) => {
        if (val) {
            applyDarkTheme();
        } else {
            applyLightTheme();
        }
    },
    { immediate: true }
);
</script>

<template>

<div className="card">
    <div class="grid">
        <!-- Employee Section -->
        <div class="col-12">
            <h5>Employee</h5>
        </div>
        <div 
          class="col-12 lg:col-6 xl:col-3" 
          v-for="(table, index) in tableData.employee" 
          :key="'employee-' + index"
        >
            <div class="card mb-0">
                <div class="flex justify-content-between mb-3">
                    <div>
                        <span class="block text-500 font-medium mb-3">{{ table.formatted_name }}</span>
                        <div class="text-900 font-medium text-xl">{{ table.count }}</div>
                    </div>
                    <div class="flex align-items-center justify-content-center bg-blue-100 border-round" style="width: 2.5rem; height: 2.5rem">
                        <i class="pi pi-users text-blue-500 text-xl"></i>
                    </div>
                </div>

            </div>
        </div>




        <!-- Candidate Section -->
        <div class="col-12">
            <h5>Candidate</h5>
        </div>
        <div 
          class="col-12 lg:col-6 xl:col-3" 
          v-for="(table, index) in tableData.candidate" 
          :key="'candidate-' + index"
        >
            <div class="card mb-0">
                <div class="flex justify-content-between mb-3">
                    <div>
                        <span class="block text-500 font-medium mb-3">{{ table.formatted_name }}</span>
                        <div class="text-900 font-medium text-xl">{{ table.count }}</div>
                    </div>
                    <div class="flex align-items-center justify-content-center bg-orange-100 border-round" style="width: 2.5rem; height: 2.5rem">
                        <i class="pi pi-user-plus text-orange-500 text-xl"></i>
                    </div>
                </div>

            </div>
        </div>


        <!-- Users Section -->
        <div class="col-12">
            <h5>Users</h5>
        </div>
        <div 
          class="col-12 lg:col-6 xl:col-3" 
          v-for="(table, index) in tableData.users" 
          :key="'users-' + index"
        >
            <div class="card mb-0">
                <div class="flex justify-content-between mb-3">
                    <div>
                        <span class="block text-500 font-medium mb-3">{{ table.formatted_name }}</span>
                        <div class="text-900 font-medium text-xl">{{ table.count }}</div>
                    </div>
                    <div class="flex align-items-center justify-content-center bg-blue-100 border-round" style="width: 2.5rem; height: 2.5rem">
                        <i class="pi pi-user text-cyan-500 text-xl"></i>
                    </div>
                </div>
    
            </div>
        </div>
    </div>
</div>
</template>