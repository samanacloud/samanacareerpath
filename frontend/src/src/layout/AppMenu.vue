<script setup>
import { ref } from 'vue';
import { onBeforeMount } from 'vue';
import AppMenuItem from './AppMenuItem.vue';

const admin = ref('');
onBeforeMount(() => {
    admin.value = document.cookie.replace(/(?:(?:^|.*;\s*)admin\s*\=\s*([^;]*).*$)|^.*$/, "$1");
});

const model = ref([]);

onBeforeMount(() => {
    const menuItems = [
        {
            label: 'Home',
            items: [{ label: 'Dashboard', icon: 'pi pi-fw pi-home', to: '/' }]
        },
        {
            label: 'Employees',
            items: [
                { label: 'Employee Profile', icon: 'pi pi-fw pi-id-card', to: '/employeeprofile' },
                { label: 'Employee Onboard', icon: 'pi pi-fw pi-check-circle', to: '/employeeonboard' },
                { label: 'AI Training', icon: 'pi pi-fw pi-prime', to: '/employeesaitraining' }
            ]
        }
    ];

    if (admin.value > 1) {
        menuItems.push(
            {
                label: 'Employee Analysis',
                items: [
                    { label: 'Employees List', icon: 'pi pi-fw pi-users', to: '/employees' },
                    { label: 'Employee Reviews', icon: 'pi pi-fw pi-chart-line', to: '/employeesreviews' },
                    { label: 'Certifications Matrix', icon: 'pi pi-fw pi-check-circle', to: '/certificationsmatrix' },
                    { label: 'Skillsets Matrix', icon: 'pi pi-fw pi-star', to: '/skillsets' }
                ]
            }
        );
    }

    if (admin.value > 2) {
        menuItems.push(
            {
                label: 'Candidates',
                items: [
                    { label: 'Candidates', icon: 'pi pi-fw pi-user-plus', to: '/candidates' },
                    { label: 'Candidate Profile', icon: 'pi pi-fw pi-check-circle', to: '/candidatesreviews' },
                    { label: 'Selection Workflows', icon: 'pi pi-fw pi-check-square', to: '/jobprocess' },
                    { label: 'Job Offers', icon: 'pi pi-fw pi-check-square', to: '/joboffers' }
                ]
            }
        );
    }
    if (admin.value >= 5) {
        menuItems.push({
            label: 'Administration',
            items: [
                { label: 'Admin Dashboard', icon: 'pi pi-fw pi-cog', to: '/admin' },
                { label: 'Skillsets Admin', icon: 'pi pi-fw pi-cog', to: '/skillsetsadmin' },
                { label: 'Certifications Admin', icon: 'pi pi-fw pi-cog', to: '/certificationsadmin' },
                { label: 'Candidates Admin', icon: 'pi pi-fw pi-cog', to: '/candidatesadmin' },
                { label: 'Reviews Admin', icon: 'pi pi-fw pi-chart-line', to: '/reviewsadmin' },
                { label: 'Admin Roles', icon: 'pi pi-fw pi-eye', to: '/adminroles' }
            ]
        });
    }

    menuItems.push({
        label: 'Get Started',
        items: [
            {
                label: 'Documentation',
                icon: 'pi pi-fw pi-question',
                to: '/documentation'
            },
            {
                label: 'Terms of Service',
                icon: 'pi pi-fw pi-verified',
                to: '/terms'
            },
            {
                label: 'Privacy Policy',
                icon: 'pi pi-fw pi-unlock',
                to: '/privacy'
            }

        ]
    });

    model.value = menuItems;
});
</script>

<template>
    <ul class="layout-menu">
        <template v-for="(item, i) in model" :key="item.label">
            <app-menu-item v-if="!item.separator" :item="item" :index="i"></app-menu-item>
            <li v-if="item.separator" class="menu-separator"></li>
        </template>
    </ul>
</template>

<style lang="scss" scoped></style>