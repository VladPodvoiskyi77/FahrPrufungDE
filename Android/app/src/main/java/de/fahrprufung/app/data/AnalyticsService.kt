package de.fahrprufung.app.data

import android.os.Bundle
import android.util.Log
import com.google.firebase.analytics.FirebaseAnalytics
import com.google.firebase.analytics.ktx.analytics
import com.google.firebase.ktx.Firebase
import de.fahrprufung.app.debug.ScreenshotSeed
import de.fahrprufung.app.model.AppLanguage

/**
 * Firebase Analytics wrapper — event names/params mirror iOS `AnalyticsService`.
 * Honors the Settings opt-out (`analyticsEnabled`) and skips logging during screenshot seeding.
 */
object AnalyticsService {
    private const val TAG = "Analytics"

    @Volatile
    var isEnabled: Boolean = true
        private set

    private val firebase: FirebaseAnalytics by lazy { Firebase.analytics }

    fun setEnabled(enabled: Boolean) {
        val wasEnabled = isEnabled
        if (wasEnabled && !enabled) {
            log("analytics_disabled", bypassEnabledCheck = true)
        }
        isEnabled = enabled
        runCatching { firebase.setAnalyticsCollectionEnabled(enabled) }
    }

    fun logAppOpen() = log("app_open")

    fun logAppBackground() = log("app_background")

    fun logAppForeground() = log("app_foreground")

    fun logOnboardingCompleted(language: AppLanguage) {
        log("onboarding_completed", mapOf("language" to language.code))
        setUserProperty("ui_language", language.code)
        setUserProperty("onboarding_done", "true")
    }

    fun logOnboardingSkipped(language: AppLanguage) {
        log("onboarding_skipped", mapOf("language" to language.code))
        setUserProperty("ui_language", language.code)
        setUserProperty("onboarding_done", "true")
    }

    fun logScreen(name: String, parameters: Map<String, Any?> = emptyMap()) {
        if (!shouldLog()) return
        val bundle = Bundle().apply {
            putString(FirebaseAnalytics.Param.SCREEN_NAME, name)
            putString(FirebaseAnalytics.Param.SCREEN_CLASS, name)
            putAll(parameters)
        }
        firebase.logEvent(FirebaseAnalytics.Event.SCREEN_VIEW, bundle)
        Log.d(TAG, "screen_view name=$name params=$parameters")
    }

    fun logHomeAction(action: String) =
        log("home_action_tapped", mapOf("action" to action))

    fun logQuizStarted(sessionTitle: String, questionCount: Int) =
        log(
            "quiz_started",
            mapOf(
                "session_title" to sessionTitle,
                "question_count" to questionCount
            )
        )

    fun logQuizCompleted(score: Int, total: Int, sessionTitle: String) {
        val accuracy = if (total > 0) Math.round(score * 100f / total) else 0
        log(
            "quiz_completed",
            mapOf(
                "score" to score,
                "total" to total,
                "accuracy_percent" to accuracy,
                "session_title" to sessionTitle
            )
        )
    }

    fun logQuizReviewOpened() = log("quiz_review_opened")

    fun logFlashcardSession(title: String, cardsSeen: Int) =
        log(
            "flashcard_session",
            mapOf(
                "session_title" to title,
                "cards_seen" to cardsSeen
            )
        )

    fun logStudyDayEarned(source: String) =
        log("study_day_earned", mapOf("source" to source))

    fun logTermMarkedKnown(categoryId: String) =
        log("term_marked_known", mapOf("category_id" to categoryId))

    fun logSignMarkedKnown(stvoCode: String?) =
        log("sign_marked_known", mapOf("stvo_code" to (stvoCode ?: "unknown")))

    fun logLanguageChanged(language: AppLanguage) {
        log("language_changed", mapOf("language" to language.code))
        setUserProperty("ui_language", language.code)
    }

    fun logKnownReset() = log("known_reset")

    fun logProgressViewed() = log("progress_viewed")

    fun syncEngagementProperties(
        onboardingCompleted: Boolean,
        studyStreak: Int,
        knownTermCount: Int
    ) {
        setUserProperty("onboarding_done", if (onboardingCompleted) "true" else "false")
        setUserProperty("has_study_streak", if (studyStreak > 0) "yes" else "no")
        setUserProperty("known_terms_bucket", knownTermsBucket(knownTermCount))
    }

    private fun knownTermsBucket(count: Int): String = when {
        count <= 0 -> "0"
        count <= 50 -> "1_50"
        count <= 150 -> "51_150"
        else -> "150_plus"
    }

    private fun shouldLog(bypassEnabledCheck: Boolean = false): Boolean {
        if (ScreenshotSeed.isSeedRequested()) return false
        return bypassEnabledCheck || isEnabled
    }

    private fun log(
        name: String,
        parameters: Map<String, Any?> = emptyMap(),
        bypassEnabledCheck: Boolean = false
    ) {
        if (!shouldLog(bypassEnabledCheck)) return
        val bundle = Bundle().apply { putAll(parameters) }
        firebase.logEvent(name, bundle)
        if (parameters.isEmpty()) {
            Log.d(TAG, name)
        } else {
            Log.d(TAG, "$name $parameters")
        }
    }

    private fun setUserProperty(name: String, value: String) {
        if (!shouldLog()) return
        firebase.setUserProperty(name, value)
    }

    private fun Bundle.putAll(parameters: Map<String, Any?>) {
        parameters.forEach { (key, value) ->
            when (value) {
                null -> Unit
                is String -> putString(key, value)
                is Int -> putLong(key, value.toLong())
                is Long -> putLong(key, value)
                is Double -> putDouble(key, value)
                is Float -> putDouble(key, value.toDouble())
                is Boolean -> putString(key, value.toString())
                else -> putString(key, value.toString())
            }
        }
    }
}
