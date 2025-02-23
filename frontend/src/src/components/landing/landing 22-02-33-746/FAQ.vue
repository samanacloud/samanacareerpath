<script setup>
import { ref } from 'vue';
const faqs = ref([
    {
        question: 'How does TimeBandit handle data security and compliance?',
        answer: 'TimeBandit employs multi-region server deployment to ensure data sovereignty and compliance with local regulations. We use enterprise-grade encryption and follow strict security protocols to protect your data.'
    },
    {
        question: 'Can I integrate TimeBandit with other tools we use?',
        answer: 'Yes! TimeBandit offers integration with popular expense management tools like Expensify, and provides robust APIs for connecting with your existing systems. We\'re continuously adding new integrations to enhance workflow automation.'
    },
    {
        question: 'How does the team time tracking feature work?',
        answer: 'Team members can easily log their hours, categorize activities, and maintain timesheets through our intuitive interface. Managers get real-time visibility into project progress and resource utilization, with automated reporting capabilities.'
    },
    {
        question: 'What kind of reports can I generate?',
        answer: 'TimeBandit offers comprehensive reporting including project status, resource utilization, burn rate analysis, and budget tracking. Reports can be automated and customized to your needs, with support for multiple currencies and detailed analytics.'
    }
]);
</script>

<template>
    <section class="py-10 lg:py-28 landing-container mx-auto">
        <div class="w-full">
            <h3 class="title-h5 lg:title-h3">Frequently Asked Questions</h3>
            <p class="mt-6 label-small lg:body-large max-w-md lg:max-w-none mx-auto">Get answers to common questions about TimeBandit's features, security, and integrations. Can't find what you're looking for? Contact our support team.</p>
            <div class="max-w-3xl lg:max-w-6xl mx-auto mt-10 p-4 lg:p-6 rounded-2xl border border-surface-200 dark:border-surface-800">
                <Accordion :value="0" expandIcon="pi pi-plus" collapseIcon="pi pi-minus">
                    <AccordionPanel
                        v-for="(faq, index) in faqs"
                        :key="index"
                        :value="index"
                        :pt="{
                            root: {
                                class: 'last:border-0 !border-surface-200 dark:!border-surface-800'
                            }
                        }"
                    >
                        <AccordionHeader
                            :pt="{
                                root: {
                                    class: '!p-6 !bg-transparent hover:opacity-70 !transition-all data-[p-active=true]:!pb-4 !transition-all !duration-200'
                                },
                                toggleIcon: {
                                    class: '!text-xl !text-surface-950 dark:!text-surface-0'
                                }
                            }"
                        >
                            <h5 class="label-medium">{{ faq.question }}</h5>
                        </AccordionHeader>
                        <AccordionContent
                            :pt="{
                                content: {
                                    class: '!px-6 !pb-6 !body-small !bg-transparent'
                                }
                            }"
                        >
                            <p class="m-0 body-small text-left">{{ faq.answer }}</p>
                        </AccordionContent>
                    </AccordionPanel>
                </Accordion>
            </div>
        </div>
    </section>
</template>
