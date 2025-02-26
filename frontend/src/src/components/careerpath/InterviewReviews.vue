<template>
  <div class="card p-4">
    <!-- Header Section -->
    <div class="flex items-center justify-between mb-4 cursor-pointer hover-effect" @click="toggleReviews">
      <div class="flex items-center gap-2">
        <i class="pi pi-comments text-indigo-500 text-lg"></i>
        <h5 class="font-semibold m-0">Interview Reviews</h5>
        <div class="bg-indigo-100 text-indigo-800 text-xs font-medium px-2 py-0.5 rounded-full">
          {{ interviewsData.length }}
        </div>
      </div>
      <i :class="`pi ${isReviewsExpanded ? 'pi-chevron-up' : 'pi-chevron-down'} text-gray-500 transform transition-transform duration-300`"></i>
    </div>

    <!-- Content Section -->
    <transition 
      name="expand" 
      @enter="startExpandAnimation" 
      @leave="startCollapseAnimation"
    >
      <div v-if="isReviewsExpanded" class="overflow-hidden">
        <!-- Empty State -->
        <div v-if="interviewsData.length === 0" class="text-gray-500 italic py-8 text-center animate-fade-in">
          <i class="pi pi-inbox text-gray-300 text-3xl mb-2 block animate-bounce-subtle"></i>
          No reviews available
        </div>
        
        <div v-else>
          <!-- Review Categories Tabs -->
          <div class="border-b border-gray-200 mb-6 animate-fade-in">
            <ul class="flex flex-wrap -mb-px text-sm font-medium text-center">
              <li v-for="(reviews, field) in groupedReviews" :key="field" class="mr-4">
                <button 
                  @click="setSelectedReviewCategory(field)" 
                  class="inline-block p-2 rounded-t-lg transition-all duration-300 ease-in-out" 
                  :class="selectedReviewCategory === field ? 'border-b-2 border-indigo-500 text-indigo-600 active' : 'border-b-2 border-transparent hover:text-gray-600 hover:border-gray-300'">
                  {{ field }}
                  <span class="ml-1 bg-gray-100 text-gray-700 text-xs font-medium px-1.5 py-0.5 rounded-full">
                    {{ reviews.length }}
                  </span>
                </button>
              </li>
            </ul>
          </div>
          
          <!-- Reviews for Selected Category -->
          <div v-for="(reviews, field) in groupedReviews" :key="field">
            <transition-group 
              name="review-list" 
              tag="div" 
              class="grid grid-cols-1 sm:grid-cols-2 gap-6"
              v-show="selectedReviewCategory === field"
            >
              <div 
                v-for="(review, index) in reviews" 
                :key="review.id || index" 
                class="bg-gray-50 rounded-lg p-5 border-l-4 shadow-sm hover:shadow-md transition-all duration-300 transform hover:-translate-y-1 review-card"
                :class="{
                  'border-green-500': review.approved === 'Yes',
                  'border-yellow-500': review.approved === 'Pending',
                  'border-red-500': review.approved === 'No'
                }"
              >
                <!-- Review Header -->
                <div class="flex justify-between items-start mb-4">
                  <div>
                    <div class="font-medium text-gray-900">{{ review.interviewedBy }}</div>
                    <div class="text-xs text-gray-500 mt-1">{{ formatDate(review.createdAt) }}</div>
                  </div>
                  <div 
                    :class="{
                      'bg-green-100 text-green-800': review.approved === 'Yes', 
                      'bg-yellow-100 text-yellow-800': review.approved === 'Pending', 
                      'bg-red-100 text-red-800': review.approved === 'No'
                    }" 
                    class="text-xs font-medium px-2.5 py-1 rounded-full transition-colors duration-300"
                  >
                    {{ review.approved }}
                  </div>
                </div>
                
                <!-- Rating Section -->
                <div class="mb-4 p-3 bg-white rounded shadow-sm">
                  <div class="text-sm font-medium text-gray-700 mb-2">Rating:</div>
                  <Rating :modelValue="review.rating" readonly :stars="5" />
                </div>
                
                <!-- Observations Section -->
                <div class="mt-3">
                  <div class="text-sm font-medium text-gray-700 mb-2">Observations:</div>
                  <p class="text-sm text-gray-600 bg-white p-3 rounded shadow-sm" :class="review.showFullObservation ? 'show-full' : 'line-clamp-3'">
                    {{ review.observations }}
                  </p>
                  <transition name="fade">
                    <button 
                      v-if="review.observations && review.observations.length > 150" 
                      @click="toggleObservation(review)" 
                      class="text-xs text-indigo-600 mt-2 hover:underline focus:outline-none transition-all duration-300 hover:text-indigo-800"
                    >
                      {{ review.showFullObservation ? 'Show less' : 'Read more' }}
                    </button>
                  </transition>
                </div>
              </div>
            </transition-group>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';
import Rating from 'primevue/rating';

const props = defineProps({
  interviewsData: { type: Array, required: true },
  groupedReviews: { type: Object, required: true },
  selectedReviewCategory: { type: String, required: true },
  setSelectedReviewCategory: { type: Function, required: true },
  isReviewsExpanded: { type: Boolean, required: true },
  toggleReviews: { type: Function, required: true },
  formatDate: { type: Function, required: true },
  toggleObservation: { type: Function, required: true }
});

// Animation functions for expand/collapse
const startExpandAnimation = (element) => {
  // Get the height of the element
  const height = element.scrollHeight;
  // Set initial height to 0
  element.style.height = '0px';
  // Force repaint
  element.offsetHeight;
  // Set the height to the final value
  element.style.height = height + 'px';
  // Clean up after animation completes
  element.addEventListener('transitionend', () => {
    element.style.height = null;
  }, { once: true });
};

const startCollapseAnimation = (element) => {
  // Set the initial height
  const height = element.scrollHeight;
  element.style.height = height + 'px';
  // Force repaint
  element.offsetHeight;
  // Set the height to 0
  element.style.height = '0px';
};
</script>

<style scoped>
/* Fade transition */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Expand/collapse transition */
.expand-enter-active,
.expand-leave-active {
  transition: height 0.3s ease-in-out, opacity 0.3s ease;
  overflow: hidden;
}
.expand-enter-from,
.expand-leave-to {
  opacity: 0;
  height: 0;
}

/* Review list transitions */
.review-list-enter-active,
.review-list-leave-active {
  transition: all 0.5s ease;
}
.review-list-enter-from {
  opacity: 0;
  transform: translateY(30px);
}
.review-list-leave-to {
  opacity: 0;
  transform: translateY(-30px);
}

/* Staggered animation for review cards */
.review-card {
  animation: fade-in-up 0.5s ease-out forwards;
  opacity: 0;
}

@keyframes fade-in-up {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Subtle bounce animation */
.animate-bounce-subtle {
  animation: bounce-subtle 2s infinite;
}

@keyframes bounce-subtle {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

/* Fade in animation */
.animate-fade-in {
  animation: fade-in 0.5s ease-out forwards;
}

@keyframes fade-in {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

/* Hover effect */
.hover-effect {
  transition: background-color 0.3s ease;
}
.hover-effect:hover {
  background-color: rgba(79, 70, 229, 0.05);
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  transition: all 0.3s ease;
}

.show-full {
  display: block;
  transition: all 0.3s ease;
}
</style> 