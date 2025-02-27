<template>
  <div class="p-4">
    <Toast />
    <ConfirmPopup />
    <!-- Breadcrumb Navigation -->
    <div class="compact-breadcrumb mb-3">
      <Breadcrumb :home="breadcrumbHome" :model="breadcrumbItems" @item-click="navigateTo" />
    </div>
    
    <div v-if="loading" class="text-center p-8">
      <ProgressSpinner style="width: 50px; height: 50px" />
      <p class="mt-2 text-gray-600">Loading candidate profile...</p>
    </div>
    
    <div v-else class="grid grid-cols-12 gap-4">
      <!-- Top Row: Profile, Radar Chart, and Interview Reviews -->
      <div :class="[
        showSkillsRadar ? 'lg:col-span-3' : 'lg:col-span-6',
        'col-span-12 md:col-span-4'
      ]">
        <CandidateBasicInfo 
          :candidateData="candidateData"
          :candidateInitials="candidateInitials"
          :formattedName="formattedName"
          :allSkillsAverage="allSkillsAverage"
          :interviewsCount="interviewsData.length"
          :approvedCounts="approvedCounts"
          :showInterviewForm="showInterviewForm"
          :toggleSkillsetAssessment="toggleSkillsetAssessment"
          :contactCandidate="contactCandidate"
          :isRefreshingSkillAverage="isRefreshingSkillAverage"
          :showSkillsRadar="showSkillsRadar"
          :toggleSkillsRadar="toggleSkillsRadar"
          class="h-full"
        />
      </div>
      
      <!-- Radar Chart Block -->
      <div v-if="showSkillsRadar" class="col-span-12 lg:col-span-6 md:col-span-4">
        <div class="card p-4 h-full flex flex-col radar-chart-container">
          <div class="flex items-center justify-between mb-4">
            <div class="flex items-center gap-2">
              <i class="pi pi-chart-line text-blue-500"></i>
              <h5 class="font-semibold m-0">Skills Radar</h5>
            </div>
            <div class="flex items-center gap-2">
              <div v-if="isRefreshingRadarChart" class="flex items-center">
                <i class="pi pi-spin pi-spinner text-blue-500 mr-2"></i>
                <span class="text-xs text-blue-500">Updating...</span>
              </div>
              <Button 
                icon="pi pi-times" 
                class="p-button-rounded p-button-text p-button-sm" 
                @click="toggleSkillsRadar" 
                v-tooltip.left="'Hide Skills Radar'"
              />
            </div>
          </div>
          <div class="grid grid-cols-1 flex-grow flex items-center justify-center">
            <Chart type="radar" :data="categoryRadarData" :options="radarChartOptions" class="h-full" />
          </div>
        </div>
      </div>
      
      <!-- Interview Reviews Section -->
      <div :class="[
        showSkillsRadar ? 'lg:col-span-3' : 'lg:col-span-6',
        'col-span-12 md:col-span-4'
      ]">
        <div class="card p-4 h-full flex flex-col">
          <div class="flex items-center justify-between mb-4">
            <div class="flex items-center gap-2">
              <i class="pi pi-comments text-indigo-500"></i>
              <h5 class="font-semibold m-0">Interview Reviews</h5>
              <div class="bg-indigo-100 text-indigo-800 text-xs font-medium px-2 py-0.5 rounded-full">
                {{ interviewsData.length }}
              </div>
            </div>
            <!-- Removing the Skills Radar toggle button from here -->
          </div>
          
          <div class="flex-grow overflow-hidden">
            <div v-if="interviewsData.length === 0" class="text-gray-500 italic py-4 text-center h-full flex items-center justify-center">
              No reviews available
            </div>
            <div v-else class="h-full flex flex-col">
              <!-- Review Categories Tabs -->
              <div class="border-b border-gray-200 mb-4">
                <ul class="flex flex-wrap -mb-px text-sm font-medium text-center">
                  <li v-for="(reviews, field) in groupedReviews" :key="field" class="mr-2">
                    <button 
                      @click="selectedReviewCategory = field"
                      class="inline-block p-2 rounded-t-lg"
                      :class="selectedReviewCategory === field 
                        ? 'border-b-2 border-indigo-500 text-indigo-600 active' 
                        : 'border-b-2 border-transparent hover:text-gray-600 hover:border-gray-300'"
                    >
                      {{ field }}
                      <span class="ml-1 bg-gray-100 text-gray-700 text-xs font-medium px-1.5 py-0.5 rounded-full">
                        {{ reviews.length }}
                      </span>
                    </button>
                  </li>
                </ul>
              </div>
              
              <!-- Reviews for Selected Category -->
              <div v-for="(reviews, field) in groupedReviews" :key="field" v-show="selectedReviewCategory === field" class="flex-grow overflow-hidden">
                <div class="grid grid-cols-1 gap-4 max-h-[calc(100%-40px)] overflow-y-auto pr-2">
                  <div 
                    v-for="(review, index) in reviews" 
                    :key="index" 
                    class="bg-gray-50 rounded-lg p-4 border-l-4"
                    :class="{
                      'border-green-500': review.approved === 'Yes',
                      'border-yellow-500': review.approved === 'Pending',
                      'border-red-500': review.approved === 'No'
                    }"
                  >
                    <div class="flex justify-between items-start mb-3">
                      <div>
                        <div class="font-medium text-gray-900">{{ review.interviewedBy }}</div>
                        <div class="text-xs text-gray-500">{{ formatDate(review.createdAt) }}</div>
                      </div>
                      <div :class="{
                        'bg-green-100 text-green-800': review.approved === 'Yes',
                        'bg-yellow-100 text-yellow-800': review.approved === 'Pending',
                        'bg-red-100 text-red-800': review.approved === 'No'
                      }" class="text-xs font-medium px-2 py-0.5 rounded-full">
                        {{ review.approved }}
                      </div>
                    </div>
                    
                    <div class="mb-3">
                      <div class="text-sm text-gray-700 mb-1">Rating:</div>
                      <Rating :modelValue="review.rating" readonly :stars="5" />
                    </div>
                    
                    <div class="mt-3">
                      <div class="text-sm text-gray-700 mb-1">Observations:</div>
                      <p class="text-sm text-gray-600" :class="review.showFullObservation ? 'show-full' : 'line-clamp-3'">
                        {{ review.observations }}
                      </p>
                      <button 
                        v-if="review.observations && review.observations.length > 150" 
                        @click="toggleObservation(review)"
                        class="text-xs text-indigo-600 mt-1 hover:underline"
                      >
                        {{ review.showFullObservation ? 'Show less' : 'Read more' }}
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Middle Row: Forms and Skillsets -->
      <div class="col-span-12 lg:col-span-12 mt-4">
        <!-- Forms and Skillsets in a grid layout on desktop -->
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-4">
          <!-- Left column for skillsets on desktop (moved from right) -->
          <div class="lg:col-span-6">
            <div class="card p-4 skillsets-container">
              <div class="flex items-center justify-between mb-4 cursor-pointer" @click="toggleAllSkillsets">
                <div class="flex items-center gap-2">
                  <i class="pi pi-list text-blue-500"></i>
                  <h5 class="font-semibold m-0">Skillsets</h5>
                  <div class="bg-blue-100 text-blue-800 text-xs font-medium px-2 py-0.5 rounded-full">
                    {{ Object.keys(groupedSkills).length }}
                  </div>
                </div>
                <div class="flex items-center">
                  <div v-if="isRefreshingSkillsets" class="flex items-center mr-2">
                    <i class="pi pi-spin pi-spinner text-blue-500 mr-1"></i>
                    <span class="text-xs text-blue-500">Updating...</span>
                  </div>
                  <i :class="`pi ${areAllSkillsetsCollapsed ? 'pi-chevron-down' : 'pi-chevron-up'} text-gray-500`"></i>
                </div>
              </div>
              
              <div v-if="skillsetData.length === 0" class="text-gray-500 italic">
                No skillset assessments available
              </div>
              <div v-else class="flex flex-wrap gap-2 md:gap-4">
                
                <!-- Dynamic Categories -->
                <div v-for="(skills, category) in groupedSkills" :key="category" class="w-full md:w-[calc(33.333%-1rem)] min-w-[300px]">
                  <fieldset class="border p-2 rounded h-full flex flex-col">
                    <legend class="cursor-pointer" @click="toggleCategory(category)">
                      <div class="flex items-center gap-2">
                        <h6 class="font-semibold">{{ category }}</h6>
                        <div class="flex items-center gap-1">
                          <span class="text-sm font-medium">{{ calculateAverage(skills) }}</span>
                          <i class="pi pi-star-fill text-yellow-500"></i>
                          <i :class="`pi pi-chevron-${isCategoryOpen(category) ? 'up' : 'down'} text-sm ml-1`"></i>
                        </div>
                      </div>
                    </legend>
                    <transition name="fade">
                      <ul v-if="isCategoryOpen(category)" class="flex-1 overflow-y-auto">
                        <li v-for="skill in skills" :key="skill.skillsetName" class="grid grid-cols-[1fr_150px_26px] items-center gap-2 mb-1">
                          <span class="text-sm">{{ skill.skillsetName }}</span>
                          <div class="flex justify-end">
                            <Rating v-model="skill.skillsetRating" readonly :stars="5" 
                                    v-tooltip="`Reviewed by: ${skill.reviewers.map(r => r.name).join(', ')}`" />
                          </div>
                          <div class="text-[10px] bg-gray-100 px-1.5 py-0.5 rounded-full border border-gray-200 text-center w-[26px]"
                               v-tooltip="`${skill.reviewCount} reviews`">
                            {{ skill.reviewCount }}
                          </div>
                        </li>
                      </ul>
                    </transition>
                  </fieldset>
                </div>
              </div>
            </div>
            
            <!-- Certifications Section (conditionally shown below skillsets when expanded) -->
            <div v-if="shouldShowCertificationsBelowSkillsets" class="mb-6">
              <div class="card p-4 mt-4">
                <div class="flex items-center justify-between mb-4 cursor-pointer" @click="toggleCertifications">
                  <div class="flex items-center gap-2">
                    <i class="pi pi-bookmark text-green-500"></i>
                    <h5 class="font-semibold m-0">Certifications</h5>
                    <div class="bg-blue-100 text-blue-800 text-xs font-medium px-2 py-0.5 rounded-full">
                      {{ certificationsData.length }}
                    </div>
                  </div>
                  <i :class="`pi ${isCertificationsCollapsed ? 'pi-chevron-down' : 'pi-chevron-up'} text-gray-500`"></i>
                </div>
                
                <transition name="fade">
                  <div v-if="!isCertificationsCollapsed">
                    <div v-if="certificationsData.length === 0" class="text-gray-500 italic py-4 text-center">
                      No certifications recorded
                    </div>
                    <div v-else class="grid grid-cols-1 gap-4 max-h-[300px] overflow-y-auto pr-2 pb-2">
                      <div 
                        v-for="(certification, index) in certificationsData" 
                        :key="index" 
                        class="bg-gray-50 rounded-lg p-3 border-l-4"
                        :class="isCertificationActive(certification) ? 'border-green-500' : 'border-red-500'"
                      >
                        <div class="flex justify-between items-start">
                          <div class="flex-1">
                            <h6 class="font-medium text-gray-900 mb-1 line-clamp-2">{{ certification.certificationName }}</h6>
                            
                            <div class="flex items-center text-xs text-gray-500 mt-2">
                              <i class="pi pi-calendar mr-1"></i>
                              <span>Expires: {{ formatDate(certification.certificationExpiration) }}</span>
                            </div>
                          </div>
                          <Tag 
                            :value="isCertificationActive(certification) ? 'active' : 'expired'"
                            :severity="isCertificationActive(certification) ? 'success' : 'danger'"
                            class="text-xs ml-2 shrink-0"
                          />
                        </div>
                      </div>
                    </div>
                  </div>
                </transition>
              </div>
            </div>
          </div>
          
          <!-- Right column for forms and two analytics charts -->
          <div class="lg:col-span-6">
            <!-- Interview Card (not modal anymore) -->
            <div v-if="showInterviewModal" ref="interviewCard" class="interview-card card mb-6 p-4 shadow-md border border-gray-200">
              <div class="flex justify-between items-center mb-4">
                <h3 class="text-xl font-bold text-indigo-700">Interview Candidate</h3>
                <Button icon="pi pi-times" class="p-button-rounded p-button-text" @click="closeInterviewForm" />
              </div>
              
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                <div class="field">
                  <label for="candidateName" class="block text-sm font-medium text-gray-700 mb-1">Candidate Name</label>
                  <InputText id="candidateName" v-model="newInterview.candidateName" disabled class="w-full" />
                </div>
                
                <div class="field">
                  <label for="evaluationField" class="block text-sm font-medium text-gray-700 mb-1">Evaluation Field</label>
                  <Select id="evaluationField" v-model="newInterview.evaluationField" :options="evaluationFields" 
                            placeholder="Select a field" class="w-full" />
                </div>
                
                <div class="field">
                  <label for="rating" class="block text-sm font-medium text-gray-700 mb-1">Rating</label>
                  <Rating v-model="newInterview.rating" :stars="5" />
                </div>
                
                <div class="field">
                  <label for="approved" class="block text-sm font-medium text-gray-700 mb-1">Approval Status</label>
                  <Select id="approved" v-model="newInterview.approved" :options="approvalOptions" 
                            optionLabel="label" optionValue="value" placeholder="Select status" class="w-full" />
                </div>
              </div>
              
              <div class="field mb-4">
                <label for="observations" class="block text-sm font-medium text-gray-700 mb-1">Observations</label>
                <Textarea id="observations" v-model="newInterview.observations" rows="3" class="w-full" />
              </div>
              
              <div class="flex justify-end gap-2">
                <Button label="Cancel" class="p-button-outlined" @click="closeInterviewForm" />
                <Button label="Submit Review" severity="success" @click="confirmSubmit" />
              </div>
            </div>

            <!-- Skillset Assessment Form -->
            <div v-if="showSkillsetAssessment" ref="skillsetAssessmentCard" class="card p-4 mb-4">
              <div class="flex items-center justify-between mb-4">
                <div class="flex items-center gap-2">
                  <i class="pi pi-star text-blue-500"></i>
                  <h5 class="font-semibold m-0">Quick Skillset Rating</h5>
                </div>
                <Button icon="pi pi-times" class="p-button-rounded p-button-text" @click="toggleSkillsetAssessment" />
              </div>
              
              <!-- Search and Filter -->
              <div class="mb-4 grid grid-cols-1 md:grid-cols-12 gap-4">
                <!-- Search Input -->
                <div class="md:col-span-5">
                  <span class="p-input-icon-left w-full">
                    <i class="pi pi-search" />
                    <InputText 
                      v-model="skillsetSearchQuery" 
                      placeholder="Search skillsets..." 
                      class="w-full"
                      @input="debounceSearch"
                    />
                  </span>
                </div>
                
                <!-- Categories Filter -->
                <div class="md:col-span-7">
                  <h6 class="text-sm font-medium text-gray-700 mb-2">Filter by Category</h6>
                  <div v-if="isLoadingCategories" class="flex justify-center py-2">
                    <ProgressSpinner style="width: 30px; height: 30px" />
                  </div>
                  <div v-else-if="skillsetCategories.length === 0" class="text-gray-500 italic py-2 text-center">
                    No categories available
                  </div>
                  <div v-else class="flex flex-wrap gap-1">
                    <Chip 
                      key="all"
                      label="All Categories"
                      :class="{ 
                        'bg-primary-500 text-gray-900 font-bold shadow-lg': quickRatingFilter === null,
                        'hover:bg-primary-50 hover:text-primary-500 hover:shadow-lg transition-all duration-200': true
                      }"
                      @click="quickRatingFilter = null"
                      class="cursor-pointer border-1 border-transparent bg-surface-100 shadow-sm text-xs px-2 py-1"
                    />
                    <Chip 
                      v-for="category in skillsetCategories" 
                      :key="category"
                      :label="category"
                      :class="{ 
                        'bg-primary-500 text-gray-900 font-bold shadow-lg': quickRatingFilter === category,
                        'hover:bg-primary-50 hover:text-primary-500 hover:shadow-lg transition-all duration-200': true
                      }"
                      @click="quickRatingFilter = category"
                      class="cursor-pointer border-1 border-transparent bg-surface-100 shadow-sm text-xs px-2 py-1"
                    />
                  </div>
                </div>
              </div>
              
              <!-- Skillsets Rating List -->
              <div class="mb-4">
                <div v-if="isLoadingCompanySkillsets" class="flex justify-center py-4">
                  <ProgressSpinner style="width: 50px; height: 50px" />
                </div>
                <div v-else-if="filteredAndSearchedSkillsets.length === 0" class="text-gray-500 italic py-8 text-center">
                  <div class="flex flex-col items-center">
                    <i v-if="quickRatingFilter && Object.keys(alreadyRatedSkillsets.value).length > 0" 
                       class="pi pi-check-circle text-green-500 text-4xl mb-2"></i>
                    <i v-else class="pi pi-search text-gray-300 text-4xl mb-2"></i>
                    <p v-if="quickRatingFilter && Object.keys(alreadyRatedSkillsets.value).length > 0">
                      You've rated all skillsets in this category
                    </p>
                    <p v-else>No skillsets found matching your criteria</p>
                    <p class="text-sm mt-1">
                      <span v-if="quickRatingFilter && Object.keys(alreadyRatedSkillsets.value).length > 0">
                        Check the "Your Previous Ratings" section below
                      </span>
                      <span v-else>Try adjusting your search or filter</span>
                    </p>
                  </div>
                </div>
                <div v-else>
                  <!-- Category Title -->
                  <div class="mb-3 flex items-center justify-between">
                    <h6 class="font-medium text-gray-800">
                      <span v-if="quickRatingFilter">{{ quickRatingFilter }} Skillsets</span>
                      <span v-else>All Skillsets</span>
                    </h6>
                    <div class="text-xs text-gray-500">
                      {{ filteredAndSearchedSkillsets.length }} skillset(s)
                    </div>
                  </div>
                  
                  <div class="bg-gray-50 p-2 rounded-t-lg grid grid-cols-12 gap-2 font-medium text-sm border-b">
                    <div class="col-span-9">Skillset</div>
                    <div class="col-span-3 text-center">Rating</div>
                  </div>
                  
                  <div class="max-h-[400px] overflow-y-auto">
                    <div 
                      v-for="skillset in filteredAndSearchedSkillsets" 
                      :key="skillset.id" 
                      class="grid grid-cols-12 gap-2 p-3 border-b hover:bg-gray-50 items-center"
                      :class="{'bg-primary-50': pendingRatings[skillset.id] !== undefined}"
                    >
                      <div class="col-span-9">
                        <div class="font-medium text-sm flex items-center gap-1">
                          <span>{{ skillset.name }}</span>
                          <Button 
                            v-if="skillset.description && isMobileView" 
                            icon="pi pi-info-circle" 
                            class="p-button-text p-button-rounded p-button-sm text-gray-500 hover:text-primary-500"
                            @click.stop="showMobileDescription(skillset.description)"
                            type="button"
                            aria-label="View description"
                          />
                        </div>
                        <div class="text-xs text-gray-500 hidden md:block">{{ truncateDescription(skillset.description) }}</div>
                      </div>
                      <div class="col-span-3 flex justify-center">
                        <Rating 
                          v-model="pendingRatings[skillset.id]" 
                          :stars="5" 
                          :disabled="isSubmittingQuickRating[skillset.id]"
                          @change="rateSkillset(skillset)"
                        />
                        <div v-if="isSubmittingQuickRating[skillset.id]" class="ml-2">
                          <i class="pi pi-spin pi-spinner text-primary-500"></i>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- Already Rated Skillsets Section -->
              <div v-if="hasRatedSkillsetsInCategory" class="mt-4 border-t pt-4">
                <div class="mb-3 flex items-center justify-between">
                  <h6 class="font-medium text-gray-800 flex items-center gap-2">
                    <span>Your Previous Ratings</span>
                    <span class="bg-blue-100 text-blue-800 text-xs font-medium px-2 py-0.5 rounded-full">
                      Already Rated
                    </span>
                    <Button 
                      @click="toggleAlreadyRatedSkillsets" 
                      :icon="showAlreadyRatedSkillsets ? 'pi pi-chevron-up' : 'pi pi-chevron-down'" 
                      class="p-button-text p-button-rounded p-button-sm"
                      aria-label="Toggle previous ratings"
                    />
                  </h6>
                  <div class="text-xs text-gray-500">
                    {{ ratedSkillsetsInCategory.length }} skillset(s)
                  </div>
                </div>
                
                <div v-if="showAlreadyRatedSkillsets">
                  <div class="bg-gray-50 p-2 rounded-t-lg grid grid-cols-12 gap-2 font-medium text-sm border-b">
                    <div class="col-span-8">Skillset</div>
                    <div class="col-span-3 text-center">Your Rating</div>
                    <div class="col-span-1 text-center">Actions</div>
                  </div>
                  
                  <div class="max-h-[200px] overflow-y-auto">
                    <div 
                      v-for="skillset in ratedSkillsetsInCategory" 
                      :key="skillset.id" 
                      class="grid grid-cols-12 gap-2 p-3 border-b hover:bg-gray-50 items-center bg-gray-100"
                    >
                      <div class="col-span-8">
                        <div class="font-medium text-sm flex items-center gap-1">
                          <span>{{ skillset.skillsetName }}</span>
                        </div>
                        <div class="text-xs text-gray-500">{{ skillset.skillsetCategory }}</div>
                      </div>
                      <div class="col-span-3 flex justify-center">
                        <Rating 
                          :modelValue="skillset.skillsetRating" 
                          :stars="5" 
                          disabled
                        />
                      </div>
                      <div class="col-span-1 flex justify-center">
                        <Button
                          icon="pi pi-trash"
                          class="p-button-rounded p-button-danger p-button-text p-button-sm"
                          @click="confirmDeleteSkillset(skillset, $event)"
                          :disabled="isDeletingSkillset[skillset.id]"
                          aria-label="Delete rating"
                        />
                        <div v-if="isDeletingSkillset[skillset.id]" class="ml-2">
                          <i class="pi pi-spin pi-spinner text-primary-500"></i>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- Existing Ratings Summary -->
              <div v-if="hasSubmittedRatings" class="mt-4 p-3 bg-green-50 rounded-lg border border-green-200">
                <div class="flex items-center gap-2 text-green-700 mb-2">
                  <i class="pi pi-check-circle"></i>
                  <span class="font-medium">Successfully Rated Skillsets</span>
                </div>
                <p class="text-sm text-green-600">
                  You've rated {{ submittedRatingsCount }} skillset(s) for this candidate. These ratings will help evaluate their technical proficiency.
                </p>
              </div>
            </div>
            
            <!-- Certifications Section (shown on right when skillsets are collapsed) -->
            <div v-if="!shouldShowCertificationsBelowSkillsets" class="mb-6">
              <div class="card p-4">
                <div class="flex items-center justify-between mb-4 cursor-pointer" @click="toggleCertifications">
                  <div class="flex items-center gap-2">
                    <i class="pi pi-bookmark text-green-500"></i>
                    <h5 class="font-semibold m-0">Certifications</h5>
                    <div class="bg-blue-100 text-blue-800 text-xs font-medium px-2 py-0.5 rounded-full">
                      {{ certificationsData.length }}
                    </div>
                  </div>
                  <i :class="`pi ${isCertificationsCollapsed ? 'pi-chevron-down' : 'pi-chevron-up'} text-gray-500`"></i>
                </div>
                
                <transition name="fade">
                  <div v-if="!isCertificationsCollapsed">
                    <div v-if="certificationsData.length === 0" class="text-gray-500 italic py-4 text-center">
                      No certifications recorded
                    </div>
                    <div v-else class="grid grid-cols-1 gap-4 max-h-[300px] overflow-y-auto pr-2 pb-2">
                      <div 
                        v-for="(certification, index) in certificationsData" 
                        :key="index" 
                        class="bg-gray-50 rounded-lg p-3 border-l-4"
                        :class="isCertificationActive(certification) ? 'border-green-500' : 'border-red-500'"
                      >
                        <div class="flex justify-between items-start">
                          <div class="flex-1">
                            <h6 class="font-medium text-gray-900 mb-1 line-clamp-2">{{ certification.certificationName }}</h6>
                            
                            <div class="flex items-center text-xs text-gray-500 mt-2">
                              <i class="pi pi-calendar mr-1"></i>
                              <span>Expires: {{ formatDate(certification.certificationExpiration) }}</span>
                            </div>
                          </div>
                          <Tag 
                            :value="isCertificationActive(certification) ? 'active' : 'expired'"
                            :severity="isCertificationActive(certification) ? 'success' : 'danger'"
                            class="text-xs ml-2 shrink-0"
                          />
                        </div>
                      </div>
                    </div>
                  </div>
                </transition>
              </div>
            </div>
            
            <!-- Two analytics charts in the right column -->
            <div v-if="isAnyCategoryOpen" class="grid grid-cols-1 gap-4 mb-4">
              <!-- Radar Chart -->
              <div>
                <SkillsetRadarChart 
                  :radarChartData="radarChartData" 
                  :radarChartOptions="radarChartOptions" 
                />
              </div>
              <!-- Knowledge Distribution Chart -->
              <div>
                <KnowledgeDistributionChart 
                  :pieChartData="pieChartData" 
                  :chartOptions="chartOptions" 
                />
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Bottom Row: Two more analytics charts -->
      <div v-if="isAnyCategoryOpen" class="col-span-12 mt-4">
        <div class="mb-3">
          <h5 class="font-semibold">Candidate Analytics - {{ selectedCategory }}</h5>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <SkillsetAverageChart 
            :basicChartData="basicChartData" 
            :chartOptions="chartOptions" 
          />
          
          <SkillsetDistributionChart 
            :verticalBarChartData="verticalBarChartData" 
            :chartOptions="chartOptions" 
          />
        </div>
      </div>
      
      <!-- Metadata Section -->
      <div class="col-span-12 mt-6">
        <CandidateMetadata :candidateData="candidateData" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, onBeforeUnmount } from "vue";
import { useRoute, useRouter } from "vue-router";
import Chart from 'primevue/chart';
import Rating from 'primevue/rating';
import Avatar from 'primevue/avatar';
import Button from 'primevue/button';
import Tag from 'primevue/tag';
import Breadcrumb from 'primevue/breadcrumb';
import ProgressSpinner from 'primevue/progressspinner';
import Select from 'primevue/select';
import Textarea from 'primevue/textarea';
import InputText from 'primevue/inputtext';
import InputNumber from 'primevue/inputnumber';
import Toast from 'primevue/toast';
import { useToast } from 'primevue/usetoast';
import ConfirmPopup from 'primevue/confirmpopup';
import Chip from 'primevue/chip';
import SkillsetRadar from '@/components/careerpath/SkillsetRadar.vue';
import Certifications from '@/components/careerpath/Certifications.vue';
import CandidateBasicInfo from '@/components/careerpath/CandidateBasicInfo.vue';
import InterviewReviews from '@/components/careerpath/InterviewReviews.vue';
import CandidateMetadata from '@/components/careerpath/CandidateMetadata.vue';
import { useConfirm } from 'primevue/useconfirm';
import SkillsetAverageChart from '@/components/careerpath/SkillsetAverageChart.vue';
import KnowledgeDistributionChart from '@/components/careerpath/KnowledgeDistributionChart.vue';
import SkillsetDistributionChart from '@/components/careerpath/SkillsetDistributionChart.vue';
import SkillsetRadarChart from '@/components/careerpath/SkillsetRadarChart.vue';

const route = useRoute();
const router = useRouter();
const loading = ref(true);
const toast = useToast();
const confirm = useConfirm();

// Add this at the top of the script section, with other reactive variables
const showSkillsetAssessment = ref(false);
const skillsetAssessmentCard = ref(null);

// Breadcrumb configuration
const breadcrumbHome = ref({ icon: 'pi pi-home', to: '/' });
const breadcrumbItems = computed(() => {
  // Use shorter labels on mobile
  const isMobile = window.innerWidth < 640;
  
  return [
    { 
      label: isMobile ? 'Career' : 'Career Path', 
      to: '/careerpath' 
    },
    { 
      label: 'Candidates', 
      command: () => router.go(-1) 
    },
    { 
      label: isMobile 
        ? (candidateData.value.candidateName ? formattedName.value.split(' ')[0] : 'Profile')
        : (candidateData.value.candidateName ? formattedName.value : 'Profile'), 
      disabled: true 
    }
  ];
});

// Updated candidateData
const candidateData = ref({
    id: "",
    candidateName: "",  // Changed from 'name' to 'candidateName'
    companyId: "",
    companyName: "",
    email: "",
    country: "",
    role: "",
    phone: "",
    status: "active",
    createdAt: "",
    updatedAt: "",
    salaryExpectation: "",
    candidateCV: "",
    recruitmentProcessId: "",
    recruitmentProcessName: ""
});

// Update the computed properties with null checks
const candidateInitials = computed(() => {
  const name = candidateData.value.candidateName || '';
  const names = name.trim().split(' ');
  
  if (names.length >= 2) {
    return (names[0][0] + names[names.length-1][0]).toUpperCase();
  } else if (names[0]?.length > 0) {
    return names[0][0].toUpperCase();
  }
  return ''; // Return empty string if no name
});

const formattedName = computed(() => {
  const name = candidateData.value.candidateName || '';
  return name
    .split(' ')
    .map(word => word.charAt(0).toUpperCase() + (word.slice(1) || '').toLowerCase())
    .join(' ');
});

// Function to generate a random integer from 0 to 5
const randomRating = () => Math.floor(Math.random() * 6);

// Random ratings for each category
const windowsRatings = {
  'Windows Server': randomRating(),
  'Active Directory': randomRating(),
  'PowerShell': randomRating(),
  'Azure': randomRating(),
  'Office 365': randomRating()
};

const linuxRatings = {
  'Ubuntu': randomRating(),
  'CentOS': randomRating(),
  'RedHat': randomRating(),
  'Debian': randomRating(),
  'Fedora': randomRating()
};

const networkingRatings = {
  'TCP/IP': randomRating(),
  'DNS': randomRating(),
  'DHCP': randomRating(),
  'Routing': randomRating(),
  'Switching': randomRating()
};

// Updated aggregateRating to return a number instead of a string
const aggregateRating = (ratingsObj) => {
  const values = Object.values(ratingsObj);
  const sum = values.reduce((a, b) => a + b, 0);
  return parseFloat((sum / values.length).toFixed(1));
};

// Aggregated ratings for charts
const aggregatedWindowsRating = aggregateRating(windowsRatings);
const aggregatedLinuxRating = aggregateRating(linuxRatings);
const aggregatedNetworkingRating = aggregateRating(networkingRatings);

// Add reactive selected category
const selectedCategory = ref('Windows');

// Update the toggleCategory function to set the selected category
const toggleCategory = (category) => {
  selectedCategory.value = category;
  if (openCategories.value.has(category)) {
    openCategories.value.delete(category);
  } else {
    openCategories.value.add(category);
  }
};

// Update chart data computations to use selected category
const basicChartData = computed(() => {
  const skills = groupedSkills.value[selectedCategory.value] || [];
  return {
    labels: [selectedCategory.value],
    datasets: [{
      label: 'Average Skill Level',
      backgroundColor: ['rgba(249, 115, 22, 0.2)'],
      borderColor: ['rgb(249, 115, 22)'],
      borderWidth: 1,
      data: [calculateAverage(skills)]
    }]
  };
});

const pieChartData = computed(() => {
  const skills = groupedSkills.value[selectedCategory.value] || [];
  return {
    labels: skills.map(skill => skill.skillsetName),
    datasets: [{
      data: skills.map(skill => skill.skillsetRating),
      backgroundColor: [
        'rgba(66, 165, 245, 0.2)',    // #42A5F5 with 0.2 alpha
        'rgba(102, 187, 106, 0.2)',   // #66BB6A with 0.2 alpha
        'rgba(255, 167, 38, 0.2)',    // #FFA726 with 0.2 alpha
        'rgba(255, 99, 132, 0.2)',    // #FF6384 with 0.2 alpha
        'rgba(54, 162, 235, 0.2)',   // #36A2EB with 0.2 alpha
        'rgba(255, 206, 86, 0.2)'     // #FFCE56 with 0.2 alpha
      ],
      borderColor: [
        'rgb(66, 165, 245)',
        'rgb(102, 187, 106)',
        'rgb(255, 167, 38)',
        'rgb(255, 99, 132)',
        'rgb(54, 162, 235)',
        'rgb(255, 206, 86)'
      ],
      borderWidth: 1
    }]
  };
});

const verticalBarChartData = computed(() => {
  const skills = groupedSkills.value[selectedCategory.value] || [];
  return {
    labels: skills.map(skill => skill.skillsetName),
    datasets: [{
      label: 'Skill Ratings',
      backgroundColor: 'rgba(66, 165, 245, 0.2)',
      borderColor: 'rgb(66, 165, 245)',
      borderWidth: 1,
      data: skills.map(skill => skill.skillsetRating)
    }]
  };
});

const radarChartData = computed(() => {
  const skills = groupedSkills.value[selectedCategory.value] || [];
  return {
    labels: skills.map(skill => skill.skillsetName),
    datasets: [{
      label: 'Skill Ratings',
      data: skills.map(skill => skill.skillsetRating),
      backgroundColor: 'rgba(179,181,198,0.2)',
      borderColor: 'rgba(179,181,198,1)',
      borderWidth: 1
    }]
  };
});

// Added new radarChartOptions with a fixed max of 5
const radarChartOptions = ref({
  scales: {
    r: {
      min: 0,
      max: 5,
      ticks: {
        stepSize: 1,
        color: '#646464'
      }
    }
  },
  plugins: {
    legend: {
      labels: {
        color: '#646464'
      }
    }
  }
});

// Add date formatting function
const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
};

// Add formattedDate computed property
const formattedDate = computed(() => {
  return formatDate(candidateData.value.createdAt);
});

// Update formattedSalary
const formattedSalary = computed(() => {
  return candidateData.value.salaryExpectation 
    ? new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
      }).format(candidateData.value.salaryExpectation)
    : 'Not specified';
});

// Add approvedCounts computed property
const approvedCounts = computed(() => {
  return interviewsData.value.reduce((acc, review) => {
    const status = review.approved?.toLowerCase() || 'pending';
    acc[status] += 1;
    return acc;
  }, { yes: 0, pending: 0, no: 0 });
});

// Add reviewCandidate function
const reviewCandidate = () => {
  // Implement review logic
  console.log('Reviewing candidate...');
};

// Add scheduleInterview function
const scheduleInterview = () => {
  // Implement interview scheduling logic
  console.log('Scheduling interview...');
};

// Add contactCandidate function
const contactCandidate = () => {
  // Get user info from localStorage
  const userName = localStorage.getItem('userName') || 'a recruiter';
  const companyName = localStorage.getItem('companyName') || 'Samana Group';
  const subject = `Regarding your application for ${candidateData.value.recruitmentProcessName}`;
  const body = `Hello, Nice to meet you! My name is ${userName} from ${companyName} and I would like to ask you some questions regarding the application you recently sent us for the role ${candidateData.value.recruitmentProcessName}`;
  
  // Open Gmail with pre-filled message
  window.open(`https://mail.google.com/mail/?view=cm&fs=1&to=${candidateData.value.email}&su=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`, '_blank');
};

// Update skillsetData - remove candidateId from all entries
const skillsetData = ref([]);

// In script setup section, add the query and fetch logic
const GET_SKILLSETS_BY_EMAIL = `
  query GetSkillsetsByEmail($email: String!) {
    getSkillsetsByEmail(email: $email) {
      id
      skillsetCategory
      skillsetName
      skillsetRating
      reviewedBy
      reviewerEmail
      companyId
      companyName
      email
      createdAt
    }
  }
`;

async function fetchSkillsets() {
  try {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/graphql`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query: GET_SKILLSETS_BY_EMAIL,
        variables: { email: candidateData.value.email }
      })
    });

    const result = await response.json();
    console.log('Fetched skillsets result:', result);
    
    // Special handling for _id error
    if (result.errors && result.errors.some(e => e.message.includes('_id'))) {
      console.warn('Received _id error in fetchSkillsets, but continuing with data processing');
      // Continue with data processing even with the _id error
    } else if (result.errors) {
      throw new Error(result.errors[0]?.message || 'Failed to load skillsets');
    }
    
    // Process the data to ensure we have the correct field names
    // This will transform any _id fields to id if needed
    const processedData = (result.data?.getSkillsetsByEmail || []).map(skill => {
      // Create a clean copy of the skill object
      const cleanSkill = { ...skill };
      
      // If the skill has _id but no id, convert it
      if (cleanSkill._id && !cleanSkill.id) {
        cleanSkill.id = cleanSkill._id;
        delete cleanSkill._id;
      }
      
      return cleanSkill;
    });
    
    skillsetData.value = processedData;
  } catch (error) {
    console.error('Error fetching skillsets:', error);
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: error.message || 'Failed to load skillsets',
      life: 3000
    });
  }
}

// Update the groupedSkills computed property to average duplicate skills
const groupedSkills = computed(() => {
  const skillsMap = new Map();
  
  // First pass to aggregate skills and calculate averages
  skillsetData.value.forEach(skill => {
    const key = `${skill.skillsetCategory}-${skill.skillsetName}`;
    if (!skillsMap.has(key)) {
      skillsMap.set(key, {
        ...skill,
        totalRating: skill.skillsetRating,
        reviewCount: 1,
        reviewers: [{
          name: skill.reviewedBy,
          email: skill.reviewerEmail
        }]
      });
    } else {
      const existing = skillsMap.get(key);
      existing.totalRating += skill.skillsetRating;
      existing.reviewCount++;
      existing.reviewers.push({
        name: skill.reviewedBy,
        email: skill.reviewerEmail
      });
    }
  });

  // Create averaged skills array
  const averagedSkills = Array.from(skillsMap.values()).map(skill => ({
    ...skill,
    skillsetRating: Math.round((skill.totalRating / skill.reviewCount) * 2) / 2, // Rounds to nearest 0.5
    reviewedBy: skill.reviewers.map(r => r.name).join(', '),
    reviewerEmail: skill.reviewers.map(r => r.email).join(', ')
  }));

  // Group averaged skills by category
  const groups = {};
  averagedSkills.forEach(skill => {
    if (!groups[skill.skillsetCategory]) {
      groups[skill.skillsetCategory] = [];
    }
    groups[skill.skillsetCategory].push(skill);
  });
  
  // Sort skills within each category alphabetically
  Object.keys(groups).forEach(category => {
    groups[category].sort((a, b) => a.skillsetName.localeCompare(b.skillsetName));
  });
  
  // Create a sorted version of the groups object
  const sortedGroups = {};
  Object.keys(groups).sort().forEach(category => {
    sortedGroups[category] = groups[category];
  });
  
  return sortedGroups;
});

// Calculate average rating for a category
const calculateAverage = (skills) => {
  const ratings = skills.map(skill => skill.skillsetRating);
  const sum = ratings.reduce((a, b) => a + b, 0);
  return (sum / ratings.length).toFixed(1);
};

// Function to get initials from a full name
const getInitials = (fullName) => {
  const names = fullName.split(' ');
  if (names.length >= 2) {
    return (names[0][0] + names[names.length - 1][0]).toUpperCase();
  }
  return names[0][0].toUpperCase();
};

// Add state for open/closed categories
const openCategories = ref(new Set());

// Check if category is open
const isCategoryOpen = (category) => openCategories.value.has(category);

// Add computed property to check if any category is open
const isAnyCategoryOpen = computed(() => openCategories.value.size > 0);

// Update chartOptions with dynamic colors
const chartOptions = computed(() => {
  const documentStyle = getComputedStyle(document.documentElement);
  const textColor = documentStyle.getPropertyValue('--p-text-color');
  const textColorSecondary = documentStyle.getPropertyValue('--p-text-muted-color');
  const surfaceBorder = documentStyle.getPropertyValue('--p-content-border-color');

  return {
    plugins: {
      legend: {
        labels: {
          color: textColor
        }
      }
    },
    scales: {
      x: {
        ticks: {
          color: textColorSecondary
        },
        grid: {
          color: surfaceBorder
        }
      },
      y: {
        beginAtZero: true,
        max: 5,
        ticks: {
          stepSize: 1,
          color: textColorSecondary
        },
        grid: {
          color: surfaceBorder
        }
      }
    }
  };
});

// Add interview query
const GET_INTERVIEWS = `
  query GetInterviewsByEmail($email: String!) {
    getInterviewsByEmail(email: $email) {
      id
      evaluationField
      rating
      interviewedBy
      interviewerEmail
      approved
      observations
      createdAt
    }
  }
`;

// Replace reviewsData with interviewsData
const interviewsData = ref([]);

// Add fetchInterviews function
async function fetchInterviews() {
  try {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/graphql`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query: GET_INTERVIEWS,
        variables: { email: candidateData.value.email }
      })
    });

    const result = await response.json();
    if (result.errors) {
      throw new Error(result.errors[0]?.message || 'Failed to load interviews');
    }
    
    interviewsData.value = result.data.getInterviewsByEmail || [];
  } catch (error) {
    console.error('Error fetching interviews:', error);
  }
}

// Add mobile detection
const isMobileView = ref(false);

// Function to check if we're on a mobile device
const checkMobileView = () => {
  isMobileView.value = window.innerWidth < 768;
};

// Update onMounted to check mobile view
onMounted(async () => {
  // Initialize UI state based on screen size
  checkScreenSize();
  checkMobileView();
  window.addEventListener('resize', checkScreenSize);
  window.addEventListener('resize', checkMobileView);
  
  const candidateId = route.params.id;
  
  if (!candidateId) {
    router.push('/careerpath');
    return;
  }
  
  try {
    loading.value = true;
    await fetchCandidate();
    
    if (candidateData.value.email) {
      await Promise.all([
        fetchSkillsets(),
        fetchInterviews(),
        fetchCertifications()
      ]);
    }
  } catch (error) {
    console.error('Error loading candidate data:', error);
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: 'Failed to load candidate data',
      life: 3000
    });
  } finally {
    loading.value = false;
  }
  
  // Test available mutations
  await testAvailableMutations();
});

// Update groupedReviews to use interviewsData
const groupedReviews = computed(() => {
  const groups = {};
  interviewsData.value.forEach(review => {
    const field = review.evaluationField;
    if (!groups[field]) {
      groups[field] = [];
    }
    groups[field].push(review);
  });
  
  // Create a new sorted object with alphabetically sorted keys
  const sortedGroups = {};
  Object.keys(groups).sort().forEach(field => {
    sortedGroups[field] = groups[field];
  });
  
  return sortedGroups;
});

// Update allSkillsAverage to handle empty skillset
const allSkillsAverage = computed(() => {
  if(skillsetData.value.length === 0) return 'N/A';
  const total = skillsetData.value.reduce((acc, skill) => acc + skill.skillsetRating, 0);
  return (total / skillsetData.value.length).toFixed(1);
});

// Add to the script section
const isCertificationsExpanded = ref(false);
const isReviewsExpanded = ref(false);
const selectedReviewCategory = ref('');
const areAllSkillsetsCollapsed = ref(true);
const isCertificationsCollapsed = ref(true);

// Add toggle function for certifications in collapsed view
const toggleCertifications = () => {
  isCertificationsCollapsed.value = !isCertificationsCollapsed.value;
};

// Watch for changes in areAllSkillsetsCollapsed to auto-expand reviews but keep certifications collapsed
watch(() => areAllSkillsetsCollapsed.value, (newValue) => {
  if (newValue === true) {
    // When skillsets are collapsed, auto-expand reviews but keep certifications collapsed
    isReviewsExpanded.value = true;
    isCertificationsCollapsed.value = true;
  }
}, { immediate: true });

// Function to toggle full observation text
const toggleObservation = (review) => {
  if (!review.showFullObservation) {
    review.showFullObservation = true;
  } else {
    review.showFullObservation = false;
  }
};

// Set the first review category as default when reviews are loaded
watch(() => interviewsData.value, (newInterviews) => {
  if (newInterviews.length > 0 && Object.keys(groupedReviews.value).length > 0) {
    selectedReviewCategory.value = Object.keys(groupedReviews.value)[0];
  }
}, { immediate: true });

// Add to the script section
const certificationsData = ref([]);

// Update the GET_CERTIFICATIONS query to match the schema
const GET_CERTIFICATIONS = `
  query GetAssignedCertificationsByEmail($email: String!) {
    getAssignedCertificationsByEmail(email: $email) {
      companyId
      companyName
      email
      certificationName
      certificationExpiration
      createdAt
      updatedAt
    }
  }
`;

// Add fetchCertifications function
async function fetchCertifications() {
  try {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/graphql`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query: GET_CERTIFICATIONS,
        variables: { email: candidateData.value.email }
      })
    });

    const result = await response.json();
    if (result.errors) {
      throw new Error(result.errors[0]?.message || 'Failed to load certifications');
    }
    
    certificationsData.value = result.data.getAssignedCertificationsByEmail || [];
  } catch (error) {
    console.error('Error fetching certifications:', error);
    // Add error handling/toast notification if needed
  }
}

// Update isCertificationActive to use the new data structure
const isCertificationActive = (certification) => {
  const expirationDate = new Date(certification.certificationExpiration);
  return expirationDate > new Date();
};

// Update the GET_CANDIDATE query with all requested fields
const GET_CANDIDATE = `
  query GetCandidate($id: String!) {
    candidate(id: $id) {
      id
      candidateCV
      salaryExpectation
      recruitmentProcessId
      phone
      candidateName
      companyId
      companyName
      country
      createdAt
      email
      recruitmentProcessName
      updatedAt
      status
    }
  }
`;

// Simplified fetch candidate function
async function fetchCandidate() {
  try {
    loading.value = true;
    const response = await fetch(`${import.meta.env.VITE_API_URL}/graphql`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query: GET_CANDIDATE,
        variables: { id: route.params.id } // Directly use route param
      })
    });

    const result = await response.json();
    if (result.errors) {
      throw new Error(result.errors[0]?.message || 'Failed to load candidate');
    }

    candidateData.value = {
      ...candidateData.value, // Keep existing dummy data as fallback
      ...result.data.candidate // Override with actual data
    };
  } catch (error) {
    console.error('Error fetching candidate:', error);
  } finally {
    loading.value = false;
  }
}

// Watch for route changes - simplified version
watch(() => route.params.id, async (newId) => {
  if (newId) {
    await fetchCandidate();
  }
});

// Add new computed property for category averages
const categoryAverages = computed(() => {
  return Object.entries(groupedSkills.value)
    .map(([category, skills]) => ({
      category,
      average: calculateAverage(skills)
    }))
    .sort((a, b) => a.category.localeCompare(b.category));
});

// Add new radar chart data for category averages
const categoryRadarData = computed(() => {
  return {
    labels: categoryAverages.value.map(item => item.category),
    datasets: [{
      label: 'Skillset Radar',
      data: categoryAverages.value.map(item => item.average),
      backgroundColor: 'rgba(54, 162, 235, 0.2)',
      borderColor: 'rgba(54, 162, 235, 1)',
      borderWidth: 1
    }]
  };
});

// Add navigation function for breadcrumb
const navigateTo = (event) => {
  if (event.item) {
    if (event.item.command) {
      event.item.command();
    } else if (event.item.to) {
      router.push(event.item.to);
    }
  }
};

// Add toggleAllSkillsets function
const toggleAllSkillsets = () => {
  areAllSkillsetsCollapsed.value = !areAllSkillsetsCollapsed.value;
  
  // If we're expanding skillsets, close any open categories
  if (!areAllSkillsetsCollapsed.value) {
    openCategories.value.clear();
  }
  
  // When skillsets are collapsed, ensure a review category is selected
  if (areAllSkillsetsCollapsed.value && interviewsData.value.length > 0) {
    if (!selectedReviewCategory.value && Object.keys(groupedReviews.value).length > 0) {
      selectedReviewCategory.value = Object.keys(groupedReviews.value)[0];
    }
  }
};

// Check if we should collapse skillsets based on screen size
const checkScreenSize = () => {
  // Always keep skillsets collapsed by default for better visibility of certifications and interviews
  areAllSkillsetsCollapsed.value = true;
};

// Clean up resize listener
onBeforeUnmount(() => {
  window.removeEventListener('resize', checkScreenSize);
  window.removeEventListener('resize', checkMobileView);
});

// Add new state for interview modal
const showInterviewModal = ref(false);
const interviewCard = ref(null);

// Function to show interview form and scroll to it
const showInterviewForm = () => {
  showInterviewModal.value = true;
  
  // Wait for the DOM to update after showing the modal
  setTimeout(() => {
    if (interviewCard.value) {
      interviewCard.value.scrollIntoView({ 
        behavior: 'smooth', 
        block: 'start'
      });
    }
  }, 100);
};

// Function to close interview form and scroll to top
const closeInterviewForm = () => {
  showInterviewModal.value = false;
  
  // Scroll to top of the page
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  });
};

const newInterview = ref({
  candidateName: '',
  evaluationField: null,
  rating: 3,
  approved: null,
  observations: ''
});

// Populate candidate name when showing the modal
watch(showInterviewModal, (newValue) => {
  if (newValue) {
    newInterview.value.candidateName = formattedName.value;
  }
});

// Reset skillset assessment form when closed
watch(showSkillsetAssessment, (newValue) => {
  if (!newValue) {
    // Reset form fields when closing
    selectedSkillsetCategory.value = null;
    selectedSkillset.value = null;
    newSkillsetAssessment.value = {
      rating: 3
    };
    
    // Scroll to profile section (same behavior as interview form)
    const profileSection = document.querySelector('.col-span-12.md\\:col-span-4');
    if (profileSection) {
      profileSection.scrollIntoView({ 
        behavior: 'smooth', 
        block: 'start'
      });
    }
  } else {
    // Set candidate email when opening
    newSkillsetAssessment.value.candidateEmail = candidateData.value?.email || '';
  }
});

// Replace the evaluationFields computed property with a static array
const evaluationFields = [
  'HR - General Technical Evaluation',
  'CTO - Technical Evaluation',
  'SDD - Portfolio Review',
  'SDM - Problem Solving and Communication Skills',
  'CEO - Alignment with Company Vision'
];

const approvalOptions = [
  { label: 'Approved', value: 'Approved' },
  { label: 'Pending', value: 'Pending' },
  { label: 'Rejected', value: 'Rejected' }
];

// Add confirmation dialog
const confirmSubmit = () => {
  confirm.require({
    message: 'Are you sure you want to submit this review? This action cannot be undone.',
    header: 'Confirmation',
    icon: 'pi pi-exclamation-triangle',
    accept: () => {
      submitInterview();
    },
    reject: () => {
      // User rejected the confirmation
    }
  });
};

// Update the submitInterview function to use the GraphQL mutation
const submitInterview = async () => {
  // Validate form
  if (!newInterview.value.evaluationField) {
    toast.add({ severity: 'error', summary: 'Error', detail: 'Please select an evaluation field', life: 3000 });
    return;
  }
  
  if (!newInterview.value.approved) {
    toast.add({ severity: 'error', summary: 'Error', detail: 'Please select an approval status', life: 3000 });
    return;
  }
  
  if (!newInterview.value.observations) {
    toast.add({ severity: 'error', summary: 'Error', detail: 'Please provide observations', life: 3000 });
    return;
  }
  
  try {
    // Prepare the interview data using stored reviewer info
    const interviewData = {
        companyId: candidateData.value.companyId,
        companyName: candidateData.value.companyName,
        email: candidateData.value.email,
        recruitmentProcessId: candidateData.value.recruitmentProcessId,
        recruitmentProcessName: candidateData.value.recruitmentProcessName,
        availability: "Within one month",
        evaluationField: newInterview.value.evaluationField,
        rating: newInterview.value.rating,
        approved: newInterview.value.approved,
        observations: newInterview.value.observations,
        interviewedBy: reviewerName.value,  // Use logged in user's name
        interviewerEmail: reviewerEmail.value  // Use logged in user's email
    };
    
    console.log('Submitting interview with data:', interviewData);
    
    // GraphQL mutation
    const ADD_INTERVIEW = `
      mutation AddInterview($input: AddInterviewInput!) {
        addInterview(input: $input) {
          id
          evaluationField
          rating
          approved
          observations
          interviewedBy
          interviewerEmail
          createdAt
        }
      }
    `;
    
    const response = await fetch(`${import.meta.env.VITE_API_URL}/graphql`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query: ADD_INTERVIEW,
        variables: { input: interviewData }
      })
    });

    const result = await response.json();
    console.log('Interview submission result:', result);
    
    if (result.errors) {
      throw new Error(result.errors[0]?.message || 'Failed to submit interview');
    }
    
    // Check if the mutation was successful but returned null
    if (result.data && result.data.addInterview === null) {
      // The interview might have been created in the database but there was an error returning it
      // We'll fetch the interviews again to update the UI
      await fetchInterviews();
      toast.add({ severity: 'success', summary: 'Success', detail: 'Interview submitted successfully', life: 3000 });
      closeInterviewForm();
      
      // Reset form
      newInterview.value = {
        candidateName: '',
        evaluationField: null,
        rating: 3,
        approved: null,
        observations: ''
      };
      return;
    }
    
    // Add the new interview to the local data if it was returned
    if (result.data?.addInterview) {
      interviewsData.value.push(result.data.addInterview);
      
      // Update the selected review category if needed
      if (!selectedReviewCategory.value) {
        selectedReviewCategory.value = result.data.addInterview.evaluationField;
      }
      
      toast.add({ severity: 'success', summary: 'Success', detail: 'Interview submitted successfully', life: 3000 });
      closeInterviewForm();
      
      // Reset form
      newInterview.value = {
        candidateName: '',
        evaluationField: null,
        rating: 3,
        approved: null,
        observations: ''
      };
    }
  } catch (error) {
    console.error('Error submitting interview:', error);
    toast.add({ severity: 'error', summary: 'Error', detail: error.message || 'Failed to submit interview', life: 3000 });
  }
};

// Inside the <script setup> section, add the following reactive variables near the other declarations
const reviewerName = ref(localStorage.getItem('userName') || '');
const reviewerEmail = ref(localStorage.getItem('userEmail') || '');

// Add new state for skillset assessment
const selectedSkillsetCategory = ref(null);
const selectedSkillset = ref(null);
const companySkillsets = ref([]);
const skillsetCategories = ref([]);
const newSkillsetAssessment = ref({
  rating: 3
});

// GraphQL queries for skillsets
const CATEGORIES_QUERY = `
  query ListSkillsetsCategories($companyId: String!) {
    listSkillsetsCategories(companyId: $companyId)
  }
`;

const SKILLSETS_QUERY = `
  query ListSkillsetsByCompanyId($companyId: String!) {
    listSkillsetsByCompanyId(companyId: $companyId) {
      id
      skillsetName
      skillsetDescription
      skillsetCategory
    }
  }
`;

const ASSIGN_SKILLSET_MUTATION = `
  mutation AssignSkillset($input: AssignSkillsetInput!) {
    assignSkillset(input: $input) {
      # Only request specific fields we need, excluding id/_id
      skillsetCategory
      skillsetName
      skillsetRating
      reviewedBy
      reviewerEmail
      companyId
      companyName
      email
      createdAt
    }
  }
`;

// Add mutation for deleting a skillset rating
const DELETE_SKILLSET_MUTATION = `
  mutation DeleteSkillset($id: String!) {
    deleteSkillset(id: $id)
  }
`;

// Add search functionality
const skillsetSearchQuery = ref('');
const debouncedSearchQuery = ref('');
let searchTimeout = null;

// Debounce search to avoid too many re-renders
const debounceSearch = () => {
  if (searchTimeout) clearTimeout(searchTimeout);
  searchTimeout = setTimeout(() => {
    debouncedSearchQuery.value = skillsetSearchQuery.value;
  }, 300);
};

// Computed property that combines filtering and searching
const filteredAndSearchedSkillsets = computed(() => {
  // First filter by category if needed
  let result = quickRatingFilter.value 
    ? companySkillsets.value.filter(s => s.category === quickRatingFilter.value)
    : companySkillsets.value;
  
  // Then filter by search query if present
  if (debouncedSearchQuery.value.trim()) {
    const searchLower = debouncedSearchQuery.value.toLowerCase().trim();
    result = result.filter(s => 
      s.name.toLowerCase().includes(searchLower) || 
      s.description.toLowerCase().includes(searchLower) ||
      s.category.toLowerCase().includes(searchLower)
    );
  }
  
  // Filter out skillsets already rated by the current user
  // This will immediately update when alreadyRatedSkillsets changes
  result = result.filter(skillset => !alreadyRatedSkillsets.value[skillset.name]);
  
  return result;
});

// Update toggleSkillsetAssessment to reset search
const toggleSkillsetAssessment = async () => {
  showSkillsetAssessment.value = !showSkillsetAssessment.value;
  
  if (showSkillsetAssessment.value) {
    // Reset quick rating state
    quickRatingFilter.value = null;
    pendingRatings.value = {};
    isSubmittingQuickRating.value = {};
    skillsetSearchQuery.value = '';
    debouncedSearchQuery.value = '';
    showAlreadyRatedSkillsets.value = true;
    
    // Fetch data
    await fetchSkillsetCategories();
    await fetchCompanySkillsets();
    
    // Check if we have existing ratings to show the success message
    if (skillsetData.value.length > 0) {
      submittedRatingsCount.value = skillsetData.value.length;
      hasSubmittedRatings.value = true;
    }
    
    // Wait for the DOM to update after showing the form
    setTimeout(() => {
      if (skillsetAssessmentCard.value) {
        skillsetAssessmentCard.value.scrollIntoView({ 
          behavior: 'smooth', 
          block: 'start'
        });
      }
    }, 100);
  } else {
    // Reset state when closing
    quickRatingFilter.value = null;
    pendingRatings.value = {};
    isSubmittingQuickRating.value = {};
    skillsetSearchQuery.value = '';
    debouncedSearchQuery.value = '';
  }
};

// Add loading states for skillset data
const isLoadingCategories = ref(false);
const isLoadingCompanySkillsets = ref(false);

// Fetch skillset categories
async function fetchSkillsetCategories() {
  try {
    isLoadingCategories.value = true;
    const response = await fetch(`${import.meta.env.VITE_API_URL}/graphql`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query: CATEGORIES_QUERY,
        variables: { companyId: candidateData.value.companyId }
      })
    });
    
    const result = await response.json();
    console.log('Skillset categories result:', result);
    
    if (result.errors) {
      throw new Error(result.errors[0]?.message || 'Failed to load skillset categories');
    }
    
    skillsetCategories.value = result.data.listSkillsetsCategories || [];
  } catch (error) {
    console.error('Error fetching skillset categories:', error);
    toast.add({ 
      severity: 'error', 
      summary: 'Error', 
      detail: error.message || 'Failed to load skillset categories', 
      life: 3000 
    });
  } finally {
    isLoadingCategories.value = false;
  }
}

// Fetch company skillsets
async function fetchCompanySkillsets() {
  try {
    isLoadingCompanySkillsets.value = true;
    const response = await fetch(`${import.meta.env.VITE_API_URL}/graphql`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query: SKILLSETS_QUERY,
        variables: { companyId: candidateData.value.companyId }
      })
    });
    
    const result = await response.json();
    console.log('Company skillsets result:', result);
    
    if (result.errors) {
      throw new Error(result.errors[0]?.message || 'Failed to load company skillsets');
    }
    
    // Map the data to a clean structure without any MongoDB-specific fields
    companySkillsets.value = (result.data.listSkillsetsByCompanyId || []).map(item => ({
      id: item.id, // Keep this as 'id', not '_id'
      name: item.skillsetName,
      description: item.skillsetDescription || '',
      category: item.skillsetCategory
    }));
  } catch (error) {
    console.error('Error fetching company skillsets:', error);
    toast.add({ 
      severity: 'error', 
      summary: 'Error', 
      detail: error.message || 'Failed to load company skillsets', 
      life: 3000 
    });
  } finally {
    isLoadingCompanySkillsets.value = false;
  }
}

// Computed property for filtered skillsets based on selected category
const filteredCompanySkillsets = computed(() => {
  if (!selectedSkillsetCategory.value) return [];
  return companySkillsets.value.filter(s => s.category === selectedSkillsetCategory.value);
});

const selectSkillsetForAssessment = (skillset) => {
  selectedSkillset.value = skillset;
};

const cancelSkillsetAssessment = () => {
  selectedSkillset.value = null;
  newSkillsetAssessment.value = {
    rating: 3
  };
};

// Add a new ref for loading state
const isSubmittingSkillset = ref(false);

// Add a new function to update all skillset-related elements
const updateSkillsetData = async () => {
  try {
    // Set loading states
    isRefreshingRadarChart.value = true;
    isRefreshingSkillsets.value = true;
    isRefreshingSkillAverage.value = true;
    
    // Add animation classes to elements
    const radarChartEl = document.querySelector('.radar-chart-container');
    const skillsetsEl = document.querySelector('.skillsets-container');
    
    if (radarChartEl) radarChartEl.classList.add('refreshing');
    if (skillsetsEl) skillsetsEl.classList.add('refreshing');
    
    // Fetch fresh skillset data
    await fetchSkillsets();
    
    // If a category is selected and no longer exists in the updated data, select the first available category
    if (selectedCategory.value && !groupedSkills.value[selectedCategory.value]) {
      const categories = Object.keys(groupedSkills.value);
      if (categories.length > 0) {
        selectedCategory.value = categories[0];
      }
    }
    
    // If we have a newly added category and no category is currently selected, select it
    if (!selectedCategory.value && Object.keys(groupedSkills.value).length > 0) {
      selectedCategory.value = Object.keys(groupedSkills.value)[0];
    }
    
    return true;
  } catch (error) {
    console.error('Error updating skillset data:', error);
    toast.add({
      severity: 'error',
      summary: 'Update Failed',
      detail: error.message || 'Failed to refresh skillset data',
      life: 3000
    });
    return false;
  } finally {
    // Clear loading states after a short delay to ensure smooth transition
    setTimeout(() => {
      isRefreshingRadarChart.value = false;
      isRefreshingSkillsets.value = false;
      isRefreshingSkillAverage.value = false;
      
      // Remove animation classes
      const radarChartEl = document.querySelector('.radar-chart-container');
      const skillsetsEl = document.querySelector('.skillsets-container');
      
      if (radarChartEl) radarChartEl.classList.remove('refreshing');
      if (skillsetsEl) skillsetsEl.classList.remove('refreshing');
    }, 500);
  }
};

// Update the submitSkillsetAssessment function to use updateSkillsetData
const submitSkillsetAssessment = async () => {
  try {
    isSubmittingSkillset.value = true;
    
    // Create a clean input object with only the fields expected by the backend
    const input = {
      companyId: candidateData.value.companyId,
      companyName: candidateData.value.companyName,
      email: candidateData.value.email,
      skillsetCategory: selectedSkillset.value.category,
      skillsetName: selectedSkillset.value.name,
      skillsetRating: newSkillsetAssessment.value.rating,
      reviewedBy: reviewerName.value,
      reviewerEmail: reviewerEmail.value
    };
    
    console.log('Submitting skillset assessment with input:', input);
    
    const response = await fetch(`${import.meta.env.VITE_API_URL}/graphql`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query: ASSIGN_SKILLSET_MUTATION,
        variables: { input }
      })
    });
    
    const result = await response.json();
    console.log('Skillset assessment result:', result);
    
    // Special handling for the _id error
    // This error occurs when MongoDB returns _id but GraphQL schema expects id
    if (result.errors && result.errors.some(e => e.message.includes('_id'))) {
      console.warn('Received _id error but proceeding with success flow');
      
      // The data was likely saved successfully despite the _id error
      toast.add({
        severity: 'success',
        summary: 'Success',
        detail: 'Skillset assessment submitted successfully',
        life: 3000
      });
      
      // Update all skillset-related elements
      await updateSkillsetData();
      
      // Reset form and close assessment panel
      selectedSkillset.value = null;
      newSkillsetAssessment.value = { rating: 3 };
      showSkillsetAssessment.value = false;
      return;
    } else if (result.errors) {
      throw new Error(result.errors[0].message);
    }
    
    toast.add({
      severity: 'success',
      summary: 'Success',
      detail: 'Skillset assessment submitted successfully',
      life: 3000
    });
    
    // Update all skillset-related elements
    await updateSkillsetData();
    
    // Reset form and close assessment panel
    selectedSkillset.value = null;
    newSkillsetAssessment.value = { rating: 3 };
    showSkillsetAssessment.value = false;
  } catch (error) {
    console.error('Error submitting skillset assessment:', error);
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: error.message || 'Failed to submit assessment',
      life: 3000
    });
  } finally {
    isSubmittingSkillset.value = false;
  }
}

// Update the rateSkillset function to properly handle the last skillset case
const rateSkillset = async (skillset) => {
  // Skip if no rating is selected or already submitting
  if (pendingRatings.value[skillset.id] === undefined || isSubmittingQuickRating.value[skillset.id]) {
    return;
  }
  
  try {
    // Set submitting state for this specific skillset
    isSubmittingQuickRating.value = {
      ...isSubmittingQuickRating.value,
      [skillset.id]: true
    };
    
    // Create a clean input object with only the fields expected by the backend
    const input = {
      companyId: candidateData.value.companyId,
      companyName: candidateData.value.companyName,
      email: candidateData.value.email,
      skillsetCategory: skillset.category,
      skillsetName: skillset.name,
      skillsetRating: pendingRatings.value[skillset.id],
      reviewedBy: reviewerName.value,
      reviewerEmail: reviewerEmail.value
    };
    
    console.log('Quick rating skillset:', input);
    
    const response = await fetch(`${import.meta.env.VITE_API_URL}/graphql`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query: ASSIGN_SKILLSET_MUTATION,
        variables: { input }
      })
    });
    
    const result = await response.json();
    console.log('Quick rating result:', result);
    
    // Special handling for the _id error
    // This error occurs when MongoDB returns _id but GraphQL schema expects id
    if (result.errors && result.errors.some(e => e.message.includes('_id'))) {
      console.warn('Received _id error but proceeding with success flow');
      
      // Show a small toast notification
      toast.add({
        severity: 'success',
        summary: 'Rated Successfully',
        detail: `Rated "${skillset.name}" with ${pendingRatings.value[skillset.id]} stars`,
        life: 2000
      });
      
      // Increment the submitted ratings count
      submittedRatingsCount.value++;
      hasSubmittedRatings.value = true;
      
      // Immediately update the alreadyRatedSkillsets to include this skillset
      alreadyRatedSkillsets.value = {
        ...alreadyRatedSkillsets.value,
        [skillset.name]: true
      };
      
      // Remove the pending rating immediately to prevent UI glitches
      const newPendingRatings = { ...pendingRatings.value };
      delete newPendingRatings[skillset.id];
      pendingRatings.value = newPendingRatings;
      
      // Also remove the submitting state immediately
      const newIsSubmittingQuickRating = { ...isSubmittingQuickRating.value };
      delete newIsSubmittingQuickRating[skillset.id];
      isSubmittingQuickRating.value = newIsSubmittingQuickRating;
      
      // Update all skillset-related elements
      await updateSkillsetData();
      return;
    } else if (result.errors) {
      throw new Error(result.errors[0].message);
    }
    
    // Show a small toast notification
    toast.add({
      severity: 'success',
      summary: 'Rated Successfully',
      detail: `Rated "${skillset.name}" with ${pendingRatings.value[skillset.id]} stars`,
      life: 2000
    });
    
    // Increment the submitted ratings count
    submittedRatingsCount.value++;
    hasSubmittedRatings.value = true;
    
    // Immediately update the alreadyRatedSkillsets to include this skillset
    alreadyRatedSkillsets.value = {
      ...alreadyRatedSkillsets.value,
      [skillset.name]: true
    };
    
    // Remove the pending rating immediately to prevent UI glitches
    const newPendingRatings = { ...pendingRatings.value };
    delete newPendingRatings[skillset.id];
    pendingRatings.value = newPendingRatings;
    
    // Also remove the submitting state immediately
    const newIsSubmittingQuickRating = { ...isSubmittingQuickRating.value };
    delete newIsSubmittingQuickRating[skillset.id];
    isSubmittingQuickRating.value = newIsSubmittingQuickRating;
    
    // Update all skillset-related elements
    await updateSkillsetData();
    
  } catch (error) {
    console.error('Error submitting quick rating:', error);
    toast.add({
      severity: 'error',
      summary: 'Rating Failed',
      detail: error.message || 'Failed to submit rating',
      life: 3000
    });
    
    // Remove the submitting state
    const newIsSubmittingQuickRating = { ...isSubmittingQuickRating.value };
    delete newIsSubmittingQuickRating[skillset.id];
    isSubmittingQuickRating.value = newIsSubmittingQuickRating;
  }
};

// Add to the script section
const showMobileDescription = (description) => {
  toast.add({
    severity: 'info',
    summary: 'Skillset Description',
    detail: description,
    life: 5000,
    closable: true,
    className: 'mobile-description-toast'
  });
};

const truncateDescription = (desc) => {
  if (!desc) return '';
  return desc.length > 50 ? desc.substring(0, 50) + '...' : desc;
};

// Also add a helper function to toggle reviews if not already defined:
const toggleReviews = () => { isReviewsExpanded.value = !isReviewsExpanded.value; };

// And a function to set selected review category:
const setSelectedReviewCategory = (field) => { selectedReviewCategory.value = field; };

// Add new state for quick rating
const quickRatingFilter = ref(null);
const pendingRatings = ref({});
const isSubmittingQuickRating = ref({});
const submittedRatingsCount = ref(0);
const hasSubmittedRatings = ref(false);

// Computed property for filtered skillsets based on quick rating filter
const filteredQuickRatingSkillsets = computed(() => {
  if (!quickRatingFilter.value) return companySkillsets.value;
  return companySkillsets.value.filter(s => s.category === quickRatingFilter.value);
});

// Add loading states for charts and skillsets
const isRefreshingRadarChart = ref(false);
const isRefreshingSkillsets = ref(false);

// Add loading state for average skill rating
const isRefreshingSkillAverage = ref(false);

// Add a computed property to identify skillsets already rated by the current user
const alreadyRatedSkillsets = computed(() => {
  // Create a map of skillsetName -> true for skillsets rated by the current user
  const ratedMap = {};
  
  // Only consider skillsets rated by the current user (matching reviewerEmail)
  skillsetData.value.forEach(skill => {
    if (skill.reviewerEmail === reviewerEmail.value) {
      ratedMap[skill.skillsetName] = true;
    }
  });
  
  return ratedMap;
});

// Computed property to get skillsets rated by current user in the selected category
const ratedSkillsetsInCategory = computed(() => {
  return skillsetData.value.filter(skill => 
    skill.reviewerEmail === reviewerEmail.value && 
    (!quickRatingFilter.value || skill.skillsetCategory === quickRatingFilter.value)
  );
});

// Check if there are any rated skillsets in the current category
const hasRatedSkillsetsInCategory = computed(() => {
  return ratedSkillsetsInCategory.value.length > 0;
});

// Add new reactive variables for showing already rated skillsets
const showAlreadyRatedSkillsets = ref(true);

// Add toggle function for already rated skillsets
const toggleAlreadyRatedSkillsets = () => {
  showAlreadyRatedSkillsets.value = !showAlreadyRatedSkillsets.value;
};

// Add state for tracking skillset deletion
const isDeletingSkillset = ref({});

// Function to delete a skillset rating
const deleteSkillsetRating = async (skillset) => {
  try {
    // Set deleting state for this specific skillset
    isDeletingSkillset.value = {
      ...isDeletingSkillset.value,
      [skillset.id]: true
    };
    
    // Debug: Log the entire skillset object to see its structure
    console.log('Deleting skillset (full object):', skillset);
    console.log('Skillset ID:', skillset.id);
    
    // Try with the first mutation name
    let response = await fetch(`${import.meta.env.VITE_API_URL}/graphql`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query: `
          mutation DeleteSkillset($id: String!) {
            deleteSkillset(id: $id)
          }
        `,
        variables: { id: skillset.id }
      })
    });
    
    let result = await response.json();
    console.log('Delete result (first attempt):', result);
    
    // If the first attempt fails, try with a different mutation name
    if (result.errors) {
      console.log('First attempt failed, trying with delete_skillset...');
      response = await fetch(`${import.meta.env.VITE_API_URL}/graphql`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: `
            mutation DeleteSkillset($id: String!) {
              delete_skillset(id: $id)
            }
          `,
          variables: { id: skillset.id }
        })
      });
      
      result = await response.json();
      console.log('Delete result (second attempt):', result);
    }
    
    // If both attempts fail, try with removeSkillset
    if (result.errors) {
      console.log('Second attempt failed, trying with removeSkillset...');
      response = await fetch(`${import.meta.env.VITE_API_URL}/graphql`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: `
            mutation RemoveSkillset($id: String!) {
              removeSkillset(id: $id)
            }
          `,
          variables: { id: skillset.id }
        })
      });
      
      result = await response.json();
      console.log('Delete result (third attempt):', result);
    }
    
    if (result.errors) {
      throw new Error(result.errors[0].message);
    }
    
    // Show a success notification
    toast.add({
      severity: 'success',
      summary: 'Rating Deleted',
      detail: `Removed rating for "${skillset.skillsetName}"`,
      life: 2000
    });
    
    // Immediately update the alreadyRatedSkillsets to remove this skillset
    const newAlreadyRatedSkillsets = { ...alreadyRatedSkillsets.value };
    delete newAlreadyRatedSkillsets[skillset.skillsetName];
    alreadyRatedSkillsets.value = newAlreadyRatedSkillsets;
    
    // Update all skillset-related elements
    await updateSkillsetData();
    
  } catch (error) {
    console.error('Error deleting skillset rating:', error);
    toast.add({
      severity: 'error',
      summary: 'Deletion Failed',
      detail: error.message || 'Failed to delete rating',
      life: 3000
    });
  } finally {
    // Remove the deleting state
    const newIsDeletingSkillset = { ...isDeletingSkillset.value };
    delete newIsDeletingSkillset[skillset.id];
    isDeletingSkillset.value = newIsDeletingSkillset;
  }
};

// Add a function to test the available mutations
const testAvailableMutations = async () => {
  try {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/graphql`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query: `
          {
            __schema {
              mutationType {
                name
                fields {
                  name
                }
              }
            }
          }
        `
      })
    });
    
    const result = await response.json();
    console.log('Available mutations:', result);
    
    // Specifically check for skillset-related mutations
    const skillsetMutations = result.data?.__schema?.mutationType?.fields?.filter(
      field => field.name.toLowerCase().includes('skillset')
    );
    console.log('Skillset-related mutations:', skillsetMutations);
  } catch (error) {
    console.error('Error fetching schema:', error);
  }
};

// Function to confirm deletion
const confirmDeleteSkillset = (skillset, event) => {
  confirm.require({
    target: event.currentTarget,
    message: `Are you sure you want to delete your rating for "${skillset.skillsetName}"?`,
    icon: 'pi pi-exclamation-triangle',
    acceptClass: 'p-button-danger',
    accept: () => {
      deleteSkillsetRating(skillset);
    },
    reject: () => {
      // Do nothing on reject
    }
  });
};

// Add new state for skillset assessment
const shouldShowCertificationsBelowSkillsets = computed(() => {
  // Show below skillsets if any category is open, interview form is shown, or skillset assessment is shown
  return isAnyCategoryOpen.value || showInterviewModal.value || showSkillsetAssessment.value;
});

// Add new state for showing skills radar
const showSkillsRadar = ref(true);

// Add function to toggle skills radar
const toggleSkillsRadar = () => {
  showSkillsRadar.value = !showSkillsRadar.value;
};
</script>

<style scoped>
.card {
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  background-color: #fff;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.card:hover {
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

/* Section headers with icons */
.card h5.font-semibold {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

/* Clickable section headers */
.cursor-pointer {
  transition: background-color 0.2s;
  border-radius: 4px;
}

.cursor-pointer:hover {
  background-color: rgba(0, 0, 0, 0.03);
}

/* Compact Breadcrumb Styles */
.compact-breadcrumb {
  padding: 0.5rem 0;
}

.compact-breadcrumb :deep(.p-breadcrumb) {
  border: none;
  padding: 0;
  background-color: transparent;
}

.compact-breadcrumb :deep(.p-breadcrumb .p-breadcrumb-list) {
  margin: 0;
  padding: 0;
}

.compact-breadcrumb :deep(.p-breadcrumb .p-menuitem-text) {
  font-size: 0.875rem;
}

.compact-breadcrumb :deep(.p-breadcrumb .p-menuitem-icon) {
  font-size: 0.875rem;
}

.compact-breadcrumb :deep(.p-breadcrumb-chevron) {
  margin: 0 0.25rem;
  font-size: 0.75rem;
}

@media (max-width: 640px) {
  .compact-breadcrumb :deep(.p-breadcrumb .p-menuitem-text) {
    font-size: 0.75rem;
  }
  
  .compact-breadcrumb :deep(.p-breadcrumb .p-menuitem-icon) {
    font-size: 0.75rem;
  }
  
  .compact-breadcrumb :deep(.p-breadcrumb-chevron) {
    margin: 0 0.15rem;
    font-size: 0.65rem;
  }
}

/* Line clamp utilities */
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Remove line-clamp when expanded */
.show-full {
  -webkit-line-clamp: unset;
}

/* Add transition for smooth collapse/expand */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease, max-height 0.3s ease;
  overflow: hidden;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  max-height: 0;
}

.fade-enter-to,
.fade-leave-from {
  opacity: 1;
  max-height: 1000px;
}

fieldset {
  border: 1px solid #e5e7eb;
  border-radius: 0.375rem;
  min-height: 100%;
  display: flex;
  flex-direction: column;
  transition: all 0.3s ease;
}

fieldset:hover {
  border-color: #d1d5db;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

legend {
  padding: 0 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
  transition: background-color 0.2s;
  border-radius: 4px;
}

legend:hover {
  background-color: #f3f4f6;
}

ul {
  max-height: 300px; /* Adjust this value based on your needs */
  overflow-y: auto;
  padding-left: 0;
  list-style-type: none;
}

:deep(.p-tooltip) {
  z-index: 50;
  background: var(--p-surface-overlay);
  color: var(--p-text-color);
  padding: 0.5rem 1rem;
  border-radius: 6px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  border: 1px solid var(--p-surface-border);
}

:deep(.p-tooltip-text) {
  font-size: 0.875rem;
  line-height: 1.25rem;
}

/* Interview Card Styles */
.interview-card {
  border-left: 4px solid #4f46e5;
  transition: all 0.3s ease;
  animation: slideDown 0.3s ease;
}

@keyframes slideDown {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Custom Chip Styles */
:deep(.p-chip) {
  padding: 0.25rem 0.5rem;
  font-size: 0.75rem;
  line-height: 1rem;
  transition: all 0.2s ease;
  background-color: var(--surface-100);
  color: var(--text-color);
  border: 1px solid var(--surface-border);
}

:deep(.p-chip:hover) {
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  background-color: var(--primary-50) !important;
  color: var(--primary-500) !important;
  border-color: var(--primary-100);
}

:deep(.p-chip.bg-primary-500) {
  background-color: var(--primary-500) !important;
  color: var(--gray-900) !important; /* Changed from white to dark gray */
  font-weight: bold; /* Added bold for better visibility */
  box-shadow: 0 2px 4px rgba(59, 130, 246, 0.2);
  border-color: var(--primary-500);
}

:deep(.mobile-description-toast) {
  @media (max-width: 768px) {
    width: 90vw;
    left: 5vw;
    right: 5vw;
    white-space: pre-wrap;
    word-break: break-word;
  }
}

:deep(.p-tooltip) {
  max-width: 300px;
  white-space: pre-wrap;
  word-break: break-word;
}

/* Add refresh animation */
@keyframes refreshPulse {
  0% { box-shadow: 0 0 0 0 rgba(59, 130, 246, 0.4); }
  70% { box-shadow: 0 0 0 10px rgba(59, 130, 246, 0); }
  100% { box-shadow: 0 0 0 0 rgba(59, 130, 246, 0); }
}

.refreshing {
  animation: refreshPulse 1.5s ease-in-out;
}

/* Add new section to show already rated skillsets */
.already-rated-skillsets {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #e0e0e0;
}

.already-rated-skillsets h6 {
  margin-bottom: 10px;
  font-size: 1rem;
  color: #333;
}

.already-rated-skillsets ul {
  list-style-type: none;
  padding-left: 0;
}

.already-rated-skillsets li {
  margin-bottom: 5px;
  font-size: 0.9rem;
  color: #666;
}
</style> 