<script setup>
import { ref } from 'vue';

import AppMenuItem from './AppMenuItem.vue';

const model = ref([
    {
        label: 'Home',
        items: [{ label: 'Dashboard', icon: 'pi pi-fw pi-home', to: '/' }]
    },
    {
        label: 'Employees',
        items: [
            

            { label: 'Employee Profile', icon: 'pi pi-fw pi-id-card', to: '/employeeprofile' },

            { label: 'Employee Onboard', icon: 'pi pi-fw pi-check-circle', to: '/employeeonboard' },
            { label: 'AI Training', icon: 'pi pi-fw pi-prime', to: '/employeesaitraining' },
          

        ]
    },
    {
        label: 'Employee Analysis',
        items: [
            
            { label: 'Employees List', icon: 'pi pi-fw pi-users', to: '/employees' },
            { label: 'Employee Reviews', icon: 'pi pi-fw pi-chart-line', to: '/employeesreviews' },
            { label: 'Certifications Matrix', icon: 'pi pi-fw pi-check-circle', to: '/certificationsmatrix' },
            { label: 'Skillsets Matrix', icon: 'pi pi-fw pi-star', to: '/skillsets' },

        ]
    },

    {
        label: 'Candidates',
        items: [
        
            { label: 'Candidates', icon: 'pi pi-fw pi-user-plus', to: '/candidates' },
            { label: 'Candidate Profile', icon: 'pi pi-fw pi-check-circle', to: '/candidatesreviews' },
            { label: 'Selection Workflows', icon: 'pi pi-fw pi-check-square', to: '/jobprocess' },
            { label: 'Job Offers', icon: 'pi pi-fw pi-check-square', to: '/joboffers' },

        ]
    },
    {
        label: 'Administration',
        items: [
        
            { label: 'Admin Dashboard', icon: 'pi pi-fw pi-cog', to: '/admin' },
            { label: 'Skillsets Admin', icon: 'pi pi-fw pi-cog', to: '/skillsetsadmin' },
            { label: 'Certifications Admin', icon: 'pi pi-fw pi-cog', to: '/certificationsadmin' },
            { label: 'Admin Roles', icon: 'pi pi-fw pi-eye', to: '/adminroles' },
        ]
    },



   
    {
        label: 'Get Started',
        items: [
            {
                label: 'Documentation',
                icon: 'pi pi-fw pi-question',
                to: '/documentation'
            }
        ]
    }
]);
</script>

<template>
    <ul class="layout-menu">
        <template v-for="(item, i) in model" :key="item">
            <app-menu-item v-if="!item.separator" :item="item" :index="i"></app-menu-item>
            <li v-if="item.separator" class="menu-separator"></li>
        </template>
    </ul>
</template>

<style lang="scss" scoped></style>
