<script setup>
import { onMounted, reactive, ref, watch } from 'vue';
import { useLayout } from '@/layout/composables/layout';
import {  onBeforeMount } from 'vue';
import { useRouter } from 'vue-router';


const { isDarkTheme } = useLayout();


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
        const response = await fetch(`/api/apitest`, {
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
        <div
        id="hero"
        class="flex flex-column pt-4 px-4 lg:px-8 overflow-hidden"
        style="background: linear-gradient(0deg, rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0.2)), radial-gradient(77.36% 256.97% at 77.36% 57.52%, rgb(238, 239, 175) 0%, rgb(195, 227, 250) 100%); clip-path: ellipse(150% 87% at 93% 13%)"
    >
        <div class="mx-4 md:mx-8 mt-0 md:mt-4">
            <h1 class="text-6xl font-bold text-gray-900 line-height-2"><span class="font-light block">Welcome to</span>SamanaGroup Jobs Portal</h1>
            <p class="font-normal text-2xl line-height-3 md:mt-3 text-gray-700">Track your skills, certifications, and career progress effortlessly with Samana CareerPath. Welcome aboard!</p>
            <br> <br> <br> <br>   
        </div>





</div>
<div class="grid p-fluid">
            <div class="col-12">
                <h5>Quick Menu</h5>
            </div>
    
            <div  class="col-12 md:col-6 lg:col-4">
                        <Card>
                            <template #title>Employees Dashboard</template>
                            <template #subtitle>Employees information, reviews and more</template>
                            <template #content>
                                Access to the employees Dashboard, provide employee feedback and register skillsets.
                            </template>
                            <template #footer>
                                <div class="flex gap-4 mt-1">
                            
                                    <Button
                                        label="Access"
                                        class="w-full"
                                        outlined
                                        raised
                                        @click="router.push('/employees')"                         />
                    
                                </div>
                            </template>
                        </Card>
            </div>
            <div  class="col-12 md:col-6 lg:col-4">
                        <Card>
                            <template #title>Candidates Dashboard</template>
                            <template #subtitle>Candidates information, reviews and more</template>
                            <template #content>
                                Access to the candidates Dashboard, provide  feedback and register skillsets during the interview.
                            </template>
                            <template #footer>
                                <div class="flex gap-4 mt-1">
                            
                                    <Button
                                        label="Access"
                                        class="w-full"
                                        outlined
                                        raised
                                        @click="router.push('/candidates')"                         />
                    
                                </div>
                            </template>
                        </Card>
            </div>               
            <div  class="col-12 md:col-6 lg:col-4">
                        <Card>
                            <template #title>Selection Process</template>
                            <template #subtitle>View active jobs, candidates reviews and more</template>
                            <template #content>
                                Access to the Selection Process Dashboard, identify the current selection process and access to the candidates reviews through this module.
                            </template>
                            <template #footer>
                                <div class="flex gap-4 mt-1">
                            
                                    <Button
                                        label="Access"
                                        class="w-full"
                                        outlined
                                        raised
                                        @click="router.push('/jobprocess')"                         />
                    
                                </div>
                            </template>
                        </Card>
            </div>  

        </div>




</template>