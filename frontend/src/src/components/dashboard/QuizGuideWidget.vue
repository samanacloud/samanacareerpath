<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';

const activeIndex = ref(0);
const autoplayInterval = ref(null);
const autoplayDuration = 8000; // 8 seconds per slide

// Quiz guide slides with descriptions
const quizGuides = [
  {
    id: 1,
    title: 'Welcome to Skill Assessment',
    description: 'Generate quizzes to assess your knowledge in various skillsets. Select a skillset from the left panel to get started.',
    icon: 'pi pi-compass',
    color: 'bg-blue-500',
    image: '/src/public/layout/images/quiz-welcome.svg',
  },
  {
    id: 2,
    title: 'Select a Skillset',
    description: 'Browse through categories or use the search bar to find specific skillsets. Click on a skillset to select it for quiz generation.',
    icon: 'pi pi-list-box',
    color: 'bg-indigo-500',
    image: '/src/public/layout/images/quiz-select.svg',
  },
  {
    id: 3,
    title: 'Generate Quiz',
    description: 'Once you\'ve selected a skillset, click the "Generate Quiz" button to create a customized quiz with questions related to your chosen topic.',
    icon: 'pi pi-cog',
    color: 'bg-green-500',
    image: '/src/public/layout/images/quiz-model.svg',
  },
  {
    id: 4,
    title: 'Answer Questions',
    description: 'Read each question carefully and select the best answer. Questions have different difficulty levels and time limits.',
    icon: 'pi pi-check-circle',
    color: 'bg-orange-500',
    image: '/src/public/layout/images/quiz-questions.svg',
  },
  {
    id: 5,
    title: 'Review Your Score',
    description: 'After completing the quiz, you\'ll see your score and a star rating. High scores will be celebrated with a confetti animation!',
    icon: 'pi pi-chart-pie',
    color: 'bg-purple-500',
    image: '/src/public/layout/images/quiz-results.svg',
  },
  {
    id: 6,
    title: 'Skill Rating',
    description: 'Your quiz results will be automatically recorded as a skill rating in your profile, helping track your progress over time.',
    icon: 'pi pi-verified',
    color: 'bg-cyan-500',
    image: '/src/public/layout/images/quiz-rating.svg',
  }
];

// Set active slide
const setActiveSlide = (index) => {
  activeIndex.value = index;
};

// Go to next slide
const nextSlide = () => {
  activeIndex.value = (activeIndex.value + 1) % quizGuides.length;
};

// Go to previous slide
const prevSlide = () => {
  activeIndex.value = (activeIndex.value - 1 + quizGuides.length) % quizGuides.length;
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

// Function to get the appropriate gradient class based on the color
const getGradientClass = (colorClass) => {
  const color = colorClass.split('-')[1];
  switch (color) {
    case 'blue': return 'bg-gradient-to-br from-blue-400 to-blue-600';
    case 'indigo': return 'bg-gradient-to-br from-indigo-400 to-indigo-600';
    case 'green': return 'bg-gradient-to-br from-green-400 to-green-600';
    case 'orange': return 'bg-gradient-to-br from-orange-400 to-orange-600';
    case 'purple': return 'bg-gradient-to-br from-purple-400 to-purple-600';
    case 'cyan': return 'bg-gradient-to-br from-cyan-400 to-cyan-600';
    default: return 'bg-gradient-to-br from-gray-400 to-gray-600';
  }
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
    class="card quiz-guide" 
    @mouseenter="pauseAutoplay" 
    @mouseleave="resumeAutoplay"
  >
    <div class="relative overflow-hidden rounded-lg">
      <!-- Background pattern -->
      <div class="absolute inset-0 opacity-5 pattern-dots"></div>
      
      <!-- Slides -->
      <div class="relative h-[300px]">
        <transition-group name="slide-fade" tag="div" class="h-full">
          <div 
            v-for="(guide, index) in quizGuides" 
            :key="guide.id"
            v-show="index === activeIndex"
            class="absolute inset-0 flex flex-col md:flex-row items-center p-6 transition-all duration-500"
          >
            <!-- Content -->
            <div class="md:w-1/2 z-10 text-center md:text-left mb-6 md:mb-0">
              <div :class="[guide.color, 'inline-flex items-center justify-center w-12 h-12 rounded-full mb-4 shadow-md']">
                <i :class="[guide.icon, 'text-white text-xl']"></i>
              </div>
              <h2 class="text-2xl font-bold mb-3 text-900">{{ guide.title }}</h2>
              <p class="text-surface-600 mb-6 leading-relaxed">{{ guide.description }}</p>
              
              <!-- Step indicator -->
              <div class="flex items-center justify-center md:justify-start gap-1 text-xs text-surface-500">
                <span>Step {{ index + 1 }} of {{ quizGuides.length }}</span>
                <div class="w-16 h-1 ml-2 bg-surface-200 rounded-full overflow-hidden">
                  <div :class="[guide.color, 'h-full rounded-full']" :style="{ width: `${((index + 1) / quizGuides.length) * 100}%` }"></div>
                </div>
              </div>
            </div>
            
            <!-- Image replaced with large icon -->
            <div class="md:w-1/2 flex justify-center items-center">
              <div class="relative">
                <!-- Decorative circles -->
                <div class="absolute inset-0 -m-4 rounded-full opacity-20" :class="[guide.color]"></div>
                <div class="absolute inset-0 -m-2 rounded-full opacity-30" :class="[guide.color]"></div>
                
                <!-- Main icon circle with gradient -->
                <div 
                  :class="[
                    'w-32 h-32 md:w-40 md:h-40 rounded-full flex items-center justify-center shadow-lg transform transition-all duration-500 hover:scale-105 animate-pulse-slow',
                    getGradientClass(guide.color)
                  ]"
                >
                  <i :class="[guide.icon, 'text-white text-5xl']"></i>
                </div>
                
                <!-- Small decorative dots -->
                <div class="absolute top-0 right-0 w-4 h-4 rounded-full bg-white opacity-50"></div>
                <div class="absolute bottom-0 left-0 w-3 h-3 rounded-full bg-white opacity-40"></div>
                <div class="absolute top-1/4 left-0 w-2 h-2 rounded-full bg-white opacity-30"></div>
              </div>
            </div>
          </div>
        </transition-group>
      </div>
      
      <!-- Navigation Arrows -->
      <button 
        @click="prevSlide" 
        class="absolute left-2 top-1/2 -translate-y-1/2 w-10 h-10 rounded-full bg-surface-0/70 hover:bg-surface-0/90 flex items-center justify-center shadow-md z-20 transition-all duration-300 hover:scale-110"
      >
        <i class="pi pi-chevron-left"></i>
      </button>
      
      <button 
        @click="nextSlide" 
        class="absolute right-2 top-1/2 -translate-y-1/2 w-10 h-10 rounded-full bg-surface-0/70 hover:bg-surface-0/90 flex items-center justify-center shadow-md z-20 transition-all duration-300 hover:scale-110"
      >
        <i class="pi pi-chevron-right"></i>
      </button>
      
      <!-- Indicators -->
      <div class="absolute bottom-4 left-0 right-0 flex justify-center gap-2 z-20">
        <button 
          v-for="(guide, index) in quizGuides" 
          :key="`indicator-${guide.id}`"
          @click="setActiveSlide(index)"
          :class="[
            'w-3 h-3 rounded-full transition-all duration-300',
            index === activeIndex 
              ? `${guide.color} w-6` 
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

.quiz-guide {
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

/* Custom slow pulse animation */
@keyframes pulse-slow {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.03); }
}

.animate-pulse-slow {
  animation: pulse-slow 3s infinite ease-in-out;
}

/* Pattern background */
.pattern-dots {
  background-image: radial-gradient(var(--surface-500) 1px, transparent 1px);
  background-size: 20px 20px;
}
</style> 