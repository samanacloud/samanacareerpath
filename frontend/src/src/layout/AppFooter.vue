<script setup>
import { useLayout } from '@/layout/composables/layout';
import { computed } from 'vue';

const { layoutConfig } = useLayout();

const logoUrl = computed(() => {
    return `${layoutConfig.darkTheme.value ? 'samana-logo-white' : 'samana-logo-dark'}.png`;
});
</script>

<template>
    <div class="layout-footer">
        <img :src="logoUrl" alt="Logo" height="20" class="mr-2" />
        by
        <span class="font-medium ml-2">Samana Group LLC </span>
         , All Rights Reserved
         <div class="ml-4">
          <a href="/TermsOfService.html" class="text-primary">Terms of Use</a> | 
          <a href="/privacy.html" class="text-primary">Privacy Policy</a>
      </div>
    </div>

</template>
<style lang="scss" scoped></style>
