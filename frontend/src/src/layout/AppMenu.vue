<script setup>
import { ref } from 'vue';

import AppMenuItem from './AppMenuItem.vue';

const model = ref([
    {
        label: 'Home',
        items: [
            { label: 'Dashboard', icon: 'pi pi-fw pi-home', to: '/' }
        ]
    },
    {
        label: 'Employees',
        items: [
            { label: 'Overview', icon: 'pi pi-fw pi-users', to: '/employees' },
          //  { label: 'Profiles', icon: 'pi pi-fw pi-id-card', to: '/employees-profiles' },
          //  { label: 'Reports', icon: 'pi pi-fw pi-chart-bar', to: '/employees-reports' }
        ]
    },
    {
        label: 'Recruitment',
        items: [
            { label: 'Recruitment Leads', icon: 'pi pi-fw pi-briefcase', to: '/recruitment-leads' },
            { label: 'Candidates', icon: 'pi pi-fw pi-user-plus', to: '/candidates' }
         //   { label: 'Profiles', icon: 'pi pi-fw pi-id-card', to: '/candidates-profiles' },
         //   { label: 'Selection Workflows', icon: 'pi pi-fw pi-sitemap', to: '/candidates-workflows' },
            
        ]
    },
    {
        label: 'Administration',
        items: [
          
            { label: 'Users', icon: 'pi pi-fw pi-user', to: '/admin-users' },
            { label: 'Employees', icon: 'pi pi-fw pi-users', to: '/admin-employees' },
            { label: 'Skillsets', icon: 'pi pi-fw pi-star', to: '/admin-skillsets' },
            { label: 'Certifications', icon: 'pi pi-fw pi-check-circle', to: '/admin-certifications' },
            { label: 'Candidates', icon: 'pi pi-fw pi-users', to: '/admin-candidates' }
           
        ]
    },
    {
        label: 'Beta Functions',
        items: [
            { label: 'AI Skillset Assesment', icon: 'pi pi-fw pi-shield', to: '/admin-roles' },
            { label: 'Career Path', icon: 'pi pi-fw pi-sitemap', to: '/admin-careerpath' }
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
