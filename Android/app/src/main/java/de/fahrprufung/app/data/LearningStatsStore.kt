package de.fahrprufung.app.data

import de.fahrprufung.app.model.FlashcardSessionRecord
import de.fahrprufung.app.model.LearningStatsData
import de.fahrprufung.app.model.QuizResultRecord
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.launch
import kotlinx.serialization.decodeFromString
import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.Json
import java.text.SimpleDateFormat
import java.util.Calendar
import java.util.Date
import java.util.Locale

/**
 * Tracks quiz results, flashcard sessions and study-day streaks, persisted as a single JSON
 * blob under the `learningStats.v1` preference key (mirrors the iOS `LearningStatsStore`).
 */
class LearningStatsStore(
    private val preferences: PreferencesRepository,
    private val scope: CoroutineScope
) {
    companion object {
        private const val MAX_QUIZ_RESULTS = 20
        private const val MAX_FLASHCARD_SESSIONS = 10
        const val MINIMUM_CARDS_FOR_STUDY_DAY = 10

        private val dayFormat = SimpleDateFormat("yyyy-MM-dd", Locale.US)

        fun dayKey(date: Date = Date()): String = dayFormat.format(date)
    }

    private val json = Json { ignoreUnknownKeys = true }

    private val _data = MutableStateFlow(LearningStatsData())
    val data: StateFlow<LearningStatsData> = _data

    init {
        scope.launch {
            val stored = preferences.learningStatsJson.first()
            if (!stored.isNullOrBlank()) {
                runCatching { json.decodeFromString<LearningStatsData>(stored) }
                    .onSuccess { _data.value = it }
            }
        }
    }

    /** Consecutive study days ending today, or ending yesterday if today isn't over yet. */
    val studyStreak: Int
        get() {
            val keys = _data.value.studyDayKeys
            if (keys.isEmpty()) return 0
            var day = streakStartDay(keys) ?: return 0
            var streak = 0
            val calendar = Calendar.getInstance()
            while (keys.contains(dayKey(day))) {
                streak += 1
                calendar.time = day
                calendar.add(Calendar.DAY_OF_YEAR, -1)
                day = calendar.time
            }
            return streak
        }

    private fun streakStartDay(keys: Set<String>): Date? {
        val today = startOfDay(Date())
        if (keys.contains(dayKey(today))) return today
        val calendar = Calendar.getInstance()
        calendar.time = today
        calendar.add(Calendar.DAY_OF_YEAR, -1)
        val yesterday = calendar.time
        return if (keys.contains(dayKey(yesterday))) yesterday else null
    }

    private fun startOfDay(date: Date): Date {
        val calendar = Calendar.getInstance()
        calendar.time = date
        calendar.set(Calendar.HOUR_OF_DAY, 0)
        calendar.set(Calendar.MINUTE, 0)
        calendar.set(Calendar.SECOND, 0)
        calendar.set(Calendar.MILLISECOND, 0)
        return calendar.time
    }

    /** Returns true if a new study day was recorded (useful for "study day earned" events). */
    fun recordStudyActivity(): Boolean {
        val key = dayKey()
        val current = _data.value
        val isNew = !current.studyDayKeys.contains(key)
        if (isNew) {
            update(current.copy(studyDayKeys = current.studyDayKeys + key))
        }
        return isNew
    }

    fun recordQuizResult(score: Int, total: Int, sessionTitle: String): Boolean {
        val isNewStudyDay = recordStudyActivity()
        val current = _data.value
        val record = QuizResultRecord(
            score = score,
            total = total,
            sessionTitle = sessionTitle,
            dateMillis = System.currentTimeMillis()
        )
        val results = (listOf(record) + current.quizResults).take(MAX_QUIZ_RESULTS)
        update(current.copy(quizResults = results))
        return isNewStudyDay
    }

    fun recordFlashcardSession(title: String, cardsSeen: Int) {
        if (cardsSeen < MINIMUM_CARDS_FOR_STUDY_DAY) return
        recordStudyActivity()
        val current = _data.value
        val record = FlashcardSessionRecord(
            sessionTitle = title,
            cardsSeen = cardsSeen,
            dateMillis = System.currentTimeMillis()
        )
        val sessions = (listOf(record) + current.flashcardSessions).take(MAX_FLASHCARD_SESSIONS)
        update(current.copy(flashcardSessions = sessions))
    }

    private fun update(newData: LearningStatsData) {
        _data.value = newData
        scope.launch {
            preferences.setLearningStatsJson(json.encodeToString(newData))
        }
    }

    /** Debug/screenshots: replace in-memory + persisted stats immediately. */
    fun replaceForScreenshots(data: LearningStatsData) {
        update(data)
    }
}
