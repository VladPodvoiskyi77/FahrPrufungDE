package de.fahrprufung.app.data

import android.content.Context
import de.fahrprufung.app.model.AppLanguage
import de.fahrprufung.app.model.TrafficSign
import de.fahrprufung.app.model.VocabularyTerm
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch

/**
 * Holds every repository/service the app needs, built once from [Application.onCreate] and
 * shared across all screens (mirrors the iOS `DataStore` + service singletons).
 */
class AppContainer(context: Context) {

    val appScope: CoroutineScope = CoroutineScope(SupervisorJob() + Dispatchers.Main.immediate)

    val preferences = PreferencesRepository(context)
    val content = ContentRepository(context)
    val speech = GermanSpeechHelper(context)
    val learningStats = LearningStatsStore(preferences, appScope)
    val knownUndo = KnownUndoController(appScope)

    val nativeLanguage: StateFlow<AppLanguage> = preferences.nativeLanguage
        .stateIn(appScope, SharingStarted.Eagerly, AppLanguage.systemDefault())

    val knownTermIds: StateFlow<Set<String>> = preferences.knownTermIds
        .stateIn(appScope, SharingStarted.Eagerly, emptySet())

    val knownSignIds: StateFlow<Set<String>> = preferences.knownSignIds
        .stateIn(appScope, SharingStarted.Eagerly, emptySet())

    val hasCompletedOnboarding: StateFlow<Boolean> = preferences.hasCompletedOnboarding
        .stateIn(appScope, SharingStarted.Eagerly, false)

    val analyticsEnabled: StateFlow<Boolean> = preferences.analyticsEnabled
        .stateIn(appScope, SharingStarted.Eagerly, true)

    init {
        appScope.launch { content.loadIfNeeded() }
    }

    fun setNativeLanguage(language: AppLanguage) {
        appScope.launch {
            preferences.setNativeLanguage(language)
            AnalyticsService.logLanguageChanged(language)
        }
    }

    fun setHasCompletedOnboarding(value: Boolean) {
        appScope.launch { preferences.setHasCompletedOnboarding(value) }
    }

    fun setAnalyticsEnabled(value: Boolean) {
        AnalyticsService.setEnabled(value)
        appScope.launch { preferences.setAnalyticsEnabled(value) }
    }

    fun isTermKnown(id: String): Boolean = knownTermIds.value.contains(id)
    fun isSignKnown(id: String): Boolean = knownSignIds.value.contains(id)

    fun setTermKnown(id: String, known: Boolean) {
        val current = knownTermIds.value
        val updated = if (known) current + id else current - id
        appScope.launch { preferences.setKnownTermIds(updated) }
    }

    fun setSignKnown(id: String, known: Boolean) {
        val current = knownSignIds.value
        val updated = if (known) current + id else current - id
        appScope.launch { preferences.setKnownSignIds(updated) }
    }

    /** Marks a term known and offers a brief undo snackbar, matching the iOS UX. */
    fun markTermAsKnown(id: String, undoMessage: String, onUndo: (() -> Unit)? = null) {
        if (isTermKnown(id)) return
        val categoryId = content.terms.value.firstOrNull { it.id == id }?.category ?: "unknown"
        setTermKnown(id, true)
        AnalyticsService.logTermMarkedKnown(categoryId)
        knownUndo.offerUndo(undoMessage) {
            setTermKnown(id, false)
            onUndo?.invoke()
        }
    }

    fun markSignAsKnown(id: String, undoMessage: String) {
        if (isSignKnown(id)) return
        val stvo = content.sign(id)?.stvoCode
        setSignKnown(id, true)
        AnalyticsService.logSignMarkedKnown(stvo)
        knownUndo.offerUndo(undoMessage) {
            setSignKnown(id, false)
        }
    }

    fun resetKnownItems() {
        knownUndo.dismiss()
        AnalyticsService.logKnownReset()
        appScope.launch { preferences.resetKnownItems() }
    }

    fun learningTerms(source: List<VocabularyTerm>): List<VocabularyTerm> =
        content.learningTerms(source, knownTermIds.value)

    fun learningSigns(source: List<TrafficSign>): List<TrafficSign> =
        content.learningSigns(source, knownSignIds.value)

    fun knownTermCountIn(categoryId: String): Int =
        content.termsForCategory(categoryId).count { isTermKnown(it.id) }

    fun categoryProgress(categoryId: String): Pair<Int, Int> {
        val categoryTerms = content.termsForCategory(categoryId)
        val known = categoryTerms.count { isTermKnown(it.id) }
        return known to categoryTerms.size
    }

    companion object {
        @Volatile private var instance: AppContainer? = null

        fun getInstance(context: Context): AppContainer =
            instance ?: synchronized(this) {
                instance ?: AppContainer(context.applicationContext).also { instance = it }
            }
    }
}
