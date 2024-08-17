<script setup>
import { ref, onBeforeMount, computed } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import InputText from 'primevue/inputtext';
import Calendar from 'primevue/calendar';
import Button from 'primevue/button';
import { useToast } from 'primevue/usetoast';
import { useConfirm } from "primevue/useconfirm";
import Timeline from 'primevue/timeline';
import Card from 'primevue/card';
import { uploadToAWSS3 } from '@/service/customScript';


//redirects to unauthorized if the user role is lower than the pagerole
import { getPageAuthorization } from '@/utils/utils';
const pageRole = 1; // Set the required role for this page
getPageAuthorization(pageRole);




const baseURL = import.meta.env.VITE_SITE_URL 
    ? `https://${import.meta.env.VITE_SITE_URL}` 
    : 'http://localhost:8080';

    
const router = useRouter();
const enrollmentPercentage = ref(null); // New ref to store enrollment percentage
const toast = useToast();
const employeeEmail = ref(sessionStorage.getItem('employeeEmail'));
const employee = ref({});
const originalEmployee = ref({});
const defaultProfileImage = ref('/public/samana-logo-blue.png');
const loading = ref(true);
const isEdit = ref(false);
const certifications = ref([]);
const showCertificationDialog = ref(false);
const allCertifications = ref([]);
const employeeReviews = ref([]);
const showObservations = ref({});

const getEmployeeDetails = async () => {
    try {
        const response = await axios.post(`${baseURL}/api/apitest.php`, {
            action: 'getEmployee',
            email: employeeEmail.value
        });
        employee.value = response.data;
        originalEmployee.value = { ...response.data };
        console.log(response.data);
    } catch (error) {
        console.error('Error fetching employee details:', error.message);
    } finally {
        loading.value = false;
    }
};

const toggleObservations = (reviewId) => {
    showObservations.value[reviewId] = !showObservations.value[reviewId];
};

const getEmployeeReviews = async (email) => {
    try {
        const response = await axios.post(`${baseURL}/api/apitest.php`, {
            action: 'listPublicEmployeeReviews',
            email
        });
        const reviews = response.data;

        for (const review of reviews) {
            const reviewerResponse = await axios.post(`${baseURL}/api/apitest.php`, {
                action: 'getReviewerName',
                email: review.reviewer_email
            });
            review.reviewer_name = reviewerResponse.data.name || 'Unknown';
           
        }

        employeeReviews.value = reviews;
    } catch (error) {
        console.error('Error fetching employee reviews:', error);
    }
};

// Function to fetch enrollment status
const fetchEnrollmentStatus = async () => {
    try {
        const response = await axios.post(`${baseURL}/api/apitest.php`, {
            action: 'getEnrollmentStatus',
            email: employeeEmail.value
        });
        if (response.data && response.data.percentage) {
            enrollmentPercentage.value = parseInt(response.data.percentage.replace('%', ''), 10);
        }
    } catch (error) {
        console.error('Error fetching enrollment status:', error.message);
    }
};



const updateEmployeeProfile = async () => {
    try {
        const response = await axios.post(`${baseURL}/api/apitest.php`, {
            action: 'updateEmployee',
            ...employee.value
        });
        if (response.data.success) {
            toast.add({ severity: 'success', summary: 'Success', detail: 'Employee updated successfully', life: 3000 });
            isEdit.value = false;
            originalEmployee.value = { ...employee.value };
        } else {
            toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to update employee', life: 3000  });
        }
    } catch (error) {
        console.error('Error updating employee profile:', error.message);
        toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to update employee', life: 3000  });
    }
};

const cancelEdit = () => {
    employee.value = { ...originalEmployee.value };
    isEdit.value = false;
};

const goBack = () => {
    router.back();
};

const onboardProcess = () => {
    sessionStorage.setItem('employeeEmail', employee.value.primaryEmail); // Use employee.value
    router.push({
        name: 'employeeonboard' // Assuming you have this route name
    });
};

const aiTraining = () => {
    sessionStorage.setItem('employeeEmail', employee.value.primaryEmail); // Use employee.value
    router.push({
        name: 'employeesaitraining' 
    });
};


const getEmployeeCertifications = async () => {
    try {
        const response = await axios.post(`${baseURL}/api/apitest.php`, {
            action: 'listEmployeeCertifications',
            email: employeeEmail.value
        });
        certifications.value = response.data;
        console.log(response.data);
    } catch (error) {
        console.error('Error fetching employee certifications:', error.message);
    }
};

onBeforeMount(() => {
    getEmployeeDetails();
    getEmployeeCertifications();
    getAllCertifications();
    fetchEnrollmentStatus(); // Fetch the enrollment status on mount
    getEmployeeReviews(employeeEmail.value); // Fetch the employee reviews on mount
    

});

const calculateDuration = (creationDate) => {
    const today = new Date();
    const creation = new Date(creationDate);
    let years = today.getFullYear() - creation.getFullYear();
    let months = today.getMonth() - creation.getMonth();

    if (months < 0) {
        years--;
        months += 12;
    }

    return `${years} years and ${months} months`;
};

// Fetch all certifications
const getAllCertifications = async () => {
    try {
        const response = await axios.post(`${baseURL}/api/apitest.php`, {
            action: 'listCertifications'
        });
        allCertifications.value = response.data;
    } catch (error) {
        console.error('Error fetching certifications:', error.message);
    }
};

// Add certification to employee
const addCertificationToEmployee = async (certification) => {
    try {
        const response = await axios.post(`${baseURL}/api/apitest.php`, {
            action: 'addEmployeeCertification',
            email: employee.value.primaryEmail,
            certification: certification.certification,
            date: new Date().toISOString().split('T')[0] // Current date in YYYY-MM-DD format
        });
        if (response.data.success) {
            toast.add({ severity: 'success', summary: 'Success', detail: 'Certification added successfully', life: 3000  });
            getEmployeeCertifications(); // Refresh certifications

            // Optionally, refresh the list of employee certifications here
        } else {
            toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to add certification', life: 3000  });
        }
    } catch (error) {
        console.error('Error adding certification:', error.message);
        toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to add certification', life: 3000  });
    }
};



const durationSinceCreation = computed(() => calculateDuration(employee.value.creationDate));

// Search certifications
const searchQuery = ref('');

const filteredCertifications = computed(() => {
    if (searchQuery.value.trim() === '') {
        return allCertifications.value;
    }
    return allCertifications.value.filter(cert => 
        cert.certification.toLowerCase().includes(searchQuery.value.toLowerCase())
    );
});
const confirm = useConfirm(); 

const deleteCertification = async (certificationId) => {
    confirm.require({
        message: 'Are you sure you want to delete this certification?',
        header: 'Confirmation',
        icon: 'pi pi-exclamation-triangle',
        accept: async () => { // Use async here
            try {
                const response = await axios.post(`${baseURL}/api/apitest.php`, {
                    action: 'deleteEmployeeCertification',
                    id: certificationId
                });
                if (response.data.success) {
                    toast.add({ severity: 'success', summary: 'Success', detail: 'Certification deleted successfully', life: 3000  });
                    
                    getEmployeeCertifications(); 
                } else {
                    toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to delete certification', life: 3000  });
                }
            } catch (error) {
                console.error('Error deleting certification:', error.message);
                toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to delete certification', life: 3000  });
            }
        },
        reject: () => {
            // Do nothing, or potentially add feedback for cancellation
        }
    });
};

// function to update the profile picture and upload it to AWS S3
const loadingProfilePhoto = ref(false);

const onUploadProfilePhoto = async (event) => {
    const file = event.files[0];
    if (!file) {
        toast.add({ severity: 'warn', summary: 'No File Selected', detail: 'Please select a file to upload.', life: 3000 });
        return;
    }

    loadingProfilePhoto.value = true;

    const result = await uploadToAWSS3(file, 'images', employee.value.primaryEmail);

    loadingProfilePhoto.value = false;

    if (result && result.success) {
        employee.value.thumbnailPhotoURL = result.url; // Update the employee's photo URL
        toast.add({ severity: 'success', summary: 'Upload Successful', detail: 'Profile photo uploaded successfully.', life: 3000 });
    } else {
        toast.add({ severity: 'error', summary: 'Upload Failed', detail: result.message, life: 3000 });
    }
};
</script>

<template>
    <div class="grid">
        <div class="col-12 lg:col-8">
            <div class="card">
               <h5>Employee Profile</h5>
                <div v-if="!loading">
                    <div v-if="isEdit">
                        <div class="field">
                            <label for="primaryEmail">Primary Email</label>
                            <InputText id="primaryEmail" v-model="employee.primaryEmail" disabled />
                        </div>
                        <div class="field">
                            <label for="recoveryEmail">Recovery Email</label>
                            <InputText id="recoveryEmail" v-model="employee.recoveryEmail" />
                        </div>
                        <div class="field">
                            <label for="fullName">Full Name</label>
                            <InputText id="fullName" v-model="employee.fullName" />
                        </div>
                        <div class="field">
                            <label for="phone_mobile">Phone Mobile</label>
                            <InputText id="phone_mobile" v-model="employee.phone_mobile" />
                        </div>
                        <div class="field">
                            <label for="thumbnailPhotoURL">Profile Photo</label>
                            <img :src="employee.thumbnailPhotoURL || defaultProfileImage" alt="Profile Photo" class="profile-photo" />
                            <FileUpload 
                                mode="basic" 
                                name="profile_photo" 
                                accept="image/*" 
                                :maxFileSize="5000000" 
                                @select="(event) => onUploadProfilePhoto(event)" 
                                customUpload 
                                chooseLabel="Upload Photo"
                            />
                            <ProgressSpinner v-if="loadingProfilePhoto" style="width: 40px; height: 40px;" strokeWidth="8" fill="#EEEEEE" animationDuration=".5s" />
                        </div>
                        <div class="field">
                            <label for="companyRole">Company Role</label>
                            <InputText id="companyRole" v-model="employee.companyRole" disabled />
                        </div>
                        <div class="field">
                            <label for="contractType">Contract Type</label>
                            <InputText id="contractType" v-model="employee.contractType" disabled />
                        </div>
                        <div class="field">
                            <label for="suspended">Suspended</label>
                            <InputText id="suspended" v-model="employee.suspended" disabled />
                        </div>
                        <div class="field">
                            <label for="creationDate">Creation Date</label>
                            <Calendar id="creationDate" v-model="employee.creationDate" dateFormat="yy-mm-dd" disabled />
                            <p>{{ durationSinceCreation }}</p>
                        </div>
                        <Button label="Cancel" severity="danger" icon="pi pi-times"  @click="cancelEdit"  outlined class="mb-2 mr-2"   />
                        <Button label="Update Employee" icon="pi pi-check" @click="updateEmployeeProfile" outlined class="mb-2 mr-2" severity="success" />
                    </div>
                    <div v-else>
                        <div class="card-content"> 
                            <div class="photo-section">
                                <img :src="employee.thumbnailPhotoURL || defaultProfileImage" alt="Profile Photo" class="profile-photo" />
                            </div>
                            <div class="details-section">
                                <h4>{{ employee.fullName }}</h4>
                                {{ employee.companyRole }} - [{{ employee.contractType }}]<br>
                                <em><i class="pi pi-envelope email-icon"></i>{{ employee.primaryEmail }}</em><br>
                                <em><i class="pi pi-envelope email-icon"></i>{{ employee.recoveryEmail }}</em><br>
                                <i class="pi pi-whatsapp phone-icon"></i>{{ employee.phone_mobile }}<br>
                                <div v-if="enrollmentPercentage !== null">
                                    <i class="pi pi-check-circle"></i> Enrollment Status: {{ enrollmentPercentage }}%
                                </div>
                                                                
                                <p>Employee Since {{ durationSinceCreation }}</p><br>
                            </div>
                        </div>
                        <Button icon="pi pi-arrow-left" label="Back" @click="goBack"  severity="secondary" outlined class="mb-2 mr-2" />
                        <Button icon="pi pi-pencil"  label="Update Profile" outlined class="mb-2 mr-2" @click="isEdit = true" />
                        <Button icon="pi pi-plus" label="Add Certifications" @click="showCertificationDialog = true" severity="warning" outlined class="mb-2 mr-2" />
                        <Button icon="pi pi-user-plus" label="Onboard Process" @click="onboardProcess"  severity="help" outlined class="mb-2 mr-2" />
                        <Button icon="pi pi-prime" label="AI Training" @click="aiTraining"  severity="info" outlined class="mb-2 mr-2" />
                    </div>
                </div>
                <div v-else>
                    <p>Loading...</p>
                </div>
            </div>

            <div class="card">
               
                <DataTable :value="certifications" v-if="certifications.length">
                    <Column field="certification" header="Certifications"></Column>
                    <Column headerStyle="width: 4rem; text-align: center" bodyStyle="text-align: center">
                        <template #body="{data}">
                            <Button 
                                v-if="data.id" 
                                icon="pi pi-trash"
                                severity="danger"
                               text raised  class="mb-2 mr-2"
                                @click="deleteCertification(data.id)"
                            />
                        </template>
                    </Column>
                </DataTable>
                <div v-else>
                    <p>No certifications found for the specified email</p>
                </div>
            </div>
        </div>
        <div class="col-12 lg:col-4"> 
          
            <div class="card">
                <h5>Employee Reviews</h5>
                <Timeline :value="employeeReviews" class="customized-timeline">
                    <template #marker="slotProps">
                        <small class="p-text-secondary">{{ new Date(slotProps.item.date).toLocaleDateString() }}</small>
                    </template>
                    <template #content="slotProps">
                        <Card>
                            <template #content>
                                <div class="flex flex-column">
                                    <strong>{{ slotProps.item.evaluation_field }}</strong>
                                    <div class="review-rating">
                                        <div class="review-interviewer">
                                            <Rating :modelValue="slotProps.item.rating" :readonly="true" :cancel="false" />
                                        </div>
                                    </div>
                                    <div class="review-observations">
                                        <a href="#" @click.prevent="toggleObservations(slotProps.item.id)">Show/Hide Details</a>
                                        <div v-if="showObservations[slotProps.item.id]" class="observations">
                                            <p><strong>Observations:</strong> {{ slotProps.item.observations }}</p>
                                            <strong>Reviewer:</strong> {{ slotProps.item.reviewer_name }} ({{ slotProps.item.reviewer_email }})
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
    <Dialog header="Add Certifications" v-model:visible="showCertificationDialog" :modal="true" :style="{ width: '50vw' }" :closable="true">
        <div class="p-fluid">
            <InputText type="text" v-model="searchQuery" placeholder="Search certifications..." />

            <DataTable :value="filteredCertifications" class="p-datatable-gridlines">
                <Column field="certification" header="Certification"></Column>
                <Column header="Actions" bodyStyle="text-align: center">
                    <template #body="slotProps">
                        <Button 
                            icon="pi pi-plus" 
                           text raised  class="mb-2 mr-2"
                            @click="addCertificationToEmployee(slotProps.data)" 
                        />
                    </template>
                </Column>
            </DataTable>
        </div>
    </Dialog>
    <ConfirmDialog />
</template>

<style scoped>
.profile-photo {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    object-fit: cover;
   
    vertical-align: top;
}
.card-content {
    display: flex;
    align-items: center;
    position: relative;
}

.photo-section {
    flex: 1;
    text-align: center;
}

.details-section {
    flex: 2;
    padding-left: 20px;
    position: relative;
}

.certification-card {
    display: flex; /* Use flexbox for easy alignment */
    align-items: center;  /* Vertically center the items */
}

.certification-name {
    margin-right: 0.5rem; /* Add some space between the name and button */
}


.certification-card .p-button .pi-times {
    font-size: 8px; 
}
</style>

