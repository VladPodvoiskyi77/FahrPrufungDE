package de.fahrprufung.app.ui.flashcards

import androidx.lifecycle.ViewModel
import de.fahrprufung.app.data.AnalyticsService
import de.fahrprufung.app.data.AppContainer
import de.fahrprufung.app.data.LearningStatsStore
import de.fahrprufung.app.model.VocabularyTerm
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow

/** Manages a single flashcard session: deck order, flip state, and known/undo bookkeeping. */
class FlashcardViewModel(
    initialTerms: List<VocabularyTerm>,
    private val container: AppContainer,
    private val sessionTitle: String
) : ViewModel() {

    private val _deck = MutableStateFlow(initialTerms.shuffled())
    val deck: StateFlow<List<VocabularyTerm>> = _deck

    private val _index = MutableStateFlow(0)
    val index: StateFlow<Int> = _index

    private val _isFlipped = MutableStateFlow(false)
    val isFlipped: StateFlow<Boolean> = _isFlipped

    private var maxCardsSeen = if (initialTerms.isEmpty()) 0 else 1
    private var didRecordSession = false
    private var didCountStudyDay = false

    val current: VocabularyTerm? get() = _deck.value.getOrNull(_index.value)

    val progress: Float
        get() {
            val deck = _deck.value
            return if (deck.isEmpty()) 0f else (_index.value + 1f) / deck.size
        }

    val canGoBack: Boolean get() = _index.value > 0
    val canGoForward: Boolean get() = _index.value < _deck.value.size - 1

    fun isCurrentKnown(): Boolean = current?.let { container.isTermKnown(it.id) } ?: false

    fun flip() {
        _isFlipped.value = !_isFlipped.value
    }

    fun resetFlip() {
        _isFlipped.value = false
    }

    fun move(offset: Int) {
        val next = _index.value + offset
        if (next !in _deck.value.indices) return
        _index.value = next
        maxCardsSeen = maxOf(maxCardsSeen, next + 1)
        _isFlipped.value = false
        countStudyDayIfNeeded()
    }

    fun finishSessionIfNeeded() {
        if (didRecordSession) return
        didRecordSession = true
        // Match iOS: only log/record once the study-day threshold is reached.
        if (maxCardsSeen < LearningStatsStore.MINIMUM_CARDS_FOR_STUDY_DAY) return
        AnalyticsService.logFlashcardSession(sessionTitle, maxCardsSeen)
        container.learningStats.recordFlashcardSession(sessionTitle, maxCardsSeen)
    }

    private fun countStudyDayIfNeeded() {
        if (didCountStudyDay) return
        if (maxCardsSeen < LearningStatsStore.MINIMUM_CARDS_FOR_STUDY_DAY) return
        didCountStudyDay = true
        val isNew = container.learningStats.recordStudyActivity()
        if (isNew) {
            AnalyticsService.logStudyDayEarned(source = "flashcards")
            AnalyticsService.syncEngagementProperties(
                onboardingCompleted = container.hasCompletedOnboarding.value,
                studyStreak = container.learningStats.studyStreak,
                knownTermCount = container.knownTermIds.value.size
            )
        }
    }

    fun toggleKnownForCurrent(undoMessage: String) {
        val term = current ?: return

        if (container.isTermKnown(term.id)) {
            container.knownUndo.dismiss()
            container.setTermKnown(term.id, false)
            return
        }

        val savedIndex = _index.value
        container.markTermAsKnown(term.id, undoMessage) {
            val deck = _deck.value
            if (deck.none { it.id == term.id }) {
                val insertAt = minOf(savedIndex, deck.size)
                _deck.value = deck.toMutableList().apply { add(insertAt, term) }
                _index.value = insertAt
                _isFlipped.value = false
            }
        }

        val newDeck = _deck.value.filterNot { it.id == term.id }
        _deck.value = newDeck
        _index.value = when {
            newDeck.isEmpty() -> 0
            _index.value >= newDeck.size -> newDeck.size - 1
            else -> _index.value
        }
        _isFlipped.value = false
    }
}
