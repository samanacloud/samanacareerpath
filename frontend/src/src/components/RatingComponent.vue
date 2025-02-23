<template>
    <div class="rating-container">
      <div class="stars">
        <span 
          v-for="star in 5" 
          :key="star" 
          class="star" 
          :class="{ 'filled': star <= currentRating }"
          @click="setRating(star)"
          @mouseover="hoverRating = star"
          @mouseleave="hoverRating = 0"
        >
          <i class="pi pi-star" />
        </span>
      </div>
      <div v-if="showValue" class="rating-value">
        {{ currentRating }} / 5
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  
  const props = defineProps({
    initialRating: {
      type: Number,
      default: 0,
      validator: value => value >= 0 && value <= 5
    },
    showValue: {
      type: Boolean,
      default: true
    }
  });
  
  const currentRating = ref(props.initialRating);
  const hoverRating = ref(0);
  
  const setRating = (rating) => {
    currentRating.value = rating;
    // Emit event to parent component
    emit('update:rating', rating);
  };
  </script>
  
  <style scoped>
  .rating-container {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  
  .stars {
    display: flex;
    gap: 0.25rem;
  }
  
  .star {
    cursor: pointer;
    color: #ccc;
    transition: color 0.2s;
  }
  
  .star.filled {
    color: #ffc107;
  }
  
  .star:hover {
    color: #ffc107;
  }
  
  .rating-value {
    font-size: 0.9rem;
    color: #666;
  }
  </style>