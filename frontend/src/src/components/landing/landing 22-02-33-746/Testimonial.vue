<script setup>
import TestimonialCard from '@/components/landing/TestimonialCard.vue';
import { ref } from 'vue';

const testimonial1 = ref([
    {
        avatar: '/demo/images/avatar/avatar-f-1.png',
        name: 'Sarah Chen',
        title: 'Project Director, Global Tech Solutions',
        message: 'TimeBandit transformed how we manage global projects. The multi-currency support and compliance features are game-changers for our international teams. We\'ve reduced reporting time by 60%.'
    },
    {
        avatar: '/demo/images/avatar/avatar-m-2.png',
        name: 'Michael Rodriguez',
        title: 'Technical Lead, Innovate Systems',
        message: 'The automated reporting saves us hours each week. Our team loves how easy it is to track time, and the burn rate analytics have helped us stay within budget consistently.'
    },
    {
        avatar: '/demo/images/avatar/avatar-f-4.png',
        name: 'Lisa Johnson',
        title: 'PMO Director, Enterprise Solutions',
        message: 'Managing multiple projects across different time zones was a nightmare before TimeBandit. Now we have real-time visibility into resource allocation and project progress.'
    },
    {
        avatar: '/demo/images/avatar/avatar-m-3.png',
        name: 'David Chang',
        title: 'Resource Manager, Tech Innovations',
        message: 'The resource utilization dashboard is brilliant. We\'ve optimized our team allocation and improved project delivery times by 40% since implementing TimeBandit.'
    },
    {
        avatar: '/demo/images/avatar/avatar-f-6.png',
        name: 'Maria Garcia',
        title: 'Senior Project Manager',
        message: 'Integration with Expensify has streamlined our expense tracking. The multi-currency support is perfect for our international projects.'
    }
]);

const testimonial2 = ref([
    {
        avatar: '/demo/images/avatar/avatar-f-5.png',
        name: 'Emma Thompson',
        title: 'Resource Director, Digital Agency',
        message: 'The resource utilization analytics helped us optimize team allocation and improve project profitability by 25%. TimeBandit pays for itself many times over.'
    },
    {
        avatar: '/demo/images/avatar/avatar-m-4.png',
        name: 'James Wilson',
        title: 'CTO, Software Solutions',
        message: 'The compliance features and multi-region deployment options were key factors in our decision. TimeBandit meets all our security requirements.'
    },
    {
        avatar: '/demo/images/avatar/avatar-f-2.png',
        name: 'Rachel Kim',
        title: 'Delivery Manager',
        message: 'Automated status reports and burn rate tracking have transformed our project management. We can spot potential issues before they become problems.'
    }
]);

const testimonial3 = ref([
    {
        avatar: '/demo/images/avatar/avatar-m-1.png',
        name: 'Alex Martinez',
        title: 'Program Manager',
        message: 'The API integration capabilities are extensive. We\'ve connected TimeBandit with our entire tool stack, creating a seamless workflow.'
    },
    {
        avatar: '/demo/images/avatar/avatar-f-7.png',
        name: 'Sophie Anderson',
        title: 'Team Lead',
        message: 'Our team adoption rate was incredible - the interface is intuitive and the mobile app makes time tracking actually convenient.'
    },
    {
        avatar: '/demo/images/avatar/avatar-m-5.png',
        name: 'Tom Bradley',
        title: 'Finance Director',
        message: 'The financial reporting and budget tracking features have given us unprecedented visibility into project costs and resource utilization.'
    }
]);

const testimonial4 = ref([
    {
        avatar: '/demo/images/avatar/avatar-f-3.png',
        name: 'Nina Patel',
        title: 'Operations Manager',
        message: 'TimeBandit\'s automated workflows have reduced our administrative overhead by 70%. The ROI was evident within the first month.'
    },
    {
        avatar: '/demo/images/avatar/avatar-m-6.png',
        name: 'Chris Morgan',
        title: 'Agile Coach',
        message: 'Perfect for agile teams. The sprint tracking and resource management features help us maintain optimal team velocity.'
    },
    {
        avatar: '/demo/images/avatar/avatar-f-8.png',
        name: 'Laura Schmidt',
        title: 'Client Success Manager',
        message: 'Our clients love the transparency TimeBandit provides. They can see project progress and resource allocation in real-time.'
    },
    {
        avatar: '/demo/images/avatar/avatar-m-7.png',
        name: 'Daniel Lee',
        title: 'Engineering Manager',
        message: 'The developer API is robust and well-documented. We\'ve built several custom integrations to streamline our workflow.'
    }
]);
</script>

<template>
    <section class="relative landing-container mx-auto py-10 lg:py-28">
        <div class="badge">Success Stories</div>
        <h2 class="title-h5 lg:title-h2 mt-4">What Our Customers Say</h2>
        <p class="body-small lg:body-large mt-4 max-w-md lg:max-w-none mx-auto">
            See how organizations of all sizes are improving project delivery and resource management with TimeBandit.
        </p>
        <div class="lg:overflow-hidden transition-all duration-500 relative z-10">
            <div class="grid grid-cols-1 lg:grid-cols-[26.5%_1fr_26.5%] items-start gap-4 xl:gap-6 mt-16 lg:pt-32 lg:-mt-16 max-w-3xl lg:max-w-none mx-auto">
                <div class="hidden lg:grid grid-cols-1 gap-4 xl:gap-6 order-2 lg:order-1">
                    <template v-for="(testimonial, index) of testimonial1" :key="index">
                        <TestimonialCard :testimonial="testimonial" />
                    </template>
                </div>
                <div class="grid grid-cols-1 gap-4 xl:gap-6 order-1 lg:order-2">
                    <div class="border border-dashed rounded-2xl border-surface-200 dark:border-surface-800">
                        <TestimonialCard
                            :testimonial="{
                                avatar: '/demo/images/avatar/avatar-f-2.png',
                                name: 'Bessie Cooper',
                                title: 'Director of Operations, TechFlow Inc.',
                                message:
                                    'TimeBandit has revolutionized how we track and manage project time. The intuitive interface and powerful analytics have helped us reduce overhead costs by 35% and improve team productivity. The automated reporting features are simply outstanding.'
                            }"
                            className="[&>p]:leading-relaxed -rotate-3 -translate-y-4 translate-x-1 bg-surface-0 dark:bg-surface-950 shadow-[0px_120px_34px_0px_rgba(0,0,0,0.00),0px_77px_31px_0px_rgba(0,0,0,0.01),0px_43px_26px_0px_rgba(0,0,0,0.04),0px_19px_19px_0px_rgba(0,0,0,0.07),0px_5px_11px_0px_rgba(0,0,0,0.08)]"
                        />
                    </div>
                    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-1 xl:grid-cols-2 items-start gap-4 xl:gap-6">
                        <div class="grid grid-cols-1 gap-4 xl:gap-6">
                            <template v-for="(testimonial, index) of testimonial2" :key="index">
                                <TestimonialCard :testimonial="testimonial" />
                            </template>
                        </div>
                        <div class="grid grid-cols-1 gap-4 xl:gap-6">
                            <template v-for="(testimonial, index) of testimonial3" :key="index">
                                <TestimonialCard :testimonial="testimonial" />
                            </template>
                        </div>
                    </div>
                </div>
                <div class="hidden lg:grid grid-cols-1 gap-4 xl:gap-6 order-3">
                    <template v-for="(testimonial, index) of testimonial4" :key="index">
                        <TestimonialCard :testimonial="testimonial" />
                    </template>
                </div>
            </div>
        </div>
        <div class="mx-auto sm:max-w-sm mt-12 lg:hidden">
            <button class="py-3 px-7 w-full rounded-xl bg-surface-950 dark:bg-surface-0 text-surface-0 dark:text-surface-950 hover:opacity-75 transition-all">All Customers Reviews</button>
        </div>
        <div
            class="opacity-100 z-20 hidden lg:block absolute transition-all duration-500 bottom-0 left-0 w-full h-[42rem] [background:linear-gradient(0deg,_#FFF_18.86%,rgba(255,255,255,0.76)_52.08%,rgba(255,255,255,0.36)_67.51%,rgba(255,255,255,0.10)_89.4%,rgba(255,255,255,0.00)_99.94%)] dark:[background:linear-gradient(0deg,var(--p-surface-950)_18.86%,color-mix(in_srgb,var(--p-surface-950)_95%,transparent_5%)_52.08%,color-mix(in_srgb,var(--p-surface-950)_60%,transparent_40%)_65.88%,color-mix(in_srgb,var(--p-surface-950)_30%,transparent_70%)_89.4%,rgba(9,9,11,0.00)_99.94%)]"
        >
            <button class="py-3 px-7 rounded-xl bg-surface-950 dark:bg-surface-0 text-surface-0 dark:text-surface-950 hover:opacity-75 transition-all absolute left-1/2 -translate-x-1/2 bottom-1/3">All Customers Reviews</button>
        </div>
    </section>
</template>
