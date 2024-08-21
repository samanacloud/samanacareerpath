<script setup>
import { ref, onBeforeMount, computed } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import Rating from 'primevue/rating';
import Divider from 'primevue/divider';
import Card from 'primevue/card';
import Button from 'primevue/button';
import Timeline from 'primevue/timeline';
import { useToast } from "primevue/usetoast"; // Import useToast
import Chip from 'primevue/badge';


//redirects to unauthorized if the user role is lower than the pagerole
import { getPageAuthorization } from '@/utils/utils';
const pageRole = 2; // Set the required role for this page
getPageAuthorization(pageRole);




const candidateDetails = ref(null);
const candidateSkillsets = ref([]);
const candidateReviews = ref([]);
const apiResponse = ref('');

const router = useRouter();
const candidateSalaryExpectation = ref({
    salary_expectation: null,
    availability: ''
});


const goBack = () => {
    router.back();
}

// Fetch candidate details
const getCandidateDetails = async (email) => {
    try {
        const response = await axios.post(`/api/api`, { action: 'getCandidate', email });
        candidateDetails.value = response.data;
    } catch (error) {
        apiResponse.value = 'Error fetching candidate details: ' + error.message;
    }
};



const getCandidateSalaryExpectation = async (email) => {
    try {
        const response = await axios.post(`/api/api`, { action: 'getCandidateSalaryExpectation', email });
        candidateSalaryExpectation.value = response.data;
    } catch (error) {
        apiResponse.value = 'Error fetching candidate salary expectation: ' + error.message;
    }
};



// Fetch candidate skillsets
const getCandidateSkillsets = async (email) => {
    try {
        const response = await axios.post(`/api/api`, { action: 'listCandidateSkillsets', email });
        const skillsets = response.data;

        for (const skill of skillsets) {
            const reviewerResponse = await axios.post(`/api/api`, {
                action: 'getReviewerName',
                email: skill.reviewer_email
            });
            skill.reviewer_name = reviewerResponse.data.name || 'Unknown';
        }

        candidateSkillsets.value = skillsets;
    } catch (error) {
        apiResponse.value = 'Error fetching candidate skillsets: ' + error.message;
    }
};

// Fetch candidate reviews
const getCandidateReviews = async (email) => {
    try {
        const response = await axios.post(`/api/api`, { action: 'listCandidateReviews', email });
        candidateReviews.value = response.data;
    } catch (error) {
        apiResponse.value = 'Error fetching candidate reviews: ' + error.message;
    }
};

// Fetch candidate certifications
const candidateCertifications = ref([]);

const getCandidateCertifications = async (email) => {
    try {
        const response = await axios.post(`/api/api`, { action: 'listCandidateCertifications', email });
        candidateCertifications.value = response.data;
    } catch (error) {
        apiResponse.value = 'Error fetching candidate certifications: ' + error.message;
    }
};

// Load candidate email from sessionStorage
const email = sessionStorage.getItem('candidateEmail');
if (email) {
    getCandidateDetails(email);
    getCandidateSkillsets(email);
    getCandidateReviews(email);
    getCandidateCertifications(email); // Fetch certifications
    getCandidateSalaryExpectation(email); // Fetch salary expectation and availability

} else {
    router.push('/'); // Redirect back to home if no email is found in sessionStorage
}

// Group skillsets by category and name
const groupedSkillsets = computed(() => {
    const groups = candidateSkillsets.value.reduce((acc, skill) => {
        if (!acc[skill.category]) {
            acc[skill.category] = {};
        }
        if (!acc[skill.category][skill.skillset]) {
            acc[skill.category][skill.skillset] = [];
        }
        acc[skill.category][skill.skillset].push(skill);
        return acc;
    }, {});
    return groups;
});

// Function to get initials from email
const getInitials = (email) => {
    if (!email) return '';
    const parts = email.split('@')[0].split('.');
    return parts.map(part => part[0].toUpperCase()).join('');
};
// Timeline section
const getMarkerColor = (rating) => {
  if (rating >= 4) return '#4caf50'; // Green for high ratings
  if (rating >= 2) return '#ffc107'; // Yellow for average ratings
  return '#f44336'; // Red for low ratings
};


const getApprovalSeverity = (approved) => {
    return approved === 'Yes' ? 'success' : 'danger';
};

const showObservations = ref({});

const toggleObservations = (reviewId) => {
    showObservations.value[reviewId] = !showObservations.value[reviewId];
};

const openCV = (cvUrl) => {
    window.open(cvUrl.replace('/open?', '/open?'), '_blank'); 
};

const items = ref([
  {
    label: 'View CV',
    icon: 'pi pi-file-pdf',
    command: () => openCV(candidateDetails.value.candidate_cv) 
  },
  {
    label: 'Interview',
    icon: 'pi pi-comments',
    // Add command for Interview action later
  },
  {
    label: 'Schedule Invitation',
    icon: 'pi pi-calendar-plus',
    command: () => scheduleInterview(candidateDetails.value.email),
  }
]);
const scheduleInterview = (candidateEmail) => {
  // Construct the Google Calendar event URL
  const calendarUrl = `https://calendar.google.com/calendar/u/0/r/eventedit?action=TEMPLATE&text=Interview+with+${encodeURIComponent(candidateDetails.value.name)}&details=Interview+for+the+[Position+Name]+position.&dates=${getTodaysDate()}T120000/${getTodaysDate()}T130000&add=${encodeURIComponent(candidateEmail)}&cc=${encodeURIComponent("recruiting@samanagroup.co")}`;
  
    // Open the Google Calendar event in a new window
    window.open(calendarUrl, '_blank');

    toast.add({ severity: 'success', summary: 'Success', detail: 'Interview Scheduled', life: 3000 });
};

const getTodaysDate = () => {
  const today = new Date();
  const year = today.getFullYear();
  const month = String(today.getMonth() + 1).padStart(2, '0'); // Months are 0-indexed
  const day = String(today.getDate()).padStart(2, '0');
  return `${year}${month}${day}`;
};

const candidateInterview = (email) => {
    sessionStorage.setItem('candidateEmail', email);
    router.push('/candidateinterview');
};


</script>

<template>
    <div class="grid">
        <div class="col-12 lg:col-8">
            <div class="card candidate-details ">
  
                <h5>Candidate Details</h5>
                <div v-if="candidateDetails" class="p-grid p-nogutter">
                    <div class="p-col-6 p-md-6">
                        <p>
                            <strong>Name:</strong> {{ candidateDetails.name }}
                        </p>
                        <p>
                            <strong>Email:</strong>
                            <a :href="'https://mail.google.com/mail/?view=cm&fs=1&to=' + candidateDetails.email + '&su=Regarding your application for ' + candidateDetails.name" target="_blank" class="email-link">
                                {{ candidateDetails.email }}
                                <i class="pi pi-envelope email-icon"></i>
                            </a>
                        </p>
                        <p>
                            <strong>Phone Number:</strong>
                            <a :href="'https://web.whatsapp.com/send?phone=' + candidateDetails.phone_number + '&text=' + encodeURIComponent('Hello ' + candidateDetails.name + ', Good afternoon. My name is ' + userName + ' and I am writing from Samana Group. You recently applied for a position we opened for Service Desk Engineer, and I would like to know if you have a few minutes for a short call to ask you a few questions about your resume.')" target="_blank">
                                {{ candidateDetails.phone_number }}
                                <i class="pi pi-whatsapp phone-icon"></i>
                            </a>
                        </p>
                        <p>
                            <strong>English Level:</strong> {{ candidateDetails.english_level }}
                        </p>
                    </div>
                    <div class="p-col-6 p-md-6">
                        <p>
                            <strong>Location:</strong> {{ candidateDetails.location }}
                        </p>
                        <p>
                            <strong>Salary Expectation:</strong> {{ candidateSalaryExpectation.salary_expectation }}
                        </p>
                        <p>
                            <strong>Availability:</strong> {{ candidateSalaryExpectation.availability }}
                        </p>
                        <p>
                            <strong>Registration Date:</strong> {{ new Date(candidateDetails.created_at).toLocaleDateString() }}
                        </p>
                    </div>
                    <div class="p-col-12 p-md-12">
                    <Button icon="pi pi-arrow-left" label="Back" @click="goBack" severity="secondary" outlined class="mb-2 mr-2"  /> 
                    <Button icon="pi pi-search" label="Interview"  severity="success" outlined class="mb-2 mr-2" @click="candidateInterview(candidateDetails.email)"  />
                    <Button icon="pi pi-calendar-plus" label="Schedule Interview" severity="info" outlined class="mb-2 mr-2" @click="scheduleInterview(candidateDetails.email)" />
                    <Button icon="pi pi-file-pdf" label="View CV" severity="warning" outlined class="mb-2 mr-2" @click="openCV(candidateDetails.candidate_cv)" />     
                    </div>               
                    
                   
                </div>
            </div>

            <div class="card" v-if="candidateCertifications.length">
                <h5>Certifications</h5>
                <div class="grid">
                    <div class="col-12 md:col-6" v-for="certification in candidateCertifications" :key="certification.id">
                        <div class="certification-card">
                            <p>{{ certification.certification }}</p>
                        </div>
                    </div>
                </div>
            </div>

            <div class="grid">
                <div class="col-12">
                    <div class="card" v-if="Object.keys(groupedSkillsets).length">
                        <h5>Skillsets</h5>
                        <div class="grid">
                            <div class="col-12 md:col-6" v-for="(skillsBySkillset, category) in groupedSkillsets" :key="category">
                                <div class="card skillset-card">
                                    <h6>{{ category }}</h6>
                                    <table class="skillsets-table">
                                        <tbody>
                                            <tr v-for="(skills, skillsetName) in skillsBySkillset" :key="skillsetName">
                                                <td>{{ skillsetName }}</td>
                                                <td class="rating-column">
                                                    <div v-for="skill in skills" :key="skill.id">
                                                        <Rating :modelValue="skill.rating" :readonly="true" :cancel="false" v-tooltip="skill.reviewer_name"/> <small v-tooltip="skill.reviewer_name">{{ getInitials(skill.reviewer_email) }}</small>
                                                    </div>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="col-12 lg:col-4">
            <div class="card" v-if="candidateReviews.length">
                <h5>Reviews</h5>
                <Timeline :value="candidateReviews" class="customized-timeline">
                    <template #marker="slotProps">
                        <small class="p-text-secondary">{{ new Date(slotProps.item.review_date).toLocaleDateString() }}</small>
                    </template>
                    <template #content="slotProps">
                        <Card>
                            <template #content>
                                <div class="flex flex-column">
                                    <strong>{{ slotProps.item.interviewer_name }}: <Badge :value="slotProps.item.approved" :severity="slotProps.item.approved === 'Yes' ? 'success' : 'danger'" /></strong>
                                    <div class="review-approval">
                                       
                                       
                                    </div>
                                    <div class="review-observations" >
                                        <a href="#" @click.prevent="toggleObservations(slotProps.item.id)">Show/Hide Details</a>
                                        <div v-if="showObservations[slotProps.item.id]" class="observations">
                                            <strong>{{ slotProps.item.interview }}:</strong>{{ slotProps.item.evaluation_field }}
                                            <div class="review-rating">
                                                <div class="review-interviewer">
                                                    
                                                    <Rating :modelValue="slotProps.item.rating" :readonly="true" :cancel="false" />
                                                </div>
                                            </div>
                                            <p><strong>Observations:</strong> {{ slotProps.item.observations }}</p>
                                            <strong>Interviewer:</strong> {{ slotProps.item.interviewer_name }} ({{ slotProps.item.interviewer_email }})
                                        </div>
                                    </div>
                                </div>
                            </template>
                        </Card>
                    </template>
                </Timeline>
            </div>
        </div>
    </div>



</template>

<style scoped lang="scss">
.grid {
    display: flex;
}

.card {
    width: 100%;
}

ul {
    list-style-type: none;
    padding: 0;
}

pre {
    background-color: #f8f9fa;
    padding: 1rem;
    border-radius: 4px;
    overflow-x: auto;
}

code {
    font-family: 'Courier New', Courier, monospace;
}

.profile-photo {
    max-width: 100px;
    height: auto;
    border-radius: 50%;
}

.skillsets-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 0.5rem;
    table-layout: auto;
}

.skillsets-table th,
.skillsets-table td {
    border: 1px dotted #dddddda5;
    padding: 1px;
    text-align: left;
    white-space: normal;
    word-wrap: break-word;
    vertical-align: top;
}

.skillsets-table th {
    background-color: #f2f2f2;
    font-weight: bold;
}

.skillsets-table .rating-column {
    text-align: right;
    width: 150px;
}

.skillsets-table .skillset-column {
    width: calc(100% - 150px);
}

.skillset-card {
    margin-bottom: 1rem;
}

.skillsets-table .rating-column div {
    display: flex;
    justify-content: flex-end;
    align-items: center;
}

.skillsets-table .rating-column span {
    margin-left: 0.5rem;
    font-weight: bold;
}

/* Add this new CSS to ensure yellow stars */
.p-rating .p-rating-icon {
    color: #FFC107 !important; /* Yellow color */
}



.customized-timeline {
    .p-timeline-event-content {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .p-timeline-event-content .p-card {
        width: 250px;
        max-width: 100%;
    }

    .p-card-content {
        display: flex;
        flex-direction: column;
    }
    .p-card-content {
        display: flex;
        flex-direction: column;
    }

    .observations {
        font-size: 1em;
        margin-top: 0.5rem;
    }

    .p-chip.approved {
        background: #C8E6C9;
        color: #388E3C;
    }

    .p-chip.rejected {
        background: #FFCDD2;
        color: #C62828;
    }
}

.review-rating {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

@media (max-width: 768px) {
    .skillsets-table {
        display: block;
        overflow-x: auto;
        white-space: nowrap;
    }
    .col-12 {
        width: 100% !important;
    }

    .card {
        margin-bottom: 1rem;
    }
    .customized-timeline {
        .p-timeline-event:before {
            top: 0;
            left: 50%;
            transform: translateX(-50%); /* Center the line */
        }
    }
    .candidate-details {
        .p-button {
            margin-bottom: 0.5rem; /* Add space between buttons on mobile */
            width: 100%;            /* Make buttons take full width on mobile */
        }
    }
 

}

.skillsets-container {
    overflow-x: auto;
}

.certification-card {
    margin-bottom: -2rem;
    text-align: left;
}

.certification-card p {
    margin-bottom: 0;
}

.email-icon,
.phone-icon {
    font-size: 1rem;
    margin-right: 0.5rem;
    color: #555;
}

.email-icon:hover,
.phone-icon:hover {
    color: #000;
}

.cv-container {
  margin-top: 1rem;
  display: flex; /* Center the button horizontally */
  justify-content: center; 
}
a {
  color: #4CAF50; // Green color (adjust to your exact shade)
  text-decoration: none;

  &:hover {
    text-decoration: underline;  // Or another hover effect
    color: #5de762;
  }

  &:active {
    color: #51ff5a;   // Darker green when clicked
  }
}
.p-grid {
    margin-left: 0;
    margin-right: 0;
}
.p-grid > .p-col-12 {
    padding-left: 0;
    padding-right: 0;
}
.email-link, .phone-icon, .email-icon {
    margin-left: 5px;
}
</style>