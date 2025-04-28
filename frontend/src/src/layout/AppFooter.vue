<script setup>
import { ref, onMounted, computed, onUnmounted } from 'vue';
import Button from 'primevue/button';

// Add state for session info
const sessionInfo = ref(null);
const sessionExpiresAt = ref(null);
const renewingSession = ref(false);
const debugInfo = ref('');
// Helper ref to force computed property recalculation
const timerTick = ref(0);

// Computed property to calculate remaining time
const remainingTime = computed(() => {
    // Use timerTick to force recalculation (its value doesn't matter)
    const _ = timerTick.value;
    
    if (!sessionExpiresAt.value) return null;
    
    try {
        // Parse the expiration time from the server (which is in ISO format, expected to be in UTC)
        let expiresAtStr = sessionExpiresAt.value;
        
        // If the string does not end with 'Z' or contain a timezone offset, assume it's UTC and append 'Z'
        if (!expiresAtStr.endsWith('Z') && !expiresAtStr.match(/[+-]\d{2}:\d{2}$/)) {
            expiresAtStr += 'Z';
        }
        
        // Create Date objects using the modified expiresAtStr
        const expiresAt = new Date(expiresAtStr);
        const now = new Date();
        
        // Check if the date is valid
        if (isNaN(expiresAt.getTime())) {
            console.error('Invalid expiration date format:', expiresAtStr);
            return null;
        }
        
        // Calculate difference in milliseconds (this is timezone-independent)
        const diffMs = expiresAt.getTime() - now.getTime();
        
        // For debugging
        console.log('Expiration time (UTC):', expiresAtStr);
        console.log('Current time (UTC):', now.toISOString());
        console.log('Difference (ms):', diffMs);
        console.log('Difference (minutes):', Math.floor(diffMs / 60000));
        
        // If already expired
        if (diffMs <= 0) {
            return { text: 'Expired', isExpiring: true, isExpired: true };
        }
        
        // Convert to hours, minutes and seconds
        const totalSeconds = Math.floor(diffMs / 1000);
        const totalMinutes = Math.floor(totalSeconds / 60);
        const hours = Math.floor(totalMinutes / 60);
        const minutes = totalMinutes % 60;
        const seconds = totalSeconds % 60;
        
        // Format the time with leading zeros for seconds if needed
        let formattedTime;
        if (hours > 0) {
            formattedTime = `${hours}h ${minutes.toString().padStart(2, '0')}m`;
        } else {
            formattedTime = `${minutes}m ${seconds.toString().padStart(2, '0')}s`;
        }
        
        // Check if less than 5 minutes remaining
        const isExpiring = totalMinutes < 5;
        
        return { 
            text: formattedTime, 
            isExpiring, 
            isExpired: false,
            hours,
            minutes,
            seconds,
            totalMinutes
        };
    } catch (error) {
        console.error('Error calculating remaining time:', error);
        return null;
    }
});

// Function to fetch and update session info
const fetchSessionInfo = async () => {
    try {
        // Proceed with API call to get session info
        const response = await fetch('/core/auth/verify/session', {
            method: 'GET',
            credentials: 'include',
            headers: {
                'Accept': 'application/json',
            }
        });

        if (response.ok) {
            const data = await response.json();
            console.log('Session data from API:', data);
            
            if (!data.user) {
                console.error('No user data in session response');
                return;
            }
            
            // Update session info from API response
            sessionInfo.value = data.user;
            
            // Store the raw expiration value if available
            if (data.expiresAt) {
                console.log('Raw expiration from API (UTC):', data.expiresAt);
                
                // Validate that we can parse the date
                const expiresDate = new Date(data.expiresAt);
                if (isNaN(expiresDate.getTime())) {
                    console.error('Invalid date format received from server:', data.expiresAt);
                    return;
                }
                
                // Store the raw string value directly (it's in UTC format)
                sessionExpiresAt.value = data.expiresAt;
                
                // Calculate and show time remaining in debug info
                const now = new Date();
                const diffMs = expiresDate.getTime() - now.getTime();
                const diffMinutes = Math.floor(diffMs / 60000);
                
                debugInfo.value = `Session expires in ${diffMinutes} minutes (UTC: ${data.expiresAt})`;
            } else {
                console.warn('No expiresAt field in the API response');
            }
        } else {
            console.error('Error fetching session info:', response.status, response.statusText);
        }
    } catch (error) {
        console.error('Error fetching session info:', error);
    }
};

// Function to renew session
const renewSession = async () => {
    renewingSession.value = true;
    try {
        console.log('Renewing session...');
        const response = await fetch('/core/auth/renew-session', {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Accept': 'application/json',
            }
        });

        if (response.ok) {
            const data = await response.json();
            console.log('Renew session response:', data);
            
            if (data.expiresAt) {
                // Store the raw string value directly
                console.log('Raw expiration from renewal (UTC):', data.expiresAt);
                
                // Validate that we can parse the date
                const newExpiration = new Date(data.expiresAt);
                if (isNaN(newExpiration.getTime())) {
                    console.error('Invalid date format received from server:', data.expiresAt);
                    debugInfo.value = `Error: Invalid expiration date format: ${data.expiresAt}`;
                    setTimeout(() => {
                        debugInfo.value = '';
                    }, 5000);
                    return;
                }
                
                // Log the current time and the new expiration time for comparison
                const now = new Date();
                const diffMs = newExpiration.getTime() - now.getTime();
                const diffMinutes = Math.floor(diffMs / 60000);
                
                console.log('Current time (UTC):', now.toISOString());
                console.log('New expiration time (UTC):', data.expiresAt);
                console.log('Time difference (minutes):', diffMinutes);
                
                // Update the expiration time (UTC format from server)
                sessionExpiresAt.value = data.expiresAt;
                debugInfo.value = `Session renewed. Expires in ${diffMinutes} minutes (UTC: ${data.expiresAt})`;
                
                // Hide debug info after 5 seconds
                setTimeout(() => {
                    debugInfo.value = '';
                }, 5000);
            } else {
                console.error('No expiration time in response');
                debugInfo.value = 'Error: No expiration time in response';
                setTimeout(() => {
                    debugInfo.value = '';
                }, 3000);
            }
        } else {
            console.error('Error response:', response.status, response.statusText);
            debugInfo.value = `Error: ${response.status} ${response.statusText}`;
            setTimeout(() => {
                debugInfo.value = '';
            }, 3000);
        }
    } catch (error) {
        console.error('Error renewing session:', error);
        debugInfo.value = `Error renewing session: ${error.message}`;
        // Hide debug info after 3 seconds
        setTimeout(() => {
            debugInfo.value = '';
        }, 3000);
    } finally {
        renewingSession.value = false;
    }
};

// Set up timer to update remaining time display
let timer = null;

onMounted(() => {
    fetchSessionInfo();
    
    // Set up a timer to update the UI every second
    timer = setInterval(() => {
        // Increment the tick to force computed property recalculation
        timerTick.value++;
    }, 1000);
});

onUnmounted(() => {
    // Clear the timer when component is unmounted
    if (timer) {
        clearInterval(timer);
        timer = null;
    }
});
</script>

<template>
    <div class="layout-footer">
        <div class="footer-left">
            CareerPath by
            <a href="https://www.samanagroup.com" target="_blank" rel="noopener noreferrer" class="text-primary font-bold hover:underline">Samana Group LLC</a>
        </div>
        
        <div v-if="sessionInfo" class="footer-right">
            <div class="session-info">
                <span class="user-role">{{ sessionInfo.role || 'User' }}</span>
                <span class="session-time" :class="{
                    'session-expiring': remainingTime && remainingTime.isExpiring,
                    'session-expired': remainingTime && remainingTime.isExpired
                }">
                    <template v-if="remainingTime">
                        Expires in: {{ remainingTime.text }}
                    </template>
                    <template v-else-if="sessionExpiresAt">
                        <!-- Fallback if remainingTime calculation fails -->
                        UTC Expires: {{ sessionExpiresAt }}
                    </template>
                    <template v-else>
                        Session info unavailable
                    </template>
                    <Button 
                        icon="pi pi-refresh" 
                        class="p-button-text p-button-rounded p-button-sm" 
                        @click="renewSession" 
                        :loading="renewingSession"
                        tooltip="Renew Session"
                        tooltipOptions="{ position: 'top' }"
                    />
                </span>
            </div>
        </div>
        
        <!-- Debug info - remove in production -->
        <div v-if="debugInfo" class="debug-info">{{ debugInfo }}</div>
    </div>
</template>

<style scoped>
.layout-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 1rem;
    position: relative;
}

.footer-left, .footer-right {
    display: flex;
    align-items: center;
}

.session-info {
    display: flex;
    align-items: center;
    gap: 1rem;
    font-size: 0.875rem;
}

.user-role {
    font-weight: 500;
}

.session-time {
    display: flex;
    align-items: center;
    gap: 0.25rem;
    color: var(--text-color-secondary);
    transition: color 0.3s ease, background-color 0.3s ease;
    padding: 0.25rem 0.5rem;
    border-radius: 0.25rem;
}

/* Style for when session is about to expire (less than 5 minutes) */
.session-expiring {
    color: var(--red-700);
    font-weight: 500;
}

/* Style for when session is expired */
.session-expired {
    color: var(--red-700);
    font-weight: 700;
}

.debug-info {
    position: absolute;
    bottom: 100%;
    right: 0;
    background: rgba(0,0,0,0.7);
    color: white;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 10px;
    max-width: 300px;
    overflow: hidden;
    text-overflow: ellipsis;
    display: none;
    z-index: 100;
}

/* Show debug info on hover - for development only */
.layout-footer:hover .debug-info {
    display: block;
}

@media screen and (max-width: 768px) {
    .layout-footer {
        flex-direction: column;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
    }
}
</style>
