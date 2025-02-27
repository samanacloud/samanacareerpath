import AppLayout from '@/layout/AppLayout.vue';
import { createRouter, createWebHistory } from 'vue-router';
import { ref } from 'vue';
import Candidates from '@/views/careerpath/candidates/Candidates.vue';
import Employees from '@/views/careerpath/employees/Employees.vue';
import EmployeesProfiles from '@/views/careerpath/employees/EmployeesProfiles.vue';
import EmployeesReports from '@/views/careerpath/employees/EmployeesReports.vue';
import CandidatesProfiles from '@/views/careerpath/candidates/CandidatesProfiles.vue';
import SelectionWorkFlows from '@/views/careerpath/candidates/SelectionWorkFlows.vue';
import AdminUsers from '@/views/careerpath/admin/AdminUsers.vue';
import AdminSkillsets from '@/views/careerpath/admin/AdminSkillsets.vue';
import AdminCertifications from '@/views/careerpath/admin/AdminCertifications.vue';
import AdminCandidates from '@/views/careerpath/admin/AdminCandidates.vue';
import AdminRoles from '@/views/careerpath/admin/AdminRoles.vue';
import AdminCareerPath from '@/views/careerpath/admin/AdminCareerPath.vue';
import AdminEmployees from '@/views/careerpath/admin/AdminEmployees.vue';
import RecruitmentLeads from '@/views/careerpath/recruitment/RecruitmentLeads.vue';
import ContactUs from '@/views/pages/ContactUs.vue';
import Landing from '@/views/pages/Landing.vue';

// Define public routes that don't require authentication
const publicRoutes = [
    '/landing',
    '/auth/login',
    '/auth/register',
    '/auth/access',
    '/auth/error',
    '/contact-us'
];

const routes = [
    {
        path: '/',
        component: AppLayout,
        children: [
            {
                path: '/',
                name: 'dashboard',
                component: () => import('@/views/Dashboard.vue'),
                meta: { requiresAuth: true }
            },
            {
                path: '/employees',
                name: 'employees',
                component: Employees,
                meta: { requiresAuth: true }
            },
            {
                path: '/employees-profiles',
                name: 'employees-profiles',
                component: EmployeesProfiles,
                meta: { requiresAuth: true }
            },
            {
                path: '/employees-profiles/:id',
                name: 'employees-profiles-id',
                component: EmployeesProfiles,
                meta: { requiresAuth: true }
            },
            {
                path: '/employees-reports',
                name: 'employees-reports',
                component: EmployeesReports,
                meta: { requiresAuth: true }
            },
            {
                path: '/candidates',
                name: 'candidates',
                component: Candidates,
                meta: { requiresAuth: true }
            },
            {
                path: '/candidates-profiles',
                name: 'candidates-profiles',
                component: CandidatesProfiles,
                meta: { requiresAuth: true }
            },
            {
                path: '/profile/:id',
                name: 'profiles-id',
                component: CandidatesProfiles,
                meta: { requiresAuth: true }
            },
            {
                path: '/candidates-workflows',
                name: 'selection-workflows',
                component: SelectionWorkFlows,
                meta: { requiresAuth: true }
            },
            {
                path: '/recruitment-leads',
                name: 'recruitment-leads',
                component: RecruitmentLeads,
                meta: { requiresAuth: true }
            },
            {
                path: '/admin-users',
                name: 'admin-users',
                component: AdminUsers,
                meta: { requiresAuth: true }
            },
            {
                path: '/admin-skillsets',
                name: 'admin-skillsets',
                component: AdminSkillsets,
                meta: { requiresAuth: true }
            },
            {
                path: '/admin-certifications',
                name: 'admin-certifications',
                component: AdminCertifications,
                meta: { requiresAuth: true }
            },
            {
                path: '/admin-candidates',
                name: 'admin-candidates',
                component: AdminCandidates,
                meta: { requiresAuth: true }
            },
            {
                path: '/admin-employees',
                name: 'admin-employees',
                component: AdminEmployees,
                meta: { requiresAuth: true }
            },
            {
                path: '/admin-roles',
                name: 'admin-roles',
                component: AdminRoles,
                meta: { requiresAuth: true }
            },
            {
                path: '/admin-careerpath',
                name: 'admin-careerpath',
                component: AdminCareerPath,
                meta: { requiresAuth: true }
            }
        ]
    },
    {
        path: '/landing',
        name: 'landing',
        component: Landing
    },
    {
        path: '/contact-us',
        name: 'contact-us',
        component: ContactUs
    },
    {
        path: '/auth/login',
        name: 'login',
        component: () => import('@/views/pages/auth/Login.vue')
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
        path: '/auth/register',
        name: 'register',
        component: () => import('@/views/pages/auth/Register.vue')
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes,
    scrollBehavior() {
        return { left: 0, top: 0 };
    }
});

// Add loading state
const isVerifying = ref(false);

// Add session cache management
const sessionCache = {
    isValid: false,
    lastChecked: 0,
    cacheTimeout: 5 * 60 * 1000, // 5 minutes in milliseconds

    needsValidation() {
        return !this.isValid || (Date.now() - this.lastChecked) > this.cacheTimeout;
    },

    updateCache(isValid) {
        this.isValid = isValid;
        this.lastChecked = Date.now();
    }
};

// Update navigation guard with caching
router.beforeEach(async (to, from, next) => {
    // Skip verification for public routes - use exact path matching
    if (publicRoutes.includes(to.path) || to.path === '/auth/google/callback') {
        return next();
    }

    // Check if we need to validate the session
    if (!sessionCache.needsValidation()) {
        return next();
    }

    // Set loading state
    isVerifying.value = true;

    try {
        const response = await fetch('/core/auth/verify/session', {
            method: 'GET',
            credentials: 'include',
            headers: {
                'Accept': 'application/json',
            }
        });

        if (!response.ok) {
            console.error('Session verification failed for path:', to.path);
            sessionCache.updateCache(false);
            return next('/landing');
        }

        const data = await response.json();
        // Check if we have valid user data in the response
        if (data && data.message === "Session is valid") {
            sessionCache.updateCache(true);
            return next(); // Allow navigation if session is valid
        }

        console.error('Invalid session data:', data);
        sessionCache.updateCache(false);
        return next('/landing');

    } catch (error) {
        console.error('Error verifying session for path:', to.path, error);
        sessionCache.updateCache(false);
        return next('/landing');
    } finally {
        isVerifying.value = false;
    }
});

// Export loading state if needed elsewhere in the app
export { isVerifying };

export default router;
