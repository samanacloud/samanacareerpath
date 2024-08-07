<script>
import ToastService from 'primevue/toastservice';
import Toast from 'primevue/toast';
import ToggleButton from 'primevue/togglebutton';
import Knob from 'primevue/knob';
import { ref, onMounted, watch } from 'vue';
import Button from 'primevue/button';
import { useRouter } from 'vue-router';

export default {
    setup() {
        const router = useRouter();
        
        const goBack = () => {
            router.back();
        };

        return {
            goBack
        };
    },
    data() {
        return {
            showIframe: false,
            iframeUrl: '',
            activeIndex: null,
            progress: 0,
            knotPath: "M 10 10 C 50 50, 150 50, 190 10...", // (Your actual path data here)
            completedTabs: new Set(),
            pathLength: 0,
            stepCompleted: {},
            totalEnrollmentValue: 0,
            enrollments: [], // Array to hold enrollment details
            employeeEmail: '', // To hold the employee's email
            enrollmentPercentage: 0 // For the second Knob
        };
    },
    components: {
        Toast,
        ToggleButton,
        Knob, 
        Button
    },
    provide() {
        return {
            ToastService
        };
    },
    methods: {
        loadIframe(url) {
            this.iframeUrl = url;
            this.showIframe = true;
        },
        onTabChange(index) {
            this.activeIndex = index;
            if (!this.completedTabs.has(index)) {
                this.completedTabs.add(index);
                this.updateProgress();
            }
        },
        updateProgress() {
            this.progress = Math.round((this.completedTabs.size / 13) * 100);
        },
        getPathLength() {
            this.$nextTick(() => {
                const path = this.$el.querySelector('path');
                if (path) { // Ensure the path element exists
                    this.pathLength = path.getTotalLength();
                }
            });
        },
        fetchEmployeeEnrollments() {
            fetch('/api/apitest.php', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    action: 'listEmployeeEnrollment',
                    email: this.employeeEmail
                })
            })
            .then(response => response.json())
            .then(data => {
                this.enrollments = data; // Assign the data to the enrollments array
                if (data && data.length) {
                    data.forEach(enrollment => {
                        this.stepCompleted[enrollment.step] = enrollment.value === 1;

                    });
                }
                this.enrollments = data;
                this.fetchEnrollmentStatus(); // Fetch the knod value
            })
            .catch(error => {
                console.error('Error:', error);
            });
        },
        setEmployeeStep(employeeEmail, step, value) {
            fetch('/api/apitest.php', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    action: 'addEmployeeEnrollment',
                    email: employeeEmail,
                    step: step,
                    value: value
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    this.$refs.toast.add({ severity: 'success', summary: 'Success', detail: `Step ${step} registered successfully`, life: 3000 });
                    this.stepCompleted[step] = value === 1;
                    this.fetchEmployeeEnrollments(); // Refresh the enrollments after adding a new one
                } else if (data.error === 'Duplicate') {
                    this.$refs.toast.add({ severity: 'info', summary: 'Info', detail: 'This step has already been registered', life: 3000 });
                } 
            })
            .catch(error => {
                console.error('Error:', error);
            });
        },
        handleStepToggle(step, isCompleted) {
            this.setEmployeeStep(this.employeeEmail, step, isCompleted ? 1 : 0);
            this.fetchEnrollmentStatus(); // Ensure the second knob updates when toggling steps
        },
        fetchEnrollmentStatus() {
            fetch('/api/apitest.php', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    action: 'getEnrollmentStatus',
                    email: this.employeeEmail
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data && data.percentage) {
                    this.enrollmentPercentage = parseInt(data.percentage.replace('%', ''), 10);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }
    },
    mounted() {
        this.employeeEmail = sessionStorage.getItem('employeeEmail');
        if (!this.employeeEmail) {
            // Handle case where email is not found
        }
        sessionStorage.setItem('employeeEmail', this.employeeEmail);
        this.getPathLength();
        this.fetchEmployeeEnrollments();
        this.fetchEnrollmentStatus(); // Fetch and display the initial enrollment status
    }
};
</script>


<template>
    <div class="grid">
        <div class="col-12 flex">
            <div class="card col-12 flex">
                <div class="card col-8">
                <h4>Samana Group LLC Onboarding Process</h4>
                <p>Welcome to Samana. We are happy to have you as part of our team!<br>
                We have already configured your corporate email account and you should have received an email explaining how to set up your password.<br>
                    <b>Important! :</b>It is a requirement that you store all credentials in our password management tool: 1Password. </p>
                    <Button icon="pi pi-arrow-left" label="Back" @click="goBack"  severity="secondary" outlined class="mb-2 mr-2" />

                </div>
                <div class="card col-4">
                    <h4>Progress</h4>
                   <div class="knob-container">
                      
                    
                        <p><Knob v-model="enrollmentPercentage" valueTemplate="{value}%" :max="100" /></p> <!-- New Knob for enrollment percentage -->
                    </div>
                    
                      
                </div>
      

            </div>
     

        </div>
        <div class="col-12 md:col-6">
            <div class="card">
                <h5>Onboarding Process Steps</h5>
                <Accordion :activeIndex="activeIndex" @tab-change="onTabChange">
                    <AccordionTab header="1. Cybersecurity Training Courses (est. 2 hours)"@click="onTabChange(1)">
                        <p class="line-height-3 m-0">
                            New employees are required to take four cybersecurity training courses and pass the corresponding exams. <br>To learn more about these courses, log in to the following link using your corporate email account.<br>
                           
                            <li><a href="https://sites.google.com/samanagroup.co/training-plans/cybersecurity-training-plan" target="_blank"> Cybersecurity training courses</a></li>
                            
                            <p>
                               <u>Mark this checkbox once you complete this step: </u>   <input type="checkbox" v-model="stepCompleted[1]" @change="handleStepToggle(1, stepCompleted[1])"  />
                            </p>
                        </p>
                    </AccordionTab>
                    <AccordionTab header="2. Samana Group Shared Desktop (est. 15 minutes)"@click="onTabChange(2)">
                        <p class="line-height-3 m-0">
                            Access to our clients environments is via the Samana Group Shared Desktop.  To access this Desktop, follow these steps:
                            Go to this <a href="https://citrix.samana.cloud" target="_blank">link</a>. (To avoid any authentication issues, be sure to use a different web browser than the one you logged into with your personal email account).
                            Authentication is with your corporate email account.
                           <ul>
                            <li>Click on the DESKTOP icon located in the top banner of the application.</li>
                            <li>Click on the "Samana Desktop New" icon. It may be necessary to install the Citrix WorkSpace App.  If the Citrix Workspace App download does not work, you can download it from this <a href="https://www.citrix.com/downloads/workspace-app/"target="_blank">link</a>. It might be necessary to restart your device and repeat the process by accessing the Samana Group Shared Desktop URL.</li>
                            <li>Fill in the following form to confirm you successfully accessed the Samana Desktop: <Button label="Shared Desktop Confirmation form" @click="loadIframe('https://docs.google.com/forms/d/e/1FAIpQLSeHqOIth1ddhvX_OknJYEuazPBD0nYE1l-mr_cUYLk4Tih9Kg/viewform?usp=sf_link ')" /></li>
                        </ul>
                             <p>
                               <u>Mark this checkbox once you complete this step: </u>   <input type="checkbox" v-model="stepCompleted[2]" @change="handleStepToggle(2, stepCompleted[2])" />
                            </p>

                        </p> 
                    </AccordionTab>
                    <AccordionTab header="3. 1Password (est. 15 minutes)"@click="onTabChange(3)">
                        <p class="line-height-3 m-0">
                            1Password is Samana's password management tool. It is a company requirement to take this course. <br>  You can log in to this course with your corporate email account.<br>
                            <a href="https://docs.google.com/presentation/d/e/2PACX-1vR3G2hwHR3OS7kOvsVaDdMkw-iegR-b86IUUmQ7ZcGmC-sqo0VIVvhFHg362fiuAQ/pub?start=false&loop=false&delayms=3000" target="_blank">1Password Training Course</a> <br>
                            When you have completed the training course, please fill in this form:                         
                            <p><Button label="1Password training course confirmation" @click="loadIframe('https://docs.google.com/forms/d/e/1FAIpQLSdJ45x4kOo0NLx9em5miZ5dKgrao3uiecZtDKEV4lo8HMBJmQ/viewform?usp=sf_link ')" /></p>
                            After confirming you have completed the course,  you will receive an invitation to join 1Password.<br>
                            <strong>Please only continue with the following steps after you have access to 1Password.</strong>
                        </p>
                        <p>
                               <u>Mark this checkbox once you complete this step: </u>   <input type="checkbox" v-model="stepCompleted[3]" @change="handleStepToggle(3, stepCompleted[3])" />
                            </p>

                    </AccordionTab>
                    <AccordionTab header="4. Slack (est. 15 minutes)"@click="onTabChange(4)">
                        <p class="line-height-3 m-0">
                            You will be sent an invitation to join Slack, a corporate messaging service used to chat with our teammates and some clients.<br>
                            <strong>Please only continue with the following steps after you have access to Slack.</strong>
                        </p>
                        <p>
                               <u>Mark this checkbox once you complete this step: </u>   <input type="checkbox" v-model="stepCompleted[4]" @change="handleStepToggle(4, stepCompleted[4])" />
                            </p>

                    </AccordionTab>
                    <AccordionTab header="5. Core Values Presentation (est. 15 minutes)"@click="onTabChange(5)">
                        <p class="line-height-3 m-0">
                            The following is our Company Core Values presentation.  In order to watch this presentation, you will need to log in to the following link using your corporate email account.<br>
                            <li><a href="https://docs.google.com/presentation/d/e/2PACX-1vQ5V5188ZVBhaxj3q-ctj0T0hLDQToYPq3Y0CozIeSFCvJgTz6wG1LU1lGTU6Wasg/pub?start=false&loop=false&delayms=3000">Core Values Presentation </a></li>
                                                      
                        </p>
                        <p>
                               <u>Mark this checkbox once you complete this step: </u>   <input type="checkbox" v-model="stepCompleted[5]" @change="handleStepToggle(5, stepCompleted[5])" />
                            </p>

                    </AccordionTab>
                    <AccordionTab header="6. Corporate Policies (est. 30 minutes)"@click="onTabChange(6)">
                        <p class="line-height-3 m-0">
                            The following is our Corporate Policies presentation.  In order to watch this presentation, you will need to log in to the following link using your corporate email account.
                            <li><a href="https://docs.google.com/presentation/d/e/2PACX-1vQBP1_JMT9UqXPpLSW1p1346kKdOjb4Iouxvs-1BuRjHLVudJ6QdWgheo-FmSXgag/pub?start=false&loop=false&delayms=3000" target="_blank">Corporate Policies Presentation </a></li>
                            <li>It is mandatory to read the Corporate Policies.  To access the policies visit:  <a href="https://sites.google.com/samanagroup.co/intranet/corporate/policies" target="_blank">Policies.</a></li>
                            <li>Please confirm you have read the Corporate Policies and the presentation by filling in this form: </li>
                            <Button label=" Corotate Policies confirmation." @click="loadIframe('https://docs.google.com/forms/d/e/1FAIpQLSeaZqom2q_sDXI57MDyOTouTTErDGbiPFngHhWakXm8GTGk2A/viewform?usp=sf_link ')" />
                        </p>
                        <p>
                               <u>Mark this checkbox once you complete this step: </u>   <input type="checkbox" v-model="stepCompleted[6]" @change="handleStepToggle(6, stepCompleted[6])" />
                            </p>

                    </AccordionTab>
                    <AccordionTab header="7. Skype Phone Number (est. 15 minutes)"@click="onTabChange(7)">
                        <p class="line-height-3 m-0">
                            All resources residing outside the US will need to procure a phone number via Skype with a <b>US based area code</b> (preferably 305, 786, or 954).<br> This cost will be reimbursed on a monthly basis. All resources must install skype on their laptop and cellphone.<br>
                            To request your Skype phone number, proceed only with steps 1 to 4: 
                            <ol>
                            <li>Open Skype (using your personal Skype account) and click on the options button (...) </li>
                            <li>Go to settings</li>
                            <li>Click on the "Skype number" option</li>
                            <li>Click on get Skype number, and follow the onscreen instructions.<br><Image :src="'https://lh5.googleusercontent.com/OYlCaHjFAkGNWsVzrD_TvGPitPIxiHU4y_TV1ZDk6pg27kU2gpinxo77TX0k2lodvjqBu1jB8VFpgIL6jT9kOG_VklFg5wo8rRlXv1ThYG9T9OXS_ELYtGXsWD6TeqmxZg=w1280'" alt="Image" width="100%" preview /></li>
                            
                            
                           <li> If your role requires you to call US numbers (confirm with your SDM), you should procure a Skype plan for international calls <a href="https://secure.skype.com/en/offers/calling?offerHref=%2Foffers%2Fcalling%2Fskus%2Fus-mixed-unlimited%3Frevision%3D1.0%26pricetierRevision%3D2.0%26language%3Den-us%26currency%3DUSD%26billingCountry%3DCO%26d-promo-trial%3D1-month-free%26strategy%3Dcheapest&cancelUrl=https%3A%2F%2Fwww.skype.com%2Fen%2Finternational-calls%2F" target="_blank">here</a>. </li>
                           <li>Choose the 1-month free trial, and you will be charged monthly afterward. This cost will be reimbursed monthly. <i>This step does not need to be completed in the onboarding process, as authorization from your SDM is required.</i></li> 
                           <li>Please confirm you have gotten your Skype number by filling out this form:  
                            <Button label=" Skype phone number confirmation." @click="loadIframe('https://forms.gle/gBC1JvtoauqpQhrr8')" /></li> 
                           
                            <b>Please only continue with the following steps after configuring your US-based Skype number.</b>
                        </ol>
                        </p>
                        <p>
                               <u>Mark this checkbox once you complete this step: </u>   <input type="checkbox" v-model="stepCompleted[7]" @change="handleStepToggle(7, stepCompleted[7])" />
                            </p>

                    </AccordionTab>
                    <AccordionTab header="8. Podio (est. 15 minutes)"@click="onTabChange(8)">
                        <p class="line-height-3 m-0">
                            You will be sent an invitation to join Podio, an application where the SDMs schedule work hours.<br>
                            After joining Podio, please edit your profile and add your Skype phone number, including your country area code (e.g. +1).                       
                            <b>Please only continue with the following steps after configuring your US-based phone number in Podio.</b>
                            <img src="https://lh3.googleusercontent.com/ozkG9LFuiqDu1NsXkggIZ7kdNUM6ecrbkWdqc4yNLrPWUE6Jmcb90zbkbzhpn15jpFZ7o_oAZzJM5HxtnljYToNIUj2e5O5nZSoVNz5SbivV4cLkQsWBzFfBGOJvIpqQLw=w1280" alt="Image" width="100%" />
                    

                        </p>
                        <p>
                               <u>Mark this checkbox once you complete this step: </u>   <input type="checkbox" v-model="stepCompleted[8]" @change="handleStepToggle(8, stepCompleted[8])" />
                            </p>

                    </AccordionTab>
                    <AccordionTab header="9. Quickbooks (est. 15 minutes)"@click="onTabChange(9)">
                        <p class="line-height-3 m-0">
                            <b>Note:</b><u>This step does not apply to Sales Representative or Service Delivery Director.</u><br>
                            QuickBooks is Samana Group’s time-tracking application, and it is a company requirement to take the QuickBooks training course.<br> To be able to log in to the course, you will need to use your corporate email account.<br>
                             <a href="https://docs.google.com/presentation/d/e/2PACX-1vS8SKR8SlFDKdXW9DcK5W7MPhe2ZB_JZuwH_n4XjxMi3yjDfrvqHxHRDhvQIyZsbw/pub?start=false&loop=false&delayms=3000" target="_blank">Quickbooks Training Course</a><br>
                            Confirm you have finished the training course by filling out the following form:  
                            <Button label=" Bring Your Own Device Survey" @click="loadIframe('https://docs.google.com/forms/d/e/1FAIpQLSdBQ8mGspsflQWWkbqG6J0AnnGcv6N0b-XcT4UQgOrwS0g_GQ/viewform?usp=sf_link')" />
                        
                        </p>
                        <p>
                               <u>Mark this checkbox once you complete this step: </u>  <input type="checkbox" v-model="stepCompleted[9]" @change="handleStepToggle(9, stepCompleted[9])" />
                            </p>

                    </AccordionTab>
                    <AccordionTab header="10. Licensing Requirements (est. 15 minutes)"@click="onTabChange(10)">
                        <p class="line-height-3 m-0">
                            Samana Group allows employees to use their own computers, smartphones, or other devices, for work purposes.<br>
                            Please fill out the following survey to identify your licensing and home office upgrade requirements:
                            
                            <Button label=" Bring Your Own Device Survey" @click="loadIframe('https://docs.google.com/forms/d/e/1FAIpQLScQzgTwYM9_An2l7Hz1X5LKgONh_SbHjXoczv2LfQhJR5t-ZQ/viewform?usp=sf_link')" />
                        </p>
                        <p>
                               <u>Mark this checkbox once you complete this step: </u>   <input type="checkbox" v-model="stepCompleted[10]" @change="handleStepToggle(10, stepCompleted[10])" />
                            </p>
                    </AccordionTab>
                    <AccordionTab header="11. Additional Information (est. 1 hour)"@click="onTabChange(11)">
                        <p class="line-height-3 m-0">
                             <li><a href="https://sites.google.com/samanagroup.co/intranet/corporate/benefits" target="_blank">Benefits</a></li> 
                             <li> <a href="https://sites.google.com/samanagroup.co/intranet" target="_blank">Intranet </a>   </li>              
                             <li><a href="https://sites.google.com/samanagroup.co/kbd/" target="_blank">Knowledge base. </a></li>
                            
                        </p>
                        <p>
                               <u>Mark this checkbox once you complete this step: </u>   <input type="checkbox" v-model="stepCompleted[11]" @change="handleStepToggle(11, stepCompleted[11])" />
                            </p>

                    </AccordionTab>
                    <AccordionTab header="12. Onboarding Process Survey (est. 15 minutes)"@click="onTabChange(12)">
                        <p class="line-height-3 m-0">
                            Your opinion about the onboarding process will help us to improve. It is mandatory to fill out the Onboarding Process Survey.
                            <Button label="Survey" @click="loadIframe('https://docs.google.com/forms/d/e/1FAIpQLSdBuVBanqrquNLorlPbxvuSh72UXlQEzTRlIwuFK9hAS6O_0A/viewform?usp=sf_link')" />

                        </p>
                        <p>
                               <u>Mark this checkbox once you complete this step: </u>   <input type="checkbox" v-model="stepCompleted[12]" @change="handleStepToggle(12, stepCompleted[12])" />
                            </p>
                    </AccordionTab>
                    <AccordionTab header="13. Next Steps"@click="onTabChange(13)">
                        <p class="line-height-3 m-0">
                            The following steps will be completed in the following days:
                            <ul>
                            <li>Schedule a meeting with your Service Delivery Manager</li>
                            <li> Work with your Service Delivery Manager to request customer accounts</li>
                            <li>Schedule a meeting with your Service Delivery Architect to review the training plan and define the certification path and goals</li>
                            <li>Schedule a meeting with Fernando Marin to create your QuickBooks account and go over the invoicing process</li></ul>
                        </p>
                        <p>
                               <u>Mark this checkbox once you complete this step: </u>   <input type="checkbox" v-model="stepCompleted[13]" @change="handleStepToggle(13, stepCompleted[13])" />
                            </p>
                    </AccordionTab>
                </Accordion>
            </div>
  
        </div>
        <div class="col-12 md:col-6">
        
      
            <Card>
                <template v-slot:title>
                    <div class="flex align-items-center justify-content-between mb-0">
                        <h5>Forms</h5>
                     
                    </div>
                  
                </template>

                <template v-slot:content>
                    <iframe v-if="showIframe" :src="iframeUrl" width="100%" height="600px" frameborder="0"></iframe>
                    <p v-else class="line-height-3 m-0">
                        No form selected.
                    </p>
                </template>
            </Card>
        </div>

     

<Toast ref="toast" />  
    </div>
  

</template>
<style lang="scss" scoped>

.p-grid .p-col-12.p-flex .p-card { /* Assuming you're using PrimeVue classes */
  display: flex; 
  flex-direction: column; 
  min-height: 100%; 
}

.p-grid .p-col-12.p-flex .p-card > * { 
  flex: 1;
}
.knob-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%; /* Adjust this value as needed */
}

</style>