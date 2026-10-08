package de.fahrprufung.app.data

import android.content.Context
import androidx.datastore.preferences.core.booleanPreferencesKey
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.stringPreferencesKey
import androidx.datastore.preferences.core.stringSetPreferencesKey
import androidx.datastore.preferences.preferencesDataStore
import de.fahrprufung.app.model.AppLanguage
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map

private val Context.dataStore by preferencesDataStore(name = "fahrprufung_prefs")

/** Thin wrapper over Jetpack DataStore holding every piece of app-local user state. */
class PreferencesRepository(private val context: Context) {

    private object Keys {
        val NATIVE_LANGUAGE = stringPreferencesKey("nativeLanguage")
        val KNOWN_TERM_IDS = stringSetPreferencesKey("knownTermIDs")
        val KNOWN_SIGN_IDS = stringSetPreferencesKey("knownSignIDs")
        val LEARNING_STATS_JSON = stringPreferencesKey("learningStats.v1")
        val HAS_COMPLETED_ONBOARDING = booleanPreferencesKey("hasCompletedOnboarding")
        val ANALYTICS_ENABLED = booleanPreferencesKey("analyticsEnabled")
    }

    val nativeLanguage: Flow<AppLanguage> = context.dataStore.data.map { prefs ->
        AppLanguage.fromCode(prefs[Keys.NATIVE_LANGUAGE]) ?: AppLanguage.systemDefault()
    }

    val knownTermIds: Flow<Set<String>> = context.dataStore.data.map { prefs ->
        prefs[Keys.KNOWN_TERM_IDS] ?: emptySet()
    }

    val knownSignIds: Flow<Set<String>> = context.dataStore.data.map { prefs ->
        prefs[Keys.KNOWN_SIGN_IDS] ?: emptySet()
    }

    val learningStatsJson: Flow<String?> = context.dataStore.data.map { prefs ->
        prefs[Keys.LEARNING_STATS_JSON]
    }

    val hasCompletedOnboarding: Flow<Boolean> = context.dataStore.data.map { prefs ->
        prefs[Keys.HAS_COMPLETED_ONBOARDING] ?: false
    }

    val analyticsEnabled: Flow<Boolean> = context.dataStore.data.map { prefs ->
        prefs[Keys.ANALYTICS_ENABLED] ?: true
    }

    suspend fun setNativeLanguage(language: AppLanguage) {
        context.dataStore.edit { it[Keys.NATIVE_LANGUAGE] = language.code }
    }

    suspend fun setKnownTermIds(ids: Set<String>) {
        context.dataStore.edit { it[Keys.KNOWN_TERM_IDS] = ids }
    }

    suspend fun setKnownSignIds(ids: Set<String>) {
        context.dataStore.edit { it[Keys.KNOWN_SIGN_IDS] = ids }
    }

    suspend fun setLearningStatsJson(json: String) {
        context.dataStore.edit { it[Keys.LEARNING_STATS_JSON] = json }
    }

    suspend fun setHasCompletedOnboarding(value: Boolean) {
        context.dataStore.edit { it[Keys.HAS_COMPLETED_ONBOARDING] = value }
    }

    suspend fun setAnalyticsEnabled(value: Boolean) {
        context.dataStore.edit { it[Keys.ANALYTICS_ENABLED] = value }
    }

    suspend fun resetKnownItems() {
        context.dataStore.edit {
            it.remove(Keys.KNOWN_TERM_IDS)
            it.remove(Keys.KNOWN_SIGN_IDS)
        }
    }
}
