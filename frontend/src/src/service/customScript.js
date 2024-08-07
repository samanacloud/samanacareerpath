// src/service/customScript.js

import axios from 'axios';
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useToast } from 'primevue/usetoast';

export function useApiFunctions(baseURL) {
    const toast = useToast();
    const apiResponse = ref('');
    const router = useRouter();
    
    const fetchData = async (action, payload = {}) => {
        try {
            const response = await axios.post(`${baseURL}/api/apitest.php`, { action, ...payload });
            return response.data;
        } catch (error) {
            apiResponse.value = 'Error: ' + error.message;
            toast.add({ severity: 'error', summary: 'Error', detail: error.message, life: 3000 });
            throw error;
        }
    };

    const showToast = (severity, summary, detail, life = 3000) => {
        toast.add({ severity, summary, detail, life });
    };

    const validateSession = async () => {
        try {
            const response = await axios.get(`${baseURL}/api/check_session.php`);
            if (!response.data.valid) {
                showToast('warn', 'Session Expired', 'Your session has expired. Redirecting to login page.');
                router.push('/auth/login');
            }
        } catch (error) {
            showToast('error', 'Error', 'Failed to validate session.');
            router.push('/auth/login');
        }
    };

    return {
        apiResponse,
        fetchData,
        showToast,
        validateSession,
    };
}