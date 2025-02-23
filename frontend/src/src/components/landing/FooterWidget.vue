<template>
    <div class="bg-surface-900 px-6 py-6 md:px-12 lg:px-20">
        <div class="flex flex-wrap items-center justify-between">
            <div class="flex items-center gap-8">
                <img src="/demo/images/samana-logo-white.png" alt="Samana Group" class="h-8" />
                <div class="flex gap-6 items-center">
                    <span class="text-surface-0/80 transition-colors font-medium">
                        <span class="font-bold">CareerPath</span> by
                    </span>
                    <a href="https://www.samanagroup.com" class="text-surface-0/80 hover:text-surface-0 transition-colors font-medium">
                        Samana Group LLC
                    </a>
                    <span class="text-surface-0/80">© {{ new Date().getFullYear() }}</span>
                </div>
            </div>
            <div class="flex items-center gap-4">
                <a href="https://github.com/samanacloud" class="flex items-center justify-center w-10 h-10 bg-surface-800 hover:bg-surface-700 rounded-lg transition-colors">
                    <i class="pi pi-github text-surface-0/80 hover:text-surface-0"></i>
                </a>
                <a href="https://linkedin.com/company/samana-group-llc" class="flex items-center justify-center w-10 h-10 bg-surface-800 hover:bg-surface-700 rounded-lg transition-colors">
                    <i class="pi pi-linkedin text-surface-0/80 hover:text-surface-0"></i>
                </a>
            </div>
        </div>
    </div>
</template>

<style scoped>
.line-height-3 {
    line-height: 1.5;
}
</style>
