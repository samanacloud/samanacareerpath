export default class HealthService {
    constructor(axios) {
        this.axios = axios;
    }

    async checkHealth() {
        try {
            const response = await this.axios.get('/health');
            return {
                isHealthy: response.data.status === 'healthy',
                details: response.data
            };
        } catch (error) {
            return {
                isHealthy: false,
                details: error.response?.data || { 
                    status: 'unhealthy',
                    error: 'Service unavailable'
                }
            };
        }
    }
} 