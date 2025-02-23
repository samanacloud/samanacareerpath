<script setup>
defineProps({
    className: {
        type: String,
        default: ''
    },
    reverseTheme: {
        type: Boolean,
        default: false
    }
});
</script>

<template>
    <svg :class="[className, reverseTheme ? 'fill-surface-0 dark:fill-surface-900' : 'fill-surface-900 dark:fill-surface-0']" width="152" height="32" viewBox="0 0 152 32" fill="none" xmlns="http://www.w3.org/2000/svg">
        <g clip-path="url(#clip0_697_2374)">
            <path d="M9.49284 22.2426L15.4179 6.9315V0L5.17065 23.3063L9.49284 22.2426Z" />
            <path
                d="M15.9999 8.65381L10.6243 22.5453L15.9999 26.7894L21.3756 22.5453L15.9999 8.65381ZM13.8527 18.8512L15.0306 18.004C15.656 17.5538 16.3358 18.4996 15.7105 18.9492L14.5327 19.7964C13.9144 20.2415 13.2245 19.303 13.8527 18.8512ZM18.4382 20.7471L14.9075 23.2866C14.2895 23.7315 13.599 22.7935 14.2276 22.3414L17.7582 19.8019C18.3839 19.3517 19.0631 20.2975 18.4382 20.7471Z"
            />
            <path d="M15.4175 27.8132L9.78876 23.3691L5.47021 24.4319L15.4175 32.0003V27.8132Z" />
            <path d="M22.2109 23.3691L16.582 27.8132V32.0003L26.5294 24.4319L22.2109 23.3691Z" />
            <path d="M16.582 6.9315L22.5071 22.2426L26.8293 23.3062L16.582 0V6.9315Z" />
        </g>
        
        <text x="43" y="24" font-family="Arial" font-size="20" font-weight="bold">
            TimeBandit
        </text>
    </svg>
</template>
