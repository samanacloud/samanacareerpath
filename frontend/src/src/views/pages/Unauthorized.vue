<template>
    
    <div className="card">
      <div class="unauthorized-container">
        <h1>Unauthorized</h1>
        <p>You do not have permission to access this page.</p>
        <Button label="Go to Dashboard" icon="pi pi-home" @click="goToDashboard" class="p-button-primary" />
    </div>
    </div>
</template>
 


<script setup>
import { useRouter } from 'vue-router';
import Button from 'primevue/button';

const router = useRouter();

const goToDashboard = () => {
    router.push('/');
};
</script>

<style scoped>
.unauthorized-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 30vh;
    text-align: center;
}

.unauthorized-container h1 {
    font-size: 2.5rem;
    margin-bottom: 1rem;
}

.unauthorized-container p {
    font-size: 1.25rem;
    margin-bottom: 2rem;
}
</style>