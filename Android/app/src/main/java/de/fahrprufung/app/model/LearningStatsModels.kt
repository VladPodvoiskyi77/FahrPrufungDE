package de.fahrprufung.app.model

import kotlinx.serialization.Serializable
import java.util.UUID

@Serializable
data class QuizResultRecord(
    val id: String = UUID.randomUUID().toString(),
    val score: Int,
    val total: Int,
    val sessionTitle: String,
    val dateMillis: Long
) {
    val accuracy: Double get() = if (total > 0) score.toDouble() / total.toDouble() else 0.0
}

@Serializable
data class FlashcardSessionRecord(
    val id: String = UUID.randomUUID().toString(),
    val sessionTitle: String,
    val cardsSeen: Int,
    val dateMillis: Long
)

/** Persisted payload backing `LearningStatsStore`, stored as JSON under `learningStats.v1`. */
@Serializable
data class LearningStatsData(
    val quizResults: List<QuizResultRecord> = emptyList(),
    val flashcardSessions: List<FlashcardSessionRecord> = emptyList(),
    val studyDayKeys: Set<String> = emptySet()
)
