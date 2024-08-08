import { createRouter, createWebHistory } from 'vue-router';
import AppLayout from '@/layout/AppLayout.vue';
const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            component: AppLayout,
            children: [
                {
                    path: '/',
                    name: 'dashboard',
                    component: () => import('@/views/Dashboard.vue')
                },
                {
                    path: '/test',
                    name: 'test',
                    component: () => import('@/views/pages/Test.vue')
                },
                {
                    path: '/upload',
                    name: 'upload',
                    component: () => import('@/views/pages/upload.vue')
                },
                {
                    path: '/admin',
                    name: 'admin',
                    component: () => import('@/views/pages/Adminpage.vue')
                },
                {
                    path: '/candidates',
                    name: 'candidates',
                    component: () => import('@/views/pages/Candidates.vue')
                },
                {
                    path: '/candidatesreviews',
                    name: 'candidatesreviews',
                    component: () => import('@/views/pages/CandidatesReviews.vue')
                },
                {
                    path: '/employeesreviews',
                    name: 'employeesreviews',
                    component: () => import('@/views/pages/EmployeesReviews.vue')
                },
                {
                    path: '/employeeprofile',
                    name: 'employeeprofile',
                    component: () => import('@/views/pages/EmployeeProfile.vue')
                },
                {
                    path: '/employeeonboard',
                    name: 'employeeonboard',
                    component: () => import('@/views/pages/EmployeeOnboard.vue')

                },
                {
                    path: '/employeesaitraining',
                    name: 'employeesaitraining',
                    component: () => import('@/views/pages/EmployeesAITraining.vue')
                },
                {
                    path: '/certificationsmatrix',
                    name: 'certificationsmatrix',
                    component: () => import('@/views/pages/CertificationsMatrix.vue')
                },
                {
                    path: '/candidateinterview',
                    name: 'candidateinterview',
                    component: () => import('@/views/pages/CandidateInterview.vue')
                },
                {
                    path: '/employees',
                    name: 'employees',
                    component: () => import('@/views/pages/Employees.vue')
                },
                {
                    path: '/skillsets',
                    name: 'skillsets',
                    component: () => import('@/views/pages/Skillsets.vue')
                },

                {
                    path: '/interviews',
                    name: 'interviews',
                    component: () => import('@/views/pages/Interviews.vue')
                },
                {
                    path: '/jobprocess',
                    name: 'jobprocess',
                    component: () => import('@/views/pages/JobProcess.vue')
                },
                {
                    path: '/joboffers',
                    name: 'joboffers',
                    component: () => import('@/views/pages/JobOffers.vue')
                },

                {
                    path: '/skillsets',
                    name: 'skillsets',
                    component: () => import('@/views/pages/Skillsets.vue')
                },
                {
                    path: '/skillsetsadmin',
                    name: 'skillsetsadmin',
                    component: () => import('@/views/pages/SkillsetsAdmin.vue')
                },
                {
                    path: '/reviewsadmin',
                    name: 'reviewsadmin',
                    component: () => import('@/views/pages/ReviewsAdmin.vue')
                },
                {
                    path: '/certificationsadmin',
                    name: 'certificationsadmin',
                    component: () => import('@/views/pages/CertificationsAdmin.vue')
                },
                {
                    path: '/adminroles',
                    name: 'adminroles',
                    component: () => import('@/views/pages/AdminRoles.vue')
                },
                {
                    path: '/unauthorized',
                    name: 'unauthorized',
                    component: () => import('@/views/pages/Unauthorized.vue')
                },
                {
                    path: '/feedback',
                    name: 'feedback',
                    component: () => import('@/views/pages/Feedback.vue')
                },
                {
                    path: '/documentation',
                    name: 'documentation',
                    component: () => import('@/views/utilities/Documentation.vue')
                },
                {
                    path: '/terms',
                    name: 'terms',
                    component: () => import('@/views/pages/TermsOfService.vue')
                },
                {
                    path: '/privacy',
                    name: 'privacy',
                    component: () => import('@/views/pages/Privacy.vue')
                },
            ]
        },
        {
            path: '/landing',
            name: 'landing',
            component: () => import('@/views/pages/Landing.vue')
        },
        {
            path: '/termsofservice',
            name: 'termsofservice',
            component: () => import('@/views/pages/TermsOfService.vue')
        },
        {
            path: '/privacypolicy',
            name: 'privacypolicy',
            component: () => import('@/views/pages/Privacy.vue')
        },
        {
            path: '/notfound',
            name: 'notfound',
            component: () => import('@/views/pages/NotFound.vue')
        },

        {
            path: '/auth/login',
            name: 'login',
            component: () => import('@/views/pages/auth/Login.vue')
        },
        {
            path: '/auth/logout',
            name: 'logout',
            component: () => import('@/views/pages/auth/Logout.vue')
        },

        {
            path: '/auth/access',
            name: 'accessDenied',
            component: () => import('@/views/pages/auth/Access.vue')
        },

        {
            path: '/auth/error',
            name: 'error',
            component: () => import('@/views/pages/auth/Error.vue')
        },
        {
            path: '/test/temployees',
            name: 'temployees',
            component: () => import('@/views/pages/Employees.vue')
        },
        {
            path: '/test/tcandidates',
            name: 'tcandidates',
            component: () => import('@/views/pages/Candidates.vue')
        },
        {
            path: '/test/tcandidatesreviews',
            name: 'tcandidatesreviews',
            component: () => import('@/views/pages/CandidatesReviews.vue')
        },
        {
            path: '/test/temployeesreviews',
            name: 'temployeesreviews',
            component: () => import('@/views/pages/CandidatesReviews.vue')
        },
        {
            path: '/test/tjobprocess',
            name: 'tjobprocess',
            component: () => import('@/views/pages/JobProcess.vue')
        },
        {
            path: '/test/tskillsetsadmin',
            name: 'tskillsetsadmin',
            component: () => import('@/views/pages/SkillsetsAdmin.vue')
        },
        {
            path: '/test/tcertificationsadmin',
            name: 'tcertificationsadmin',
            component: () => import('@/views/pages/CertificationsAdmin.vue')
        },
        
        {
            path: '/test/tcandidateinterview',
            name: 'tcandidateinterview',
            component: () => import('@/views/pages/CandidateInterview.vue')
        },



    ]
});

export default router;
