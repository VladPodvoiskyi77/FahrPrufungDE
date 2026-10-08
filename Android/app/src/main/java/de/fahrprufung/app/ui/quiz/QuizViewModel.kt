package de.fahrprufung.app.ui.quiz

import androidx.lifecycle.ViewModel
import de.fahrprufung.app.data.AnalyticsService
import de.fahrprufung.app.data.AppContainer
import de.fahrprufung.app.model.VocabularyTerm
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow

data class QuizQuestion(
    val term: VocabularyTerm,
    val choices: List<VocabularyTerm>
)

data class QuizAnswer(
    val question: QuizQuestion,
    val selected: VocabularyTerm?
) {
    val isCorrect: Boolean get() = selected?.id == question.term.id
}

private const val MAX_QUESTIONS = 10
private const val CHOICES_PER_QUESTION = 4

/**
 * Quiz session matching iOS `QuizViewModel`:
 * - questions from learning terms only
 * - distractors from learning + known terms in [sourceTerms]
 */
class QuizViewModel(
    private val sourceTerms: List<VocabularyTerm>,
    private val container: AppContainer,
    private val sessionTitle: String
) : ViewModel() {

    private val _questions = MutableStateFlow<List<QuizQuestion>>(emptyList())
    val questions: StateFlow<List<QuizQuestion>> = _questions

    private val _currentIndex = MutableStateFlow(0)
    val currentIndex: StateFlow<Int> = _currentIndex

    private val _selected = MutableStateFlow<VocabularyTerm?>(null)
    val selected: StateFlow<VocabularyTerm?> = _selected

    private val _answers = MutableStateFlow<List<QuizAnswer>>(emptyList())
    val answers: StateFlow<List<QuizAnswer>> = _answers

    private val _isFinished = MutableStateFlow(false)
    val isFinished: StateFlow<Boolean> = _isFinished

    private var didRecord = false
    private var didLogStart = false
    private var didStart = false

    val currentQuestion: QuizQuestion? get() = _questions.value.getOrNull(_currentIndex.value)
    val score: Int get() = _answers.value.count { it.isCorrect }
    val total: Int get() = _questions.value.size

    val learningTerms: List<VocabularyTerm>
        get() = container.learningTerms(sourceTerms)

    /** True when the user has marked every term in this session as known. */
    val isAllKnown: Boolean
        get() = sourceTerms.isNotEmpty() && learningTerms.isEmpty()

    fun startIfNeeded() {
        if (didStart) return
        didStart = true
        start()
    }

    fun start() {
        didRecord = false
        didLogStart = false
        val learning = learningTerms.shuffled()
        if (learning.isEmpty()) {
            _questions.value = emptyList()
            _currentIndex.value = 0
            _selected.value = null
            _answers.value = emptyList()
            _isFinished.value = false
            return
        }

        val optionPool = buildOptionPool(learning)
        if (optionPool.size < 2) {
            _questions.value = emptyList()
            _currentIndex.value = 0
            _selected.value = null
            _answers.value = emptyList()
            _isFinished.value = false
            return
        }

        val questionCount = minOf(MAX_QUESTIONS, learning.size)
        _questions.value = learning.take(questionCount).map { makeQuestion(it, optionPool) }
        _currentIndex.value = 0
        _selected.value = null
        _answers.value = emptyList()
        _isFinished.value = false
        logStartedIfNeeded()
    }

    fun logStartedIfNeeded() {
        if (didLogStart || _questions.value.isEmpty()) return
        didLogStart = true
        AnalyticsService.logQuizStarted(sessionTitle, _questions.value.size)
    }

    fun selectAnswer(choice: VocabularyTerm) {
        if (_selected.value != null) return
        _selected.value = choice
    }

    fun goToNext() {
        val question = currentQuestion ?: return
        _answers.value = _answers.value + QuizAnswer(question, _selected.value)
        _selected.value = null

        val next = _currentIndex.value + 1
        if (next >= _questions.value.size) {
            finish()
        } else {
            _currentIndex.value = next
        }
    }

    private fun finish() {
        _isFinished.value = true
        if (didRecord) return
        didRecord = true
        val isNewStudyDay = container.learningStats.recordQuizResult(score, total, sessionTitle)
        AnalyticsService.logQuizCompleted(score, total, sessionTitle)
        if (isNewStudyDay) {
            AnalyticsService.logStudyDayEarned(source = "quiz")
            AnalyticsService.syncEngagementProperties(
                onboardingCompleted = container.hasCompletedOnboarding.value,
                studyStreak = container.learningStats.studyStreak,
                knownTermCount = container.knownTermIds.value.size
            )
        }
    }

    /** Learning terms are questions; known terms fill wrong-answer options when needed. */
    private fun buildOptionPool(learning: List<VocabularyTerm>): List<VocabularyTerm> {
        val pool = learning.toMutableList()
        val learningIds = learning.map { it.id }.toSet()
        val knownSupplement = sourceTerms
            .filter { container.isTermKnown(it.id) && it.id !in learningIds }
            .shuffled()
        val targetSize = maxOf(CHOICES_PER_QUESTION, learning.size)
        for (term in knownSupplement) {
            if (pool.size >= targetSize) break
            pool.add(term)
        }
        return pool
    }

    private fun makeQuestion(term: VocabularyTerm, pool: List<VocabularyTerm>): QuizQuestion {
        val wrong = pool.filter { it.id != term.id }.shuffled().take(CHOICES_PER_QUESTION - 1)
        val choices = (wrong + term).shuffled()
        return QuizQuestion(term = term, choices = choices)
    }
}
