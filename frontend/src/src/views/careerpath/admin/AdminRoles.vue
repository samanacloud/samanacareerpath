<template>
    <div class="quiz-container">
        <h1>Generate Quiz</h1>

        <!-- Topic Input Section -->
        <div class="topic-input">
            <InputText v-model="form.topic" placeholder="Enter quiz topic" class="w-full mb-3" />
            <Button @click="generateQuiz" :loading="loading" :disabled="!form.topic || loading">
                Generate Quiz
            </Button>
        </div>

        <!-- Loading Indicator -->
        <div v-if="loading" class="loading-container">
            <ProgressSpinner />
            <div class="mt-2">Generating quiz questions...</div>
        </div>

        <!-- Quiz Section -->
        <div v-if="questions.length && !loading" class="quiz-content">
            <div class="question-header">
                <div class="question-info">
                    <span>Question {{ currentQuestionIndex + 1 }}/{{ questions.length }}</span>
                    <Tag :severity="getDifficultySeverity(currentQuestion.difficulty)" :value="currentQuestion.difficulty" />
                </div>
                <ProgressBar :value="(currentQuestionIndex / questions.length) * 100" class="question-progress" />
                
                <!-- Timer -->
                <div class="timer" :class="{ 'warning': timeLeft <= 5 }">
                    Time left: {{ timeLeft }}s
                </div>
            </div>

            <div class="question-text">{{ currentQuestion.question }}</div>

            <div class="answers-grid">
                <div v-for="(answer, index) in currentQuestion.answers" 
                     :key="index"
                     class="answer-option"
                     :class="{ 'selected': selectedAnswers[currentQuestionIndex] === answer }"
                     @click="selectAnswer(answer)">
                    <span class="answer-letter">{{ String.fromCharCode(65 + index) }}.</span>
                    <span class="answer-text">{{ answer }}</span>
                </div>
            </div>

            <div class="navigation-buttons">
                <Button @click="previousQuestion" :disabled="currentQuestionIndex === 0">
                    <i class="pi pi-chevron-left mr-2" />Previous
                </Button>
                <Button v-if="currentQuestionIndex < questions.length - 1"
                    @click="nextQuestion" 
                    :disabled="!selectedAnswers[currentQuestionIndex]">
                    Next<i class="pi pi-chevron-right ml-2" />
                </Button>
                <Button v-else
                    @click="finishQuiz"
                    :disabled="!selectedAnswers[currentQuestionIndex]"
                    severity="success">
                    <i class="pi pi-check mr-2" />Finish Quiz
                </Button>
            </div>
        </div>

        <!-- Results Dialog -->
        <Dialog 
            v-model:visible="showResults" 
            modal 
            header="Quiz Results" 
            :style="{ width: isMobile ? '90vw' : '50vw' }"
            :closable="false"
            class="results-dialog"
        >
            <div class="text-center mb-4">
                <div class="text-4xl font-bold mb-2">{{ score }}%</div>
                <div class="star-rating mb-2">
                    <i v-for="index in 5" 
                       :key="index"
                       class="pi"
                       :class="[index <= scoreToStars ? 'pi-star-fill text-yellow-500' : 'pi-star text-gray-300']"
                    ></i>
                </div>
                <Tag :severity="getScoreSeverity(score)" class="text-xl">
                    {{ getScoreMessage(score) }}
                </Tag>
            </div>

            <div class="mt-4">
                <div v-for="(question, index) in questions" :key="index" class="mb-4 p-3 surface-ground border-round">
                    <div class="flex align-items-center gap-2 mb-2">
                        <span class="font-medium">Question {{ index + 1 }}</span>
                        <i :class="selectedAnswers[index] === question.correctAnswer ? 
                            'pi pi-check text-green-500' : 'pi pi-times text-red-500'"></i>
                    </div>
                    <div class="text-900 mb-2">{{ question.question }}</div>
                    <div class="pl-2 mb-1">
                        Your answer: 
                        <span :class="selectedAnswers[index] === question.correctAnswer ? 
                            'text-green-500 font-medium' : 'text-red-500 font-medium'">
                            {{ selectedAnswers[index] }}
                        </span>
                    </div>
                    <div v-if="selectedAnswers[index] !== question.correctAnswer" 
                         class="pl-2 text-green-500 font-medium">
                        Correct answer: {{ question.correctAnswer }}
                    </div>
                </div>
            </div>

            <template #footer>
                <Button label="Try Another Quiz" icon="pi pi-refresh" @click="resetQuiz" class="w-full md:w-auto" />
            </template>
        </Dialog>
    </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted, watch } from 'vue';
import { useToast } from 'primevue/usetoast';

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

const form = reactive({
    topic: ''
});

const currentQuestion = computed(() => 
    questions.value[currentQuestionIndex.value] || { question: '', answers: [], difficulty: '' }
);

const isMobile = ref(window.innerWidth < 768);

const handleResize = () => {
    isMobile.value = window.innerWidth < 768;
};

onMounted(() => {
    window.addEventListener('resize', handleResize);
});

onUnmounted(() => {
    window.removeEventListener('resize', handleResize);
});

const generateQuiz = async () => {
    if (!form.topic) {
        toast.add({ severity: 'warn', summary: 'Warning', detail: 'Please enter a topic', life: 3000 });
        return;
    }

    loading.value = true;
    try {
        const query = {
            query: `
                query GenerateQuiz($topic: String!) {
                    generateQuizByTopic(topic: $topic) {
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
                topic: form.topic
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

        if (result.errors) {
            throw new Error(result.errors[0].message);
        }

        const data = result.data.generateQuizByTopic;
        
        if (data.status === 'error') {
            throw new Error(data.error);
        }

        questions.value = data.questions;
        selectedAnswers.value = new Array(questions.value.length).fill(null);
        quizStarted.value = true;
        currentQuestionIndex.value = 0;

        toast.add({ 
            severity: 'success', 
            summary: 'Success', 
            detail: 'Quiz generated successfully', 
            life: 3000 
        });

    } catch (error) {
        toast.add({ 
            severity: 'error', 
            summary: 'Error', 
            detail: error.message || 'Failed to generate quiz', 
            life: 3000 
        });
    } finally {
        loading.value = false;
    }
};

const selectAnswer = (answer) => {
    selectedAnswers.value[currentQuestionIndex.value] = answer;
};

const nextQuestion = () => {
    if (currentQuestionIndex.value < questions.value.length - 1) {
        currentQuestionIndex.value++;
    }
};

const previousQuestion = () => {
    if (currentQuestionIndex.value > 0) {
        currentQuestionIndex.value--;
    }
};

const finishQuiz = () => {
    const correctAnswers = questions.value.reduce((count, question, index) => {
        return count + (selectedAnswers.value[index] === question.correctAnswer ? 1 : 0);
    }, 0);
    
    score.value = Math.round((correctAnswers / questions.value.length) * 100);
    showResults.value = true;
};

const resetQuiz = () => {
    quizStarted.value = false;
    currentQuestionIndex.value = 0;
    questions.value = [];
    selectedAnswers.value = [];
    showResults.value = false;
    score.value = 0;
    form.topic = '';
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
    timeLeft.value = difficulty === 'easy' ? 10 : difficulty === 'medium' ? 15 : 20;
    
    timerInterval = setInterval(() => {
        if (timeLeft.value > 0) {
            timeLeft.value--;
        } else {
            clearInterval(timerInterval);
            if (!selectedAnswers.value[currentQuestionIndex.value]) {
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
</script>

<style scoped>
.quiz-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
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
}

.question-info {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.timer {
    font-size: 1.1rem;
    font-weight: bold;
    color: var(--primary-color);
}

.timer.warning {
    color: var(--red-500);
}

.answers-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1rem;
    margin: 2rem 0;
}

.answer-option {
    display: flex;
    align-items: flex-start;
    gap: 0.5rem;
    padding: 1rem;
    border: 1px solid var(--surface-border);
    border-radius: var(--border-radius);
    cursor: pointer;
    transition: all 0.2s ease;
}

.answer-option:hover {
    background-color: var(--surface-hover);
}

.answer-option.selected {
    background-color: var(--primary-color);
    color: var(--primary-color-text);
    border-color: var(--primary-color);
}

.answer-letter {
    font-weight: bold;
    min-width: 25px;
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
    transition: all 0.2s ease;
}
</style> 