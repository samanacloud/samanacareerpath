
<script>
import axios from 'axios';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Button from 'primevue/button';

//redirects to unauthorized if the user role is lower than the pagerole
import { getPageAuthorization } from '@/utils/utils';
const pageRole = 1; // Set the required role for this page
getPageAuthorization(pageRole);




const openaiBaseURL = 'https://api.openai.com/v1';
const openaiApiKey = import.meta.env.VITE_OPENAI_API_KEY;

export default {
    data() {
        return {
            employeeName: '',
            certifications: [],
            recommendedTraining: [],
            loading: false,
            responseContent: '', // Add this to store the raw response
        };
    },
    async created() {
        try {
            const sessionEmail = this.getSessionEmailFromCookie(); // Fetch session email from cookie
            if (!sessionEmail) {
                throw new Error('Session email not found in cookies');
            }
            const employeeDetails = await this.fetchEmployeeDetails(sessionEmail);
  
            if (employeeDetails) {
                this.employeeName = employeeDetails.fullName;
                this.certifications = await this.fetchCertifications(sessionEmail);
            }
        } catch (error) {
            console.error('Error fetching employee details:', error);
        }
    },
    methods: {
        getSessionEmailFromCookie() {
            const name = 'userEmail=';
            const decodedCookie = decodeURIComponent(document.cookie);
            const ca = decodedCookie.split(';');
            for (let i = 0; i < ca.length; i++) {
                let c = ca[i];
                while (c.charAt(0) === ' ') {
                    c = c.substring(1);
                }
                if (c.indexOf(name) === 0) {
                    return c.substring(name.length, c.length);
                }
            }
            return '';
        },
        async fetchEmployeeDetails(email) {
            try {
                const response = await axios.post(`/api/apitest`, {
                    action: 'getEmployee',
                    email: email,
                });
                return response.data;
            } catch (error) {
                console.error('Error fetching employee details:', error);
                return null;
            }
        },
        async fetchCertifications(email) {
            try {
                const response = await axios.post(`/api/apitest`, {
                    action: 'listEmployeeCertifications',
                    email: email,
                });
                return response.data;
            } catch (error) {
                console.error('Error fetching certifications:', error);
                return [];
            }
        },
        async showRecommendedTraining() {
        try {
            this.loading = true;

            // Convert the certifications array into a single string
            const certificationsString = this.certifications.map(cert => cert.certification).join(', ');

            const response = await axios.post('/api/ainode.php', {
                certifications: certificationsString, // Send as a single string
            });

            if (response.data.recommendedTraining.error) {
                console.error('Error from OpenAI:', response.data.recommendedTraining.error);
                this.recommendedTraining = []; // Handle error
            } else {
                this.recommendedTraining = response.data.recommendedTraining; // Set the valid training data
            }
        } catch (error) {
            console.error('Error fetching recommended training:', error);
        } finally {
            this.loading = false;
        }
    },
    },
    components: {
        DataTable,
        Column,
        Button,
    },
};
</script>

<template>
    <div class="card">
        <h5>Samana AI Training</h5>
        <p v-if="employeeName">Hello {{ employeeName }}! Ready to learn new stuff?</p>
        <p v-else>Loading...</p>
  
        <DataTable v-if="certifications.length" :value="certifications" responsiveLayout="scroll">
            <Column field="certification" header="Certification"></Column>
            <Column field="date" header="Date"></Column>
        </DataTable>
        <p v-else>No certifications found.</p>
    </div>
        <Button label="Show Me Recommended Training" @click="showRecommendedTraining" />
  
        <div v-if="loading" class="loading-spinner">
            <i class="pi pi-spin pi-spinner" style="font-size: 2rem"></i>
        </div>
  

   
    <div v-if="recommendedTraining.length" class="training-cards">
           
            <div class="card" v-for="training in recommendedTraining" :key="training.title">
                <h5>{{ training.title }}</h5>
                <p>{{ training.description }}</p>
                <a :href="training.link" target="_blank">Access Course</a>
            </div>
        </div>
        
</template>
  


<style scoped>
.card {
    padding: 20px;
  
    border-radius: 8px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}
.training-cards {
    display: flex; 
    flex-wrap: wrap;
    gap: 20px;
}
.training-cards .card {
    flex: 1;
    padding: 20px;
   
    border-radius: 8px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}
.loading-spinner {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100px;
}
</style>