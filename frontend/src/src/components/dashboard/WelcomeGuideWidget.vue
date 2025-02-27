<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const activeIndex = ref(0);
const autoplayInterval = ref(null);
const autoplayDuration = 8000; // 8 seconds per slide

// Module guides with descriptions and actions
const moduleGuides = [
  {
    id: 1,
    title: 'Welcome to CareerPath',
    description: 'Your all-in-one platform for managing employees, candidates, and recruitment processes. This dashboard gives you a quick overview of your organization.',
    icon: 'pi pi-home',
    color: 'bg-blue-500',
    image: '/layout/images/dashboard-welcome.svg',
    action: {
      label: 'Explore Dashboard',
      route: '/'
    }
  },
  {
    id: 2,
    title: 'Employee Management',
    description: 'Track employee information, skills, certifications, and performance. Manage your team effectively with comprehensive profiles and analytics.',
    icon: 'pi pi-users',
    color: 'bg-indigo-500',
    image: '/layout/images/dashboard-employees.svg',
    action: {
      label: 'View Employees',
      route: '/employees'
    }
  },
  {
    id: 3,
    title: 'Candidate Tracking',
    description: 'Streamline your recruitment process by tracking candidates, their applications, and interview progress all in one place.',
    icon: 'pi pi-user-plus',
    color: 'bg-green-500',
    image: '/layout/images/dashboard-candidates.svg',
    action: {
      label: 'View Candidates',
      route: '/candidates'
    }
  },
  {
    id: 4,
    title: 'Recruitment Process',
    description: 'Create and manage recruitment processes, schedule interviews, and evaluate candidates efficiently.',
    icon: 'pi pi-briefcase',
    color: 'bg-orange-500',
    image: '/layout/images/dashboard-recruitment.svg',
    action: {
      label: 'Manage Recruitment',
      route: '/recruitment-leads'
    }
  },
  {
    id: 5,
    title: 'Skillset Management',
    description: 'Define and track skills across your organization. Identify skill gaps and plan training initiatives based on real data.',
    icon: 'pi pi-star',
    color: 'bg-purple-500',
    image: '/layout/images/dashboard-skills.svg',
    action: {
      label: 'Manage Skillsets',
      route: '/admin-skillsets'
    }
  },
  {
    id: 6,
    title: 'Certification Tracking',
    description: 'Keep track of professional certifications across your organization. Monitor expiration dates and certification coverage.',
    icon: 'pi pi-check-circle',
    color: 'bg-cyan-500',
    image: '/layout/images/dashboard-certifications.svg',
    action: {
      label: 'View Certifications',
      route: '/admin-certifications'
    }
  }
];

// Navigate to the specified route
const navigateTo = (route) => {
  router.push(route);
};

// Set active slide
const setActiveSlide = (index) => {
  activeIndex.value = index;
};

// Go to next slide
const nextSlide = () => {
  activeIndex.value = (activeIndex.value + 1) % moduleGuides.length;
};

// Go to previous slide
const prevSlide = () => {
  activeIndex.value = (activeIndex.value - 1 + moduleGuides.length) % moduleGuides.length;
};

// Start autoplay
const startAutoplay = () => {
  stopAutoplay(); // Clear any existing interval
  autoplayInterval.value = setInterval(() => {
    nextSlide();
  }, autoplayDuration);
};

// Stop autoplay
const stopAutoplay = () => {
  if (autoplayInterval.value) {
    clearInterval(autoplayInterval.value);
    autoplayInterval.value = null;
  }
};

// Pause autoplay on hover
const pauseAutoplay = () => {
  stopAutoplay();
};

// Resume autoplay when not hovering
const resumeAutoplay = () => {
  startAutoplay();
};

onMounted(() => {
  startAutoplay();
});

onBeforeUnmount(() => {
  stopAutoplay();
});
</script>

<template>
  <div 
    class="card welcome-guide" 
    @mouseenter="pauseAutoplay" 
    @mouseleave="resumeAutoplay"
  >
    <div class="relative overflow-hidden rounded-lg">
      <!-- Slides -->
      <div class="relative h-[400px]">
        <transition-group name="slide-fade" tag="div" class="h-full">
          <div 
            v-for="(guide, index) in moduleGuides" 
            :key="guide.id"
            v-show="index === activeIndex"
            class="absolute inset-0 flex flex-col md:flex-row items-center p-6 transition-all duration-500"
          >
            <!-- Content -->
            <div class="md:w-1/2 z-10 text-center md:text-left mb-6 md:mb-0">
              <div :class="[guide.color, 'inline-flex items-center justify-center w-12 h-12 rounded-full mb-4']">
                <i :class="[guide.icon, 'text-white text-xl']"></i>
              </div>
              <h2 class="text-2xl font-bold mb-3 text-900">{{ guide.title }}</h2>
              <p class="text-surface-600 mb-6 leading-relaxed">{{ guide.description }}</p>
              <Button 
                :label="guide.action.label" 
                :icon="guide.icon" 
                class="p-button-rounded" 
                @click="navigateTo(guide.action.route)"
              />
            </div>
            
            <!-- Image -->
            <div class="md:w-1/2 flex justify-center items-center">
              <img 
                :src="guide.image" 
                :alt="guide.title"
                class="max-h-[200px] md:max-h-[250px] object-contain"
                onerror="this.src='/layout/images/placeholder-image.svg'"
              />
            </div>
          </div>
        </transition-group>
      </div>
      
      <!-- Navigation Arrows -->
      <button 
        @click="prevSlide" 
        class="absolute left-2 top-1/2 -translate-y-1/2 w-10 h-10 rounded-full bg-surface-0/70 hover:bg-surface-0/90 flex items-center justify-center shadow-md z-20"
      >
        <i class="pi pi-chevron-left"></i>
      </button>
      
      <button 
        @click="nextSlide" 
        class="absolute right-2 top-1/2 -translate-y-1/2 w-10 h-10 rounded-full bg-surface-0/70 hover:bg-surface-0/90 flex items-center justify-center shadow-md z-20"
      >
        <i class="pi pi-chevron-right"></i>
      </button>
      
      <!-- Indicators -->
      <div class="absolute bottom-4 left-0 right-0 flex justify-center gap-2 z-20">
        <button 
          v-for="(guide, index) in moduleGuides" 
          :key="`indicator-${guide.id}`"
          @click="setActiveSlide(index)"
          :class="[
            'w-3 h-3 rounded-full transition-all duration-300',
            index === activeIndex 
              ? 'bg-primary-500 w-6' 
              : 'bg-surface-300 hover:bg-surface-400'
          ]"
        ></button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.card {
  background-color: var(--surface-card);
  border-radius: 0.75rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border: 1px solid var(--surface-border);
  overflow: hidden;
  height: 100%;
}

.welcome-guide {
  position: relative;
}

/* Slide transitions */
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.5s ease;
}

.slide-fade-enter-from {
  opacity: 0;
  transform: translateX(30px);
}

.slide-fade-leave-to {
  opacity: 0;
  transform: translateX(-30px);
}
</style> 