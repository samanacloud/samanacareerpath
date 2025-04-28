<template>
    <div class="quiz-container">
       

        <!-- Session Information -->
        <div class="mb-4" v-if="false">
            <h6 class="text-sm font-medium text-gray-700 mb-2">Session Information</h6>
            <div class="p-3 border rounded-lg bg-surface-100">
                <p><strong>Company ID:</strong> {{ sessionInfo?.companyId }}</p>
                <p><strong>Company Name:</strong> {{ sessionInfo?.companyName }}</p>
                <p><strong>Email:</strong> {{ sessionInfo?.email }}</p>
            </div>
        </div>

        <!-- Two-column layout -->
        <div class="grid grid-cols-12 gap-4">
            <!-- Left Column - Skillset Selection (4/12) - Hidden during active quiz -->
            <Transition name="slide-fade">
                <div ref="skillsetsSection" class="col-span-12 lg:col-span-4" v-if="!quizStarted" key="skillset-selection">
                    <div class="card p-3 mb-4 border rounded-lg shadow-sm">
                        <!-- Header -->
                        <div class="flex items-center justify-between mb-3">
                            <div class="flex items-center gap-2">
                                <i class="pi pi-star text-blue-500"></i>
                                <h5 class="font-semibold m-0">Skillset Selection</h5>
                                <div class="bg-blue-100 text-blue-800 text-xs font-medium px-2 py-0.5 rounded-full">
                                    {{ filteredAndSearchedSkillsets.length }}
                                </div>
                            </div>
                        </div>
                        
                        <!-- Search Input -->
                        <div class="mb-3">
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
                        
                        <!-- Categories Section -->
                        <div class="mb-3" v-if="!selectedSkillsetCategory">
                            <h5 class="text-sm font-medium text-gray-700 mb-2"><b>Categories</b></h5>
                            <div class="flex flex-wrap gap-1">
                                <Chip 
                                    v-for="category in skillsetCategories" 
                                    :key="category"
                                    :label="category"
                                    :class="{
                                        'bg-primary-500 text-primary-500 shadow-lg': selectedSkillsetCategory === category,
                                        'hover:bg-primary-50 hover:text-primary-500 hover:shadow-lg transition-all duration-200': true
                                    }"
                                    @click="setSelectedSkillsetCategory(category)"
                                    class="cursor-pointer border-1 border-transparent bg-surface-100 shadow-sm text-xs px-2 py-1"
                                />
                            </div>
                        </div>

                        <!-- Skillsets DataTable -->
                        <div class="mb-3">
                            <h5 class="text-sm font-medium text-gray-700 mb-2">
                              <b> {{ selectedSkillsetCategory ? `Skillsets in ${selectedSkillsetCategory}` : 'All Skillsets' }}</b> 
                            </h5>
                            
                            <div v-if="filteredAndSearchedSkillsets.length === 0" class="text-gray-500 italic py-2 text-center">
                                No matching skillsets found
                            </div>
                            
                            <div class="skillsets-container">
                                <DataTable 
                                    :value="filteredAndSearchedSkillsets" 
                                    class="p-datatable-sm" 
                                    responsiveLayout="scroll"
                                    :rowHover="true"
                                    selectionMode="single"
                                    v-model:selection="selectedSkillset"
                                    dataKey="id"
                                    @row-select="onSkillsetSelect"
                                    stripedRows
                                    size="small"
                                    scrollHeight="350px"
                                    scrollable
                                >
                                    <Column field="name" header="Name">
                                        <template #body="slotProps">
                                            <div class="text-sm font-medium">
                                                {{ slotProps.data.name }}
                                                <div class="text-xs text-gray-500">{{ slotProps.data.description }}</div>
                                            </div>
                                        </template>
                                    </Column>
                                    <Column field="category" header="Category" v-if="!selectedSkillsetCategory">
                                        <template #body="slotProps">
                                            <div class="text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded-full inline-block">
                                                {{ slotProps.data.category }}
                                            </div>
                                        </template>
                                    </Column>
                                </DataTable>
                            </div>
                        </div>
                    </div>
                </div>
            </Transition>

            <!-- Right Column - Quiz Content (8/12 or 12/12 during quiz) -->
            <Transition name="zoom-fade" mode="out-in">
                <div ref="modelSelectionSection" :class="quizStarted ? 'col-span-12' : 'col-span-12 lg:col-span-8'" key="quiz-content">
                    <!-- Generate Quiz Button Section (After Skillset) -->
                    <div v-if="selectedSkillset && !quizStarted" class="card p-3 mb-4 border rounded-lg shadow-sm">
                        <!-- Header with icon -->
                        <div class="flex items-center justify-between mb-3">
                            <div class="flex items-center gap-2">
                                <i class="pi pi-brain text-blue-500"></i>
                                <h5 class="font-semibold m-0">Generate Quiz for: {{ selectedSkillset.name }}</h5>
                            </div>
                        </div>

                        <!-- Generate Quiz Button -->
                        <div class="mb-2">
                            <p class="text-sm text-gray-600 mb-3">
                                Click the button below to generate a quiz for the selected skillset. The quiz will contain multiple-choice questions of varying difficulty levels.
                            </p>
                        </div>
                        
                        <Button @click="generateQuiz" :loading="loading" :disabled="loading" class="w-full md:w-auto">
                            Generate Quiz
                        </Button>
                    </div>

                    <!-- Loading Indicator -->
                    <Transition name="scale-fade">
                        <div v-if="loading" class="loading-container p-6 border rounded-lg shadow-sm bg-white" key="loading">
                            <ProgressSpinner class="mb-4" />
                            <h3 class="text-lg font-medium text-gray-800 mb-2">Generating Quiz Questions...</h3>
                            <p class="text-gray-600 mb-4 text-center max-w-md mx-auto">
                                We're using AI to create questions about <span class="font-medium">{{ selectedSkillset?.name }}</span>. 
                                This may take up to 30 seconds.
                            </p>
                            <div class="w-full max-w-sm mx-auto bg-surface-50 h-2 rounded-full overflow-hidden">
                                <div class="h-full bg-primary-500 loading-bar"></div>
                            </div>
                        </div>
                    </Transition>

                    <!-- Quiz Section - Enhanced styling -->
                    <TransitionGroup ref="quizContentSection" name="question-slide" tag="div" class="quiz-content p-6 border rounded-lg shadow-lg bg-white">
                        <div v-if="questions.length && !loading" key="questions">
                            <!-- Quiz Header with improved styling -->
                            <div class="question-header mb-6">
                                <div class="flex justify-between items-center mb-4">
                                    <div class="flex items-center gap-2">
                                        <span class="bg-primary-100 text-primary-800 font-medium px-3 py-1 rounded-full text-sm">
                                            Question {{ currentQuestionIndex + 1 }}/{{ questions.length }}
                                        </span>
                                        <Tag :severity="getDifficultySeverity(currentQuestion.difficulty)"
                                            :value="currentQuestion.difficulty" class="uppercase text-xs font-bold" />
                                    </div>
                                    
                                    <!-- Timer with enhanced styling -->
                                    <div class="timer-container flex items-center gap-2 bg-surface-50 px-3 py-1 rounded-full">
                                        <i class="pi pi-clock" :class="timeLeft <= 5 ? 'text-red-500' : 'text-primary-500'"></i>
                                        <div class="timer font-mono" :class="{ 'warning': timeLeft <= 5 }">
                                            {{ timeLeft }}s
                                        </div>
                                    </div>
                                </div>
                                
                                <!-- Progress bar with improved styling -->
                                <ProgressBar 
                                    :value="(currentQuestionIndex / questions.length) * 100" 
                                    class="question-progress h-2 rounded-full overflow-hidden" 
                                    :class="getDifficultyProgressClass(currentQuestion.difficulty)"
                                />
                            </div>

                            <!-- Question text with improved styling -->
                            <div class="question-text text-xl font-medium mb-6 p-4 bg-surface-50 rounded-lg border-l-4 border-primary-500">
                                {{ currentQuestion.question }}
                            </div>

                            <!-- Answers grid with improved styling -->
                            <div class="answers-grid mb-6">
                                <div 
                                    v-for="(answer, index) in currentQuestion.answers" 
                                    :key="index" 
                                    class="answer-option"
                                    :class="{ 
                                        'selected': selectedAnswers[currentQuestionIndex] === answer,
                                        'hover:border-primary-200 hover:bg-primary-50': !selectedAnswers[currentQuestionIndex]
                                    }" 
                                    @click="selectAnswer(answer)"
                                >
                                    <div class="answer-letter-container">
                                        <span class="answer-letter">{{ String.fromCharCode(65 + index) }}</span>
                                    </div>
                                    <span class="answer-text">{{ answer }}</span>
                                </div>
                            </div>

                            <!-- Navigation buttons with improved styling -->
                            <div class="navigation-buttons flex justify-end">
                                <Button v-if="currentQuestionIndex < questions.length - 1" @click="nextQuestion"
                                    :disabled="!selectedAnswers[currentQuestionIndex]"
                                    class="p-button-outlined p-button-primary" iconPos="right" icon="pi pi-chevron-right" label="Next" />
                            </div>
                            
                            <!-- Exit quiz button -->
                            <div class="exit-quiz-container mt-4 text-center">
                                <Button @click="confirmExitQuiz" severity="secondary" text class="p-button-sm">
                                    <i class="pi pi-times mr-2"></i>Exit Quiz
                                </Button>
                            </div>
                        </div>
                    </TransitionGroup>

                    <!-- Empty state when no skillset is selected -->
                    <div v-if="!selectedSkillset && !loading && !questions.length" class="empty-state p-4 border rounded-lg shadow-sm">
                        <h3 class="text-xl font-medium text-gray-700 mb-4 flex items-center">
                            <i class="pi pi-info-circle text-primary mr-2"></i>
                            Instructions
                        </h3>
                        <QuizGuideWidget />
                    </div>
                </div>
            </Transition>
        </div>

        <!-- Results Dialog - Enhanced styling -->
        <Dialog v-model:visible="showResults" modal :header="getScoreHeader(score)" :style="{ width: isMobile ? '90vw' : '30vw' }"
            :closable="true" :dismissableMask="true" class="results-dialog">
            <div class="text-center py-8">
                <div class="result-circle mb-6">
                    <i class="pi pi-star-fill certificate-icon" :style="{ animationDuration: score >= 80 ? '6s' : score >= 60 ? '9s' : '12s' }"></i>
                    <div class="result-score">{{ score }}%</div>
                </div>
                <div class="star-rating mb-6 animate-fade-in">
                    <i v-for="index in 5" :key="index" class="pi text-4xl"
                        :class="[index <= scoreToStars ? 'pi-star-fill text-yellow-400' : 'pi-star text-gray-300']"></i>
                </div>
                <Tag :severity="getScoreSeverity(score)" class="text-xl px-5 py-3 animate-slide-up">
                    {{ getScoreMessage(score) }}
                </Tag>
                <div class="countdown-timer mt-6 animate-fade-in-delayed">
                <!--<ProgressBar :value="resultCountdown * 20" class="mb-2" show-value="true" />--> 
                    <div class="text-sm text-gray-500">Closing in {{ resultCountdown }} seconds</div>
                </div>
            </div>
        </Dialog>

        <!-- Confirm Exit Dialog -->
        <Dialog v-model:visible="showExitConfirmation" modal header="Exit Quiz?" :style="{ width: '350px' }" :closable="true">
            <div class="p-4">
                <p class="mb-4">Are you sure you want to exit the quiz? Your progress will be lost.</p>
                <div class="flex justify-end gap-2">
                    <Button label="Cancel" class="p-button-text" @click="showExitConfirmation = false" />
                    <Button label="Exit Quiz" severity="danger" @click="exitQuiz" />
                </div>
            </div>
        </Dialog>
    </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted, watch } from 'vue';
import { useToast } from 'primevue/usetoast';
import Button from 'primevue/button';
import InputText from 'primevue/inputtext';
import ProgressSpinner from 'primevue/progressspinner';
import ProgressBar from 'primevue/progressbar';
import Tag from 'primevue/tag';
import Dialog from 'primevue/dialog';
import Select from 'primevue/select';
import Chip from 'primevue/chip';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import QuizGuideWidget from '@/components/dashboard/QuizGuideWidget.vue';

const toast = useToast();
const loading = ref(false);
const quizStarted = ref(false);
const currentQuestionIndex = ref(0);
const questions = ref([]);
const selectedAnswers = ref([]);
const showResults = ref(false);
const score = ref(0);
const timeLeft = ref(0);
let timerInterval = null;
const resultCountdown = ref(5);
let resultCountdownInterval = null;

// Skillset-related variables
const skillsetCategories = ref([]);
const selectedSkillsetCategory = ref(null);
const skillsets = ref([]);
const selectedSkillset = ref(null);
const skillsetSearchQuery = ref('');
const debouncedSearchQuery = ref('');
let searchTimeout = null;

const form = reactive({
    model: "google/gemini-flash-1.5-8b-exp",
    topic: null,
});

const currentQuestion = computed(() =>
    questions.value[currentQuestionIndex.value] || { question: '', answers: [], difficulty: '' }
);

const isMobile = ref(window.innerWidth < 768);

const handleResize = () => {
    isMobile.value = window.innerWidth < 768;
};

// Add sessionInfo
const sessionInfo = ref(null);

// Add fetchSessionInfo function
async function fetchSessionInfo() {
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
    }
}

const handleVisibilityChange = () => {
    if (document.hidden && quizStarted.value) {
        toast.add({
            severity: 'error',
            summary: 'Quiz Cancelled',
            detail: 'Quiz was cancelled because you switched to another window.',
            life: 5000
        });
        resetQuiz();
    }
};

const handleMouseLeave = (event) => {
    // Check if the mouse has left the window (clientY <= 0 means mouse moved above the window)
    if (event.clientY <= 0 && quizStarted.value) {
        toast.add({
            severity: 'error',
            summary: 'Quiz Cancelled',
            detail: 'Quiz was cancelled because you moved the mouse out of the window.',
            life: 5000
        });
        resetQuiz();
    }
};

onMounted(async () => {
    window.addEventListener('resize', handleResize);
    document.addEventListener('visibilitychange', handleVisibilityChange);
    document.addEventListener('mouseleave', handleMouseLeave);
    document.addEventListener('fullscreenchange', () => {
        if (!document.fullscreenElement && quizStarted.value) {
            toast.add({
                severity: 'error',
                summary: 'Quiz Cancelled',
                detail: 'Quiz was cancelled because you exited fullscreen mode.',
                life: 5000
            });
            resetQuiz();
        }
    });
    await fetchSessionInfo();
    if (sessionInfo.value?.companyId) {
        fetchSkillsets();
    }
    
    document.addEventListener('contextmenu', preventInspection);
    document.addEventListener('keydown', preventDevTools);
});

onUnmounted(() => {
    window.removeEventListener('resize', handleResize);
    document.removeEventListener('visibilitychange', handleVisibilityChange);
    document.removeEventListener('mouseleave', handleMouseLeave);
    clearInterval(timerInterval);
    clearInterval(resultCountdownInterval);
    document.removeEventListener('contextmenu', preventInspection);
    document.removeEventListener('keydown', preventDevTools);
});

const requestFullscreen = () => {
    const elem = document.documentElement;
    if (elem.requestFullscreen) {
        elem.requestFullscreen();
    } else if (elem.webkitRequestFullscreen) { /* Safari */
        elem.webkitRequestFullscreen();
    } else if (elem.msRequestFullscreen) { /* IE11 */
        elem.msRequestFullscreen();
    }
};

const exitFullscreen = () => {
    if (document.exitFullscreen) {
        document.exitFullscreen();
    } else if (document.webkitExitFullscreen) { /* Safari */
        document.webkitExitFullscreen();
    } else if (document.msExitFullscreen) { /* IE11 */
        document.msExitFullscreen();
    }
};

const generateQuiz = async () => {
    if (!selectedSkillset.value) {
        toast.add({ severity: 'warn', summary: 'Warning', detail: 'Please select a skillset first', life: 3000 });
        return;
    }

    // Set the topic based on selected skillset if not already set
    if (!form.topic) {
        form.topic = `${selectedSkillsetCategory.value} : ${selectedSkillset.value.name}`;
    }

    // Ensure we have a default model
    if (!form.model) {
        form.model = "google/gemini-flash-1.5-8b-exp";
    }

    loading.value = true;
    try {
        console.log('Generating quiz with:', { topic: form.topic, model: form.model });
        
        const query = {
            query: `
                query GenerateQuiz($topic: String!, $model: String!) {
                    generateQuizByTopic(topic: $topic, model: $model) {
                        status
                        error
                        questions {
                            question
                            answers
                            correctAnswer
                            difficulty
                        }
                    }
                }
            `,
            variables: {
                topic: form.topic,
                model: form.model,
            }
        };

        const response = await fetch('/graphql', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(query)
        });

        const result = await response.json();
        console.log('Quiz generation response:', result);

        if (result.errors) {
            console.error('GraphQL errors:', result.errors);
            throw new Error(result.errors[0].message);
        }

        const data = result.data.generateQuizByTopic;

        if (data.status === 'error') {
            console.error('Quiz generation error:', data.error);
            throw new Error(data.error);
        }

        if (!data.questions || data.questions.length === 0) {
            console.error('No questions returned');
            throw new Error('No questions were generated. Please try a different model or skillset.');
        }

        questions.value = data.questions;
        selectedAnswers.value = new Array(questions.value.length).fill(null);
        quizStarted.value = true;
        currentQuestionIndex.value = 0;
        startTimer();
        
        // Request fullscreen mode when quiz starts
        requestFullscreen();

        toast.add({
            severity: 'success',
            summary: 'Success',
            detail: 'Quiz generated successfully',
            life: 3000
        });

    } catch (error) {
        console.error('Quiz generation failed:', error);
        toast.add({
            severity: 'error',
            summary: 'Error',
            detail: error.message || 'Failed to generate quiz. Please try a different model.',
            life: 5000
        });
    } finally {
        loading.value = false;
    }
};

const selectAnswer = (answer) => {
    selectedAnswers.value[currentQuestionIndex.value] = answer;
    if (currentQuestionIndex.value < questions.value.length - 1) {
        nextQuestion();
    } else {
        // If it's the last question, automatically finish the quiz
        finishQuiz();
    }
};

const nextQuestion = () => {
    if (currentQuestionIndex.value < questions.value.length - 1) {
        currentQuestionIndex.value++;
    } else {
        finishQuiz();
    }
};

const finishQuiz = async () => {
    const correctAnswers = questions.value.reduce((count, question, index) => {
        return count + (selectedAnswers.value[index] === question.correctAnswer ? 1 : 0);
    }, 0);

    const percentage = Math.round((correctAnswers / questions.value.length) * 100);
    score.value = percentage;
    
    // Convert percentage to 1-5 star rating
    const starRating = Math.max(1, Math.min(5, Math.ceil(percentage / 20)));
    
    showResults.value = true;
    clearInterval(timerInterval);

    // Call assignSkillset with the star rating
    await assignSkillset(starRating);
    
    // Show confetti for high scores
    if (percentage >= 80) {
        showConfetti();
    }
    
    // Reset and start countdown
    resultCountdown.value = 5;
    resultCountdownInterval = setInterval(() => {
        resultCountdown.value--;
        if (resultCountdown.value <= 0) {
            clearInterval(resultCountdownInterval);
            showResults.value = false;
            resetQuiz();
        }
    }, 1000);
};

// Function to show confetti
const showConfetti = () => {
    const canvas = document.createElement('canvas');
    canvas.style.position = 'fixed';
    canvas.style.top = '0';
    canvas.style.left = '0';
    canvas.style.width = '100vw';
    canvas.style.height = '100vh';
    canvas.style.zIndex = '9999';
    canvas.style.pointerEvents = 'none';
    document.body.appendChild(canvas);
    
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    
    const pieces = [];
    const numberOfPieces = 200;
    const colors = ['#f44336', '#e91e63', '#9c27b0', '#673ab7', '#3f51b5', '#2196f3', '#03a9f4', '#00bcd4', '#009688', '#4CAF50', '#8BC34A', '#CDDC39', '#FFEB3B', '#FFC107', '#FF9800', '#FF5722'];
    
    for (let i = 0; i < numberOfPieces; i++) {
        pieces.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height - canvas.height,
            rotation: Math.random() * 360,
            size: Math.random() * 15 + 5,
            color: colors[Math.floor(Math.random() * colors.length)],
            velocity: {
                x: Math.random() * 6 - 3,
                y: Math.random() * 3 + 2
            },
            rotationSpeed: Math.random() * 2 - 1
        });
    }
    
    const update = () => {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        pieces.forEach(piece => {
            piece.y += piece.velocity.y;
            piece.x += piece.velocity.x;
            piece.rotation += piece.rotationSpeed;
            
            if (piece.y > canvas.height) {
                piece.y = -piece.size;
                piece.x = Math.random() * canvas.width;
            }
            
            ctx.save();
            ctx.translate(piece.x, piece.y);
            ctx.rotate(piece.rotation * Math.PI / 180);
            ctx.fillStyle = piece.color;
            ctx.fillRect(-piece.size / 2, -piece.size / 2, piece.size, piece.size);
            ctx.restore();
        });
        
        requestAnimationFrame(update);
    };
    
    update();
    
    // Remove confetti after 4 seconds
    setTimeout(() => {
        document.body.removeChild(canvas);
    }, 4000);
};

const resetQuiz = () => {
    quizStarted.value = false;
    currentQuestionIndex.value = 0;
    questions.value = [];
    selectedAnswers.value = [];
    showResults.value = false;
    score.value = 0;
    form.model = "google/gemini-flash-1.5-8b-exp";
    form.topic = null;
    selectedSkillset.value = null;
    selectedSkillsetCategory.value = null;
    clearInterval(timerInterval);
    clearInterval(resultCountdownInterval);
    // Exit fullscreen mode when quiz ends
    exitFullscreen();
};

const getDifficultySeverity = (difficulty) => {
    switch (difficulty.toLowerCase()) {
        case 'easy': return 'success';
        case 'medium': return 'warning';
        case 'hard': return 'danger';
        default: return 'info';
    }
};

const getScoreSeverity = (score) => {
    if (score >= 80) return 'success';
    if (score >= 60) return 'warning';
    return 'danger';
};

const getScoreMessage = (score) => {
    if (score >= 80) return 'Excellent!';
    if (score >= 60) return 'Good Job!';
    return 'Keep Practicing';
};

const startTimer = () => {
    clearInterval(timerInterval);
    const difficulty = currentQuestion.value.difficulty;
    timeLeft.value = difficulty === 'easy' ? 25 : difficulty === 'medium' ? 35 : 45;

    timerInterval = setInterval(() => {
        if (timeLeft.value > 0) {
            timeLeft.value--;
        } else {
            clearInterval(timerInterval);
            if (!selectedAnswers.value[currentQuestionIndex.value] && currentQuestionIndex.value < questions.value.length -1) {
                nextQuestion();
            }
        }
    }, 1000);
};

watch(() => currentQuestionIndex.value, () => {
    if (questions.value.length) {
        startTimer();
    }
});

const scoreToStars = computed(() => {
    return Math.round((score.value / 100) * 5);
});

const fetchSkillsets = async () => {
    if (!sessionInfo.value?.companyId) {
        toast.add({
            severity: 'warn',
            summary: 'No Company Selected',
            detail: 'Please select a company first.',
            life: 3000
        });
        return; // Stop if no companyId
    }
    try {
        const response = await fetch('/graphql', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                query: `
                    query ListSkillsetsAndCategories($companyId: String!) {
                        listSkillsetsByCompanyId(companyId: $companyId) {
                            id
                            skillsetName
                            skillsetDescription
                            skillsetCategory
                        }
                        listSkillsetsCategories(companyId: $companyId)
                    }
                `,
                variables: { companyId: sessionInfo.value.companyId }
            })
        });
        const result = await response.json();

        if (result.errors) {
            throw new Error(result.errors[0].message);
        }
        //Correctly process the data
        skillsets.value = result.data.listSkillsetsByCompanyId.map(item => ({
            id: item.id,
            name: item.skillsetName,
            description: item.skillsetDescription,
            category: item.skillsetCategory
        }));
        skillsetCategories.value = result.data.listSkillsetsCategories;

    } catch (error) {
        toast.add({ severity: 'error', summary: 'Error', detail: error.message, life: 3000 });
    }
};

const setSelectedSkillsetCategory = (category) => {
    selectedSkillsetCategory.value = category;
    selectedSkillset.value = null;
    form.model = null;
    form.topic = null;
    // Scroll to skillsets section on mobile
    scrollToSkillsets();
};

const filteredSkillsets = computed(() => {
    // Use the correct field names here
    return skillsets.value.filter(skillset => skillset.category === selectedSkillsetCategory.value);
});

// Add the filtered and searched skillsets computed property
const filteredAndSearchedSkillsets = computed(() => {
    // First filter by category if needed
    let result = selectedSkillsetCategory.value 
        ? skillsets.value.filter(s => s.category === selectedSkillsetCategory.value)
        : skillsets.value;
    
    // Then filter by search query if present
    if (debouncedSearchQuery.value.trim()) {
        const searchLower = debouncedSearchQuery.value.toLowerCase().trim();
        result = result.filter(s => 
            s.name.toLowerCase().includes(searchLower) || 
            s.description.toLowerCase().includes(searchLower) ||
            s.category.toLowerCase().includes(searchLower)
        );
    }
    
    return result;
});

const selectSkillset = (skillset) => {
    selectedSkillset.value = skillset;
    form.topic = `${selectedSkillsetCategory.value} : ${skillset.name}`;
    
    // Set a default model (hidden from user)
    form.model = "google/gemini-flash-1.5-8b-exp";
    
    // Scroll to generate quiz section on mobile
    scrollToModelSelection();
};

const showMobileDescription = (description) => {
    toast.add({ severity: 'info', summary: 'Description', detail: description, life: 5000 });
};

const truncateDescription = (description) => {
    if (!description) return "";
    return description.length > 50 ? description.substring(0, 50) + "..." : description;
};

// Debounce search to avoid too many re-renders
const debounceSearch = () => {
  if (searchTimeout) clearTimeout(searchTimeout);
  searchTimeout = setTimeout(() => {
    debouncedSearchQuery.value = skillsetSearchQuery.value;
  }, 300);
};

// Updated assignSkillset function
async function assignSkillset(starRating) {
  try {
    const mutation = {
      query: `
        mutation AssignSkillset($input: AssignSkillsetInput!) {
          assignSkillset(input: $input) {
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
      `,
      variables: {
        input: {
          companyId: sessionInfo.value.companyId,
          companyName: sessionInfo.value.companyName,
          email: sessionInfo.value.email,
          skillsetCategory: selectedSkillsetCategory.value,
          skillsetName: selectedSkillset.value.name,
          skillsetRating: starRating,
          reviewedBy: "AI Module",
          reviewerEmail: "careerpath@samanagroup.com",
        }
      }
    };

    const response = await fetch('/graphql', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(mutation),
    });

    const result = await response.json();

    if (result.errors) {
      throw new Error(result.errors[0].message);
    }

    toast.add({
      severity: 'success',
      summary: 'Success',
      detail: 'Skillset assigned successfully',
      life: 3000,
    });

  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: error.message || 'Failed to assign skillset',
      life: 3000,
    });
  }
}

const onSkillsetSelect = (event) => {
    if (event.data) {
        selectedSkillset.value = event.data;
        form.topic = `${selectedSkillsetCategory.value} : ${event.data.name}`;
        form.model = "google/gemini-flash-1.5-8b-exp";
        
        // Scroll to generate quiz section on mobile
        if (isMobile.value && modelSelectionSection.value) {
            setTimeout(() => {
                modelSelectionSection.value.scrollIntoView({ behavior: 'smooth' });
            }, 100);
        }
    }
};

// Add these variables
const showExitConfirmation = ref(false);

// Add these functions
const confirmExitQuiz = () => {
    showExitConfirmation.value = true;
};

const exitQuiz = () => {
    resetQuiz();
    showExitConfirmation.value = false;
};

const getDifficultyProgressClass = (difficulty) => {
    switch (difficulty.toLowerCase()) {
        case 'easy': return 'progress-success';
        case 'medium': return 'progress-warning';
        case 'hard': return 'progress-danger';
        default: return 'progress-info';
    }
};

const getScoreHeader = (score) => {
    if (score >= 80) return '🎉 Excellent Result!';
    if (score >= 60) return '👍 Good Result';
    return '📝 Quiz Result';
};

const preventInspection = (e) => {
    e.preventDefault();
    return false;
};

const preventDevTools = (e) => {
    // Block F12, Ctrl+Shift+I, Ctrl+Shift+C, Ctrl+Shift+J
    if (e.key === 'F12' || 
        (e.ctrlKey && e.shiftKey && e.key === 'I') || 
        (e.ctrlKey && e.shiftKey && e.key === 'C') ||
        (e.ctrlKey && e.shiftKey && e.key === 'J') ||
        (e.metaKey && e.altKey && e.key === 'I')) {
        e.preventDefault();
        return false;
    }
};

// In the <script setup> section, add the following new refs and functions near the top
const skillsetsSection = ref(null);
const modelSelectionSection = ref(null);
const quizContentSection = ref(null);

const scrollToSkillsets = () => {
  if (isMobile.value && skillsetsSection.value) {
    skillsetsSection.value.scrollIntoView({ behavior: 'smooth' });
  }
};

const scrollToModelSelection = () => {
  if (isMobile.value && modelSelectionSection.value) {
    modelSelectionSection.value.scrollIntoView({ behavior: 'smooth' });
  }
};

// Add a watch for quizStarted to scroll into view when quiz starts
watch(quizStarted, (newVal) => {
  if (newVal && quizContentSection.value) {
    // Use setTimeout to ensure the element is rendered before scrolling
    setTimeout(() => {
      quizContentSection.value.scrollIntoView({ behavior: 'smooth' });
    }, 300);
  }
});
</script>

<style scoped>
.quiz-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 1.5rem;
    width: 100%;
    display: flex;
    flex-direction: column;
    min-height: calc(100vh - 64px); /* Adjust based on your header height */
}

.loading-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 200px;
}

.question-header {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin-bottom: 2rem;
    color: var(--text-color);
}

.question-info {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.timer {
    font-size: 1rem;
    font-weight: 600;
    color: var(--primary-600);
    transition: color 0.3s ease;
}

.timer.warning {
    color: var(--red-500);
    animation: pulse 1s infinite;
}

.answers-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1rem;
    margin: 2rem 0;
}

.answer-option {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1rem;
    border: 1px solid var(--surface-border);
    border-radius: 0.75rem;
    cursor: pointer;
    transition: all 0.2s ease;
    background-color: var(--surface-card);
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    color: var(--text-color);
}

.answer-option:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    background-color: var(--surface-hover);
}

.answer-option.selected {
    background: linear-gradient(135deg, var(--primary-50), var(--primary-100));
    border-color: var(--primary-300);
    box-shadow: 0 4px 8px rgba(59, 130, 246, 0.15);
    color: var(--primary-700);
}

.answer-letter-container {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background-color: var(--surface-200);
    flex-shrink: 0;
}

.answer-letter {
    font-weight: bold;
    font-size: 1rem;
}

.answer-text {
    flex: 1;
    word-break: break-word;
}

.navigation-buttons {
    display: flex;
    justify-content: space-between;
    margin-top: 2rem;
}

.empty-state {
    min-height: 400px;
    display: flex;
    flex-direction: column;
}

@media (max-width: 768px) {
    .quiz-container {
        padding: 1rem;
    }

    .answers-grid {
        grid-template-columns: 1fr;
    }

    :deep(.results-dialog) {
        width: 90vw !important;
        max-height: 90vh;
        overflow-y: auto;
    }
}

.star-rating {
    display: flex;
    justify-content: center;
    gap: 0.5rem;
    font-size: 1.5rem;
}

.star-rating i {
    transition: all 0.3s ease;
}

.star-rating i:hover {
    transform: scale(1.2) rotate(15deg);
}

:deep(.p-chip) {
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
    color: var(--gray-900) !important;
    font-weight: bold;
    box-shadow: 0 2px 4px rgba(59, 130, 246, 0.2);
    border-color: var(--primary-500);
}

:deep(.p-tooltip) {
    max-width: 300px;
    white-space: pre-wrap;
    word-break: break-word;
}

.skillsets-container {
    scrollbar-width: thin;
    scrollbar-color: var(--surface-400) var(--surface-100);
}

.skillsets-container::-webkit-scrollbar {
    width: 6px;
}

.skillsets-container::-webkit-scrollbar-track {
    background: var(--surface-100);
    border-radius: 10px;
}

.skillsets-container::-webkit-scrollbar-thumb {
    background-color: var(--surface-400);
    border-radius: 10px;
}

.skillsets-container::-webkit-scrollbar-thumb:hover {
    background-color: var(--surface-500);
}

/* DataTable styling */
:deep(.p-datatable-sm .p-datatable-thead > tr > th) {
    padding: 0.4rem 0.5rem;
    font-size: 0.75rem;
    background-color: var(--surface-100);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    font-weight: 600;
    color: var(--text-color-secondary);
}

:deep(.p-datatable-sm .p-datatable-tbody > tr > td) {
    padding: 0.3rem 0.5rem;
    font-size: 0.875rem;
    border-bottom: 1px solid var(--surface-200);
}

:deep(.p-datatable .p-datatable-tbody > tr.p-highlight) {
    background-color: var(--primary-50);
    color: var(--primary-700);
}

:deep(.p-datatable .p-datatable-tbody > tr:hover) {
    background-color: var(--surface-100);
}

:deep(.p-datatable-wrapper) {
    border-radius: 0.375rem;
    border: 1px solid var(--surface-200);
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

:deep(.p-datatable-sm .p-datatable-header) {
    padding: 0.5rem;
    background-color: var(--surface-50);
}

:deep(.p-datatable.p-datatable-striped .p-datatable-tbody > tr.p-row-odd) {
    background-color: var(--surface-50);
}

:deep(.p-datatable.p-datatable-sm .p-datatable-tbody > tr.p-highlight.p-row-odd) {
    background-color: var(--primary-50);
}

:deep(.p-datatable .p-datatable-tbody > tr > td:first-child) {
    font-weight: 500;
}

:deep(.p-datatable .p-datatable-tbody > tr:last-child > td) {
    border-bottom: none;
}

:deep(.p-datatable .p-paginator) {
    padding: 0.3rem;
    background-color: var(--surface-50);
    border-top: 1px solid var(--surface-200);
}

:deep(.p-datatable .p-datatable-footer) {
    padding: 0.4rem 0.5rem;
    font-size: 0.75rem;
    background-color: var(--surface-50);
    border-top: 1px solid var(--surface-200);
}

.results-dialog {
    z-index: 99999 !important;
    backdrop-filter: blur(10px);
    background: rgba(255, 255, 255, 0.98) !important;
    border: 1px solid rgba(255, 255, 255, 0.4) !important;
    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37) !important;
}

.result-circle {
    width: 180px;
    height: 180px;
    position: relative;
    margin: 0 auto;
    display: flex;
    align-items: center;
    justify-content: center;
}

.certificate-icon {
    position: absolute;
    font-size: 9rem;
    color: var(--primary-400);
    transform: scale(1.2);
    animation: spin 12s linear infinite;
    z-index: 1;
}

.result-score {
    position: relative;
    font-size: 3rem;
    font-weight: 800;
    color: var(--primary-800);
    z-index: 2;
    text-shadow: 
        0 0 5px rgba(255, 255, 255, 0.8),
        0 0 10px rgba(255, 255, 255, 0.8);
    background: linear-gradient(135deg, var(--primary-700), var(--primary-500));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.result-circle::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: radial-gradient(circle at center, 
        rgba(255, 255, 255, 0.9) 30%, 
        rgba(255, 255, 255, 0.5) 70%);
    z-index: 0;
    border-radius: 50%;
}

@keyframes spin {
    from { transform: rotate(0deg) scale(1.2); }
    to { transform: rotate(360deg) scale(1.2); }
}

:deep(.p-dialog) {
    overflow: visible;
}

:deep(.p-dialog-content) {
    overflow: visible;
    position: relative;
    z-index: 3;
}

:deep(.p-dialog-mask) {
    backdrop-filter: blur(5px);
    background-color: rgba(0, 0, 0, 0.2);
}

@keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-8px); }
}

.results-dialog {
    animation: float 4s ease-in-out infinite;
}

@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.03); }
}

@keyframes fade-in {
    from { opacity: 0; }
    to { opacity: 1; }
}

@keyframes slide-up {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.vendor-badge {
    @apply px-2 py-1 rounded-md text-xs font-bold uppercase tracking-wider border;
    min-width: 80px;
    text-align: center;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    height: 22px;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.vendor-anthropic { @apply bg-purple-100 border-purple-300 text-purple-800; }
.vendor-openai { @apply bg-green-100 border-green-300 text-green-800; }
.vendor-google { @apply bg-blue-100 border-blue-300 text-blue-800; }
.vendor-meta { @apply bg-pink-100 border-pink-300 text-pink-800; }
.vendor-mistral { @apply bg-orange-100 border-orange-300 text-orange-800; }
.vendor-perplexity { @apply bg-indigo-100 border-indigo-300 text-indigo-800; }
.vendor-cohere { @apply bg-yellow-100 border-yellow-300 text-yellow-800; }
.vendor-groq { @apply bg-red-100 border-red-300 text-red-800; }
.vendor-deepinfra { @apply bg-teal-100 border-teal-300 text-teal-800; }
.vendor-fireworks { @apply bg-amber-100 border-amber-300 text-amber-800; }
.vendor-together { @apply bg-cyan-100 border-cyan-300 text-cyan-800; }
.vendor-anyscale { @apply bg-lime-100 border-lime-300 text-lime-800; }
.vendor-azure { @apply bg-sky-100 border-sky-300 text-sky-800; }
.vendor-ollama { @apply bg-violet-100 border-violet-300 text-violet-800; }
.vendor-default { @apply bg-gray-100 border-gray-300 text-gray-800; }

.model-name {
    @apply text-gray-700 font-medium;
    max-width: 250px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    font-size: 0.9rem;
}

:deep(.p-dropdown-item) .vendor-badge {
    font-size: 0.65rem;
    padding: 2px 6px;
}

/* Slide fade transition for skillset panel */
.slide-fade-enter-active,
.slide-fade-leave-active {
    transition: all 0.5s cubic-bezier(0.68, -0.55, 0.27, 1.55);
}
.slide-fade-enter-from {
    opacity: 0;
    transform: translateX(-20px);
}
.slide-fade-leave-to {
    opacity: 0;
    transform: translateX(-100%);
}

/* Zoom fade for main content */
.zoom-fade-enter-active,
.zoom-fade-leave-active {
    transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.zoom-fade-enter-from,
.zoom-fade-leave-to {
    opacity: 0;
    transform: scale(0.95);
}

/* Scale fade for loading */
.scale-fade-enter-active,
.scale-fade-leave-active {
    transition: all 0.3s ease;
}
.scale-fade-enter-from,
.scale-fade-leave-to {
    opacity: 0;
    transform: scale(0.9);
}

/* Question slide transition */
.question-slide-enter-active {
    transition: all 0.4s cubic-bezier(0.68, -0.55, 0.27, 1.55);
}
.question-slide-leave-active {
    transition: all 0.3s cubic-bezier(0.55, 0.085, 0.68, 0.53);
}
.question-slide-enter-from {
    opacity: 0;
    transform: translateX(50px);
}
.question-slide-leave-to {
    opacity: 0;
    transform: translateX(-50px);
}

/* Add animation to answer options */
.answer-option {
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.answer-option:hover {
    transform: translateY(-3px) scale(1.02);
}

.answer-option.selected {
    transform: scale(0.98);
}

/* Animate DataTable rows */
:deep(.p-datatable-tbody) > tr {
    transition: all 0.3s ease;
}

:deep(.p-datatable-tbody) > tr-enter-active {
    transition: all 0.3s ease;
}
:deep(.p-datatable-tbody) > tr-enter-from {
    opacity: 0;
    transform: translateX(30px);
}

/* Animate buttons */
.button-transition {
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.button-transition:hover {
    transform: translateY(-1px);
}

.button-transition:active {
    transform: translateY(1px);
}

/* Loading bar animation */
@keyframes loading-pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

.loading-bar {
    animation: loading-pulse 1.5s ease-in-out infinite;
}

/* Add subtle animation to vendor badges */
.vendor-badge {
    transition: all 0.2s ease;
    transform-origin: left center;
}

.vendor-badge:hover {
    transform: scale(1.05) rotate(-2deg);
}

/* Add animation to progress bar */
:deep(.question-progress) {
    transition: width 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
}

/* Add animation to stars */
.star-rating i {
    transition: all 0.3s ease;
}

.star-rating i:hover {
    transform: scale(1.2) rotate(15deg);
}

:deep(.p-dropdown-panel) {
    max-height: 350px;
    overflow-y: auto;
}

:deep(.p-dropdown-items) {
    padding: 0.5rem 0;
}

:deep(.p-dropdown-item) {
    padding: 0.5rem 1rem;
    transition: all 0.2s ease;
}

:deep(.p-dropdown-item:hover) {
    background-color: var(--surface-100);
    transform: translateX(2px);
}

:deep(.p-dropdown-filter-container) {
    padding: 0.5rem;
    position: sticky;
    top: 0;
    background-color: white;
    z-index: 2;
    border-bottom: 1px solid var(--surface-200);
}

:deep(.p-dropdown-filter) {
    width: 100%;
    padding: 0.5rem;
    border-radius: 0.375rem;
    border: 1px solid var(--surface-300);
}

:deep(.p-dropdown-filter:focus) {
    border-color: var(--primary-400);
    box-shadow: 0 0 0 2px var(--primary-100);
}

:deep(.p-dropdown) {
    border-radius: 0.375rem;
}

:deep(.p-dropdown:hover) {
    border-color: var(--primary-400);
}

:deep(.p-dropdown-label) {
    padding: 0.5rem 0.75rem;
}

:deep(.p-virtualscroller) {
    scrollbar-width: thin;
    scrollbar-color: var(--surface-400) var(--surface-100);
}

:deep(.p-virtualscroller::-webkit-scrollbar) {
    width: 6px;
}

:deep(.p-virtualscroller::-webkit-scrollbar-track) {
    background: var(--surface-100);
    border-radius: 10px;
}

:deep(.p-virtualscroller::-webkit-scrollbar-thumb) {
    background-color: var(--surface-400);
    border-radius: 10px;
}

:deep(.p-virtualscroller::-webkit-scrollbar-thumb:hover) {
    background-color: var(--surface-500);
}
</style> 