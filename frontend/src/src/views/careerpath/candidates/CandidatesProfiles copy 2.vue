<template>
  <div class="p-4">
    <Toast />
    <ConfirmDialog />
    <!-- Breadcrumb Navigation -->
    <div class="compact-breadcrumb mb-3">
      <Breadcrumb :home="breadcrumbHome" :model="breadcrumbItems" @item-click="navigateTo" />
    </div>
    
    <div v-if="loading" class="text-center p-8">
      <ProgressSpinner style="width: 50px; height: 50px" />
      <p class="mt-2 text-gray-600">Loading candidate profile...</p>
    </div>
    
    <div v-else class="grid grid-cols-12 gap-4">
      <!-- Candidate Basic Info Card -->
      <div class="col-span-12 md:col-span-4">
        <div class="card p-4">
          <div class="flex flex-col items-center">
            <Avatar :label="candidateInitials" shape="circle" size="xlarge" class="mb-4" />
            <h2 class="text-xl font-bold mb-2">{{ formattedName }}</h2>
            
            <!-- Add counters -->
            <div class="flex space-x-6 mb-4">
              <div class="flex items-center">
                <i class="pi pi-star-fill text-yellow-500 mr-1"></i>
                <span>{{ allSkillsAverage }}</span>
              </div>
              <div class="flex items-center">
                <i class="pi pi-comment text-blue-500 mr-1"></i>
                <span>{{ interviewsData.length }}</span>
              </div>
              <div class="flex items-center">
                <i class="pi pi-thumbs-up text-green-500 mr-1"></i>
                <span>{{ approvedCounts.yes }}</span>
              </div>
              <div class="flex items-center">
                <i class="pi pi-clock text-yellow-500 mr-1"></i>
                <span>{{ approvedCounts.pending }}</span>
              </div>
              <div class="flex items-center">
                <i class="pi pi-thumbs-down text-red-500 mr-1"></i>
                <span>{{ approvedCounts.no }}</span>
              </div>
            </div>
            
            <p class="text-sm text-gray-600">Position Applied For: {{ candidateData.recruitmentProcessName }}</p>
            
            <!-- Add additional candidate information -->
            <div class="w-full mt-4 space-y-2 text-sm">
              <div class="flex items-center">
                <i class="pi pi-envelope mr-2"></i>
                <span>{{ candidateData.email }}</span>
              </div>
              <div class="flex items-center">
                <i class="pi pi-globe mr-2"></i>
                <span>{{ candidateData.country }}</span>
              </div>
              <div class="flex items-center">
                <i class="pi pi-phone mr-2"></i>
                <span>{{ candidateData.phone }}</span>
              </div>
              <div class="flex items-center">
                <i class="pi pi-money-bill mr-2"></i>
                <span>Salary Expectation: {{ formattedSalary }}</span>
              </div>
              <div class="flex items-center">
                <i class="pi pi-file mr-2"></i>
                <a v-if="candidateData.candidateCV" 
                   :href="candidateData.candidateCV" 
                   target="_blank" 
                   class="text-blue-500 hover:underline">
                  View CV
                </a>
                <span v-else class="text-gray-500">No CV uploaded</span>
              </div>
              <div class="flex items-center">
                <i class="pi pi-calendar mr-2"></i>
                <span>Applied on: {{ formattedDate }}</span>
              </div>
              
            </div>
            

   
   
            <!-- Update action buttons -->
            <div class="w-full mt-6 flex gap-2">
              <Button class="flex-1" severity="info" @click="showInterviewForm" size="small" 
                     v-tooltip.top="'Interview Candidate'">
                <i class="pi pi-eye"></i>
              </Button>
              <Button class="flex-1" severity="warning" @click="toggleSkillsetAssessment" size="small"
                     v-tooltip.top="'Assess Skillsets'">
                <i class="pi pi-star"></i>
              </Button>
              <Button class="flex-1" severity="success" @click="contactCandidate" size="small"
                     v-tooltip.top="'Contact Candidate'">
                <i class="pi pi-envelope"></i>
              </Button>
            </div>
          </div>
        </div>
        <div class="col-span-12">
        <div class="card p-4">
          
          <div class="grid grid-cols-1">
            <div class="card p-4">
              <Chart 
                type="radar" 
                :data="categoryRadarData" 
                :options="radarChartOptions" 
               
              />
            </div>
          </div>
        </div>
      </div>
      </div>
      
      
      <!-- Skillset Widget Card -->
      <div class="col-span-12 md:col-span-8 relative">
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
          <div class="flex items-center justify-between mb-4 cursor-pointer">
            <div class="flex items-center gap-2">
              <i class="pi pi-star text-blue-500"></i>
              <h5 class="font-semibold m-0">Skillset Assessment</h5>
              <div class="bg-blue-100 text-blue-800 text-xs font-medium px-2 py-0.5 rounded-full">
                {{ filteredCompanySkillsets.length }}
              </div>
            </div>
            <Button icon="pi pi-times" class="p-button-rounded p-button-text" @click="showSkillsetAssessment = false" />
          </div>
          
          <!-- Categories Section -->
          <div class="mb-4">
            <h6 class="text-sm font-medium text-gray-700 mb-2">Categories</h6>
            <div class="flex flex-wrap gap-1">
              <Chip 
                v-for="category in skillsetCategories" 
                :key="category"
                :label="category"
                :class="{ 
                  'bg-primary-500 text-primary-500 shadow-lg': selectedSkillsetCategory === category,
                  'hover:bg-primary-50 hover:text-primary-500 hover:shadow-lg transition-all duration-200': true
                }"
                @click="selectedSkillsetCategory = category"
                class="cursor-pointer border-1 border-transparent bg-surface-100 shadow-sm text-xs px-2 py-1"
              />
            </div>
          </div>
          
          <!-- Skillsets List -->
          <div v-if="selectedSkillsetCategory" class="mb-4">
            <h6 class="text-sm font-medium text-gray-700 mb-2">Skillsets in {{ selectedSkillsetCategory }}</h6>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
              <div 
                v-for="skillset in filteredCompanySkillsets" 
                :key="skillset.id" 
                class="p-3 border rounded-lg hover:bg-surface-100 cursor-pointer relative"
                :class="{'border-primary-500 bg-primary-50': selectedSkillset && selectedSkillset.id === skillset.id}"
              >
                <div class="flex justify-between items-start">
                  <div class="flex-1">
                    <div class="font-medium flex items-center gap-1">
                      <span v-tooltip.right="skillset.description" class="hidden md:inline">
                        {{ skillset.name }}
                      </span>
                      <span class="md:hidden">{{ skillset.name }}</span>
                      <Button 
                        icon="pi pi-info-circle" 
                        class="p-button-text p-button-rounded p-button-sm text-gray-500 hover:text-primary-500 md:hidden"
                        @click.stop="showMobileDescription(skillset.description)"
                      />
                    </div>
                    <div class="text-xs text-gray-500 md:hidden mt-1">
                      {{ truncateDescription(skillset.description) }}
                    </div>
                  </div>
                  <i 
                    v-if="selectedSkillset?.id === skillset.id" 
                    class="pi pi-check-circle text-primary-500 ml-2"
                  ></i>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Assessment Form -->
          <div v-if="selectedSkillset" class="border-t pt-4 mt-4">
            <h6 class="font-medium mb-3">Assess: {{ selectedSkillset.name }}</h6>
            <div class="mb-3">
              <label class="block text-sm font-medium text-gray-700 mb-1">Rating</label>
              <Rating v-model="newSkillsetAssessment.rating" :stars="5" />
            </div>
            <div class="mb-3">
              <label class="block text-sm font-medium text-gray-7 mb-1">Notes</label>
              <Textarea v-model="newSkillsetAssessment.notes" rows="2" class="w-full" />
            </div>
            <div class="flex justify-end gap-2">
              <Button label="Cancel" class="p-button-outlined" @click="cancelSkillsetAssessment" />
              <Button label="Submit Assessment" severity="warning" @click="submitSkillsetAssessment" />
            </div>
          </div>
        </div>

        <div class="card p-4">
          <div class="flex items-center justify-between mb-4 cursor-pointer" @click="toggleAllSkillsets">
            <div class="flex items-center gap-2">
              <i class="pi pi-list text-blue-500"></i>
              <h5 class="font-semibold m-0">Skillsets</h5>
              <div class="bg-blue-100 text-blue-800 text-xs font-medium px-2 py-0.5 rounded-full">
                {{ Object.keys(groupedSkills).length }}
              </div>
            </div>
            <i :class="`pi ${areAllSkillsetsCollapsed ? 'pi-chevron-down' : 'pi-chevron-up'} text-gray-500`"></i>
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
        
        <!-- Conditionally show certifications and reviews in the same column when skillsets are collapsed -->
        <div v-if="areAllSkillsetsCollapsed" class="mt-4 space-y-4">
          <!-- Interview Reviews Section -->
          <div class="card p-4">
            <div class="flex items-center justify-between mb-4">
              <div class="flex items-center gap-2">
                <i class="pi pi-comments text-indigo-500"></i>
                <h5 class="font-semibold m-0">Interview Reviews</h5>
                <div class="bg-indigo-100 text-indigo-800 text-xs font-medium px-2 py-0.5 rounded-full">
                  {{ interviewsData.length }}
                </div>
              </div>
            </div>
            
            <div>
              <div v-if="interviewsData.length === 0" class="text-gray-500 italic py-4 text-center">
                No reviews available
              </div>
              <div v-else>
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
                <div v-for="(reviews, field) in groupedReviews" :key="field" v-show="selectedReviewCategory === field">
                  <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
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
          
          <!-- Certifications Section -->
          <div class="card p-4">
            <div class="flex items-center justify-between mb-4 cursor-pointer" @click="toggleCertifications">
              <div class="flex items-center gap-2">
                <i class="pi pi-certificate text-blue-500"></i>
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
                <div v-else class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div 
                    v-for="(certification, index) in certificationsData" 
                    :key="index" 
                    class="bg-gray-50 rounded-lg p-4 border-l-4"
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
      
      <!-- Charts Section -->
      <transition name="fade">
        <div v-if="isAnyCategoryOpen" class="col-span-12">
          <div class="card p-4">
            <h5 class="mb-4">Candidate Analytics - {{ selectedCategory }}</h5>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <!-- Basic Bar Chart Widget -->
              <div class="card p-4">
                <h6 class="mb-2 font-semibold">Skillset Average Rating</h6>
                <Chart type="bar" :data="basicChartData" :options="chartOptions" />
              </div>
              <!-- Pie Chart Widget -->
              <div class="card p-4">
                <h6 class="mb-2 font-semibold">Knowledge Distribution by Skillset</h6>
                <Chart type="pie" :data="pieChartData" :options="chartOptions" />
              </div>
              <!-- Vertical Bar Chart Widget -->
              <div class="card p-4">
                <h6 class="mb-2 font-semibold">Skillset Knowledge Distribution</h6>
                <Chart type="bar" :data="verticalBarChartData" :options="chartOptions" />
              </div>
              <!-- Radar Chart Widget -->
              <div class="card p-4">
                <h6 class="mb-2 font-semibold">Skillset Knowledge Distribution</h6>
                <Chart type="radar" :data="radarChartData" :options="radarChartOptions" />
              </div>
            </div>
          </div>
        </div>
      </transition>
      
      <!-- Certifications and Reviews Sections (only shown when skillsets are not collapsed) -->
      <div v-if="!areAllSkillsetsCollapsed" class="col-span-12">
        <!-- Updated Candidate Reviews Section -->
        <div class="card p-4">
          <div class="flex items-center justify-between mb-4 cursor-pointer" @click="isReviewsExpanded = !isReviewsExpanded">
            <div class="flex items-center gap-2">
              <i class="pi pi-comments text-indigo-500"></i>
              <h5 class="font-semibold m-0">Interview Reviews</h5>
              <div class="bg-indigo-100 text-indigo-800 text-xs font-medium px-2 py-0.5 rounded-full">
                {{ interviewsData.length }}
              </div>
            </div>
            <i :class="`pi ${isReviewsExpanded ? 'pi-chevron-up' : 'pi-chevron-down'} text-gray-500`"></i>
          </div>
          
          <transition name="fade">
            <div v-if="isReviewsExpanded">
              <div v-if="interviewsData.length === 0" class="text-gray-500 italic py-4 text-center">
                No reviews available
              </div>
              <div v-else>
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
                <div v-for="(reviews, field) in groupedReviews" :key="field" v-show="selectedReviewCategory === field">
                  <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
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
          </transition>
        </div>
        
        <!-- Updated Certifications Section -->
        <div class="card p-4">
          <div class="flex items-center justify-between mb-4 cursor-pointer" @click="toggleCertifications">
            <div class="flex items-center gap-2">
              <i class="pi pi-certificate text-blue-500"></i>
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
              <div v-else class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div 
                  v-for="(certification, index) in certificationsData" 
                  :key="index" 
                  class="bg-gray-50 rounded-lg p-4 border-l-4"
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
      
      <!-- Metadata Section -->
      <div class="col-span-12">
        <div class="card p-4">
          <div class="flex items-center gap-2 mb-4">
            <i class="pi pi-cog text-gray-500"></i>
            <h5 class="font-semibold m-0">System Information</h5>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
            <div class="flex items-center gap-2 p-3 bg-gray-50 rounded-lg">
              <i class="pi pi-id-card text-gray-500"></i>
              <div>
                <div class="text-gray-500">Profile ID</div>
                <div class="font-mono text-primary-500">{{ candidateData.id }}</div>
              </div>
            </div>
            <div class="flex items-center gap-2 p-3 bg-gray-50 rounded-lg">
              <i class="pi pi-database text-gray-500"></i>
              <div>
                <div class="text-gray-500">Company ID</div>
                <div class="font-mono text-primary-500">{{ candidateData.companyId }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- In the Charts Section -->
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
import ConfirmDialog from 'primevue/confirmdialog';
import { useConfirm } from 'primevue/useconfirm';
import Chip from 'primevue/chip';

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
  // Implement contact logic
  console.log('Contacting candidate...');
};

// Update skillsetData - remove candidateId from all entries
const skillsetData = ref([]);

// In script setup section, add the query and fetch logic
const GET_SKILLSETS_BY_EMAIL = `
  query GetSkillsetsByEmail($email: String!) {
    getSkillsetsByEmail(email: $email) {
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
    if (result.errors) {
      throw new Error(result.errors[0]?.message || 'Failed to load skillsets');
    }
    
    skillsetData.value = result.data.getSkillsetsByEmail || [];
  } catch (error) {
    console.error('Error fetching skillsets:', error);
    // You might want to add a toast notification here
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

// Update onMounted to fetch data
onMounted(async () => {
  // Initialize UI state based on screen size
  checkScreenSize();
  window.addEventListener('resize', checkScreenSize);
  
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
      label: 'Skillser Radar',
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
      candidateEmail: '',
      skillsetName: '',
      skillsetCategory: '',
      score: 0,
      notes: '',
      assessedBy: ''
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
  rating: 3,
  notes: ''
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
      id
      skillsetCategory
      skillsetName
      skillsetRating
      reviewedBy
      reviewerEmail
      companyId
      email
    }
  }
`;

// Add skillset assessment functions
const toggleSkillsetAssessment = async () => {
  showSkillsetAssessment.value = !showSkillsetAssessment.value;
  
  if (showSkillsetAssessment.value) {
    await fetchSkillsetCategories();
    await fetchCompanySkillsets();
    
    // Wait for the DOM to update after showing the form
    setTimeout(() => {
      if (skillsetAssessmentCard.value) {
        skillsetAssessmentCard.value.scrollIntoView({ 
          behavior: 'smooth', 
          block: 'start'
        });
      }
    }, 100);
  }
};

// Fetch skillset categories
async function fetchSkillsetCategories() {
  try {
    const response = await fetch('/graphql', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query: CATEGORIES_QUERY,
        variables: { companyId: candidateData.value.companyId }
      })
    });
    
    const data = await response.json();
    skillsetCategories.value = data.data.listSkillsetsCategories;
  } catch (error) {
    toast.add({ 
      severity: 'error', 
      summary: 'Error', 
      detail: 'Failed to load skillset categories', 
      life: 3000 
    });
  }
}

// Fetch company skillsets
async function fetchCompanySkillsets() {
  try {
    const response = await fetch('/graphql', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query: SKILLSETS_QUERY,
        variables: { companyId: candidateData.value.companyId }
      })
    });
    
    const data = await response.json();
    companySkillsets.value = data.data.listSkillsetsByCompanyId.map(item => ({
      id: item.id,
      name: item.skillsetName,
      description: item.skillsetDescription,
      category: item.skillsetCategory
    }));
  } catch (error) {
    toast.add({ 
      severity: 'error', 
      summary: 'Error', 
      detail: 'Failed to load company skillsets', 
      life: 3000 
    });
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
    rating: 3,
    notes: ''
  };
};

const submitSkillsetAssessment = async () => {
  try {
    const response = await fetch('/graphql', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query: ASSIGN_SKILLSET_MUTATION,
        variables: {
          input: {
            companyId: candidateData.value.companyId,
            email: candidateData.value.email,
            skillsetCategory: selectedSkillset.value.category,
            skillsetName: selectedSkillset.value.name,
            skillsetRating: newSkillsetAssessment.value.rating,
            reviewedBy: reviewerName.value,
            reviewerEmail: reviewerEmail.value,
            notes: newSkillsetAssessment.value.notes
          }
        }
      })
    });
    
    const result = await response.json();
    
    if (result.errors) {
      throw new Error(result.errors[0].message);
    }
    
    toast.add({
      severity: 'success',
      summary: 'Success',
      detail: 'Skillset assessment submitted successfully',
      life: 3000
    });
    
    // Refresh skillsets data
    await fetchSkillsets();
    
    // Reset form
    selectedSkillset.value = null;
    newSkillsetAssessment.value = {
      rating: 3,
      notes: ''
    };
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: error.message || 'Failed to submit assessment',
      life: 3000
    });
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
  color: white !important;
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
</style> 