<template>
  <div class="card">
    <Toast />
    <ConfirmDialog />
    
    <!-- Breadcrumb Navigation -->
    <div class="compact-breadcrumb mb-3">
      <Breadcrumb :home="breadcrumbHome" :model="breadcrumbItems" />
    </div>
    
    <div class="flex items-center justify-between mb-4">
        <div>
          <h1 class="text-2xl font-medium text-900">Recruitment Leads</h1>
          <p class="text-sm font-medium text-500">Manage your recruitment processes</p>
        </div>
        <Button 
          label="Add Process" 
          icon="pi pi-plus" 
          outlined raised 
          @click="openNewProcess" 
        />
      </div>
    <!-- Header Section -->
    <div class="card p-2 md:p-4">
      <!-- Processes Section -->
      <div class="bg-white p-2 md:p-4 rounded-lg shadow-sm">
        <div class="flex flex-col md:flex-row md:justify-between md:items-center gap-2 mb-4">
          <!-- Search Bar -->
          <IconField class="w-full md:w-96">
            <InputIcon class="pi pi-search" />
            <InputText 
              v-model="filters.global.value" 
              placeholder="Search processes..." 
              class="w-full"
            />
          </IconField>

          <!-- Show Inactive Toggle -->
          <div class="flex items-center gap-3">
            <label class="text-gray-600">Show Inactive</label>
            <ToggleSwitch v-model="showInactive" @change="filterProcesses" />
          </div>
        </div>

        <!-- Processes Grid -->
        <template v-if="processes.length === 0">
          <div class="text-gray-500 text-center py-4">
            No recruitment processes available.
          </div>
        </template>
        <template v-else>
          <!-- Process Grid (visible when no process is selected or showProcessDetails is false) -->
          <div v-if="!selectedProcessId || !showProcessDetails" class="grid grid-cols-1 md:grid-cols-2 gap-3 md:gap-4">
            <div v-for="process in filteredProcesses" 
                 :key="process.id" 
                 class="border rounded-lg p-3 hover:bg-blue-50 hover:border-blue-200 transition-all cursor-pointer process-card"
                 @click="selectProcess(process.id)">
              <div class="flex justify-between items-start mb-2">
                <div class="flex flex-col">
                  <h3 class="text-lg font-semibold">{{ process.jobName }}</h3>
                  <span class="text-sm text-gray-500">{{ process.jobCategory }}</span>
                </div>
                
                <div class="flex gap-2">
                  <Button 
                    icon="pi pi-pencil" 
                    text 
                    rounded 
                    @click.stop="editProcess(process)"
                    class="text-green-500 hover:text-green-700"
                  />
                  <Button 
                    icon="pi pi-user-plus" 
                    text 
                    rounded 
                    @click.stop="openEnrollCandidateDialog(process)"
                    class="text-blue-500 hover:text-blue-700"
                    v-tooltip.top="'Enroll Candidate'"
                  />
                  <Button 
                    icon="pi pi-trash" 
                    text 
                    rounded 
                    @click.stop="confirmDelete(process)"
                    class="text-red-500 hover:text-red-700"
                    severity="danger"
                  />
                </div>
              </div>
              <div class="grid grid-cols-2 gap-x-2 gap-y-1 text-sm">
                <div>
                  <span class="font-medium text-gray-700">Workplace:</span>
                  <span class="text-gray-600 ml-1">{{ process.workplaceType }}</span>
                </div>
                <div>
                  <span class="font-medium text-gray-700">Type:</span>
                  <span class="text-gray-600 ml-1">{{ process.jobType }}</span>
                </div>
                <div class="col-span-2">
                  <span class="font-medium text-gray-700">Salary Range:</span>
                  <span class="text-gray-600 ml-1">{{ process.salaryRange }}</span>
                </div>
                <div class="col-span-2 text-gray-500 mb-1">
                  <i class="pi pi-calendar mr-1"></i>
                  Created: {{ new Date(process.createdAt).toLocaleDateString('en-US', {
                    year: 'numeric',
                    month: 'short',
                    day: 'numeric'
                  }) }}
                </div>
              </div>
              <div class="mt-2 flex justify-end">
                <Tag 
                  :value="process.status" 
                  :severity="process.status === 'active' ? 'success' : 'danger'" 
                  class="text-xs"
                />
              </div>
            </div>
          </div>

          <!-- Process Details View (visible when a process is selected and showProcessDetails is true) -->
          <div v-if="selectedProcessId && showProcessDetails" class="process-details-view">
            <div class="flex justify-between items-center mb-4">
              <h3 class="text-xl font-semibold text-blue-800">
                {{ selectedProcess?.jobName }}
                <span class="text-sm font-normal text-blue-600 ml-2">({{ selectedProcess?.jobCategory }})</span>
              </h3>
              <Button 
                icon="pi pi-arrow-left" 
                :label="isMobile ? undefined : 'Back to Leads'" 
                severity="danger" 
                outlined raised
                @click="closeProcessDetails"
                class="close-details-btn"
              />
            </div>

            <!-- Details Section as Fieldset -->
            <Fieldset 
              class="mt-4 process-details-fieldset" 
              :toggleable="true" 
              v-model:collapsed="detailsCollapsed"
              ref="processDetailsFieldset"
            >
              <template #legend>
                <div class="flex items-center gap-2">
                  <i class="pi pi-info-circle text-blue-500"></i>
                  <span class="font-medium">Process Details</span>
                  <span v-if="selectedProcess" class="text-sm text-primary-500">({{ selectedProcess.jobName }})</span>
                  <Button v-if="detailsCollapsed" 
                    icon="pi pi-chevron-down" 
                    class="expand-button p-button-primary"
                    @click="expandDetails"
                  >
                    <span class="text-xs ml-1">Expand Details</span>
                  </Button>
                </div>
              </template>
              
              <div v-if="selectedProcess" class="text-gray-600">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-3 md:gap-4">
                  <div class="p-3 bg-white rounded shadow">
                    <h4 class="font-medium mb-2">Process Information</h4>
                    <div class="text-sm space-y-2">
                      <div class="flex justify-between">
                        <span class="text-gray-500">Job Name:</span>
                        <span class="font-medium">{{ selectedProcess.jobName }}</span>
                      </div>
                      <div class="flex justify-between">
                        <span class="text-gray-500">Category:</span>
                        <span>{{ selectedProcess.jobCategory }}</span>
                      </div>
                      <div class="flex justify-between">
                        <span class="text-gray-500">Workplace:</span>
                        <span>{{ selectedProcess.workplaceType }}</span>
                      </div>
                      <div class="flex justify-between">
                        <span class="text-gray-500">Job Type:</span>
                        <span>{{ selectedProcess.jobType }}</span>
                      </div>
                      <div class="flex justify-between">
                        <span class="text-gray-500">Salary Range:</span>
                        <span>{{ selectedProcess.salaryRange }}</span>
                      </div>
                    </div>
                  </div>
                  
                  <div class="p-3 bg-white rounded shadow">
                    <h4 class="font-medium mb-2">Candidate Pipeline</h4>
                    <div v-if="candidates.length > 0" class="text-sm space-y-2">
                      <div class="flex justify-between">
                        <span class="text-gray-500">Total Candidates:</span>
                        <span class="font-medium">{{ candidates.length }}</span>
                      </div>
                      <div class="flex justify-between">
                        <span class="text-gray-500">New:</span>
                        <span>{{ candidates.filter(c => c.status === 'new').length }}</span>
                      </div>
                      <div class="flex justify-between">
                        <span class="text-gray-500">Reviewed:</span>
                        <span>{{ candidates.filter(c => c.status === 'reviewed').length }}</span>
                      </div>
                      <div class="flex justify-between">
                        <span class="text-gray-500">Interviewed:</span>
                        <span>{{ candidates.filter(c => c.status === 'interviewed').length }}</span>
                      </div>
                      <div class="flex justify-between">
                        <span class="text-gray-500">Rejected:</span>
                        <span>{{ candidates.filter(c => c.status === 'rejected').length }}</span>
                      </div>
                    </div>
                    <div v-else class="text-sm text-gray-500 italic">
                      No candidates found for this process.
                    </div>
                  </div>
                </div>
              </div>
              <div v-else class="text-gray-600">
                Select a recruitment process to view details and candidates.
              </div>
            </Fieldset>
          </div>
        </template>
      </div>
    </div>

    <!-- Process Dialog -->
    <Dialog 
      v-model:visible="processDialog" 
      :style="{ width: '95%', maxWidth: '900px' }" 
      header="Process Details" 
      :modal="true" 
      class="p-fluid"
    >
      <form @submit.prevent="saveProcess">
        <div class="card flex flex-col gap-4">
          <Fieldset 
            legend="Process Information" 
            :toggleable="true" 
            class="mb-4 p-2 md:p-3"
          >
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="flex flex-col gap-2">
                <FloatLabel variant="on">
                  <InputText 
                    id="jobName" 
                    v-model="process.jobName" 
                    :class="{'p-invalid': submitted && !process.jobName}"
                    autofocus
                  />
                  <label for="jobName">Job Name*</label>
                </FloatLabel>
                <small class="p-error" v-if="submitted && !process.jobName">Job Name is required.</small>
              </div>

              <div class="flex flex-col gap-2">
                <FloatLabel variant="on">
                  <InputText 
                    id="jobCategory" 
                    v-model="process.jobCategory"
                    :class="{'p-invalid': submitted && !process.jobCategory}"
                  />
                  <label for="jobCategory">Job Category*</label>
                </FloatLabel>
                <small class="p-error" v-if="submitted && !process.jobCategory">Job Category is required.</small>
              </div>

              <div class="flex flex-col gap-2">
                <FloatLabel variant="on">
                  <InputText 
                    id="workplaceType" 
                    v-model="process.workplaceType"
                    :class="{'p-invalid': submitted && !process.workplaceType}"
                  />
                  <label for="workplaceType">Workplace Type*</label>
                </FloatLabel>
                <small class="p-error" v-if="submitted && !process.workplaceType">Workplace Type is required.</small>
              </div>

              <div class="flex flex-col gap-2">
                <FloatLabel variant="on">
                  <InputText 
                    id="jobType" 
                    v-model="process.jobType"
                    :class="{'p-invalid': submitted && !process.jobType}"
                  />
                  <label for="jobType">Job Type*</label>
                </FloatLabel>
                <small class="p-error" v-if="submitted && !process.jobType">Job Type is required.</small>
              </div>

              <div class="flex flex-col gap-2">
                <FloatLabel variant="on">
                  <InputText 
                    id="salaryRange" 
                    v-model="process.salaryRange"
                    :class="{'p-invalid': submitted && !process.salaryRange}"
                  />
                  <label for="salaryRange">Salary Range*</label>
                </FloatLabel>
                <small class="p-error" v-if="submitted && !process.salaryRange">Salary Range is required.</small>
              </div>

              <div class="flex flex-col gap-2" v-if="process.id">
                <FloatLabel variant="on">
                  <InputText 
                    id="createdAt" 
                    v-model="process.createdAt" 
                    readonly
                  />
                  <label for="createdAt">Creation Date</label>
                </FloatLabel>
              </div>

              <div class="flex flex-col gap-2">
                <div class="flex items-center gap-2">
                  <ToggleSwitch 
                    v-model="processStatus" 
                    id="status"
                  />
                  <span class="text-sm text-surface-500">{{ processStatus ? 'Active' : 'Inactive' }}</span>
                </div>
              </div>
            </div>
          </Fieldset>
          
          <div class="flex justify-end gap-2 mt-4">
            <Button 
              type="button" 
              label="Cancel" 
              icon="pi pi-times" 
              outlined 
              @click="hideDialog" 
            />
            <Button 
              type="submit"
              label="Save" 
              icon="pi pi-check" 
            />
          </div>
        </div>
      </form>
    </Dialog>

    <!-- Delete Confirmation Dialog -->
    <Dialog
      v-model:visible="deleteDialog"
      :style="{ width: '450px' }"
      header="Delete Confirmation"
      :modal="true"
      class="p-fluid"
    >
      <div class="flex flex-col gap-4">
        <div class="text-red-600 font-semibold">Warning: This action cannot be undone</div>
        
        <div class="text-gray-700">
          To confirm deletion, type the {{ deleteType === 'process' ? 'job name' : 'category' }}:
          <span class="font-semibold">{{ deleteType === 'process' ? itemToDelete?.jobName : itemToDelete?.category }}</span>
        </div>
        
        <div class="flex flex-col gap-2">
          <InputText
            v-model="confirmationText"
            :class="{'p-invalid': deleteSubmitted && !isConfirmationValid}"
            :placeholder="deleteType === 'process' ? 'Enter job name' : 'Enter category'"
          />
          <small class="p-error" v-if="deleteSubmitted && !isConfirmationValid">
            {{ deleteType === 'process' ? 'Job name' : 'Category' }} doesn't match
          </small>
        </div>
      </div>
      
      <template #footer>
        <div class="flex justify-end gap-2">
          <Button
            label="Cancel"
            icon="pi pi-times"
            outlined
            @click="deleteDialog = false"
          />
          <Button
            label="Delete"
            icon="pi pi-trash"
            severity="danger"
            @click="handleDelete"
          />
        </div>
      </template>
    </Dialog>

    <!-- Enroll Candidate Dialog -->
    <Dialog
      v-model:visible="enrollCandidateDialog"
      :style="{ width: '95%', maxWidth: '550px' }"
      header="Enroll Candidate"
      :modal="true"
      class="p-fluid"
    >
      <div class="flex flex-col gap-4">
        <div class="flex flex-col gap-1">
          <label for="candidate" class="font-medium text-gray-700">Select Candidate</label>
          <AutoComplete
            id="candidate"
            v-model="selectedCandidate"
            :suggestions="filteredCandidates"
            @complete="searchCandidates"
            field="candidateName"
            optionLabel="candidateName"
            dropdown
            forceSelection
            class="w-full"
            placeholder="Type to search candidates"
          >
            <template #item="slotProps">
              <div class="flex flex-col">
                <div>{{ slotProps.item.candidateName }}</div>
                <small class="text-gray-500">{{ slotProps.item.email }}</small>
              </div>
            </template>
            <template #option="slotProps">
              <div class="flex flex-col">
                <div>{{ slotProps.option.candidateName }}</div>
                <small class="text-gray-500">{{ slotProps.option.email }}</small>
              </div>
            </template>
            <template #value="slotProps">
              <div>{{ slotProps.value?.candidateName || '' }}</div>
            </template>
          </AutoComplete>
          <small v-if="enrollSubmitted && !selectedCandidate" class="p-error">Candidate is required.</small>
        </div>
        
        <div class="flex flex-col gap-1">
          <label for="salaryExpectation" class="font-medium text-gray-700">Salary Expectation</label>
          <InputNumber
            id="salaryExpectation"
            v-model="salaryExpectation"
            mode="currency"
            currency="USD"
            locale="en-US"
            :minFractionDigits="0"
            class="w-full"
          />
          <small v-if="enrollSubmitted && !salaryExpectation" class="p-error">Salary expectation is required.</small>
        </div>
        
        <div class="flex justify-end gap-2 mt-4">
          <Button
            label="Cancel"
            icon="pi pi-times"
            text
            @click="closeEnrollCandidateDialog"
          />
          <Button
            label="Enroll"
            icon="pi pi-check"
            @click="enrollCandidate"
          />
        </div>
      </div>
    </Dialog>

    <!-- Candidates and Analytics Section -->
    <div class="mt-6 grid grid-cols-1 lg:grid-cols-3 gap-4" v-if="selectedProcess && showProcessDetails">
      <!-- Candidates Table (takes 2/3 of the space on large screens) -->
      <div class="lg:col-span-2 p-4 bg-white rounded-lg border border-gray-200">
        <h3 class="text-lg font-semibold mb-4">Candidates for {{ selectedProcess.jobName }}</h3>
        
        <div v-if="loadingCandidates" class="text-center py-4">
          <i class="pi pi-spin pi-spinner text-2xl"></i>
          <p class="text-gray-600 mt-2">Loading candidates...</p>
        </div>

        <div v-else>
          <div class="mb-3 text-sm text-gray-600">
            <i class="pi pi-info-circle mr-1"></i>
            Candidates are sorted by Approved Interviews (highest first), then by Skillset Rating (highest first).
          </div>
          <DataTable
            :value="sortedCandidates" 
            dataKey="id"
            class="p-datatable-sm"
            :paginator="true" 
            :rows="10"
            :rowsPerPageOptions="[5, 10, 20, 50]"
            responsiveLayout="stack"
            breakpoint="960px"
            :loading="loadingCandidates"
            :globalFilterFields="['candidateName', 'email', 'country']"
            v-model:filters="filters"
            filterDisplay="menu"
            @row-click="onRowClick"
          >
            <Column field="candidateName" header="Candidate" sortable>
              <template #body="{ data }">
                <div class="flex items-center gap-2">
                  <Avatar 
                    :label="getInitials(data.candidateName)" 
                    class="w-8 h-8 bg-primary-100 text-primary-700 font-medium" 
                    size="normal" 
                    shape="circle"
                  />
                  <div class="flex flex-col">
                    <span class="font-medium">{{ data.candidateName }}</span>
                    <span class="text-sm text-gray-500">{{ data.email }}</span>
                    <!-- Mobile-only metrics display -->
                    <div class="md:hidden mt-2 flex flex-wrap gap-3 text-sm" v-if="candidateAnalytics[data.email]">
                      <div class="flex items-center gap-1" v-tooltip="`Average Skillset Rating`">
                        <i class="pi pi-star-fill text-yellow-500"></i>
                        <span>{{ candidateAnalytics[data.email]?.skillsetAvg?.toFixed(1) || '0.0' }}</span>
                      </div>
                      <div class="flex items-center gap-1" v-tooltip="`Approved Interviews`">
                        <i class="pi pi-check-circle text-green-500"></i>
                        <span>{{ candidateAnalytics[data.email]?.interviewYes || 0 }}</span>
                      </div>
                      <div class="flex items-center gap-1" v-tooltip="`Pending Interviews`">
                        <i class="pi pi-clock text-yellow-500"></i>
                        <span>{{ candidateAnalytics[data.email]?.interviewMaybe || 0 }}</span>
                      </div>
                      <div class="flex items-center gap-1" v-tooltip="`Rejected Interviews`">
                        <i class="pi pi-times-circle text-red-500"></i>
                        <span>{{ candidateAnalytics[data.email]?.interviewNo || 0 }}</span>
                      </div>
                      <div class="flex items-center gap-1" v-tooltip="`Certifications`">
                        <i class="pi pi-id-card text-blue-500"></i>
                        <span>{{ candidateAnalytics[data.email]?.certificationCount || 0 }}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </template>
            </Column>

            <Column field="country" header="Country" sortable class="hidden md:table-cell">
              <template #body="{ data }">
                <span class="text-gray-700 capitalize">{{ data.country?.toLowerCase() }}</span>
              </template>
            </Column>

            <Column header="Metrics" class="hidden md:table-cell">
              <template #body="{ data }">
                <div v-if="candidateAnalytics[data.email]" class="flex items-center gap-3 text-sm">
                  <div class="flex items-center gap-1" v-tooltip="`Average Skillset Rating`">
                    <i class="pi pi-star-fill text-yellow-500"></i>
                    <span>{{ candidateAnalytics[data.email]?.skillsetAvg?.toFixed(1) || '0.0' }}</span>
                  </div>
                  <div class="flex items-center gap-1" v-tooltip="`Approved Interviews`">
                    <i class="pi pi-check-circle text-green-500"></i>
                    <span>{{ candidateAnalytics[data.email]?.interviewYes || 0 }}</span>
                  </div>
                  <div class="flex items-center gap-1" v-tooltip="`Pending Interviews`">
                    <i class="pi pi-clock text-yellow-500"></i>
                    <span>{{ candidateAnalytics[data.email]?.interviewMaybe || 0 }}</span>
                  </div>
                  <div class="flex items-center gap-1" v-tooltip="`Rejected Interviews`">
                    <i class="pi pi-times-circle text-red-500"></i>
                    <span>{{ candidateAnalytics[data.email]?.interviewNo || 0 }}</span>
                  </div>
                  <div class="flex items-center gap-1" v-tooltip="`Certifications`">
                    <i class="pi pi-id-card text-blue-500"></i>
                    <span>{{ candidateAnalytics[data.email]?.certificationCount || 0 }}</span>
                  </div>
                </div>
                <div v-else class="text-gray-400 text-sm">
                  Loading metrics...
                </div>
              </template>
            </Column>
          </DataTable>
        </div>
      </div>

      <!-- Process Analytics Summary (takes 1/3 of the space on large screens) -->
      <div class="p-4 bg-white rounded-lg border border-gray-200">
        <h3 class="text-lg font-semibold mb-4">Process Analytics</h3>
        
        <div v-if="loadingProcessAnalytics" class="text-center py-4">
          <i class="pi pi-spin pi-spinner text-2xl"></i>
          <p class="text-gray-600 mt-2">Loading analytics...</p>
        </div>

        <div v-else-if="processAnalytics.candidates.length === 0" class="text-center py-4 text-gray-500">
          No analytics data available for this process.
        </div>

        <div v-else class="space-y-4">
          <!-- Skillset Ratings Card -->
          <div class="p-3 bg-gray-50 rounded-lg border border-gray-200">
            <h4 class="font-medium text-gray-800 mb-3 flex items-center">
              <i class="pi pi-star-fill text-yellow-500 mr-2"></i>
              Skillset Ratings
            </h4>
            <div class="flex items-center justify-between mb-2">
              <span class="text-sm text-gray-600">Average Rating:</span>
              <span class="font-medium">
                {{ calculateAverage(processAnalytics.candidates.map(c => c.skillsetAvg)).toFixed(1) }}
              </span>
            </div>
            <div class="flex items-center justify-between mb-2">
              <span class="text-sm text-gray-600">Highest Rating:</span>
              <span class="font-medium">
                {{ Math.max(...processAnalytics.candidates.map(c => c.skillsetAvg)).toFixed(1) }}
              </span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-sm text-gray-600">Lowest Rating:</span>
              <span class="font-medium">
                {{ Math.min(...processAnalytics.candidates.map(c => c.skillsetAvg || 0)).toFixed(1) }}
              </span>
            </div>
          </div>

          <!-- Interview Stats Card -->
          <div class="p-3 bg-gray-50 rounded-lg border border-gray-200">
            <h4 class="font-medium text-gray-800 mb-3 flex items-center">
              <i class="pi pi-comments text-blue-500 mr-2"></i>
              Interview Statistics
            </h4>
            <div class="flex items-center justify-between mb-2">
              <span class="text-sm text-gray-600">Approved:</span>
              <span class="font-medium text-green-600">
                {{ processAnalytics.candidates.reduce((sum, c) => sum + c.interviewYes, 0) }}
              </span>
            </div>
            <div class="flex items-center justify-between mb-2">
              <span class="text-sm text-gray-600">Pending:</span>
              <span class="font-medium text-yellow-600">
                {{ processAnalytics.candidates.reduce((sum, c) => sum + c.interviewMaybe, 0) }}
              </span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-sm text-gray-600">Rejected:</span>
              <span class="font-medium text-red-600">
                {{ processAnalytics.candidates.reduce((sum, c) => sum + c.interviewNo, 0) }}
              </span>
            </div>
          </div>

          <!-- Certifications Card -->
          <div class="p-3 bg-gray-50 rounded-lg border border-gray-200">
            <h4 class="font-medium text-gray-800 mb-3 flex items-center">
              <i class="pi pi-id-card text-blue-500 mr-2"></i>
              Certifications
            </h4>
            <div class="flex items-center justify-between mb-2">
              <span class="text-sm text-gray-600">Total Certifications:</span>
              <span class="font-medium">
                {{ processAnalytics.candidates.reduce((sum, c) => sum + c.certificationCount, 0) }}
              </span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-sm text-gray-600">Average per Candidate:</span>
              <span class="font-medium">
                {{ (processAnalytics.candidates.reduce((sum, c) => sum + c.certificationCount, 0) / 
                    processAnalytics.candidates.length).toFixed(1) }}
              </span>
            </div>
          </div>

          <!-- Salary Expectations Card -->
          <div class="p-3 bg-gray-50 rounded-lg border border-gray-200">
            <h4 class="font-medium text-gray-800 mb-3 flex items-center">
              <i class="pi pi-dollar text-green-500 mr-2"></i>
              Salary Expectations
            </h4>
            <div class="flex items-center justify-between mb-2">
              <span class="text-sm text-gray-600">Average:</span>
              <span class="font-medium">
                ${{ calculateAverage(processAnalytics.candidates.map(c => c.salaryExpectation)).toFixed(0) }}
              </span>
            </div>
            <div class="flex items-center justify-between mb-2">
              <span class="text-sm text-gray-600">Highest:</span>
              <span class="font-medium">
                ${{ Math.max(...processAnalytics.candidates.map(c => c.salaryExpectation || 0)).toFixed(0) }}
              </span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-sm text-gray-600">Lowest:</span>
              <span class="font-medium">
                ${{ Math.min(...processAnalytics.candidates.filter(c => c.salaryExpectation > 0).map(c => c.salaryExpectation)).toFixed(0) }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeMount, watch } from 'vue';
import { useToast } from 'primevue/usetoast';
import { useConfirm } from 'primevue/useconfirm';
import Select from 'primevue/select';
import ToggleSwitch from 'primevue/toggleswitch';
import FloatLabel from 'primevue/floatlabel';
import Fieldset from 'primevue/fieldset';
import { useRouter } from 'vue-router';
import IconField from 'primevue/iconfield';
import InputIcon from 'primevue/inputicon';
import Avatar from 'primevue/avatar';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Dropdown from 'primevue/dropdown';
import Breadcrumb from 'primevue/breadcrumb';
import Dialog from 'primevue/dialog';
import AutoComplete from 'primevue/autocomplete';
import InputNumber from 'primevue/inputnumber';

const toast = useToast();
const confirm = useConfirm();
const router = useRouter();
const loading = ref(false);
const processDialog = ref(false);
const deleteDialog = ref(false);
const submitted = ref(false);
const processes = ref([]);
const process = ref({});
const sessionInfo = ref(null);
const deleteType = ref('');
const itemToDelete = ref(null);
const confirmationText = ref('');
const deleteSubmitted = ref(false);
const showInactive = ref(false);
const allProcesses = ref([]);
const candidates = ref([]);
const selectedProcessId = ref(null);
const loadingCandidates = ref(false);
const statusOptions = ref(['new', 'reviewed', 'interviewed', 'rejected']);
const candidateAnalytics = ref({});
const processAnalytics = ref({ candidates: [] });
const loadingProcessAnalytics = ref(false);

// Add breadcrumb configuration
const breadcrumbHome = ref({ icon: 'pi pi-home', to: '/' });
const breadcrumbItems = ref([
  { label: 'Career Path', to: '/careerpath' },
  { label: 'Recruitment', disabled: true }
]);

// Add mobile detection
const isMobile = ref(false);
const detailsCollapsed = ref(true);
const showProcessDetails = ref(false);

const checkMobile = () => {
  const windowIsMobile = window.innerWidth < 768;
  
  // Check if user has a preference for the details section
  const userPreference = localStorage.getItem('recruitmentLeadsDetailsExpanded');
  
  if (userPreference === 'true') {
    // User previously expanded the details, so keep it expanded
    detailsCollapsed.value = false;
  } else {
    // Otherwise use the window size to determine if collapsed
    detailsCollapsed.value = windowIsMobile;
  }
  
  // Update isMobile for responsive behaviors
  isMobile.value = windowIsMobile;
};

// Handle details toggle
const handleDetailsToggle = (e) => {
  console.log('Details toggled:', e);
  
  // Store user preference in localStorage
  if (e.value === false) {
    // User expanded the details
    localStorage.setItem('recruitmentLeadsDetailsExpanded', 'true');
  } else {
    // User collapsed the details
    localStorage.setItem('recruitmentLeadsDetailsExpanded', 'false');
  }
};

// Check mobile on mount and window resize
onBeforeMount(() => {
  checkMobile();
  window.addEventListener('resize', checkMobile);
});

onMounted(() => {
  // Cleanup event listener
  return () => {
    window.removeEventListener('resize', checkMobile);
  };
});

// Simple filter setup
const filters = ref({
  global: { value: null }
});

// Add this computed property after your existing computed properties
const filteredProcesses = computed(() => {
  let filtered = showInactive.value 
    ? processes.value 
    : processes.value.filter(process => process.status === 'active');
  
  if (filters.value.global.value) {
    const query = filters.value.global.value.toLowerCase();
    filtered = filtered.filter(process => 
      process.jobName?.toLowerCase().includes(query) ||
      process.jobCategory?.toLowerCase().includes(query) ||
      process.workplaceType?.toLowerCase().includes(query) ||
      process.jobType?.toLowerCase().includes(query) ||
      process.salaryRange?.toLowerCase().includes(query)
    );
  }
  
  return filtered.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
});

// GraphQL Queries
const LIST_PROCESSES = `
    query getRecruitmentProcessByCompanyId($companyId: String!) {
        getRecruitmentProcessByCompanyId(companyId: $companyId) {
            id
            companyId
            jobName
            jobCategory
            workplaceType
            jobType
            salaryRange
            status
            jobDetails
            createdAt
            updatedAt
        }
    }
`;

const CREATE_PROCESS = `
    mutation CreateRecruitmentProcess($input: CreateRecruitmentProcessInput!) {
        createRecruitmentProcess(input: $input) {
            id
            companyId
            jobName
            jobCategory
            workplaceType
            jobType
            salaryRange
            status
            createdAt
            updatedAt
        }
    }
`;

const UPDATE_PROCESS = `
    mutation UpdateRecruitmentProcess($id: String!, $input: UpdateRecruitmentProcessInput!) {
        updateRecruitmentProcess(id: $id, input: $input) {
            id
            companyId
            jobName
            jobCategory
            workplaceType
            jobType
            salaryRange
            status
            createdAt
            updatedAt
        }
    }
`;

const DELETE_PROCESS = `
    mutation DeleteRecruitmentProcess($id: String!) {
        deleteRecruitmentProcess(id: $id)
    }
`;

const CANDIDATES_QUERY = `
  query CandidatesByRecruitmentProcessId($recruitmentProcessId: String!) {
    candidatesByRecruitmentProcessId(recruitmentProcessId: $recruitmentProcessId) {
      id
      candidateCV
      candidateName
      companyId
      country
      companyName
      createdAt
      email
      salaryExpectation
      status
    }
  }
`;

const CANDIDATE_ANALYTICS_QUERY = `
  query CandidateAnalytics($email: String!) {
    candidateAnalytics(email: $email) {
      skillsetAvg
      interviewYes
      interviewMaybe
      interviewNo
      interviewRating
      certificationCount
    }
  }
`;

const RECRUITMENT_PROCESS_ANALYTICS_QUERY = `
  query RecruitmentProcessAnalytics($recruitmentProcessId: String!) {
    recruitmentProcessAnalytics(recruitmentProcessId: $recruitmentProcessId) {
      candidates {
        candidateName
        email
        country
        salaryExpectation
        skillsetAvg
        interviewYes
        interviewMaybe
        interviewNo
        interviewRating
        certificationCount
      }
    }
  }
`;

// Add fetchSessionInfo function
const fetchSessionInfo = async () => {
  try {
    const response = await fetch('core/auth/verify/session', {
      method: 'GET',
      credentials: 'include',
      headers: {
        'Accept': 'application/json',
      }
    });

    if (response.ok) {
      const data = await response.json();
      sessionInfo.value = data.user;
    }
  } catch (error) {
    console.error('Error fetching session info:', error);
    router.push({ name: 'login' });
  }
};

// Modify the loadProcesses function
async function loadProcesses() {
  if (!sessionInfo.value?.companyId) {
    toast.add({ severity: 'warn', summary: 'No Company Selected', detail: 'Please select a company first', life: 3000 });
    return;
  }

  try {
    loading.value = true;
    const response = await fetch(`${import.meta.env.VITE_API_URL}/graphql`, {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json'
      },
      credentials: 'include',
      body: JSON.stringify({
        query: LIST_PROCESSES,
        variables: {
          companyId: sessionInfo.value.companyId
        }
      })
    });
    const result = await response.json();
    
    if (result.data?.getRecruitmentProcessByCompanyId) {
      allProcesses.value = result.data.getRecruitmentProcessByCompanyId.map(process => ({
        ...process,
        jobDetailsArray: process.jobDetailsArray || []
      }));
      processes.value = [...allProcesses.value];
      filterProcesses();
    } else if (result.errors) {
      // Ignore jobDetailsArray errors as they are expected when null
      const nonJobDetailsErrors = result.errors.filter(error => 
        !error.message.includes("'dict' object has no attribute 'category'") &&
        !error.path?.some(p => p === 'jobDetailsArray')
      );
      
      if (nonJobDetailsErrors.length > 0) {
        throw new Error(nonJobDetailsErrors[0]?.message || 'Failed to load processes');
      }
    }
  } catch (error) {
    console.error('Error loading processes:', error);
    toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to load processes', life: 3000 });
  } finally {
    loading.value = false;
  }
}

// Add this function after loadProcesses
function filterProcesses() {
  if (showInactive.value) {
    processes.value = [...allProcesses.value];
  } else {
    processes.value = allProcesses.value.filter(process => process.status === 'active');
  }
}

// Dialog management functions
function openNewProcess() {
  process.value = {
    jobName: '',
    jobCategory: '',
    workplaceType: '',
    jobType: '',
    salaryRange: '',
    status: 'active'
  };
  submitted.value = false;
  processDialog.value = true;
}

function editProcess(data) {
  process.value = { ...data };
  processDialog.value = true;
}

function hideDialog() {
  processDialog.value = false;
  submitted.value = false;
}

// Save functions
async function saveProcess() {
  submitted.value = true;

  if (!process.value.jobName?.trim() || !process.value.jobCategory?.trim() || 
      !process.value.workplaceType?.trim() || !process.value.jobType?.trim() || 
      !process.value.salaryRange?.trim()) {
    toast.add({ severity: 'error', summary: 'Required Fields', detail: 'Please fill in all required fields', life: 3000 });
    return;
  }

  try {
    const isNewProcess = !process.value.id;
    const query = isNewProcess ? CREATE_PROCESS : UPDATE_PROCESS;
    
    const variables = isNewProcess 
      ? { 
          input: {
            companyId: sessionInfo.value.companyId,
            companyName: sessionInfo.value.companyName,
            jobName: process.value.jobName,
            jobCategory: process.value.jobCategory,
            workplaceType: process.value.workplaceType,
            jobType: process.value.jobType,
            salaryRange: process.value.salaryRange,
            status: process.value.status,
            jobDetails: process.value.jobDetails || '',
            postUrl: process.value.postUrl || '',
            createdBy: sessionInfo.value.email,
            updatedBy: sessionInfo.value.email
          }
        }
      : { 
          id: process.value.id,
          input: {
            jobName: process.value.jobName,
            jobCategory: process.value.jobCategory,
            workplaceType: process.value.workplaceType,
            jobType: process.value.jobType,
            salaryRange: process.value.salaryRange,
            status: process.value.status,
            jobDetails: process.value.jobDetails || '',
            postUrl: process.value.postUrl || '',
            updatedBy: sessionInfo.value.email
          }
        };

    const response = await fetch(`${import.meta.env.VITE_API_URL}/graphql`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ query, variables })
    });

    const result = await response.json();
    
    if (result.errors) {
      throw new Error(result.errors[0]?.message || 'Failed to save process');
    }

    toast.add({
      severity: 'success',
      summary: 'Success',
      detail: isNewProcess ? 'Process Created' : 'Process Updated',
      life: 3000
    });

    processDialog.value = false;
    await loadProcesses();
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: error.message || 'Failed to save process',
      life: 3000
    });
  }
}

// Delete functions
function confirmDelete(data) {
  deleteType.value = 'process';
  itemToDelete.value = data;
  confirmationText.value = '';
  deleteSubmitted.value = false;
  deleteDialog.value = true;
}

async function handleDelete() {
  deleteSubmitted.value = true;
  
  if (!isConfirmationValid.value) {
    return;
  }
  
  await deleteProcess();
  
  deleteDialog.value = false;
  deleteSubmitted.value = false;
  confirmationText.value = '';
}

async function deleteProcess() {
  try {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/graphql`, {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json'
      },
      credentials: 'include',
      body: JSON.stringify({
        query: DELETE_PROCESS,
        variables: { 
          id: itemToDelete.value.id 
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
      detail: 'Process deleted successfully', 
      life: 3000 
    });
    
    await loadProcesses();
  } catch (error) {
    toast.add({ 
      severity: 'error', 
      summary: 'Error', 
      detail: error.message || 'Failed to delete process', 
      life: 3000 
    });
  }
}

// Computed properties
const processStatus = computed({
  get: () => process.value.status === 'active',
  set: (newValue) => {
    process.value.status = newValue ? 'active' : 'inactive'
  }
});

const isConfirmationValid = computed(() => {
  if (deleteType.value === 'process') {
    return confirmationText.value === itemToDelete.value?.jobName;
  } else {
    return confirmationText.value === itemToDelete.value?.category;
  }
});

// Update the fetchCandidates function to also fetch process analytics
async function fetchCandidates(processId) {
  try {
    loadingCandidates.value = true;
    loadingProcessAnalytics.value = true;
    selectedProcessId.value = processId;
    
    // Fetch candidates
    const candidatesResponse = await fetch(`${import.meta.env.VITE_API_URL}/graphql`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({
        query: CANDIDATES_QUERY,
        variables: { recruitmentProcessId: processId }
      })
    });

    const candidatesResult = await candidatesResponse.json();
    
    if (candidatesResult.errors) {
      throw new Error(candidatesResult.errors[0]?.message || 'Failed to fetch candidates');
    }

    candidates.value = candidatesResult.data?.candidatesByRecruitmentProcessId || [];
    
    // Fetch process analytics in parallel
    const analyticsResponse = await fetch(`${import.meta.env.VITE_API_URL}/graphql`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({
        query: RECRUITMENT_PROCESS_ANALYTICS_QUERY,
        variables: { recruitmentProcessId: processId }
      })
    });

    const analyticsResult = await analyticsResponse.json();
    
    if (analyticsResult.errors) {
      console.error('Analytics error:', analyticsResult.errors);
      // Don't throw here, just log the error and continue
    } else {
      processAnalytics.value = analyticsResult.data?.recruitmentProcessAnalytics || { candidates: [] };
      
      // Create a map of analytics by email for easy access
      const analyticsMap = {};
      processAnalytics.value.candidates.forEach(candidate => {
        analyticsMap[candidate.email] = candidate;
      });
      
      // Update candidateAnalytics with the data from process analytics
      processAnalytics.value.candidates.forEach(candidate => {
        candidateAnalytics.value[candidate.email] = {
          skillsetAvg: candidate.skillsetAvg,
          interviewYes: candidate.interviewYes,
          interviewMaybe: candidate.interviewMaybe,
          interviewNo: candidate.interviewNo,
          interviewRating: candidate.interviewRating,
          certificationCount: candidate.certificationCount
        };
      });
    }

    // If we didn't get analytics for all candidates, fetch them individually
    const missingAnalytics = candidates.value.filter(
      candidate => !candidateAnalytics.value[candidate.email]
    );
    
    if (missingAnalytics.length > 0) {
      const analyticsPromises = missingAnalytics.map(async candidate => {
        const res = await fetch(`${import.meta.env.VITE_API_URL}/graphql`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include',
          body: JSON.stringify({
            query: CANDIDATE_ANALYTICS_QUERY,
            variables: { email: candidate.email }
          })
        });
        const result = await res.json();
        return { email: candidate.email, data: result.data?.candidateAnalytics };
      });

      const individualAnalyticsResults = await Promise.all(analyticsPromises);
      individualAnalyticsResults.forEach(result => {
        if (result.data) {
          candidateAnalytics.value[result.email] = result.data;
        }
      });
    }

    // Add analytics data directly to candidates for sorting
    candidates.value = candidates.value.map(candidate => {
      const analytics = candidateAnalytics.value[candidate.email] || {};
      return {
        ...candidate,
        skillsetAvg: analytics.skillsetAvg || 0,
        interviewYes: analytics.interviewYes || 0,
        interviewMaybe: analytics.interviewMaybe || 0,
        interviewNo: analytics.interviewNo || 0,
        interviewRating: analytics.interviewRating || 0,
        certificationCount: analytics.certificationCount || 0
      };
    });

  } catch (error) {
    console.error('Error fetching data:', error);
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: error.message || 'Failed to load candidates',
      life: 3000
    });
  } finally {
    loadingCandidates.value = false;
    loadingProcessAnalytics.value = false;
  }
}

// Add computed property to find selected process
const selectedProcess = computed(() => 
  processes.value.find(p => p.id === selectedProcessId.value)
);

// Add initials generator
const getInitials = (name) => {
  if (!name) return '??';
  const names = name.split(' ');
  let initials = names[0].substring(0, 1).toUpperCase();
  if (names.length > 1) {
    initials += names[names.length - 1].substring(0, 1).toUpperCase();
  }
  return initials;
};

// Update status severity mapping to handle all cases
const getStatusSeverity = (status) => {
  const statusMap = {
    'new': 'info',
    'reviewed': 'warning',
    'interviewed': 'success',
    'rejected': 'danger'
  };
  return statusMap[status?.toLowerCase()] || 'info';
};

// Add to script section
function viewCandidate(candidate) {
  // Implement candidate detail view
  console.log('View candidate:', candidate);
}

function confirmDeleteCandidate(candidate) {
  // Implement candidate deletion logic
  console.log('Delete candidate:', candidate);
}

// Add to script section
function onRowClick(event) {
  // Only navigate if clicking the row (not buttons)
  const isButton = event.originalEvent.target.closest('button') || 
                  event.originalEvent.target.closest('.p-column-header');
  
  if (!isButton && event.data?.id) {
    router.push({
      name: 'profiles-id',
      params: { id: event.data.id }
    });
  }
}

// Add helper function for calculating averages
function calculateAverage(values) {
  const validValues = values.filter(v => v !== null && v !== undefined && !isNaN(v));
  if (validValues.length === 0) return 0;
  return validValues.reduce((sum, val) => sum + val, 0) / validValues.length;
}

// Initialize component
onMounted(async () => {
  try {
    await fetchSessionInfo();
    await loadProcesses();
  } catch (error) {
    console.error('Error initializing recruitment leads page:', error);
    toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to load data', life: 3000 });
  }
});

// Add a reference to the fieldset
const processDetailsFieldset = ref(null);

// Function to expand the details
const expandDetails = (event) => {
  event.stopPropagation(); // Prevent the fieldset's own toggle from firing
  detailsCollapsed.value = false;
  localStorage.setItem('recruitmentLeadsDetailsExpanded', 'true');
};

// Watch for changes to the collapsed state
watch(detailsCollapsed, (newValue) => {
  localStorage.setItem('recruitmentLeadsDetailsExpanded', (!newValue).toString());
});

// Add a function to select a process and show details
function selectProcess(processId) {
  selectedProcessId.value = processId;
  showProcessDetails.value = true;
  fetchCandidates(processId);
}

// Add a function to close process details and return to the grid
function closeProcessDetails() {
  showProcessDetails.value = false;
}

// Add these variables for the enroll candidate dialog
const enrollCandidateDialog = ref(false);
const selectedCandidate = ref(null);
const salaryExpectation = ref(null);
const enrollSubmitted = ref(false);
const filteredCandidates = ref([]);
const allCandidates = ref([]);
const enrollmentProcess = ref(null);

// Add these functions for the enroll candidate dialog
function openEnrollCandidateDialog(process) {
  enrollmentProcess.value = process;
  selectedCandidate.value = null;
  salaryExpectation.value = null;
  enrollSubmitted.value = false;
  enrollCandidateDialog.value = true;
  
  // Fetch candidates if not already loaded
  if (allCandidates.value.length === 0) {
    fetchAllCandidates();
  }
}

function closeEnrollCandidateDialog() {
  enrollCandidateDialog.value = false;
  selectedCandidate.value = null;
  salaryExpectation.value = null;
  enrollSubmitted.value = false;
}

async function fetchAllCandidates() {
  try {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/graphql`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query: `
          query CandidatesByCompanyId($companyId: String!) {
            candidatesByCompanyId(companyId: $companyId) {
              candidateName
              email
              id
            }
          }
        `,
        variables: {
          companyId: sessionInfo.value?.companyId || '',
        },
      }),
    });

    const result = await response.json();
    if (result.errors) {
      throw new Error(result.errors[0]?.message || 'Failed to fetch candidates');
    }

    allCandidates.value = result.data.candidatesByCompanyId || [];
  } catch (error) {
    console.error('Error fetching candidates:', error);
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: 'Failed to fetch candidates',
      life: 3000,
    });
  }
}

function searchCandidates(event) {
  const query = event.query.toLowerCase();
  filteredCandidates.value = allCandidates.value.filter(
    candidate => 
      candidate.candidateName.toLowerCase().includes(query) || 
      candidate.email.toLowerCase().includes(query)
  );
}

async function enrollCandidate() {
  enrollSubmitted.value = true;
  
  // Validate form
  if (!selectedCandidate.value || !salaryExpectation.value) {
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: 'Please fill in all required fields',
      life: 3000,
    });
    return;
  }
  
  try {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/graphql`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query: `
          mutation EnrollCandidate($input: EnrollCandidateInput!) {
            enrollCandidate(input: $input) {
              id
              candidateName
              email
              status
              salaryExpectation
              recruitmentProcessId
            }
          }
        `,
        variables: {
          input: {
            id: selectedCandidate.value.id,
            recruitmentProcessId: enrollmentProcess.value.id,
            recruitmentProcessName: enrollmentProcess.value.jobName,
            salaryExpectation: salaryExpectation.value
          },
        },
      }),
    });

    const result = await response.json();
    if (result.errors) {
      throw new Error(result.errors[0]?.message || 'Failed to enroll candidate');
    }

    // Show success toast
    toast.add({
      severity: 'success',
      summary: 'Success',
      detail: 'Candidate enrolled successfully',
      life: 3000,
    });
    
    // Refresh candidates list if we're viewing this process
    if (selectedProcessId.value === enrollmentProcess.value.id) {
      fetchCandidates(selectedProcessId.value);
    }
    
    // Ask if user wants to enroll another candidate - only show this dialog once
    confirm.require({
      message: 'Do you want to enroll another candidate?',
      header: 'Confirmation',
      icon: 'pi pi-question-circle',
      acceptClass: 'p-button-success',
      accept: () => {
        // Reset form but keep dialog open
        selectedCandidate.value = null;
        salaryExpectation.value = null;
        enrollSubmitted.value = false;
      },
      reject: () => {
        closeEnrollCandidateDialog();
      }
    });
    
  } catch (error) {
    console.error('Error enrolling candidate:', error);
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: error.message || 'Failed to enroll candidate',
      life: 3000,
    });
  }
}

// Replace the existing sortedCandidates computed property with the following:
const sortedCandidates = computed(() => {
  return candidates.value.slice().sort((a, b) => {
    // Sort by number of interviewYes descending
    if (b.interviewYes !== a.interviewYes) {
      return b.interviewYes - a.interviewYes;
    }
    // Then sort by skillsetAvg descending; ensure they are numbers
    return Number(b.skillsetAvg) - Number(a.skillsetAvg);
  });
});
</script>

<style scoped>
/* Form Control Base Styles */
:deep(.p-inputtext),
:deep(.p-dropdown),
:deep(.p-autocomplete),
:deep(.p-inputnumber) {
  width: 100%;
  height: 40px;
}

/* Input Text and AutoComplete */
:deep(.p-inputtext),
:deep(.p-autocomplete-input) {
  padding: 0.5rem 0.75rem;
  font-size: 14px;
  line-height: 1.5;
}

/* Dropdown Specific */
:deep(.p-dropdown) {
  display: flex;
  align-items: center;
}

:deep(.p-dropdown-label) {
  padding: 0.5rem 0.75rem;
  line-height: 1.5;
}

:deep(.p-dropdown-trigger) {
  width: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* ToggleSwitch Adjustments */
:deep(.p-toggleswitch) {
  height: 24px;
}

:deep(.p-toggleswitch .p-toggleswitch-slider) {
  border-radius: 12px;
}

/* Form Layout Spacing */
.form-field {
  margin-bottom: 1rem;
}

/* Label Styling */
label {
  display: block;
  margin-bottom: 0.5rem;
  font-size: 14px;
  color: var(--text-color);
}

.p-dialog .p-dialog-content {
  padding: 2rem;
}

/* Update Fieldset padding */
:deep(.p-fieldset-content) {
  padding: 0.75rem;
}

@media (max-width: 768px) {
  :deep(.p-fieldset-content) {
    padding: 1rem;
  }
  
  /* Adjust grid gap for mobile */
  .grid {
    gap: 0.75rem;
  }
  
  /* Make form fields slightly larger on mobile */
  :deep(.p-inputtext),
  :deep(.p-dropdown),
  :deep(.p-autocomplete) {
    height: 44px;
    font-size: 15px;
  }
  
  /* Adjust toggle switch size */
  :deep(.p-toggleswitch) {
    height: 28px;
  }
}

/* Add to the style section */
:deep(.p-datatable .p-datatable-tbody tr:hover) {
  background-color: #f8f9fa;
  cursor: pointer;
  transition: background-color 0.2s;
}

:deep(.p-datatable .p-datatable-tbody tr:focus) {
  outline: none;
  background-color: #e9ecef;
}

/* For better visual hierarchy */
:deep(.p-datatable .p-datatable-tbody td) {
  transition: background-color 0.2s;
}

:deep(.p-datatable-responsive-stack) .p-datatable-tbody > tr {
  display: flex;
  flex-direction: column;
  padding: 1rem;
  margin-bottom: 1rem;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  background-color: white;
}

:deep(.p-datatable-responsive-stack) .p-datatable-tbody > tr > td {
  width: 100%;
  display: flex;
  align-items: center;
  padding: 0.5rem 0;
  border-bottom: none;
}

:deep(.p-datatable-responsive-stack) .p-datatable-tbody > tr > td:last-child {
  justify-content: flex-end;
  padding-top: 0.75rem;
  margin-top: 0.5rem;
  border-top: 1px solid #f0f0f0;
}

@media (max-width: 768px) {
  :deep(.p-datatable .p-paginator-bottom) {
    flex-wrap: wrap;
    justify-content: center;
    gap: 0.5rem;
  }
  
  :deep(.p-datatable .p-paginator-element) {
    min-width: 2.5rem;
    height: 2.5rem;
  }
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

/* Add to the style section */
:deep(.p-fieldset) {
  border-radius: 8px;
  transition: all 0.2s ease;
}

:deep(.p-fieldset:hover) {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

:deep(.p-fieldset-legend) {
  padding: 0.75rem 1.25rem;
  border-radius: 6px;
  background-color: #f8f9fa;
  transition: background-color 0.2s;
}

:deep(.p-fieldset-legend:hover) {
  background-color: #e9ecef;
  cursor: pointer;
}

:deep(.p-fieldset-toggleable .p-fieldset-legend) {
  padding-right: 2.5rem;
  position: relative;
}

:deep(.p-fieldset-toggleable .p-fieldset-legend-text) {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

:deep(.p-fieldset-toggler) {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  width: 1.5rem;
  height: 1.5rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f0f0f0;
  transition: all 0.2s;
}

:deep(.p-fieldset-toggler:hover) {
  background-color: #e0e0e0;
}

@media (max-width: 768px) {
  :deep(.p-fieldset-legend) {
    padding: 0.5rem 1rem;
  }
  
  :deep(.p-fieldset-toggler) {
    width: 1.25rem;
    height: 1.25rem;
  }
}

/* Add styles for the process details fieldset */
.process-details-fieldset {
  border: 1px solid #e0e7ff;
  border-radius: 8px;
  overflow: visible;
  position: relative;
}

.process-details-fieldset:deep(.p-fieldset-legend) {
  background-color: #f0f7ff;
  border-left: 3px solid #3b82f6;
  padding-left: 1rem;
  cursor: pointer;
  width: auto;
  min-width: 200px;
}

.process-details-fieldset:deep(.p-fieldset-toggler) {
  background-color: #3b82f6;
  color: white;
  box-shadow: 0 2px 4px rgba(59, 130, 246, 0.3);
  z-index: 1;
}

.process-details-fieldset:deep(.p-fieldset-toggler:hover) {
  background-color: #2563eb;
  transform: translateY(-50%) scale(1.1);
}

.expand-button {
  margin-left: 8px;
  background-color: rgba(59, 130, 246, 0.1);
  border: 1px solid #3b82f6;
  color: #3b82f6;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  display: flex;
  align-items: center;
  gap: 4px;
  animation: pulse 2s infinite;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
}

.expand-button:hover {
  background-color: rgba(59, 130, 246, 0.2);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.3);
}

.expand-button:focus {
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.4);
  outline: none;
}

.expand-button .p-button-icon {
  font-size: 0.75rem;
}

@media (max-width: 768px) {
  .expand-button {
    padding: 0.35rem 0.6rem;
  }
  
  .expand-button .p-button-icon {
    font-size: 0.85rem;
  }
  
  .expand-button span {
    font-size: 0.8rem !important;
  }
}

.expand-hint {
  font-weight: 500;
}

/* Add keyframes animation for the pulse effect */
@keyframes pulse {
  0% {
    opacity: 0.8;
    transform: scale(1);
    box-shadow: 0 0 0 0 rgba(59, 130, 246, 0.4);
  }
  50% {
    opacity: 1;
    transform: scale(1.03);
    box-shadow: 0 0 0 5px rgba(59, 130, 246, 0.2);
  }
  100% {
    opacity: 0.8;
    transform: scale(1);
    box-shadow: 0 0 0 0 rgba(59, 130, 246, 0.4);
  }
}

.process-card {
  border-width: 1px;
  transition: all 0.2s ease;
}

.process-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.process-details-view {
  animation: fadeIn 0.3s ease;
}

.close-details-btn {
  transition: all 0.2s ease;
}

.close-details-btn:hover {
  background-color: rgba(59, 130, 246, 0.1);
  color: #3b82f6;
  transform: scale(1.02);
}

/* Mobile-specific styles for the back button */
@media (max-width: 768px) {
  .close-details-btn {
    width: 2.5rem;
    height: 2.5rem;
    padding: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
  }
  
  .close-details-btn:deep(.p-button-icon) {
    font-size: 1rem;
    margin-right: 0;
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>

