<template>
    <div class="relative bg-surface-0 dark:bg-surface-950 min-h-[70rem]">
        <div class="relative h-[38rem] w-full">
            <div class="absolute inset-0 bg-black/40 dark:bg-black/60 z-10" />
            <img class="w-full h-full object-cover" src="/demo/images/landing/contact-cover.svg" alt="Cover" />
        </div>

        <div class="absolute inset-0 flex flex-col items-center justify-start px-6 lg:px-8 z-30">
            <div class="flex flex-col items-center text-center mt-20 lg:mt-40">
                <h2 class="text-4xl lg:text-5xl font-semibold text-surface-0 leading-tight">Contact Us</h2>
                <p class="mt-4 text-lg lg:text-xl text-surface-0/80 max-w-xl leading-normal">Have questions about CareerPath? We're here to help. Fill out the form below and our team will get back to you shortly.</p>
            </div>

            <div class="w-full lg:max-w-3xl mt-10 lg:mt-16 bg-surface-0 dark:bg-surface-900 rounded-2xl shadow-xl">
                <Toast />
                <div class="p-6 lg:p-8">
                    <div class="flex flex-col gap-6">
                        <div class="flex flex-col md:flex-row gap-6">
                            <span class="p-float-label w-full">
                                <InputText id="first_name" v-model="contact.first_name" type="text" class="w-full" :class="{ 'p-invalid': submitted && !contact.first_name }" />
                                <label for="first_name">First Name</label>
                                <small v-if="submitted && !contact.first_name" class="p-error">First name is required.</small>
                            </span>
                            <span class="p-float-label w-full">
                                <InputText id="last_name" v-model="contact.last_name" type="text" class="w-full" :class="{ 'p-invalid': submitted && !contact.last_name }" />
                                <label for="last_name">Last Name</label>
                                <small v-if="submitted && !contact.last_name" class="p-error">Last name is required.</small>
                            </span>
                        </div>
                        <span class="p-float-label">
                            <InputText id="company" v-model="contact.company" type="text" class="w-full" :class="{ 'p-invalid': submitted && !contact.company }" />
                            <label for="company">Company</label>
                            <small v-if="submitted && !contact.company" class="p-error">Company is required.</small>
                        </span>
                        <span class="p-float-label">
                            <InputText id="email" v-model="contact.email" type="text" class="w-full" :class="{ 'p-invalid': submitted && !isValidEmail(contact.email) }" />
                            <label for="email">Email Address</label>
                            <small v-if="submitted && !contact.email" class="p-error">Email is required.</small>
                            <small v-else-if="submitted && !isValidEmail(contact.email)" class="p-error">Please enter a valid email address.</small>
                        </span>
                        <span class="p-float-label">
                            <Textarea id="message" v-model="contact.message" rows="7" class="w-full" :class="{ 'p-invalid': submitted && !contact.message }" />
                            <label for="message">Message</label>
                            <small v-if="submitted && !contact.message" class="p-error">Message is required.</small>
                        </span>
                        <Button label="Submit" class="w-full" :loading="loading" @click="submitForm" />
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import Button from 'primevue/button';
import InputText from 'primevue/inputtext';
import Textarea from 'primevue/textarea';
import Toast from 'primevue/toast';
import { ref } from 'vue';
import { useToast } from 'primevue/usetoast';

const toast = useToast();
const loading = ref(false);
const submitted = ref(false);

const contact = ref({
    first_name: '',
    last_name: '',
    company: '',
    email: '',
    message: ''
});

// Simple email validation function
const isValidEmail = (email) => {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
};

// Form validation
const validateForm = () => {
    if (!contact.value.first_name || 
        !contact.value.last_name || 
        !contact.value.company || 
        !contact.value.email || 
        !isValidEmail(contact.value.email) || 
        !contact.value.message) {
        return false;
    }
    return true;
};

const submitForm = async () => {
    submitted.value = true;
    
    // Validate form
    if (!validateForm()) {
        toast.add({
            severity: 'error',
            summary: 'Validation Error',
            detail: 'Please fill in all required fields correctly.',
            life: 5000
        });
        return;
    }
    
    loading.value = true;
    
    try {
        const response = await fetch('/core/contact/send', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(contact.value)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            toast.add({
                severity: 'success',
                summary: 'Message Sent',
                detail: 'Thank you for contacting us! We will get back to you soon.',
                life: 5000
            });
            
            // Reset form
            contact.value = {
                first_name: '',
                last_name: '',
                company: '',
                email: '',
                message: ''
            };
            submitted.value = false;
        } else {
            throw new Error(data.detail || 'Something went wrong. Please try again later.');
        }
    } catch (error) {
        toast.add({
            severity: 'error',
            summary: 'Error',
            detail: error.message || 'Something went wrong. Please try again later.',
            life: 5000
        });
    } finally {
        loading.value = false;
    }
};
</script> 