<script setup>
import { ref } from 'vue';
import { useToast } from 'primevue/usetoast';
import axios from 'axios';

const fileInput = ref(null);
const loading = ref(false);
const uploadedUrl = ref(null);
const toast = useToast();

const uploadFile = async () => {
    if (!fileInput.value.files.length) {
        toast.add({ severity: 'warn', summary: 'No File Selected', detail: 'Please select a file to upload.', life: 3000 });
        return;
    }

    const file = fileInput.value.files[0];
    const reader = new FileReader();

    reader.onload = async () => {
        const fileBase64 = reader.result.split(',')[1]; // Get base64 without the prefix
        const folder = 'CVs';
        const email = document.cookie.split('; ').find(row => row.startsWith('userEmail=')).split('=')[1];

        try {
            loading.value = true;
            const response = await axios.post('/api/upload_file_api.php', {
                file: fileBase64,
                folder: folder,
                email: email,
                fileName: file.name,
            });
            uploadedUrl.value = response.data.url;
            toast.add({ severity: 'success', summary: 'Upload Successful', detail: 'File uploaded successfully.', life: 3000 });
        } catch (error) {
            toast.add({ severity: 'error', summary: 'Upload Failed', detail: 'An error occurred during file upload.', life: 3000 });
        } finally {
            loading.value = false;
        }
    };

    reader.readAsDataURL(file);
};
</script>

<template>
    <div class="grid justify-content-center">
        <div class="col-12 md:col-6">
            <div class="card">
                <h5>AWS S3 File Upload</h5>
                <div class="field">
                    <input type="file" ref="fileInput" accept="*" class="w-full" />
                </div>
                <Button label="Upload File" icon="pi pi-upload" @click="uploadFile" :disabled="loading" />
                <ProgressSpinner v-if="loading" style="width: 50px; height: 50px;" strokeWidth="8" fill="#EEEEEE" animationDuration=".5s" />
                <div v-if="uploadedUrl" class="mt-4">
                    <h6>Uploaded File URL:</h6>
                    <a :href="uploadedUrl" target="_blank">{{ uploadedUrl }}</a>
                </div>
            </div>
        </div>
    </div>
</template>